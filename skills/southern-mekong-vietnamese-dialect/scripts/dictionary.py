#!/usr/bin/env python3
"""Read and update references/tu-dien-mien-tay.yaml without breaking its format.

The file is a small YAML subset, parsed here with the stdlib only:

    Group:                  # indent 0, no value
      Subgroup:             # optional level, indent 2, no value
        <từ>: <nghĩa>       # entries live only in groups that have no subgroups

Commands:
    groups                              list leaf groups with entry counts
    find TEXT                           entries whose word or meaning contains TEXT
    add WORD MEANING --group G          append an entry to group G (leaf name or "A/B" path)
        [--example TEXT] [--create] [--dry-run]
    check                               validate format and duplicates (exit 1 on problems)

Use --file PATH to target another dictionary file.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

DEFAULT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "references", "tu-dien-mien-tay.yaml"
)
STEP = 2
YAML_INDICATORS = tuple("-?:,[]{}#&*!|>'\"%@`")


def nfc(text):
    return unicodedata.normalize("NFC", text).strip()


def aliases(word):
    """'Hồ (nước) / Cái mền' -> {'hồ', 'mền'}: the forms used for duplicate detection.

    Parenthesised notes and a leading classifier (cái, con) are ignored, so
    "Cái mền" is caught as a duplicate of "Mền".
    """
    forms = set()
    for part in word.split(" / "):
        part = re.sub(r"\([^)]*\)", "", part).strip().lower()
        part = re.sub(r"^(cái|con)\s+", "", part)
        if part:
            forms.add(part)
    return forms


def needs_quotes(text):
    return ": " in text or " #" in text or text.endswith(":") or text.startswith(YAML_INDICATORS)


def scalar(text):
    return json.dumps(text, ensure_ascii=False) if needs_quotes(text) else text


def unquote(text):
    return json.loads(text) if len(text) >= 2 and text[0] == text[-1] == '"' else text


def split_entry(body):
    """Split '<từ>: <nghĩa>' (either side may be double-quoted). Return (key, value) or None."""
    if body.startswith('"'):
        m = re.match(r'("(?:[^"\\]|\\.)*")\s*:\s(.*)$', body)
        if not m:
            return None
        return unquote(m.group(1)), m.group(2).strip()
    if ": " not in body:
        return None
    key, value = body.split(": ", 1)
    return key.strip(), value.strip()


class Dictionary:
    def __init__(self, path):
        self.path = path
        with open(path, encoding="utf-8") as f:
            self.lines = f.read().splitlines()
        self.groups = {}  # path -> {"line", "indent", "entries", "children"}
        self.entries = []  # {"group", "word", "meaning", "line"}
        self.problems = []
        self._parse()

    def _problem(self, lineno, msg):
        self.problems.append(f"{self.path}:{lineno}: {msg}")

    def _parse(self):
        stack = []  # [(indent, name)]
        for lineno, raw in enumerate(self.lines, 1):
            body = raw.strip()
            if not body or body.startswith("#"):
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            if "\t" in raw[: indent + 1]:
                self._problem(lineno, "dùng dấu cách, không dùng tab")
                continue
            while stack and stack[-1][0] >= indent:
                stack.pop()
            expected = stack[-1][0] + STEP if stack else 0
            if indent != expected:
                self._problem(lineno, f"thụt lề {indent}, cần {expected}")
                continue
            parent = "/".join(name for _, name in stack)

            if body.endswith(":") and ": " not in body and not body.startswith('"'):
                name = nfc(body[:-1])
                path = f"{parent}/{name}" if parent else name
                if path in self.groups:
                    self._problem(lineno, f"nhóm '{path}' bị lặp")
                self.groups[path] = {"line": lineno, "indent": indent, "entries": 0, "children": 0}
                if parent:
                    self.groups[parent]["children"] += 1
                stack.append((indent, name))
                continue

            if not stack:
                self._problem(lineno, "mục nằm ngoài nhóm nào")
                continue
            pair = split_entry(body)
            if pair is None:
                self._problem(lineno, "cần đúng dạng '<từ>: <nghĩa>'")
                continue
            word, meaning = pair
            if not meaning.startswith('"') and (" #" in meaning or ": " in meaning):
                self._problem(lineno, "nghĩa có ': ' hoặc ' #', phải bọc trong \"...\"")
            if not word or not meaning:
                self._problem(lineno, "thiếu từ hoặc nghĩa")
            self.groups[parent]["entries"] += 1
            self.entries.append(
                {"group": parent, "word": nfc(word), "meaning": nfc(unquote(meaning)), "line": lineno}
            )

        for path, g in self.groups.items():
            if g["entries"] and g["children"]:
                self._problem(g["line"], f"nhóm '{path}' vừa có mục vừa có nhóm con")
            if not g["entries"] and not g["children"]:
                self._problem(g["line"], f"nhóm '{path}' trống")

    def leaf_groups(self):
        return [p for p, g in self.groups.items() if not g["children"]]

    def duplicates_of(self, word):
        forms = aliases(word)
        return [e for e in self.entries if forms & aliases(e["word"])]

    def resolve_group(self, query):
        q = nfc(query).lower()
        return [p for p in self.leaf_groups() if p.lower() == q or p.split("/")[-1].lower() == q]

    def block_end(self, path):
        """Index (0-based) of the last content line inside group `path`."""
        g = self.groups[path]
        end = g["line"] - 1
        for i in range(g["line"], len(self.lines)):
            body = self.lines[i].strip()
            if not body or body.startswith("#"):
                continue
            if len(self.lines[i]) - len(self.lines[i].lstrip(" ")) <= g["indent"]:
                break
            end = i
        return end


def cmd_groups(d, _args):
    for path in d.leaf_groups():
        print(f"{d.groups[path]['entries']:4d}  {path}")
    return 0


def cmd_find(d, args):
    q = nfc(args.text).lower()
    hits = [e for e in d.entries if q in e["word"].lower() or q in e["meaning"].lower()]
    for e in hits:
        print(f"{d.path}:{e['line']}: [{e['group']}] {e['word']}: {e['meaning']}")
    return 0 if hits else 1


def cmd_check(d, _args):
    problems = list(d.problems)
    seen = {}
    for e in d.entries:
        for form in aliases(e["word"]):
            if form in seen:
                problems.append(f"{d.path}:{e['line']}: '{form}' đã có ở dòng {seen[form]}")
            else:
                seen[form] = e["line"]
    for p in problems:
        print(p)
    if not problems:
        print(f"OK: {len(d.entries)} mục, {len(d.leaf_groups())} nhóm")
    return 1 if problems else 0


def cmd_add(d, args):
    if d.problems:
        print("Từ điển đang lỗi định dạng, sửa trước (chạy 'check'):", file=sys.stderr)
        print("\n".join(d.problems), file=sys.stderr)
        return 1
    word, meaning = nfc(args.word), nfc(args.meaning)
    if args.example:
        meaning = f"{meaning} (VD. {nfc(args.example)})"
    if not word or not meaning:
        print("Thiếu từ hoặc nghĩa.", file=sys.stderr)
        return 1

    dupes = d.duplicates_of(word)
    if dupes:
        for e in dupes:
            print(f"Đã có: {d.path}:{e['line']}: [{e['group']}] {e['word']}: {e['meaning']}", file=sys.stderr)
        return 1

    matches = d.resolve_group(args.group)
    if len(matches) > 1:
        print(f"Nhóm '{args.group}' không rõ ràng: {', '.join(matches)}", file=sys.stderr)
        return 1
    new_lines = []
    if matches:
        group = matches[0]
        insert_at = d.block_end(group) + 1
        indent = d.groups[group]["indent"] + STEP
    elif args.create:
        parts = [nfc(p) for p in args.group.split("/")]
        parent = "/".join(parts[:-1])
        if len(parts) > 2 or (parent and parent not in d.groups):
            print("--create chỉ tạo nhóm cấp 1, hoặc nhóm con của một nhóm đã có.", file=sys.stderr)
            return 1
        if parent and d.groups[parent]["entries"]:
            print(f"Nhóm '{parent}' đang chứa mục, không thêm nhóm con được.", file=sys.stderr)
            return 1
        group = "/".join(parts)
        if parent:
            insert_at = d.block_end(parent) + 1
            header_indent = d.groups[parent]["indent"] + STEP
        else:
            insert_at = len(d.lines)
            header_indent = 0
        new_lines += ["", " " * header_indent + f"{parts[-1]}:"]
        indent = header_indent + STEP
    else:
        print(f"Không có nhóm '{args.group}'. Nhóm hiện có:", file=sys.stderr)
        print("\n".join(f"  {p}" for p in d.leaf_groups()), file=sys.stderr)
        print("Thêm --create để tạo nhóm mới.", file=sys.stderr)
        return 1

    entry = " " * indent + f"{scalar(word)}: {scalar(meaning)}"
    new_lines.append(entry)
    if args.dry_run:
        print(f"[dry-run] {group} (sau dòng {insert_at}):\n" + "\n".join(new_lines))
        return 0
    d.lines[insert_at:insert_at] = new_lines
    with open(d.path, "w", encoding="utf-8") as f:
        f.write("\n".join(d.lines) + "\n")
    print(f"Đã thêm vô [{group}]: {entry.strip()}")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=DEFAULT_FILE)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("groups")
    sub.add_parser("check")
    p = sub.add_parser("find")
    p.add_argument("text")
    p = sub.add_parser("add")
    p.add_argument("word")
    p.add_argument("meaning")
    p.add_argument("--group", required=True)
    p.add_argument("--example")
    p.add_argument("--create", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    d = Dictionary(os.path.normpath(args.file))
    return {"groups": cmd_groups, "find": cmd_find, "check": cmd_check, "add": cmd_add}[args.cmd](d, args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
