#!/usr/bin/env python3
"""Build knm-questions.json + extend knm-dict.json from the KNM exam-question md."""
import json
import re
from pathlib import Path

PROJECT = Path("/Users/liceline/Documents/荷兰语融入考试阅读")
MD = PROJECT / "KNM_exam_questions_answers_english_vocabulary.md"
OUT_DATA = PROJECT / "knm-questions.json"
DICT_PATH = PROJECT / "knm-dict.json"

md = MD.read_text()

# Roman/ordinal Dutch words → numeric label, for nicer titles
DEEL_NUM = {
    "Eerste": 1, "Tweede": 2, "Derde": 3, "Vierde": 4, "Vijfde": 5,
    "Zesde": 6, "Zevende": 7, "Achtste": 8, "Negende": 9, "Tiende": 10,
    "Elfde": 11, "Twaalfde": 12,
}

section_re = re.compile(r"^## KNM\s+(\S+)\s+deel\s+—\s+(.+)$", re.MULTILINE)
sections = []
matches = list(section_re.finditer(md))
for i, m in enumerate(matches):
    deel = m.group(1).strip()
    topic = m.group(2).strip()
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
    body = md[start:end]
    sections.append({"deel": deel, "topic": topic, "body": body, "num": DEEL_NUM.get(deel, i + 1)})


def split_options(block: str) -> list[str]:
    """Extract option lines like 'A. text' from a question block."""
    opts = []
    for line in block.splitlines():
        m = re.match(r"^\s*([A-E])\.\s*(.+?)\s*$", line)
        if m:
            opts.append({"letter": m.group(1), "text": m.group(2)})
    return opts


# Per-question block: ### Vraag N ... (until next ### or section end)
vraag_re = re.compile(r"^### Vraag\s+\d+\s*$", re.MULTILINE)
all_vocab_lines: list[str] = []
lessons = []

for sec in sections:
    body = sec["body"]
    vm = list(vraag_re.finditer(body))
    questions = []
    for i, v in enumerate(vm):
        start = v.end()
        end = vm[i + 1].start() if i + 1 < len(vm) else len(body)
        qblock = body[start:end]

        # Dutch sub-block (between '#### Dutch' and '#### English translation')
        dm = re.search(r"####\s*Dutch\s*\n(.*?)(?=####\s*English translation)", qblock, re.DOTALL)
        em = re.search(r"####\s*English translation\s*\n(.*?)(?=####\s*Vocabulary|\Z)", qblock, re.DOTALL)
        vmb = re.search(r"####\s*Vocabulary[^\n]*\n(.*?)(?=\Z)", qblock, re.DOTALL)
        if not (dm and em):
            continue
        dutch_block = dm.group(1).strip()
        english_block = em.group(1).strip()
        vocab_block = (vmb.group(1).strip() if vmb else "")

        # Answer line: "**Answer:** B. xxx"
        ans_m = re.search(r"\*\*Answer:\*\*\s*([A-E])\.", dutch_block)
        # Strip the answer line out of the question text
        dutch_text_block = re.sub(r"\*\*Answer:\*\*[^\n]*", "", dutch_block).strip()
        english_text_block = re.sub(r"\*\*Answer in English:\*\*[^\n]*", "", english_block).strip()

        # Split into question stem (lines before options) + options
        dutch_lines = dutch_text_block.splitlines()
        english_lines = english_text_block.splitlines()
        dutch_stem = []
        for ln in dutch_lines:
            if re.match(r"^\s*[A-E]\.\s+", ln):
                break
            dutch_stem.append(ln)
        english_stem = []
        for ln in english_lines:
            if re.match(r"^\s*[A-E]\.\s+", ln):
                break
            english_stem.append(ln)
        nl_question = re.sub(r"\s+", " ", " ".join(dutch_stem)).strip()
        en_question = re.sub(r"\s+", " ", " ".join(english_stem)).strip()

        nl_opts = split_options(dutch_text_block)
        en_opts = split_options(english_text_block)
        options = []
        for j, o in enumerate(nl_opts):
            en_text = en_opts[j]["text"] if j < len(en_opts) else o["text"]
            options.append({"letter": o["letter"], "nl": o["text"], "en": en_text})

        if not (nl_question and options and ans_m):
            continue

        questions.append({
            "id": f"q{i + 1}",
            "nl": nl_question,
            "en": en_question,
            "options": options,
            "answer": ans_m.group(1),
        })

        # Collect vocabulary lines for dict augmentation
        for line in vocab_block.splitlines():
            line = line.strip()
            if not line.startswith("|") or line.startswith("|---") or line.startswith("| Dutch"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) == 2:
                all_vocab_lines.append(f"{cells[0]} = {cells[1]}")

    if questions:
        # Reshape each question as a `sentence` so the existing flatten / picker logic works.
        sentences = [
            {
                "nl": q["nl"],
                "en": q["en"],
                "question": {
                    "options": q["options"],
                    "answer": q["answer"],
                },
            }
            for q in questions
        ]
        lessons.append({
            "id": f"knm-q-{sec['num']}",
            "les": 300 + sec["num"],         # 301..310, separate range from knowledge points
            "exam": "knm-questions",
            "examIndex": sec["num"],
            "label": f"KNM-Q.{sec['num']}",
            "title": f"KNM Q{sec['num']} — {sec['topic']}",
            "rawTitle": f"{sec['deel']} deel — {sec['topic']}",
            "sentences": sentences,
        })

OUT_DATA.write_text(json.dumps(lessons, ensure_ascii=False, indent=2) + "\n")
total_q = sum(len(l["sentences"]) for l in lessons)
print(f"Wrote {len(lessons)} sections, {total_q} questions → {OUT_DATA.name}")
for l in lessons:
    print(f"  {l['id']} ({l['title']}): {len(l['sentences'])} vragen")

# Augment knm-dict.json with new vocabulary (additive, never overwrite)
existing = []
if DICT_PATH.exists():
    existing = json.loads(DICT_PATH.read_text())
by_nl = {e["nl"].lower(): e for e in existing}
new_count = 0
for line in all_vocab_lines:
    if "=" not in line:
        continue
    nl, en = line.split("=", 1)
    nl = nl.strip().lower().strip("()")
    en = en.strip()
    if not nl or len(nl) > 60 or not en:
        continue
    if nl in by_nl:
        continue
    by_nl[nl] = {"nl": nl, "en": en}
    new_count += 1
merged = sorted(by_nl.values(), key=lambda e: e["nl"])
DICT_PATH.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n")
print(f"\nAdded {new_count} new entries to {DICT_PATH.name} (total {len(merged)})")
