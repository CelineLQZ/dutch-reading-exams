#!/usr/bin/env python3
"""Build exam3-dict.json from the md word dictionaries, with verb conjugations."""
import json
import re
from pathlib import Path

PROJECT = Path("/Users/liceline/Documents/荷兰语融入考试阅读")
MD = PROJECT / "Lezen_A2_oefenexamen_3_sentence_word_dictionary.md"
OUT = PROJECT / "exam3-dict.json"

# Verb conjugation table: infinitive → (hij_3sg, verleden/past, voltooid/perfect)
VERBS = {
    # zijn / hebben / worden
    "zijn":      ("is",       "was",         "geweest"),
    "hebben":    ("heeft",    "had",         "gehad"),
    "worden":    ("wordt",    "werd",        "geworden"),
    # modals
    "kunnen":    ("kan",      "kon",         "gekund"),
    "moeten":    ("moet",     "moest",       "gemoeten"),
    "willen":    ("wil",      "wilde",       "gewild"),
    "mogen":     ("mag",      "mocht",       "gemogen"),
    "hoeven":    ("hoeft",    "hoefde",      "gehoeven"),
    "zullen":    ("zal",      "zou",         "—"),
    "laten":     ("laat",     "liet",        "gelaten"),
    # common irregular
    "gaan":      ("gaat",     "ging",        "gegaan"),
    "doen":      ("doet",     "deed",        "gedaan"),
    "komen":     ("komt",     "kwam",        "gekomen"),
    "zien":      ("ziet",     "zag",         "gezien"),
    "weten":     ("weet",     "wist",        "geweten"),
    "geven":     ("geeft",    "gaf",         "gegeven"),
    "nemen":     ("neemt",    "nam",         "genomen"),
    "blijven":   ("blijft",   "bleef",       "gebleven"),
    "vinden":    ("vindt",    "vond",        "gevonden"),
    "kopen":     ("koopt",    "kocht",       "gekocht"),
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
    "vertrekken":("vertrekt", "vertrok",     "vertrokken"),
    "vergeten":  ("vergeet",  "vergat",      "vergeten"),
    "breken":    ("breekt",   "brak",        "gebroken"),
    "leggen":    ("legt",     "legde",       "gelegd"),
    "bellen":    ("belt",     "belde",       "gebeld"),
    "zitten":    ("zit",      "zat",         "gezeten"),
    "afspreken": ("spreekt af","sprak af",   "afgesproken"),
    # regular -en verbs
    "volgen":    ("volgt",    "volgde",      "gevolgd"),
    "werken":    ("werkt",    "werkte",      "gewerkt"),
    "wonen":     ("woont",    "woonde",      "gewoond"),
    "stoppen":   ("stopt",    "stopte",      "gestopt"),
    "betalen":   ("betaalt",  "betaalde",    "betaald"),
    "maken":     ("maakt",    "maakte",      "gemaakt"),
    "parkeren":  ("parkeert", "parkeerde",   "geparkeerd"),
    "zoeken":    ("zoekt",    "zocht",       "gezocht"),
    "groeien":   ("groeit",   "groeide",     "gegroeid"),
    "helpen":    ("helpt",    "hielp",       "geholpen"),
    "zorgen":    ("zorgt",    "zorgde",      "gezorgd"),
    "passen":    ("past",     "paste",       "gepast"),
    "solliciteren":("solliciteert","solliciteerde","gesolliciteerd"),
    "bekijken":  ("bekijkt",  "bekeek",      "bekeken"),
    "vragen":    ("vraagt",   "vroeg",       "gevraagd"),
    "mailen":    ("mailt",    "mailde",      "gemaild"),
    "vertellen": ("vertelt",  "vertelde",    "verteld"),
    "oefenen":   ("oefent",   "oefende",     "geoefend"),
    "hopen":     ("hoopt",    "hoopte",      "gehoopt"),
    "beschrijven":("beschrijft","beschreef", "beschreven"),
    "kosten":    ("kost",     "kostte",      "gekost"),
    "duren":     ("duurt",    "duurde",      "geduurd"),
    "opsturen":  ("stuurt op","stuurde op",  "opgestuurd"),
    "sturen":    ("stuurt",   "stuurde",     "gestuurd"),
    "uitrekenen":("rekent uit","rekende uit","uitgerekend"),
    "bespreken": ("bespreekt","besprak",     "besproken"),
    "verhuizen": ("verhuist", "verhuisde",   "verhuisd"),
    "kennen":    ("kent",     "kende",       "gekend"),
    "verplaatsen":("verplaatst","verplaatste","verplaatst"),
    "informeren":("informeert","informeerde","geïnformeerd"),
    "meenemen":  ("neemt mee","nam mee",     "meegenomen"),
    "bestellen": ("bestelt",  "bestelde",    "besteld"),
    "leren":     ("leert",    "leerde",      "geleerd"),
    "beginnen":  ("begint",   "begon",       "begonnen"),
    "ontwerpen": ("ontwerpt", "ontwierp",    "ontworpen"),
    "inschrijven":("schrijft in","schreef in","ingeschreven"),
    "afmelden":  ("meldt af", "meldde af",   "afgemeld"),
    "melden":    ("meldt",    "meldde",      "gemeld"),
    "aanvragen": ("vraagt aan","vroeg aan",  "aangevraagd"),
    "opnemen":   ("neemt op", "nam op",      "opgenomen"),
    "plannen":   ("plant",    "plande",      "gepland"),
    "uitleggen": ("legt uit", "legde uit",   "uitgelegd"),
}

