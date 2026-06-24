#!/usr/bin/env python3
"""Build knm.json + knm-dict.json from KNM md, with fact-blank quiz data per sentence."""
import json
import random
import re
from pathlib import Path

PROJECT = Path("/Users/liceline/Documents/荷兰语融入考试阅读")
MD = PROJECT / "KNM_knowledge_points_translation_vocabulary.md"
OUT_DATA = PROJECT / "knm.json"
OUT_DICT = PROJECT / "knm-dict.json"

random.seed(20260101)  # deterministic distractor selection

md = MD.read_text()

NUMBER_WORDS = {
    "twee", "drie", "vier", "vijf", "zes", "zeven", "acht", "negen", "tien",
    "elf", "twaalf", "dertien", "veertien", "vijftien", "zestien", "zeventien",
    "achttien", "negentien", "twintig", "dertig", "veertig", "vijftig",
    "zestig", "zeventig", "tachtig", "negentig", "honderd", "duizend",
}

# Words that look capitalized but aren't worth blanking (sentence-start filler,
# month names alone, etc.)
SKIP_PROPER = {
    # Common Dutch capitalized non-proper words / sentence-internal capitalizations
    "Nederland", "Nederlandse", "Nederlanders", "Een", "De", "Het", "Een",
    "Maar", "Want", "Omdat", "Voor", "Ook", "Als", "Bij", "In", "Op",
    "Mensen", "Iedereen", "Dat", "Dit", "Die", "Er", "Je", "Jij", "Hij", "Zij",
    "Wij", "Wie", "Wat", "Waar", "Wanneer", "Hoe", "Welke", "Wel", "Niet",
    "Iemand", "Niemand", "Iets", "Niets", "Soms", "Vaak", "Altijd", "Nooit",
    "Veel", "Weinig", "Sommige", "Andere", "Ander", "Elke", "Elk", "Alle",
    "Vandaag", "Morgen", "Gisteren", "Eerst", "Daarna", "Dan", "Toen",
    "Nu", "Toch", "Daarom", "Misschien", "Bijvoorbeeld",
}

lesson_re = re.compile(r"^# Lesson (\d+) — (.+)$", re.MULTILINE)
point_re = re.compile(
    r"##\s*Kennispunt\s*\d+\s*\n\s*\*\*Dutch:\*\*\s*(.+?)\s*\n\s*\*\*English:\*\*\s*(.+?)\s*\n\s*\*\*Vocabulary:\*\*\s*(.+?)(?=\n## |\Z)",
    re.DOTALL,
)


def find_blank_candidate(sentence: str):
    """Return (category, blank_text, start, end) of the best blank target, or None."""
    # 1. Digits (highest priority — clear facts)
    for m in re.finditer(r"\b\d[\d.,]*\b", sentence):
        # Skip year-ranges in parens like "(1815-1830)" — too brittle
        return ("number", m.group(), m.start(), m.end())
    # 2. Number words
    for m in re.finditer(r"\b(" + "|".join(NUMBER_WORDS) + r")\b", sentence, re.IGNORECASE):
        return ("number-word", m.group(), m.start(), m.end())
    # 3. Mid-sentence capitalized proper nouns (place names, institutions, holidays)
    for m in re.finditer(r"(?<=[a-zà-ÿ\s])\b([A-Z][a-zà-ÿ]+(?:[- ][A-Z][a-zà-ÿ]+){0,3})\b", sentence):
        text = m.group(1)
        if text in SKIP_PROPER:
            continue
        return ("proper", text, m.start(1), m.end(1))
    return None


# First pass: collect all candidates by category for distractor pools
all_lessons_raw = []
pools: dict[str, list[str]] = {"number": [], "number-word": [], "proper": []}
all_vocab_lines: list[str] = []

for lm in lesson_re.finditer(md):
    num = int(lm.group(1))
    raw_title = lm.group(2).strip()
    start = lm.end()
    next_match = lesson_re.search(md, lm.end())
    end = next_match.start() if next_match else len(md)
    body = md[start:end]
    points = []
    for pm in point_re.finditer(body):
        nl = re.sub(r"\s+", " ", pm.group(1)).strip()
        en = re.sub(r"\s+", " ", pm.group(2)).strip()
        vocab = re.sub(r"\s+", " ", pm.group(3)).strip()
        all_vocab_lines.append(vocab)
        cand = find_blank_candidate(nl)
        if cand:
            cat, text, s, e = cand
            # Don't seed the proper-noun pool with anything in SKIP_PROPER (safety net)
            if cat == "proper" and text in SKIP_PROPER:
                cand = None
            elif text not in pools[cat]:
                pools[cat].append(text)
        points.append({"nl": nl, "en": en, "cand": cand})
    all_lessons_raw.append({"num": num, "raw_title": raw_title, "points": points})

# Second pass: emit lessons with quiz blanks + distractors
def pick_distractors(pool: list[str], correct: str, n: int = 3) -> list[str]:
    others = [w for w in pool if w.lower() != correct.lower()]
    if len(others) <= n:
        return others
    return random.sample(others, n)


lessons = []
for lr in all_lessons_raw:
    sentences = []
    for p in lr["points"]:
        item = {"nl": p["nl"], "en": p["en"]}
        cand = p["cand"]
        if cand:
            cat, text, s, e = cand
            distractors = pick_distractors(pools[cat], text)
            if distractors:
                item["quiz"] = {
                    "blank": text,
                    "category": cat,
                    "before": p["nl"][:s],
                    "after": p["nl"][e:],
                    "distractors": distractors,
                }
        sentences.append(item)
    lessons.append({
        "id": f"knm-{lr['num']}",
        "les": 200 + lr["num"],
        "exam": "knm",
        "examIndex": lr["num"],
        "label": f"KNM.{lr['num']}",
        "title": f"KNM.{lr['num']} {lr['raw_title']}",
        "rawTitle": lr["raw_title"],
        "sentences": sentences,
    })

OUT_DATA.write_text(json.dumps(lessons, ensure_ascii=False, indent=2) + "\n")
print(f"Wrote {len(lessons)} KNM lessons → {OUT_DATA.name}")
quiz_count = sum(sum(1 for s in l["sentences"] if s.get("quiz")) for l in lessons)
total_count = sum(len(l["sentences"]) for l in lessons)
print(f"  {quiz_count} / {total_count} sentences have a fact-blank quiz")
for l in lessons:
    qn = sum(1 for s in l["sentences"] if s.get("quiz"))
    print(f"  {l['id']}: {len(l['sentences'])} points, {qn} quizzable")
print(f"\nDistractor pool sizes: number={len(pools['number'])}, number-word={len(pools['number-word'])}, proper={len(pools['proper'])}")

# Vocabulary dict
entries: dict[str, dict] = {}
for line in all_vocab_lines:
    for chunk in line.split(";"):
        chunk = chunk.strip().rstrip(".")
        if "=" not in chunk:
            continue
        nl, en = chunk.split("=", 1)
        nl = nl.strip().lower().strip("()")
        en = en.strip()
        if not nl or len(nl) > 60 or not en:
            continue
        if nl in entries:
            continue
        entries[nl] = {"nl": nl, "en": en}

result = sorted(entries.values(), key=lambda e: e["nl"])
OUT_DICT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(f"\nWrote {len(result)} dict entries → {OUT_DICT.name}")
