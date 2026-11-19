#!/usr/bin/env python3
"""Scan Vietnamese text for forms that break the Southern / Mekong Delta dialect rules.

Usage:
    check_dialect.py FILE [FILE ...]
    printf '%s' "$TEXT" | check_dialect.py -

ERROR = banned word ("ạ", "vâng"); exit code 1 if any are found.
WARN  = likely Northern form; review in context before changing.
"""
import re
import sys
import unicodedata

ERRORS = {
    "ạ": "bỏ 'ạ': mở đầu bằng 'Dạ' hoặc kết câu bằng 'nha / nghen / nè'",
    "vâng": "dùng 'Dạ' / 'Dạ phải' / 'Dạ được'",
}

# Only forms that are rarely false positives. Single syllables such as
# "quả", "bố", "hoa" are left out because they appear in compounds
# (kết quả, công bố, Hoa Kỳ) that are also correct in the South.
WARNINGS = {
    "nhé": "nha / nghen",
    "nhỉ": "ha / hen",
    "đấy": "đó",
    "thế à": "vậy hả",
    "thế nhé": "vậy nha",
    "thế thì": "vậy thì",
    "anh ấy": "ảnh",
    "chị ấy": "chỉ",
    "ông ấy": "ổng",
    "bà ấy": "bả",
    "cô ấy": "cổ",
    "thìa": "muỗng",
    "lợn": "heo",
    "dứa": "thơm / khóm",
    "hoa quả": "trái cây",
    "mì chính": "bột ngọt",
    "xì dầu": "nước tương",
    "ô tô": "xe hơi",
    "điều hoà": "máy lạnh",
    "điều hòa": "máy lạnh",
    "vỉa hè": "lề",
    "ngõ": "hẻm",
    "bệnh viện": "nhà thương",
    "trượt": "trợt (trợt chân, trơn trợt); thi trượt → thi rớt",
    "đen đủi": "xui, xui xẻo",
    "giá đỗ": "giá",
    "thế này": "vầy, như vầy",
    "hẵng": "rồi mới…, … đã",
    "thảo nào": "hèn chi, hèn gì",
    "ai bảo": "ai biểu",
    "trông có vẻ": "coi bộ",
}


def compile_rules(rules, level):
    out = []
    for word, hint in rules.items():
        pattern = re.compile(r"(?<!\w)" + re.escape(word) + r"(?!\w)", re.IGNORECASE)
        out.append((level, word, hint, pattern))
    return out


RULES = compile_rules(ERRORS, "ERROR") + compile_rules(WARNINGS, "WARN")


def check(name, text):
    errors = 0
    for lineno, line in enumerate(unicodedata.normalize("NFC", text).splitlines(), 1):
        hits = sorted(
            (m.start(), level, m.group(0), hint)
            for level, _, hint, pattern in RULES
            for m in pattern.finditer(line)
        )
        for col, level, found, hint in hits:
            errors += level == "ERROR"
            print(f"{name}:{lineno}:{col + 1}: {level} '{found}' -> {hint}")
            print(f"    {line.strip()}")
    return errors


def main(argv):
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    errors = 0
    for path in argv:
        if path == "-":
            errors += check("<stdin>", sys.stdin.read())
        else:
            with open(path, encoding="utf-8") as f:
                errors += check(path, f.read())
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
