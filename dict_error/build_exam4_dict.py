#!/usr/bin/env python3
"""Build exam4-dict.json from md vocab tables, with verb conjugations and
sensible English meanings for every conjugated form."""
import json
import re
from pathlib import Path

PROJECT = Path("/Users/liceline/Documents/荷兰语融入考试阅读")
MD = PROJECT / "Lezen_A2_oefenexamen_4_sentence_translation_vocabulary.md"
OUT = PROJECT / "exam4-dict.json"

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
    "schilderen":("schildert","schilderde",  "geschilderd"),
    "vieren":    ("viert",    "vierde",      "gevierd"),
    "uitnodigen":("nodigt uit","nodigde uit","uitgenodigd"),
    "verkopen":  ("verkoopt", "verkocht",    "verkocht"),
    "starten":   ("start",    "startte",     "gestart"),
    "aanmelden": ("meldt aan","meldde aan",  "aangemeld"),
    "inschrijven":("schrijft in","schreef in","ingeschreven"),
    "repareren": ("repareert","repareerde",  "gerepareerd"),
    "bestellen": ("bestelt",  "bestelde",    "besteld"),
    "veranderen":("verandert","veranderde",  "veranderd"),
    "reserveren":("reserveert","reserveerde","gereserveerd"),
    "ophalen":   ("haalt op", "haalde op",   "opgehaald"),
    "doorlezen": ("leest door","las door",   "doorgelezen"),
    "controleren":("controleert","controleerde","gecontroleerd"),
    "bespreken": ("bespreekt","besprak",     "besproken"),
    "meenemen":  ("neemt mee","nam mee",     "meegenomen"),
    "lopen":     ("loopt",    "liep",        "gelopen"),
    "klaarzetten":("zet klaar","zette klaar","klaargezet"),
    "winnen":    ("wint",     "won",         "gewonnen"),
    "eindigen":  ("eindigt",  "eindigde",    "geëindigd"),
    "knippen":   ("knipt",    "knipte",      "geknipt"),
    "wassen":    ("wast",     "waste",       "gewassen"),
    "zingen":    ("zingt",    "zong",        "gezongen"),
    "merken":    ("merkt",    "merkte",      "gemerkt"),
    "bepalen":   ("bepaalt",  "bepaalde",    "bepaald"),
    "schoonmaken":("maakt schoon","maakte schoon","schoongemaakt"),
    "stofzuigen":("stofzuigt","stofzuigde",  "gestofzuigd"),
    "downloaden":("downloadt","downloadde",  "gedownload"),
    "studeren":  ("studeert", "studeerde",   "gestudeerd"),
    "overslaan": ("slaat over","sloeg over", "overgeslagen"),
    "doorgaan":  ("gaat door","ging door",   "doorgegaan"),
    "verzamelen":("verzamelt","verzamelde",  "verzameld"),
    "inhalen":   ("haalt in", "haalde in",   "ingehaald"),
    "uitzoeken": ("zoekt uit","zocht uit",   "uitgezocht"),
    "trouwen":   ("trouwt",   "trouwde",     "getrouwd"),
    "missen":    ("mist",     "miste",       "gemist"),
    "haalt":     ("haalt",    "haalde",      "gehaald"),  # alias
}

