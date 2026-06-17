#!/usr/bin/env python3
"""Build listenings.json + listening-dict.json from the listening exam md."""
import json
import re
from pathlib import Path

PROJECT = Path("/Users/liceline/Documents/荷兰语融入考试阅读")
MD = PROJECT / "Luisteren_A2_Exam_1_sentence_translation_vocabulary.md"
OUT_READ = PROJECT / "listenings.json"
OUT_DICT = PROJECT / "listening-dict.json"

# verb table reused from exam dicts
VERBS = {
    "zijn":      ("is",       "was",         "geweest"),
    "hebben":    ("heeft",    "had",         "gehad"),
    "worden":    ("wordt",    "werd",        "geworden"),
    "kunnen":    ("kan",      "kon",         "gekund"),
    "moeten":    ("moet",     "moest",       "gemoeten"),
    "willen":    ("wil",      "wilde",       "gewild"),
    "mogen":     ("mag",      "mocht",       "gemogen"),
    "hoeven":    ("hoeft",    "hoefde",      "gehoeven"),
    "zullen":    ("zal",      "zou",         "—"),
    "laten":     ("laat",     "liet",        "gelaten"),
    "gaan":      ("gaat",     "ging",        "gegaan"),
    "doen":      ("doet",     "deed",        "gedaan"),
    "komen":     ("komt",     "kwam",        "gekomen"),
    "zien":      ("ziet",     "zag",         "gezien"),
    "weten":     ("weet",     "wist",        "geweten"),
    "geven":     ("geeft",    "gaf",         "gegeven"),
    "nemen":     ("neemt",    "nam",         "genomen"),
    "blijven":   ("blijft",   "bleef",       "gebleven"),
    "vinden":    ("vindt",    "vond",        "gevonden"),
    "kiezen":    ("kiest",    "koos",        "gekozen"),
    "lezen":     ("leest",    "las",         "gelezen"),
    "eten":      ("eet",      "at",          "gegeten"),
    "schrijven": ("schrijft", "schreef",     "geschreven"),
    "spreken":   ("spreekt",  "sprak",       "gesproken"),
    "krijgen":   ("krijgt",   "kreeg",       "gekregen"),
    "brengen":   ("brengt",   "bracht",      "gebracht"),
    "denken":    ("denkt",    "dacht",       "gedacht"),
    "houden":    ("houdt",    "hield",       "gehouden"),
    "rijden":    ("rijdt",    "reed",        "gereden"),
    "vergeten":  ("vergeet",  "vergat",      "vergeten"),
    "breken":    ("breekt",   "brak",        "gebroken"),
    "leggen":    ("legt",     "legde",       "gelegd"),
    "bellen":    ("belt",     "belde",       "gebeld"),
    "zitten":    ("zit",      "zat",         "gezeten"),
    "afspreken": ("spreekt af","sprak af",   "afgesproken"),
    "volgen":    ("volgt",    "volgde",      "gevolgd"),
    "werken":    ("werkt",    "werkte",      "gewerkt"),
    "wonen":     ("woont",    "woonde",      "gewoond"),
    "stoppen":   ("stopt",    "stopte",      "gestopt"),
    "betalen":   ("betaalt",  "betaalde",    "betaald"),
    "maken":     ("maakt",    "maakte",      "gemaakt"),
    "zoeken":    ("zoekt",    "zocht",       "gezocht"),
    "helpen":    ("helpt",    "hielp",       "geholpen"),
    "zorgen":    ("zorgt",    "zorgde",      "gezorgd"),
    "passen":    ("past",     "paste",       "gepast"),
    "vragen":    ("vraagt",   "vroeg",       "gevraagd"),
    "mailen":    ("mailt",    "mailde",      "gemaild"),
    "vertellen": ("vertelt",  "vertelde",    "verteld"),
    "oefenen":   ("oefent",   "oefende",     "geoefend"),
    "hopen":     ("hoopt",    "hoopte",      "gehoopt"),
    "kosten":    ("kost",     "kostte",      "gekost"),
    "duren":     ("duurt",    "duurde",      "geduurd"),
    "sturen":    ("stuurt",   "stuurde",     "gestuurd"),
    "kennen":    ("kent",     "kende",       "gekend"),
    "halen":     ("haalt",    "haalde",      "gehaald"),
    "leren":     ("leert",    "leerde",      "geleerd"),
    "horen":     ("hoort",    "hoorde",      "gehoord"),
    "wachten":   ("wacht",    "wachtte",     "gewacht"),
    "kijken":    ("kijkt",    "keek",        "gekeken"),
    "luisteren": ("luistert", "luisterde",   "geluisterd"),
    "melden":    ("meldt",    "meldde",      "gemeld"),
    "bedanken":  ("bedankt",  "bedankte",    "bedankt"),
    "gebruiken": ("gebruikt", "gebruikte",   "gebruikt"),
    "praten":    ("praat",    "praatte",     "gepraat"),
    "openen":    ("opent",    "opende",      "geopend"),
    "sluiten":   ("sluit",    "sloot",       "gesloten"),
    "bereiken":  ("bereikt",  "bereikte",    "bereikt"),
    "draaien":   ("draait",   "draaide",     "gedraaid"),
    "schilderen":("schildert","schilderde",  "geschilderd"),
    "klussen":   ("klust",    "kluste",      "geklust"),
    "vieren":    ("viert",    "vierde",      "gevierd"),
    "uitnodigen":("nodigt uit","nodigde uit","uitgenodigd"),
    "verkopen":  ("verkoopt", "verkocht",    "verkocht"),
    "verwerken": ("verwerkt", "verwerkte",   "verwerkt"),
    "verpakken": ("verpakt",  "verpakte",    "verpakt"),
    "starten":   ("start",    "startte",     "gestart"),
    "aanmelden": ("meldt aan","meldde aan",  "aangemeld"),
    "inschrijven":("schrijft in","schreef in","ingeschreven"),
    "repareren": ("repareert","repareerde",  "gerepareerd"),
    "bestellen": ("bestelt",  "bestelde",    "besteld"),
    "snijden":   ("snijdt",   "sneed",       "gesneden"),
    "veranderen":("verandert","veranderde",  "veranderd"),
    "reserveren":("reserveert","reserveerde","gereserveerd"),
    "ophalen":   ("haalt op", "haalde op",   "opgehaald"),
    "terugbellen":("belt terug","belde terug","teruggebeld"),
    "doorlezen": ("leest door","las door",   "doorgelezen"),
    "controleren":("controleert","controleerde","gecontroleerd"),
    "bespreken": ("bespreekt","besprak",     "besproken"),
    "meenemen":  ("neemt mee","nam mee",     "meegenomen"),
    "lopen":     ("loopt",    "liep",        "gelopen"),
    "ontbijten": ("ontbijt",  "ontbeet",     "ontbeten"),
    "klaarzetten":("zet klaar","zette klaar","klaargezet"),
    "dansen":    ("danst",    "danste",      "gedanst"),
    "winnen":    ("wint",     "won",         "gewonnen"),
    "versieren": ("versiert", "versierde",   "versierd"),
    "eindigen":  ("eindigt",  "eindigde",    "geëindigd"),
    "doen":      ("doet",     "deed",        "gedaan"),
    "tegenkomen":("komt tegen","kwam tegen", "tegengekomen"),
}

