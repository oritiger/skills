#!/usr/bin/env python3
"""Flag machine-like patterns in Vietnamese text. Advisory only: it never edits.

Usage:
    check_ai_tells.py [--mode MODE] FILE
    printf '%s' "$TEXT" | check_ai_tells.py [--mode MODE] -

MODE: story (default), ads, script (video/voiceover), chat, polite, formal, academic.
Formal and academic texts are naturally more even, so rhythm warnings are
softened for them. Chat messages are short, so rhythm is not measured.

Phrase lists live in phrases.txt next to this script; add new ones there.
Tests: python3 test_check_ai_tells.py
"""
import argparse
import os
import re
import sys
import unicodedata
from statistics import mean, pstdev

HERE = os.path.dirname(os.path.abspath(__file__))
PHRASES_FILE = os.path.join(HERE, "phrases.txt")
MODES = ["story", "ads", "script", "chat", "polite", "formal", "academic"]
SOFT = {"formal", "academic"}
EMOTION_MODES = {"story", "ads", "script", "chat"}
NO_MARKDOWN_MODES = {"story", "chat", "script"}

# Sentence-length CV measured on real prose (see references/van-phong-tac-gia.md).
HUMAN_CV = {
    "Nam Cao": (0.65, 0.68),
    "Sơn Nam": (0.60, 0.67),
    "Nguyễn Ngọc Tư": (0.51, 0.63),
    "Nguyễn Nhật Ánh": (0.53, 0.65),
}
CV_LOW, CV_OK = 0.35, 0.45
CV_HIGH = 0.9  # narration choppier than any measured author: over-fragmented
SCRIPT_MAX_WORDS = 25  # longer than this is hard to read aloud in one breath
CLOSER_MODES = {"story", "ads", "script"}
DIALOGUE_START = re.compile(r"^\s*[\"“«‘'\-–—]")

WORD = re.compile(r"\w+")
CHUNK_SPLIT = re.compile(r",\s+|\s+và\s+|\s+hoặc\s+|\s+hay\s+")
ANAPHORA = re.compile(
    r"(?<!\w)(\w+) [^,.!?]{1,30}, \1 [^,.!?]{1,30}(?:,| và| hay| hoặc) \1(?!\w)(?: [^\s,.!?]+)?", re.IGNORECASE
)
OPENER = re.compile(r"^(trong (thời đại|bối cảnh|cuộc sống|thế giới|xã hội)|ngày nay|hiện nay)\b")
CLOSER = re.compile(r"^(tóm lại|nói tóm lại|nhìn chung|có thể nói|tất cả|hãy|đừng bỏ lỡ|còn chần chừ|cuối cùng)\b")
SELF_ANSWER = re.compile(r"^(đó (chính )?là|câu trả lời|rất đơn giản|bí mật nằm ở)\b")
DUMMY_NO = re.compile(r"^nó (là|sẽ|giúp|có|được|cho phép|mang)\b")
ONE_OF_MOST = re.compile(r"một trong những\b.{1,40}?\bnhất\b")
CUA_CHAIN = re.compile(r"(?<!\w)của [^,.!?]{1,25} của(?!\w)")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿]")
HASHTAG = re.compile(r"(?<![\w&])#\w+")
MARKDOWN_LINE = re.compile(r"^\s*(#{1,6}\s|[-*•]\s|\d+[.)]\s)")


def load_phrases(path=PHRASES_FILE):
    sections, current = {}, None
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            m = re.fullmatch(r"\[([\w-]+)\]", line)
            if m:
                current = m.group(1)
                sections.setdefault(current, [])
                continue
            if current is None:
                raise ValueError(f"{path}:{lineno}: cụm từ nằm ngoài mục [..]")
            sections[current].append(unicodedata.normalize("NFC", line.lower()))
    return sections


def phrase_re(p):
    return re.compile(r"(?<!\w)" + re.escape(p) + r"(?!\w)")


def words(text):
    return WORD.findall(text)