VERB_EN = {
    "zijn": "to be", "hebben": "to have", "worden": "to become / be (passive)",
    "kunnen": "can / be able to", "moeten": "must / have to", "willen": "to want",
    "mogen": "may / be allowed to", "hoeven": "need to / have to",
    "zullen": "shall / will", "laten": "to let / to have done",
    "gaan": "to go", "doen": "to do", "komen": "to come", "zien": "to see",
    "weten": "to know", "geven": "to give", "nemen": "to take",
    "blijven": "to stay / remain", "vinden": "to find / think",
    "kopen": "to buy", "kiezen": "to choose", "lezen": "to read",
    "eten": "to eat", "schrijven": "to write", "spreken": "to speak",
    "krijgen": "to get / receive", "brengen": "to bring", "denken": "to think",
    "houden": "to hold / love", "rijden": "to drive / ride",
    "vergeten": "to forget", "leggen": "to lay / put",
    "bellen": "to call (phone)", "zitten": "to sit",
    "afspreken": "to agree / make an appointment",
    "volgen": "to follow / take (a course)", "werken": "to work",
    "wonen": "to live (somewhere)", "stoppen": "to stop", "betalen": "to pay",
    "maken": "to make", "zoeken": "to search / look for", "helpen": "to help",
    "zorgen": "to take care of / ensure", "passen": "to fit / suit",
    "vragen": "to ask", "mailen": "to email", "vertellen": "to tell",
    "oefenen": "to practise", "hopen": "to hope", "kosten": "to cost",
    "duren": "to last / take (time)", "sturen": "to send",
    "kennen": "to know (be familiar with)", "halen": "to fetch / pass (exam)",
    "leren": "to learn / teach", "horen": "to hear", "wachten": "to wait",
    "kijken": "to look / watch", "luisteren": "to listen", "melden": "to report",
    "bedanken": "to thank", "gebruiken": "to use", "praten": "to talk",
    "openen": "to open", "sluiten": "to close", "bereiken": "to reach",
    "schilderen": "to paint", "vieren": "to celebrate", "uitnodigen": "to invite",
    "verkopen": "to sell", "starten": "to start", "aanmelden": "to sign up",
    "inschrijven": "to register / enrol", "repareren": "to repair",
    "bestellen": "to order", "veranderen": "to change",
    "reserveren": "to reserve / book", "ophalen": "to pick up",
    "doorlezen": "to read through", "controleren": "to check",
    "bespreken": "to discuss", "meenemen": "to bring along",
    "lopen": "to walk", "klaarzetten": "to set up / prepare",
    "winnen": "to win", "eindigen": "to end",
    "knippen": "to cut (hair)", "wassen": "to wash", "zingen": "to sing",
    "merken": "to notice", "bepalen": "to decide / determine",
    "schoonmaken": "to clean", "stofzuigen": "to vacuum",
    "downloaden": "to download", "studeren": "to study",
    "overslaan": "to skip", "doorgaan": "to go on / take place",
    "verzamelen": "to gather / collect", "inhalen": "to make up / catch up",
    "uitzoeken": "to choose / pick out", "trouwen": "to marry",
    "missen": "to miss",
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
    "gaf": "geven", "ging": "gaan", "deed": "doen",
    "las": "lezen", "vroeg": "vragen", "vonden": "vinden",
    "kostte": "kosten", "belde": "bellen", "kreeg": "krijgen",
    "geef": "geven", "lees": "lezen", "schrijf": "schrijven",
    "neem": "nemen", "stuur": "sturen", "zoek": "zoeken",
    "doe": "doen", "kom": "komen", "zei": "zeggen",
    "praatte": "praten", "haalt": "halen",
    "getrouwd": "trouwen", "gepland": "plannen",
    "ziet": "zien",
}
FORM_TO_INF.update(EXTRAS)

md = MD.read_text()
table_re = re.compile(r"## Vocabulary dictionary\s*\n.*?\n\|[\s\-:|]+\|\s*\n((?:\s*\|[^\n]+\|[^\n]+\|\s*\n?)+)", re.DOTALL)
table_blocks = table_re.findall(md)

entries: dict[str, dict] = {}
for block in table_blocks:
    for line in block.strip().splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Dutch"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 2:
            continue
        nl, en = cells
        if not nl or nl == "Dutch":
            continue
        key = nl.lower().strip()
        if key in entries:
            continue
        entry = {"nl": key, "en": en}
        single = key.split()
        if len(single) == 1 and single[0] in FORM_TO_INF:
            inf = FORM_TO_INF[single[0]]
            if inf in VERBS:
                hij, past, perf = VERBS[inf]
                entry["pos"] = "verb"
                entry["verb"] = {"inf": inf, "hij": hij, "past": past, "perfect": perf}
        entries[key] = entry

# Add every known conjugated form with a sensible English so popovers show the grid.
for form, inf in list(FORM_TO_INF.items()):
    if form in entries:
        if inf in VERBS and not entries[form].get("verb"):
            hij, past, perf = VERBS[inf]
            entries[form]["pos"] = "verb"
            entries[form]["verb"] = {"inf": inf, "hij": hij, "past": past, "perfect": perf}
        continue
    if inf in VERBS:
        hij, past, perf = VERBS[inf]
        entries[form] = {
            "nl": form,
            "en": VERB_EN.get(inf, f"to {inf}"),
            "pos": "verb",
            "verb": {"inf": inf, "hij": hij, "past": past, "perfect": perf},
        }

MANUAL = {
    "komende": ("coming, upcoming", "adjective"),
    "aankomende": ("upcoming, coming", "adjective"),
    "afgesloten": ("closed off", "adjective"),
    "afgesproken": ("agreed, arranged", "adjective"),
    "gesloten": ("closed", "adjective"),
    "geopend": ("open, opened", "adjective"),
    "vriendelijke": ("kind, friendly", "adjective"),
    "geweldige": ("wonderful, great", "adjective"),
    "fantastische": ("fantastic", "adjective"),
    "verdieping": ("floor, storey", "noun"),
}
for nl, (en, pos) in MANUAL.items():
    entries[nl] = {"nl": nl, "en": en, "pos": pos}

result = sorted(entries.values(), key=lambda e: e["nl"])
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
verb_count = sum(1 for e in result if e.get("pos") == "verb")
print(f"Wrote {len(result)} entries to {OUT.name} ({verb_count} verbs)")
