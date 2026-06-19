#!/usr/bin/env python3
"""Rebuild exam 4 articles in readings.json from the new md."""
import json
import re
from pathlib import Path

PROJECT = Path("/Users/liceline/Documents/荷兰语融入考试阅读")
MD = PROJECT / "Lezen_A2_oefenexamen_4_sentence_translation_vocabulary.md"
READINGS = PROJECT / "readings.json"

TITLES = {
    1: "4.1 Hallo allemaal",
    2: "4.2 Cursus Techniek",
    3: "4.3 Andere routes bus 14 en bus 323",
    4: "4.4 Verbouwing Kuijpergebouw",
    5: "4.5 Beste collega's",
    6: "4.6 Beste Yuri",
    7: "4.7 Kapper Style",
    8: "4.8 Hallo iedereen",
    9: "4.9 Beste collega's",
}
RAW = {n: t.split(" ", 1)[1] for n, t in TITLES.items()}

md = MD.read_text()

# Each article begins with `# N. Title` (top-level header)
scene_re = re.compile(r"^# (\d+)\.\s+(.+)$", re.MULTILINE)
matches = list(scene_re.finditer(md))
articles = []
for i, m in enumerate(matches):
    num = int(m.group(1))
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
    block = md[start:end]

    # Find the "Sentence translation" section
    sec_match = re.search(
        r"## Sentence translation\s*(.*?)\s*## ",
        block, re.DOTALL,
    )
    if not sec_match:
        continue
    body = sec_match.group(1)
    sentences = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Dutch"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 2:
            continue
        nl, en = cells
        if not nl or nl == "Dutch":
            continue
        sentences.append({"nl": nl, "en": en})
    articles.append({
        "id": f"exam4-{num}",
        "les": 30 + num,
        "exam": 4,
        "examIndex": num,
        "label": f"4.{num}",
        "title": TITLES[num],
        "rawTitle": RAW[num],
        "sentences": sentences,
    })

readings = json.loads(READINGS.read_text())
new_readings = [r for r in readings if not r.get("id", "").startswith("exam4-")]
out = []
inserted = False
for r in new_readings:
    rid = r.get("id", "")
    if not inserted and (rid.startswith("listen") or rid.startswith("exam5") or rid.startswith("examR")):
        out.extend(articles)
        inserted = True
    out.append(r)
if not inserted:
    # exam 4 goes after exam 3, before everything else
    out_with_4 = []
    inserted = False
    for r in new_readings:
        out_with_4.append(r)
        if not inserted and r.get("id", "").startswith("exam3-9"):
            out_with_4.extend(articles)
            inserted = True
    if not inserted:
        out_with_4.extend(articles)
    out = out_with_4

READINGS.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(f"Wrote {len(articles)} new exam4 articles. Total readings = {len(out)}")
for a in articles:
    print(f"  {a['id']} ({a['title']}): {len(a['sentences'])} sentences")
