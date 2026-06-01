#!/usr/bin/env python3
"""Rebuild exam 3 articles in readings.json from the md dictionary file."""
import json
import re
from pathlib import Path

PROJECT = Path("/Users/liceline/Documents/荷兰语融入考试阅读")
MD = PROJECT / "Lezen_A2_oefenexamen_3_sentence_word_dictionary.md"
READINGS = PROJECT / "readings.json"

TITLES = {
    1: "3.1 Beste cursist",
    2: "3.2 Gratis stadsbus",
    3: "3.3 Beste buurtbewoner",
    4: "3.4 Verkopers Gezocht",
    5: "3.5 Hoi Chang",
    6: "3.6 Beste Selina",
    7: "3.7 Cursus Houten Meubels Maken",
    8: "3.8 Geachte mevrouw",
    9: "3.9 Dag Lito",
}
RAW_TITLES = {n: t.split(" ", 1)[1] for n, t in TITLES.items()}

md = MD.read_text()
# Split by sections "## One", "## Two", etc.
NUMBER_NAMES = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
    "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9
}
articles = []
sections = re.split(r"^## (One|Two|Three|Four|Five|Six|Seven|Eight|Nine)\b", md, flags=re.MULTILINE)
# sections[0] is preamble; then pairs of (name, content)
for i in range(1, len(sections), 2):
    name = sections[i]
    content = sections[i + 1]
    n = NUMBER_NAMES[name]
    # extract sentence dict — between "### Sentence dictionary" and "### Word dictionary"
    sd_match = re.search(
        r"### Sentence dictionary\s*(.*?)\s*### Word dictionary",
        content, re.DOTALL,
    )
    if not sd_match:
        continue
    block = sd_match.group(1)
    # Each entry: `N. **NL:** ...\n   **EN:** ...`
    entries = re.findall(
        r"\d+\.\s+\*\*NL:\*\*\s*(.+?)\s*\n\s+\*\*EN:\*\*\s*(.+?)(?=\n\d+\.\s+\*\*NL:\*\*|\Z)",
        block, re.DOTALL,
    )
    sentences = []
    for nl, en in entries:
        nl_clean = re.sub(r"\s+", " ", nl).strip()
        en_clean = re.sub(r"\s+", " ", en).strip()
        sentences.append({"nl": nl_clean, "en": en_clean})
    articles.append({
        "id": f"exam3-{n}",
        "les": 21 + n,
        "exam": 3,
        "examIndex": n,
        "label": f"3.{n}",
        "title": TITLES[n],
        "rawTitle": RAW_TITLES[n],
        "sentences": sentences,
    })

# Load existing readings.json
readings = json.loads(READINGS.read_text())
# Remove old exam 3
new_readings = [r for r in readings if not r.get("id", "").startswith("exam3-")]
# Find insertion point — keep order: insert exam3 articles between exam2 and exam4
out = []
inserted = False
for r in new_readings:
    if not inserted and r.get("id", "").startswith("exam4-"):
        out.extend(articles)
        inserted = True
    out.append(r)
if not inserted:
    out.extend(articles)

READINGS.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(f"Wrote {len(articles)} new exam3 articles, total readings = {len(out)}")
for a in articles:
    print(f"  {a['id']} ({a['title']}): {len(a['sentences'])} sentences")