FORM_TO_INF = {}
for inf, (hij, past, perf) in VERBS.items():
    for form in [inf, hij, past, perf]:
        head = form.split(" ", 1)[0]
        if head and head != "—":
            FORM_TO_INF.setdefault(head, inf)
    if hij and hij.endswith("t") and not hij.endswith("st") and hij not in {"zit", "is"}:
        stem = hij[:-1]
        if stem:
            FORM_TO_INF.setdefault(stem, inf)

EXTRAS = {
    "ben": "zijn", "bent": "zijn", "waren": "zijn",
    "heb": "hebben", "hebt": "hebben", "hadden": "hebben",
    "wordt": "worden", "werden": "worden",
    "kunt": "kunnen", "kun": "kunnen", "konden": "kunnen",
    "wilt": "willen", "wilden": "willen",
    "kwam": "komen", "kwamen": "komen",
    "wist": "weten",
    "zag": "zien",
    "gaf": "geven",
    "ging": "gaan",
    "deed": "doen",
    "las": "lezen",
    "vroeg": "vragen",
    "vonden": "vinden",
    "kostte": "kosten",
    "belde": "bellen",
    "kreeg": "krijgen",
    "geef": "geven",
    "lees": "lezen",
    "schrijf": "schrijven",
    "neem": "nemen",
    "stuur": "sturen",
    "zoek": "zoeken",
    "doe": "doen",
    "kom": "komen",
    "praatte": "praten",
    "zei": "zeggen",
    "zien": "zien",
    "ziet": "zien",
}
FORM_TO_INF.update(EXTRAS)