def split_sentences(paragraph):
    paragraph = re.sub(r"^\s*[-–—]\s*", "", paragraph)  # dialogue dash
    parts = re.split(r"(?<=[.!?…])[\"”»)]*\s+", paragraph)
    return [p.strip() for p in parts if words(p)]


def split_paragraphs(text):
    blocks = [b for b in re.split(r"\n\s*\n", text) if b.strip()]
    if len(blocks) == 1:
        blocks = [b for b in text.splitlines() if b.strip()]
    return blocks


def cv(values):
    return pstdev(values) / mean(values) if len(values) > 1 and mean(values) else 0.0


def similar_run(lengths, tol=0.2):
    """Longest run of consecutive sentences whose lengths stay within ±tol of the run's first."""
    best = run = 1
    for i in range(1, len(lengths)):
        base = lengths[i - run]
        if base and abs(lengths[i] - base) / base <= tol:
            run += 1
        else:
            run = 1
        best = max(best, run)
    return best if lengths else 0


def triplet(sentence):
    """Tidy three-part lists: "A, B và C" with short even items, or "có X, có Y, có Z"."""
    m = ANAPHORA.search(sentence)
    if m:
        return m.group(0)
    chunks = [c.strip(" .!?…\"'”") for c in CHUNK_SPLIT.split(sentence) if words(c)]
    for i in range(len(chunks) - 2):
        trio = chunks[i:i + 3]
        lens = [len(words(c)) for c in trio]
        firsts = {words(c)[0].lower() for c in trio}
        if (max(lens) <= 6 and max(lens) - min(lens) <= 2) or len(firsts) == 1:
            return " | ".join(trio)
    for i in range(1, len(chunks) - 1):  # "…tạo video nhanh chóng, dễ dàng và chuyên nghiệp"
        a, b = len(words(chunks[i])), len(words(chunks[i + 1]))
        if a <= 4 and b <= 4 and abs(a - b) <= 1:
            tail = " ".join(words(chunks[i - 1])[-max(a, b):])
            return f"…{tail} | {chunks[i]} | {chunks[i + 1]}"
    return None


def first_word(sentence):
    w = words(sentence)
    return w[0].lower() if w else ""


