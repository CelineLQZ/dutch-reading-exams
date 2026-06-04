#!/usr/bin/env python3
"""Rebuild exam 2 articles in readings.json from the md sentence dictionary."""
import json
import re
from pathlib import Path

PROJECT = Path("/Users/liceline/Documents/荷兰语融入考试阅读")
MD = PROJECT / "Lezen_A2_oefenexamen_2_sentence_word_dictionary_corrected.md"
READINGS = PROJECT / "readings.json"

# Map md section number → title from existing readings.json
TITLES = {
    1: "2.1 Tandartspraktijk",
    2: "2.2 CV maken",
    3: "2.3 Talenschool Het Palet",
    4: "2.4 Ziekmelding",
    5: "2.5 Buurtbijeenkomst",
    6: "2.6 Sportcentrum",
    7: "2.7 Brief aan docent",
    8: "2.8 Huisarts",
    9: "2.9 Woorden leren",
    10: "2.10 Hotelrooster",
    11: "2.11 Bloemenwinkel",
}
RAW_TITLES = {n: t.split(" ", 1)[1] for n, t in TITLES.items()}

NUMBER_NAMES = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
    "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9,
    "Ten": 10, "Eleven": 11,
}

md = MD.read_text()
articles = []
# section headings look like: ## One — Tandartspraktijk
sections = re.split(
    r"^## (One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven)\b.*?$",
    md,
    flags=re.MULTILINE,
)
for i in range(1, len(sections), 2):
    name = sections[i]
    content = sections[i + 1]
    n = NUMBER_NAMES[name]
    # Sentence dictionary block: ### Sentence dictionary ... ### Word dictionary
    sd_match = re.search(
        r"### Sentence dictionary\s*(.*?)\s*### Word dictionary",
        content, re.DOTALL,
    )
    if not sd_match:
        continue
    block = sd_match.group(1)
    sentences = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Dutch sentence"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) != 2:
            continue
        nl, en = parts
        if not nl or nl in ("Dutch sentence",):
            continue
        sentences.append({"nl": nl, "en": en})
    articles.append({
        "id": f"exam2-{n}",
        "les": 10 + n,
        "exam": 2,
        "examIndex": n,
        "label": f"2.{n}",
        "title": TITLES[n],
        "rawTitle": RAW_TITLES[n],
        "sentences": sentences,
    })

readings = json.loads(READINGS.read_text())
new_readings = [r for r in readings if not r.get("id", "").startswith("exam2-")]
out = []
inserted = False
for r in new_readings:
    if not inserted and r.get("id", "").startswith("exam3-"):
        out.extend(articles)
        inserted = True
    out.append(r)
if not inserted:
    out.extend(articles)

READINGS.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(f"Wrote {len(articles)} new exam2 articles, total readings = {len(out)}")
for a in articles:
    print(f"  {a['id']} ({a['title']}): {len(a['sentences'])} sentences")
