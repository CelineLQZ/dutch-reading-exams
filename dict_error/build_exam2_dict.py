#!/usr/bin/env python3
"""Build exam2-dict.json from the md word dictionaries, with verb conjugations."""
import json
import re
from pathlib import Path

PROJECT = Path("/Users/liceline/Documents/荷兰语融入考试阅读")
MD = PROJECT / "Lezen_A2_oefenexamen_2_sentence_word_dictionary_corrected.md"
OUT = PROJECT / "exam2-dict.json"

# Verb conjugation table — same shape as exam3
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
    "vergeten":  ("vergeet",  "vergat",      "vergeten"),
    "breken":    ("breekt",   "brak",        "gebroken"),
    "leggen":    ("legt",     "legde",       "gelegd"),
    "bellen":    ("belt",     "belde",       "gebeld"),
    "zitten":    ("zit",      "zat",         "gezeten"),
    "afspreken": ("spreekt af","sprak af",   "afgesproken"),
    # regular verbs from exam 2
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
    "solliciteren":("solliciteert","solliciteerde","gesolliciteerd"),
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
    "schrijven": ("schrijft", "schreef",     "geschreven"),
    "melden":    ("meldt",    "meldde",      "gemeld"),
    "bedanken":  ("bedankt",  "bedankte",    "bedankt"),
    "gebruiken": ("gebruikt", "gebruikte",   "gebruikt"),
    "begrijpen": ("begrijpt", "begreep",     "begrepen"),
    "praten":    ("praat",    "praatte",     "gepraat"),
    "proberen":  ("probeert", "probeerde",   "geprobeerd"),
    "openen":    ("opent",    "opende",      "geopend"),
    "sluiten":   ("sluit",    "sloot",       "gesloten"),
    "bereiken":  ("bereikt",  "bereikte",    "bereikt"),
    "kunnen":    ("kan",      "kon",         "gekund"),
    "informeren":("informeert","informeerde","geïnformeerd"),
    "gaan":      ("gaat",     "ging",        "gegaan"),
    "draaien":   ("draait",   "draaide",     "gedraaid"),
    "regelen":   ("regelt",   "regelde",     "geregeld"),
    "ruilen":    ("ruilt",    "ruilde",      "geruild"),
    "schuiven":  ("schuift",  "schoof",      "geschoven"),
    "uitspreken":("spreekt uit","sprak uit", "uitgesproken"),
    "herhalen":  ("herhaalt", "herhaalde",   "herhaald"),
    "onthouden": ("onthoudt", "onthield",    "onthouden"),
    "pakken":    ("pakt",     "pakte",       "gepakt"),
    "dweilen":   ("dweilt",   "dweilde",     "gedweild"),
    "sparen":    ("spaart",   "spaarde",     "gespaard"),
    "afmaken":   ("maakt af", "maakte af",   "afgemaakt"),
    "slagen":    ("slaagt",   "slaagde",     "geslaagd"),
    "bespreken": ("bespreekt","besprak",     "besproken"),
    "houden aan":("houdt aan","hield aan",   "gehouden aan"),
    "meepraten": ("praat mee","praatte mee", "meegepraat"),
    "opgeven":   ("geeft op", "gaf op",      "opgegeven"),
    "nodigen uit":("nodigt uit","nodigde uit","uitgenodigd"),
    "planten":   ("plant",    "plantte",     "geplant"),
    "aanmelden": ("meldt aan","meldde aan",  "aangemeld"),
    "vervangen": ("vervangt", "verving",     "vervangen"),
    "schoonhouden":("houdt schoon","hield schoon","schoongehouden"),
    "durven":    ("durft",    "durfde",      "gedurfd"),
    "weten":     ("weet",     "wist",        "geweten"),
}

FORM_TO_INF = {}
for inf, (hij, past, perf) in VERBS.items():
    for form in [inf, hij, past, perf]:
        head = form.split(" ", 1)[0]
        if head and head != "—":
            FORM_TO_INF.setdefault(head, inf)
    # heuristic ik form (no -t)
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
    "praatte": "praten",
    "houd": "houden",
    "houdt": "houden",
    "denkt": "denken",
    "schrijft": "schrijven",
    "leest": "lezen",
    "neemt": "nemen",
    "kijkt": "kijken",
    "luistert": "luisteren",
    "krijgt": "krijgen",
    "stuurt": "sturen",
    "geleerd": "leren",
    "geweest": "zijn",
    "gehad": "hebben",
    "geweten": "weten",
    "gepraat": "praten",
    "geweest": "zijn",
    "afgemaakt": "afmaken",
    "geslaagd": "slagen",
    "gemaakt": "maken",
    "geholpen": "helpen",
    "gehaald": "halen",
    "gedaan": "doen",
    "gepland": "plannen",
    "geplant": "planten",
    "gebracht": "brengen",
    "gehouden": "houden",
    "gesloten": "sluiten",
    "geopend": "openen",
    "geschreven": "schrijven",
    "gevraagd": "vragen",
    "gepraat": "praten",
    "gegeten": "eten",
    "geweest": "zijn",
    "verteld": "vertellen",
    "vervangt": "vervangen",
    "begrepen": "begrijpen",
    "bereikt": "bereiken",
    "bedankt": "bedanken",
    "leert": "leren",
    "praat": "praten",
    "voert": "voeren",
    "vindt": "vinden",
    "vraag": "vragen",
}
FORM_TO_INF.update(EXTRAS)

# Parse md
md = MD.read_text()
table_blocks = re.findall(
    r"### Word dictionary\s*\n\s*\|[^\n]+\|[^\n]+\|\s*\n\s*\|[\s\-:|]+\|\s*\n((?:\s*\|[^\n]+\|[^\n]+\|\s*\n?)+)",
    md,
)

SKIP_EN = {"name", "number", "option A / article a", "option B", "option C", "option D"}
SKIP_NL = {"a", "b", "c", "d"}

def is_verb_form(token: str) -> bool:
    return token in FORM_TO_INF

entries: dict[str, dict] = {}
for block in table_blocks:
    for line in block.strip().splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Dutch"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) != 2:
            continue
        nl, en = parts
        if not nl or en in SKIP_EN:
            continue
        # md sometimes lists alternate forms with /  e.g. "ben / bent / is / zijn"
        # add an entry per form
        for n in re.split(r"\s*/\s*", nl):
            key = n.lower().strip().strip('’\'')
            if not key or key in SKIP_NL:
                continue
            if key in entries:
                continue
            entry = {"nl": key, "en": en}
            if is_verb_form(key):
                inf = FORM_TO_INF[key]
                if inf in VERBS:
                    hij, past, perf = VERBS[inf]
                    entry["pos"] = "verb"
                    entry["verb"] = {
                        "inf": inf,
                        "hij": hij,
                        "past": past,
                        "perfect": perf,
                    }
            entries[key] = entry

result = sorted(entries.values(), key=lambda e: e["nl"])
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
verb_count = sum(1 for e in result if e.get("pos") == "verb")
print(f"Wrote {len(result)} entries to {OUT.name} ({verb_count} verbs)")