md = MD.read_text()

# Each scene is a `# N. Title` block.
scene_re = re.compile(r"^# (\d+)\.\s+(.+)$", re.MULTILINE)
matches = list(scene_re.finditer(md))
listenings = []
all_dict_lines = []  # collect words from every Vocabulary Dictionary table

for i, m in enumerate(matches):
    num = int(m.group(1))
    title_raw = m.group(2).strip()
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
    block = md[start:end]

    # Collect sentences from Context / Dialogue / Text / Voicemail / Announcement / Teacher / News report
    # NOT from Questions or Vocabulary Dictionary.
    sentences = []
    SECTION_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    section_matches = list(SECTION_RE.finditer(block))
    for j, sm in enumerate(section_matches):
        section_name = sm.group(1).strip()
        sec_start = sm.end()
        sec_end = section_matches[j + 1].start() if j + 1 < len(section_matches) else len(block)
        section_body = block[sec_start:sec_end]
        if section_name == "Vocabulary Dictionary":
            # collect for dict
            for line in section_body.strip().splitlines():
                line = line.strip()
                if not line.startswith("|") or line.startswith("|---") or "Dutch" in line.split("|")[1:2]:
                    continue
                all_dict_lines.append(line)
            continue
        if section_name == "Questions":
            # skip — questions aren't main content
            continue
        # Otherwise parse a table of NL | EN pairs
        for line in section_body.strip().splitlines():
            line = line.strip()
            if not line.startswith("|") or line.startswith("|---"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) != 2:
                continue
            nl, en = cells
            if nl == "Dutch" or not nl:
                continue
            sentences.append({"nl": nl, "en": en})

    listenings.append({
        "id": f"listen1-{num}",
        "les": 100 + num,  # use 101..110 so they don't collide with reading article les
        "exam": "listen1",
        "examIndex": num,
        "label": f"L1.{num}",
        "title": f"L1.{num} {title_raw}",
        "rawTitle": title_raw,
        "sentences": sentences,
    })

OUT_READ.write_text(json.dumps(listenings, ensure_ascii=False, indent=2) + "\n")
print(f"Wrote {len(listenings)} listening scenes to {OUT_READ.name}")
for a in listenings:
    print(f"  {a['id']} ({a['title']}): {len(a['sentences'])} sentences")

# Build dictionary
SKIP_EN = {"name", "number"}
entries: dict[str, dict] = {}
for line in all_dict_lines:
    cells = [c.strip() for c in line.strip("|").split("|")]
    if len(cells) != 2:
        continue
    nl, en = cells
    if not nl or nl == "Dutch":
        continue
    # Split phrase entries by whitespace into individual word keys but also keep the phrase key
    keys_to_add = [nl.lower().strip()]
    for ks in keys_to_add:
        if ks in entries or not ks:
            continue
        entry = {"nl": ks, "en": en}
        # check if any token in the phrase matches a verb form — only mark the whole entry as verb if the entry is a single token
        single = ks.split()
        if len(single) == 1 and single[0] in FORM_TO_INF:
            inf = FORM_TO_INF[single[0]]
            if inf in VERBS:
                hij, past, perf = VERBS[inf]
                entry["pos"] = "verb"
                entry["verb"] = {"inf": inf, "hij": hij, "past": past, "perfect": perf}
        entries[ks] = entry

# Also add individual word entries for tokens inside phrases that we know are verbs
phrase_tokens_added = set()
for line in all_dict_lines:
    cells = [c.strip() for c in line.strip("|").split("|")]
    if len(cells) != 2:
        continue
    nl, _ = cells
    for tok in re.findall(r"[A-Za-zÀ-ÿ]+", nl.lower()):
        if tok in entries or tok in phrase_tokens_added:
            continue
        if tok in FORM_TO_INF:
            inf = FORM_TO_INF[tok]
            if inf in VERBS:
                hij, past, perf = VERBS[inf]
                entries[tok] = {
                    "nl": tok,
                    "en": f"({inf}) — see dictionary entry",
                    "pos": "verb",
                    "verb": {"inf": inf, "hij": hij, "past": past, "perfect": perf},
                }
                phrase_tokens_added.add(tok)

result = sorted(entries.values(), key=lambda e: e["nl"])
OUT_DICT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
verb_count = sum(1 for e in result if e.get("pos") == "verb")
print(f"\nWrote {len(result)} dict entries to {OUT_DICT.name} ({verb_count} verbs)")
