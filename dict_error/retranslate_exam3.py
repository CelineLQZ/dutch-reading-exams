#!/usr/bin/env python3
"""Replace the literal English translations of every exam 3 sentence
with natural English, keyed by the Dutch source text."""

import json
from pathlib import Path

READINGS = Path("/Users/liceline/Documents/荷兰语融入考试阅读/readings.json")

TRANSLATIONS = {
    # ─── 3.1 Beste cursist ──────────────────────────────────────────────
    "Irena volgt een cursus Nederlands.": "Irena is taking a Dutch course.",
    "Ze krijgt een e-mail van een docent.": "She receives an email from a teacher.",
    "Lees eerst de vraag.": "Read the question first.",
    "Lees daarna de tekst.": "Then read the text.",
    "Beste cursist,": "Dear course participant,",
    "Harry de Bont gaat weg.": "Harry de Bont is leaving.",
    "Op 1 mei wordt hij namelijk 67 jaar.": "He will turn 67 on 1 May.",
    "Hij stopt dan met werken.": "He will stop working then.",
    "Op woensdag 18 april geeft hij zijn laatste les Nederlands en op donderdag 19 april zijn laatste les Engels.":
        "On Wednesday 18 April he will give his last Dutch lesson, and on Thursday 19 April his last English lesson.",
    "Daarna geeft Nadia Luiten de lessen Nederlands.": "After that, Nadia Luiten will teach the Dutch lessons.",
    "Nirosha Brouwer neemt de lessen Engels over.": "Nirosha Brouwer will take over the English lessons.",
    "Harry heeft bijna dertig jaar gewerkt bij ons cursuscentrum.":
        "Harry has worked at our course centre for almost thirty years.",
    "Dat is heel bijzonder.": "That is very special.",
    "Daarom geven we een groot feest voor hem.": "That's why we are throwing a big party for him.",
    "Het feest is op vrijdag 20 april in de kantine.":
        "The party is on Friday 20 April in the canteen.",
    "Het begint om 20.00 uur.": "It starts at 20:00.",
    "Harry krijgt een mooi cadeau van ons allemaal.":
        "Harry will get a beautiful gift from all of us.",
    "We hebben met de docenten een mooi geldbedrag bij elkaar gelegd.":
        "Together with the teachers we have put together a nice sum of money.",
    "Daarvan hebben we een bijzonder boek voor Harry gekocht.":
        "With that we bought a special book for Harry.",
    "Willen jullie ook iets doen?": "Would you like to do something too?",
    "Schrijf dan iets voor Harry.": "Then write something for Harry.",
    "Geef je tekst aan Leo Coppens.": "Give your text to Leo Coppens.",
    "Hij maakt er een boek van.": "He will turn it into a book.",
    "Kom je ook afscheid nemen van Harry?": "Will you also come to say goodbye to Harry?",
    "We hopen dat het een gezellig feest wordt!":
        "We hope it will be a fun party!",
    "Groet, Pascal van Dijk": "Regards, Pascal van Dijk",
    "Wanneer is de laatste les Nederlands van Harry de Bont?":
        "When is Harry de Bont's last Dutch lesson?",
    "Van wie krijgt Irena straks Nederlandse les?":
        "Who will be giving Irena her Dutch lessons from now on?",

    # ─── 3.2 Gratis stadsbus ────────────────────────────────────────────
    "Carmen woont in Maastricht.": "Carmen lives in Maastricht.",
    "Ze leest een artikel op de website van de gemeente.":
        "She reads an article on the municipality's website.",
    "Gratis stadsbus": "Free city bus",
    "Waarom wordt de stadsbus gratis?":
        "Why is the city bus becoming free?",
    "Het centrum van Maastricht wordt drukker en drukker.":
        "The centre of Maastricht is getting busier and busier.",
    "Er rijden steeds meer auto’s en er is vaak niet genoeg plek om te parkeren.":
        "More and more cars are on the road and there is often not enough space to park.",
    "Daarom wordt de stadsbus gratis tijdens drukke winkeltijden.":
        "That's why the city bus will be free during busy shopping hours.",
    "We hopen dat het dan minder druk wordt in de stad.":
        "We hope this will make the city less crowded.",
    "En we willen natuurlijk de schoonste gemeente van Limburg blijven!":
        "And of course we want to remain the cleanest municipality in Limburg!",
    "Wanneer is de stadsbus gratis?": "When is the city bus free?",
    "De stadsbus gaat gratis rijden vanaf 1 september.":
        "The city bus will run for free from 1 September.",
    "Het gaat om deze dagen en tijden:":
        "These are the days and times it applies to:",
    "Dag: gratis busdienst.": "Day: free bus service.",
    "Vrijday: van 18.00 tot 22.00 uur (koopavond).":
        "Friday: from 18:00 to 22:00 (late-night shopping).",
    "Zaterdag: van 09.00 tot 17.00 uur.": "Saturday: from 09:00 to 17:00.",
    "Zondag: van 12.00 tot 17.30 uur.": "Sunday: from 12:00 to 17:30.",
    "Maandag tot en met donderdag betaalt u de hele dag voor de stadsbus.":
        "From Monday through Thursday you pay for the city bus all day.",
    "Wanneer rijdt de stadsbus?": "When does the city bus run?",
    "De stadsbus rijdt van 08.00 tot 22.00 uur.":
        "The city bus runs from 08:00 to 22:00.",
    "Op werkdagen vertrekt de bus elke twintig minuten vanaf het station.":
        "On weekdays, the bus departs from the station every twenty minutes.",
    "Op zaterdag rijdt de bus elke tien minuten.":
        "On Saturdays the bus runs every ten minutes.",
    "Na 18.00 uur rijdt de bus nog elk kwartier.":
        "After 18:00 the bus still runs every fifteen minutes.",
    "Op zondag rijdt de bus elke dertig minuten.":
        "On Sundays the bus runs every thirty minutes.",
    "Waarom maakt de gemeente de stadsbus gratis?":
        "Why is the municipality making the city bus free?",
    "Carmen wil op maandag de stadsbus nemen.":
        "Carmen wants to take the city bus on Monday.",
    "Hoe vaak gaat de bus die dag?":
        "How often does the bus run that day?",
    "Carmen wil op vrijdag gratis met de stadsbus.":
        "Carmen wants to take the city bus for free on Friday.",
    "Wanneer kan dat?": "When is that possible?",

    # ─── 3.3 Beste buurtbewoner ────────────────────────────────────────
    "Lisa krijgt een brief van een buurman.":
        "Lisa receives a letter from a neighbour.",
    "Beste buurtbewoner,": "Dear neighbour,",
    "Op 3 juli was er een buurtvergadering.":
        "On 3 July there was a neighbourhood meeting.",
    "We hebben toen een datum afgesproken voor een activiteit voor de hele buurt.":
        "At that meeting we agreed on a date for an activity for the whole neighbourhood.",
    "De activiteit is op zaterdag 16 september.":
        "The activity is on Saturday 16 September.",
    "Heb jij een goed idee voor een activiteit?":
        "Do you have a good idea for an activity?",
    "Stuur het dan op!": "Then send it in!",
    "Wat moet je doen?": "What do you need to do?",
    "Beschrijf jouw idee voor een activiteit.":
        "Describe your idea for an activity.",
    "De activiteit moet leuk zijn voor buurtbewoners van alle leeftijden.":
        "The activity has to be fun for neighbours of all ages.",
    "Schrijf op wanneer jouw activiteit is: is het overdag, ’s avonds of de hele dag?":
        "Write down when your activity is — during the day, in the evening, or all day?",
    "Reken uit hoeveel de activiteit kost.":
        "Calculate how much the activity will cost.",
    "Vorig jaar kostte de activiteit € 25,- per persoon.":
        "Last year the activity cost €25 per person.",
    "Veel mensen vonden dat te duur.": "Many people thought that was too expensive.",
    "Daarom mag de activiteit dit jaar maximaal € 15,- per persoon kosten.":
        "That's why this year the activity may cost a maximum of €15 per person.",
    "Als je ook wilt eten met zijn allen mag het iets duurder zijn.":
        "If you want everyone to eat together as well, it may be a bit more expensive.",
    "Dan is het maximaal € 20,- per persoon.":
        "In that case the maximum is €20 per person.",
    "Stuur jouw idee op naar boris.de.vries@mail.nl.":
        "Send your idea to boris.de.vries@mail.nl.",
    "Doe dat voor 1 augustus.": "Do that before 1 August.",
    "We bespreken alle ideeën in de buurtvergadering van 5 augustus.":
        "We will discuss all the ideas at the neighbourhood meeting on 5 August.",
    "We hopen dat we uit veel ideeën kunnen kiezen!":
        "We hope we'll have many ideas to choose from!",
    "Wat is het belangrijkst aan de activiteit?":
        "What is the most important thing about the activity?",
    "Lisa weet een leuke activiteit.": "Lisa has a fun activity in mind.",
    "Voor wanneer moet ze haar idee opsturen?":
        "By when does she need to send in her idea?",
    "Lisa heeft een idee voor een activiteit: spelletjes doen en pannenkoeken eten in het buurthuis.":
        "Lisa has an idea for an activity: playing games and eating pancakes at the community centre.",
    "Hoe duur mag die activiteit maximaal zijn?":
        "What is the maximum that activity may cost?",

    # ─── 3.4 Verkopers Gezocht ─────────────────────────────────────────
    "Aziza wil graag in een winkel werken.": "Aziza would like to work in a shop.",
    "Ze bekijkt een vacature op internet.":
        "She looks at a job listing on the internet.",
    "Verkopers gezocht.": "Salespeople wanted.",
    "Nino’s is een van de bekendste winkels voor kinderkleding in Amsterdam.":
        "Nino's is one of the best-known children's clothing shops in Amsterdam.",
    "Onze eerste winkel in het centrum was al snel een succes.":
        "Our first shop in the city centre was quickly a success.",
    "Ook onze tweede winkel in Amsterdam-Oost groeit hard.":
        "Our second shop in Amsterdam-East is also growing fast.",
    "We zoeken daarom nog goede verkopers voor deze winkel.":
        "That's why we are still looking for good salespeople for this shop.",
    "Er zijn zelfs plannen voor een nieuwe winkel, in Amsterdam-Zuid!":
        "There are even plans for a new shop in Amsterdam-South!",
    "Je helpt alle klanten vriendelijk en je zorgt dat iedereen tevreden naar huis gaat.":
        "You help every customer in a friendly way and make sure that everyone leaves satisfied.",
    "We zoeken verkopers die 16 tot 24 uur kunnen werken.":
        "We are looking for salespeople who can work 16 to 24 hours.",
    "Je werkt minimaal op twee doordeweekse dagen (maandag - vrijdag).":
        "You work at least two weekdays (Monday–Friday).",
    "Je bent ook op zaterdag beschikbaar.": "You are also available on Saturdays.",
    "Wie zoeken wij?": "Who are we looking for?",
    "Wij zoeken iemand die flexibel is en hard wil werken.":
        "We are looking for someone who is flexible and willing to work hard.",
    "Je hoeft niet veel van mode te weten, maar je moet wel van kleding houden.":
        "You don't need to know a lot about fashion, but you do have to love clothes.",
    "Ervaring met werken in een kledingwinkel is een voordeel, maar is niet verplicht.":
        "Experience working in a clothing shop is a plus, but it isn't required.",
    "Het belangrijkste is dat je goed met kinderen kunt omgaan.":
        "The most important thing is that you're good with children.",
    "Past dit bij jou?": "Does this sound like you?",
    "Dan ben jij de verkoper die we zoeken!":
        "Then you are the salesperson we are looking for!",
    "Interesse?": "Interested?",
    "Solliciteer direct via het online formulier op onze website!":
        "Apply right away through the online form on our website!",
    "Voor welke winkel zoekt Nino’s nog mensen?":
        "Which shop is Nino's still hiring for?",
    "Voor wanneer zoekt Nino’s nog mensen?":
        "For when is Nino's still looking for people?",
    "Wat is het belangrijkste als Aziza bij Nino’s wil werken?":
        "What is most important if Aziza wants to work at Nino's?",

    # ─── 3.5 Hoi Chang ─────────────────────────────────────────────────
    "Chang doet een taalcursus.": "Chang is taking a language course.",
    "Hij leest een e-mail van een medecursist.":
        "He reads an email from a fellow course participant.",
    "Hoi Chang,": "Hi Chang,",
    "Ik mail je, omdat wij maandag onze presentatie over een Nederlandse stad moeten geven.":
        "I'm emailing you because we have to give our presentation about a Dutch city on Monday.",
    "Eliza en Jamil doen hun presentatie donderdag over Utrecht.":
        "Eliza and Jamil are doing their presentation on Thursday — about Utrecht.",
    "En de presentatie van gisteren ging over Haarlem.":
        "And yesterday's presentation was about Haarlem.",
    "Welke stad kiezen wij?": "Which city should we pick?",
    "Zullen wij iets over Groningen vertellen?":
        "Shall we talk about Groningen?",
    "Ik heb daar een jaar gewoond, het is echt een leuke stad.":
        "I lived there for a year — it's a really nice city.",
    "Ik heb al een paar foto’s van mooie plekken gevonden.":
        "I've already found a few photos of nice spots.",
    "Kun jij dan iets zoeken over de geschiedenis van de stad?":
        "Could you then look up something about the city's history?",
    "Dat vind jij niet erg, toch?": "You don't mind, do you?",
    "We moeten ook iets vertellen over de winkels en restaurants.":
        "We also need to say something about the shops and restaurants.",
    "Daarover zoeken we dan wel samen informatie.":
        "We can look that up together.",
    "Zullen we nog een keer afspreken?": "Shall we meet up one more time?",
    "Dan kunnen we de presentatie oefenen.":
        "Then we can practise the presentation.",
    "Ik kan woensdag wel, bij mij thuis.":
        "I'm free on Wednesday, at my place.",
    "Donderdag kan het niet bij mij.":
        "Thursday doesn't work at my place.",
    "Mijn man heeft dan bezoek.":
        "My husband will have visitors then.",
    "We kunnen wel na de les in de mediatheek zitten.":
        "We could sit in the media library after class.",
    "Vrijdag moet ik werken, dus dan kan ik helemaal niet.":
        "I have to work on Friday, so I can't make it at all then.",
    "Laat je me weten wanneer jij kunt?":
        "Let me know when you're free?",
    "Bedankt!": "Thanks!",
    "Groetjes, Sasha": "Cheers, Sasha",
    "Over welke stad wil Sasha de presentatie geven?":
        "Which city does Sasha want to give the presentation about?",
    "Waarover wil Sasha samen met Chang informatie zoeken?":
        "What does Sasha want to research together with Chang?",
    "Wanneer kan Chang bij Sasha thuis oefenen voor de presentatie?":
        "When can Chang practise for the presentation at Sasha's home?",

    # ─── 3.6 Beste Selina ──────────────────────────────────────────────
    "Selina werkt bij een schoonmaakbedrijf.":
        "Selina works at a cleaning company.",
    "Ze krijgt een e-mail van haar manager, Coen.":
        "She receives an email from her manager, Coen.",
    "Beste Selina,": "Dear Selina,",
    "Ik wil je graag iets vragen.": "I'd like to ask you something.",
    "Ik heb een probleem met het werkrooster.":
        "I have a problem with the work schedule.",
    "Farouk belde net: hij heeft zijn arm gebroken.":
        "Farouk just called: he has broken his arm.",
    "Hij moet volgende week twee dagen werken, maar dat gaat nu niet.":
        "He's supposed to work two days next week, but that's not possible now.",
    "Dus ik zoek mensen die extra dagen kunnen werken.":
        "So I'm looking for people who can work extra days.",
    "Ik heb Rachel al gevraagd, maar zij moet drie dagen naar school.":
        "I've already asked Rachel, but she has school three days.",
    "Zij kan daarom maar één dag extra werken: op woensdag.":
        "So she can only work one extra day — on Wednesday.",
    "En Kiki werkt volgende week al vijf dagen.":
        "And Kiki is already working five days next week.",
    "Dus wil jij volgende week misschien een extra dag werken, op dinsdag?":
        "So could you maybe work an extra day next week, on Tuesday?",
    "Het zou fijn zijn als je kunt.":
        "It would be great if you can.",
    "Laat je me dat vóór vrijdag even weten?":
        "Could you let me know before Friday?",
    "Hartelijke groet, Coen de Weerdt":
        "Kind regards, Coen de Weerdt",
    "Coen vraagt of Selina extra kan werken.":
        "Coen is asking whether Selina can work extra.",
    "Voor wie moet Selina werken?": "Who does Selina need to cover for?",
    "Selina kan volgende week extra werken.":
        "Selina can work extra next week.",
    "Hoeveel dagen moet ze dan extra werken?":
        "How many extra days does she have to work then?",
    "Wanneer moet Selina iets laten weten aan Coen?":
        "By when does Selina have to let Coen know?",

    # ─── 3.7 Cursus Houten Meubels Maken ───────────────────────────────
    "Abid gaat de cursus Houten Meubels Maken volgen.":
        "Abid is going to take the course \"Making Wooden Furniture\".",
    "Hij leest informatie over de cursus.":
        "He reads information about the course.",
    "Cursus Houten Meubels Maken.": "Course: Making Wooden Furniture.",
    "De lessen.": "The lessons.",
    "De cursus Houten Meubels Maken bestaat uit zes lessen.":
        "The course \"Making Wooden Furniture\" consists of six lessons.",
    "De eerste les is op 18 juni van 10.00 uur tot 15.00 uur.":
        "The first lesson is on 18 June from 10:00 to 15:00.",
    "Wij zorgen voor de lunch en koffie of thee.":
        "We provide lunch and coffee or tea.",
    "Het enige wat u moet meenemen, is het theorieboek van de cursus.":
        "The only thing you need to bring is the course theory book.",
    "Dat kunt u online bestellen.": "You can order it online.",
    "Verder hebben wij alles wat u nodig hebt voor de cursus.":
        "We have everything else you need for the course.",
    "U kunt uw eigen gereedschap dus thuis laten!":
        "So you can leave your own tools at home!",
    "In de eerste les leert u welke soorten hout er zijn en wat u daarmee kunt maken.":
        "In the first lesson you learn what kinds of wood exist and what you can make with them.",
    "In de lessen daarna gaat u zelf werken met verschillende gereedschappen.":
        "In the lessons after that you will work with various tools yourself.",
    "In de tweede les begint u met het maken van een klein kistje.":
        "In the second lesson you start by making a small box.",
    "En in de lessen erna gaat u uw eigen meubelstuk ontwerpen en maken, bijvoorbeeld een stoel of tafeltje!":
        "And in the lessons after that you will design and build your own piece of furniture — for example a chair or a small table!",
    "Inschrijven.": "Registration.",
    "Inschrijven voor de cursus kan via deze website.":
        "You can register for the course on this website.",
    "U kunt ook mailen naar meubelmakers@home.nl.":
        "You can also email meubelmakers@home.nl.",
    "Afmelden.": "Cancelling.",
    "Hebt u zich ingeschreven, maar kunt u niet naar de les komen of bent u later?":
        "Have you registered but can't make it to class, or will you be late?",
    "Bel dan onze receptie: 023-3691117.":
        "Then call our reception: 023-3691117.",
    "Zij melden u dan af bij de docent.":
        "They will report your absence to the teacher.",
    "Wat moet Abid meenemen naar de cursus?":
        "What does Abid have to bring to the course?",
    "Wat gaan de cursisten in de eerste les doen?":
        "What will the participants do in the first lesson?",
    "Abid kan niet op tijd in de les zijn.":
        "Abid can't be at the lesson on time.",
    "Wat moet hij doen?": "What should he do?",

    # ─── 3.8 Geachte mevrouw Krüger ────────────────────────────────────
    "Mia krijgt een brief van de tandarts.":
        "Mia receives a letter from the dentist.",
    "Geachte mevrouw Krüger,": "Dear Mrs. Krüger,",
    "U hebt op dinsdag 4 oktober om 14.00 uur een afspraak bij tandarts Altman.":
        "You have an appointment with dentist Altman on Tuesday 4 October at 14:00.",
    "Tandarts Altman stopt helaas per 1 oktober met werken bij onze praktijk.":
        "Unfortunately, dentist Altman is leaving our practice as of 1 October.",
    "Hij gaat namelijk verhuizen.": "He is moving house.",
    "Wij hebben nu een afspraak voor u gemaakt bij tandarts Jensma.":
        "We have now made an appointment for you with dentist Jensma.",
    "Wilt u liever naar een andere tandarts?":
        "Would you prefer a different dentist?",
    "Dat kan.": "That's possible.",
    "Meld dit dan bij ons.": "Just let us know.",
    "Tandarts Diepenveen werkt nu ook bij onze praktijk.":
        "Dentist Diepenveen is now also working at our practice.",
    "Hij is net klaar met studeren.":
        "He has just finished his studies.",
    "Tandarts De Groot kent u misschien al, maar hij zit op dit moment vol.":
        "You may already know dentist De Groot, but he is fully booked at the moment.",
    "Uw afspraak van 4 oktober is verplaatst naar een andere datum: 16 oktober.":
        "Your appointment of 4 October has been moved to a new date: 16 October.",
    "Het tijdstip van de afspraak (14.00 uur) blijft hetzelfde.":
        "The time of the appointment (14:00) stays the same.",
    "Kunt u dan niet?": "Are you not available then?",
    "Neem even contact met ons op.": "Please get in touch with us.",
    "Wij hopen dat we u voldoende hebben geïnformeerd.":
        "We hope we have informed you sufficiently.",
    "Met vriendelijke groet, Jenny Koolstra, Secretaresse":
        "Kind regards, Jenny Koolstra, Secretary",
    "Waarom is de afspraak van Mia verplaatst?":
        "Why has Mia's appointment been moved?",
    "Wanneer heeft Mia een nieuwe afspraak?":
        "When is Mia's new appointment?",

    # ─── 3.9 Dag Lito ──────────────────────────────────────────────────
    "Lito werkt bij de gemeente.": "Lito works at the municipality.",
    "Hij krijgt een e-mail van zijn baas, Pascal.":
        "He receives an email from his boss, Pascal.",
    "Dag Lito,": "Hello Lito,",
    "Je hebt je zomervakantie nog niet aangevraagd.":
        "You haven't requested your summer holiday yet.",
    "Wil je dat deze week doen?":
        "Could you do that this week?",
    "Dan kan ik een nieuwe planning voor de vakantieperiode maken.":
        "Then I can make a new schedule for the holiday period.",
    "In het rooster kun je zien wie wanneer al vakantie heeft.":
        "In the schedule you can see who already has holiday and when.",
    "Vergeet ook de vakantieregels niet:":
        "And don't forget the holiday rules:",
    "Je mag maximaal twee weken vakantie opnemen.":
        "You may take a maximum of two weeks of holiday.",
    "Je mag twee weken achter elkaar vrij nemen, maar het mogen ook twee losse weken zijn.":
        "You may take two consecutive weeks off, but they may also be two separate weeks.",
    "Er is altijd iemand nodig aan de balie én iemand om de telefoon op te nemen.":
        "Someone always needs to be at the front desk and someone needs to answer the phone.",
    "Er moeten dus altijd twee collega’s aan het werk zijn.":
        "So there always have to be two colleagues on duty.",
    "Zorg ervoor dat je geen belangrijk werk hebt in de weken waarin je vakantie wilt.":
        "Make sure you don't have any important work in the weeks when you want to be on holiday.",
    "Vanaf week 35 wordt het weer druk.":
        "From week 35 it will be busy again.",
    "Dan moet iedereen weer aan het werk zijn.":
        "Then everyone has to be back at work.",
    "Vriendelijke groet, Pascal": "Kind regards, Pascal",
    "Waarom stuurt Pascal deze e-mail?":
        "Why is Pascal sending this email?",
    "Waarom moeten er altijd twee collega’s aan het werk zijn in de zomer?":
        "Why do there always have to be two colleagues on duty in the summer?",
    "Lito wil twee weken achter elkaar vrij.":
        "Lito wants two consecutive weeks off.",
    "Wanneer kan Lito het beste vakantie nemen?":
        "When is the best time for Lito to take his holiday?",

    # 3.4 shared with intro: "Wat moet je doen?"  — already covered by 3.3 version
    "Wat moet je doen?": "What do you need to do?",
}

readings = json.loads(READINGS.read_text())
updated = 0
missing = []
for article in readings:
    if not article.get("id", "").startswith("exam3-"):
        continue
    for s in article["sentences"]:
        nl = s["nl"]
        if nl in TRANSLATIONS:
            if s["en"] != TRANSLATIONS[nl]:
                s["en"] = TRANSLATIONS[nl]
                updated += 1
        else:
            missing.append(nl)

READINGS.write_text(json.dumps(readings, ensure_ascii=False, indent=2) + "\n")
print(f"Updated {updated} sentences.")
if missing:
    print(f"Missing translations for {len(missing)} sentences:")
    for m in missing[:30]:
        print(f"  - {m!r}")