# Map each conjugated form back to its infinitive
FORM_TO_INF = {}
for inf, (hij, past, perf) in VERBS.items():
    for form in [inf, hij, past, perf]:
        # Strip particle for separable verbs (e.g., "stuurt op" → key "stuurt")
        head = form.split(" ", 1)[0]
        FORM_TO_INF[head] = inf
    # Also map common 1st-person forms (verb stem)
    # heuristic: remove final 't' from hij to get ik form for regular verbs
    if hij.endswith("t") and not hij.endswith("st") and hij not in {"zit", "is"}:
        stem = hij[:-1]
        if stem and stem not in FORM_TO_INF:
            FORM_TO_INF[stem] = inf
# Manual extras for 1st-person/2nd-person forms
EXTRA_FORMS = {
    "ben": "zijn", "bent": "zijn", "waren": "zijn",
    "heb": "hebben", "hebt": "hebben", "hadden": "hebben",
    "wordt": "worden", "werden": "worden",
    "kunt": "kunnen", "kun": "kunnen", "konden": "kunnen",
    "wilt": "willen", "wilden": "willen",
    "kwam": "komen", "kwamen": "komen",
    "wist": "weten", "wisten": "weten",
    "zag": "zien", "zagen": "zien",
    "gaf": "geven", "gaven": "geven",
    "ging": "gaan", "gingen": "gaan",
    "deed": "doen", "deden": "doen",
    "las": "lezen", "lazen": "lezen",
    "vroeg": "vragen", "vroegen": "vragen",
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
    "zorg": "zorgen",
    "meld": "melden",
    "bel": "bellen",
    "kom": "komen",
}
FORM_TO_INF.update(EXTRA_FORMS)

# Now parse md word dictionaries
md = MD.read_text()
# Find all word-dict tables
entries: dict[str, dict] = {}
# Pattern: section per article. Each `### Word dictionary` followed by table
table_blocks = re.findall(
    r"### Word dictionary\s*\n\s*\|[^\n]+\|[^\n]+\|\s*\n\s*\|[\s\-:|]+\|\s*\n((?:\s*\|[^\n]+\|[^\n]+\|\s*\n?)+)",
    md,
)

# Words to skip (md tags these as names/numbers/options)
SKIP_EN = {"name", "number", "option A / article a", "option B", "option C", "option D"}
SKIP_NL = {"a", "b", "c", "d"}  # skip option-letter entries

def is_verb(form: str) -> bool:
    return form in FORM_TO_INF

for block in table_blocks:
    for line in block.strip().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) != 2:
            continue
        nl, en = parts
        nl_lower = nl.lower()
        if not nl_lower or nl_lower in SKIP_NL:
            continue
        if en.strip() in SKIP_EN:
            continue
        if nl_lower in entries:
            # already have an entry — skip duplicate
            continue
        entry = {"nl": nl_lower, "en": en}
        if is_verb(nl_lower):
            inf = FORM_TO_INF[nl_lower]
            hij, past, perf = VERBS[inf]
            entry["pos"] = "verb"
            entry["verb"] = {
                "inf": inf,
                "hij": hij,
                "past": past,
                "perfect": perf,
            }
        entries[nl_lower] = entry

# sort and write
result = sorted(entries.values(), key=lambda e: e["nl"])
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
verb_count = sum(1 for e in result if e.get("pos") == "verb")
print(f"Wrote {len(result)} entries to {OUT.name} ({verb_count} verbs)")