def analyze(text, mode="story", phrases=None):
    """Return {"sentences", "lengths", "cv", "n_words", "paragraphs", "warnings": [(code, message)]}."""
    if mode not in MODES:
        raise ValueError(f"mode phải là một trong {MODES}")
    phrases = phrases or load_phrases()
    text = unicodedata.normalize("NFC", text)
    low = text.lower()
    soft = mode in SOFT
    paragraphs = split_paragraphs(text)
    sentences = [s for p in paragraphs for s in split_sentences(p)]
    lengths = [len(words(s)) for s in sentences]
    narration = [len(words(s)) for p in paragraphs if not DIALOGUE_START.match(p)
                 for s in split_sentences(p) if not DIALOGUE_START.match(s)]
    n_words = len(words(text))
    warns = []

    def warn(code, msg):
        warns.append((code, msg))

    # Rhythm
    c = cv(lengths) if len(lengths) >= 5 else None
    if c is not None and mode != "chat" and not soft:
        if c < CV_LOW:
            warn("rhythm", f"Nhịp đều (CV {c:.2f} < {CV_LOW}): gộp hai câu thành một câu dài, tách một ý thành câu 2–5 chữ.")
        elif c < CV_OK:
            warn("rhythm", f"Nhịp hơi đều (CV {c:.2f}): cần một câu thật dài hoặc một câu thật ngắn.")
        run = similar_run(lengths)
        if run >= 4:
            warn("run", f"{run} câu liền nhau dài xấp xỉ nhau: phá chuỗi này.")
    c_narr = cv(narration) if len(narration) >= 8 else None
    if c_narr is not None and c_narr > CV_HIGH and mode != "chat":
        warn("choppy", f"Lời kể vụn quá (CV {c_narr:.2f} > {CV_HIGH}, cao hơn mọi nhà văn đã đo): "
                       "câu cụt chỉ mạnh khi đứng cạnh câu dài, gộp bớt vài câu cụt.")
    counts = [len(split_sentences(p)) for p in paragraphs]
    if len(counts) >= 4 and max(counts) - min(counts) <= 1 and not soft and mode != "chat":
        warn("paragraphs", f"Đoạn đều nhau {counts}: cho một đoạn chỉ một câu, một đoạn dài hơn hẳn.")
    if mode == "script":
        for s, n in zip(sentences, lengths):
            if n > SCRIPT_MAX_WORDS:
                warn("long-sentence", f"Câu {n} chữ khó đọc một hơi: «{s[:50]}…» → tách hoặc ngắt nghỉ.")

    # Structure
    for s in sentences:
        t = triplet(s)
        if t:
            warn("triplet", f"Liệt kê ba vế đều nhịp: «{t}» → giữ hai vế, hoặc cho một vế lệch hẳn.")
    firsts = [first_word(s) for s in sentences]
    run_word, run_len = None, 0
    for w in firsts:
        run_len = run_len + 1 if w == run_word else 1
        run_word = w
        if run_len == 3:
            warn("same-opener", f"Ba câu liền nhau cùng mở bằng «{w}»: đổi cách mở hoặc gộp câu.")
    if len(sentences) >= 5 and firsts.count("bạn") >= 3:
        warn("same-opener", f"«Bạn» mở {firsts.count('bạn')} câu: nói chuyện thôi, không cần gọi «bạn» mỗi câu.")

    # Phrases
    def hits(section):
        return [(p, len(phrase_re(p).findall(low))) for p in phrases.get(section, []) if phrase_re(p).search(low)]

    def listing(found):
        return ", ".join(f"«{p}»×{k}" if k > 1 else f"«{p}»" for p, k in found)

    for section, code, label in (
        ("strong", "phrases:strong", "Từ sáo"),
        ("ads", "phrases:ads", "Sáo quảng cáo"),
        ("wrappers", "wrappers", "Vỏ bọc trợ lý"),
        ("translationese", "translationese", "Dấu vết dịch máy"),
    ):
        found = hits(section)
        if found:
            warn(code, f"{label}: {listing(found)}")
    found = hits("connectors")
    if found and not (soft and sum(k for _, k in found) <= 2):
        warn("connectors", f"Liên từ khung: {listing(found)} → dùng mà/rồi/còn/nhưng hoặc bỏ.")
    dense = sum(k for _, k in hits("density"))
    if n_words and dense * 100 / n_words > 1.5:
        warn("density", f"Từ dùng nhiều thì lộ (mang lại, thực sự, vô cùng…): {dense} lần / {n_words} chữ.")
    found = hits("emotion")
    if found and mode in EMOTION_MODES:
        warn("emotion", f"Gọi tên cảm xúc: {listing(found)} → giao cho đồ vật, cơ thể, hành động.")

    # Translationese patterns
    extra = []
    extra += [f"«{s[:30]}…» (chủ ngữ giả «Nó»)" for s in sentences if DUMMY_NO.search(s.lower())]
    extra += [f"«{s[:30]}…» (danh hóa «Việc…»)" for s in sentences if s.lower().startswith("việc ")]
    extra += [f"«{m.group(0)}»" for m in ONE_OF_MOST.finditer(low)]
    extra += [f"«{m.group(0)}» (chuỗi «của»)" for m in CUA_CHAIN.finditer(low)]
    if extra:
        warn("translationese", "Dấu vết dịch máy: " + "; ".join(extra))

    k = len(re.findall(r"không chỉ\b.{1,80}?\bmà còn", low))
    if k:
        warn("khong-chi", f"«không chỉ… mà còn» ×{k}: nói thẳng một ý.")
    k = len(re.findall(r"(?<!\w)một cách \w+", low))
    if n_words and k * 150 / n_words > 1:
        warn("mot-cach", f"«một cách + tính từ» ×{k}: bỏ «một cách».")
    k = text.count("—")
    if n_words and k * 200 / n_words > 1:
        warn("emdash", f"Gạch ngang dài (—) ×{k}: thay bằng phẩy, ngoặc đơn, hoặc tách câu.")

    # Openers, closers, formulas
    if sentences:
        if OPENER.search(sentences[0].lower()):
            warn("opener", f"Mở bài khái quát: «{sentences[0][:60]}» → mở bằng việc đang xảy ra.")
        if len(sentences) > 2 and CLOSER.search(sentences[-1].lower()):
            warn("closer", f"Câu chốt công thức: «{sentences[-1][:60]}».")
        last, last_par = sentences[-1], paragraphs[-1]
        own_par = len(paragraphs) >= 3 and len(split_sentences(last_par)) == 1
        after_long = len(lengths) >= 2 and lengths[-2] >= 15
        trails_off = last.rstrip().endswith(("...", "…"))
        if (mode in CLOSER_MODES and len(sentences) >= 2 and not DIALOGUE_START.match(last_par)
                and lengths[-1] <= 10 and last.rstrip().endswith((".", "!")) and not trails_off
                and (own_par or after_long)):
            warn("closer-punch", f"Câu cuối có thể là câu chốt đắt giá: «{last[:60]}». "
                                 "Thử bỏ nó: bài vẫn đứng được thì bỏ.")
    formula = [s for s in sentences if re.match(r"(chỉ cần|chỉ với)\b", s.lower())]
    if formula and mode in ("ads", "script"):
        warn("formula", f"Công thức quảng cáo «Chỉ cần…»: «{formula[0][:60]}» → kể một lần dùng thật, cụ thể.")
    for a, b in zip(sentences, sentences[1:]):
        if a.rstrip().endswith("?") and SELF_ANSWER.search(b.lower()):
            warn("self-answer", f"Tự hỏi tự đáp kiểu công thức: «{a[:40]}» → «{b[:40]}».")

    # Formatting
    lines = [l for l in text.splitlines() if l.strip()]
    emoji_starts = sum(1 for l in lines if EMOJI.match(l.strip()))
    n_emoji = len(EMOJI.findall(text))
    if emoji_starts >= 3 or (n_words and n_emoji * 20 / n_words > 1):
        warn("emoji", f"Emoji dày ({n_emoji} cái, {emoji_starts} dòng mở bằng emoji): giữ 0–2 cái, đừng đặt đầu dòng.")
    n_tags = len(HASHTAG.findall(text))
    if n_tags > 3:
        warn("hashtag", f"{n_tags} hashtag: giữ tối đa 3.")
    md = sum(1 for l in lines if MARKDOWN_LINE.match(l)) + text.count("**")
    if md and mode in NO_MARKDOWN_MODES:
        warn("markdown", "Văn xuôi có tiêu đề, gạch đầu dòng hoặc in đậm: viết thành câu, thành đoạn.")

    return {"sentences": sentences, "lengths": lengths, "cv": c, "cv_narration": c_narr, "n_words": n_words,
            "paragraphs": len(paragraphs), "warnings": warns}


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--mode", default="story", choices=MODES)
    args = ap.parse_args(argv)
    raw = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    r = analyze(raw, args.mode)

    print(f"Câu: {len(r['sentences'])} | Chữ: {r['n_words']} | Đoạn: {r['paragraphs']} | Chế độ: {args.mode}")
    if r["cv"] is None:
        print("\n[NHỊP] dưới 5 câu, bỏ qua đo CV (đọc to để tự nghe nhịp).")
    else:
        ref = ", ".join(f"{k} {a:.2f}–{b:.2f}" for k, (a, b) in HUMAN_CV.items())
        print(f"\n[NHỊP] độ dài câu: {r['lengths']}")
        print(f"  TB {mean(r['lengths']):.1f} chữ, CV {r['cv']:.2f}  (người viết thật: {ref})")
        if r["cv_narration"] is not None:
            print(f"  CV riêng lời kể (bỏ lời thoại): {r['cv_narration']:.2f}")
    print(f"\n[CẢNH BÁO] {len(r['warnings'])}")
    for _, msg in r["warnings"]:
        print(f"  - {msg}")
    if not r["warnings"]:
        print("  Không thấy dấu hiệu máy rõ ràng. Vẫn đọc to một lần: chỗ nào trơn quá, chỗ đó đáng ngờ.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
