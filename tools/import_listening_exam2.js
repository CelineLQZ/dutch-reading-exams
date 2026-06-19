const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const MD_PATH = path.join(ROOT, 'listening_mock_exam_2_sentence_translation_vocabulary.md');
const LISTENINGS_PATH = path.join(ROOT, 'listenings.json');
const DICT_PATH = path.join(ROOT, 'listening-dict.json');

const VERBS = {
  zijn: ['is', 'was', 'geweest'],
  hebben: ['heeft', 'had', 'gehad'],
  worden: ['wordt', 'werd', 'geworden'],
  kunnen: ['kan', 'kon', 'gekund'],
  moeten: ['moet', 'moest', 'gemoeten'],
  willen: ['wil', 'wilde', 'gewild'],
  mogen: ['mag', 'mocht', 'gemogen'],
  hoeven: ['hoeft', 'hoefde', 'gehoeven'],
  zullen: ['zal', 'zou', ''],
  gaan: ['gaat', 'ging', 'gegaan'],
  doen: ['doet', 'deed', 'gedaan'],
  komen: ['komt', 'kwam', 'gekomen'],
  krijgen: ['krijgt', 'kreeg', 'gekregen'],
  geven: ['geeft', 'gaf', 'gegeven'],
  nemen: ['neemt', 'nam', 'genomen'],
  zien: ['ziet', 'zag', 'gezien'],
  weten: ['weet', 'wist', 'geweten'],
  vinden: ['vindt', 'vond', 'gevonden'],
  lezen: ['leest', 'las', 'gelezen'],
  spreken: ['spreekt', 'sprak', 'gesproken'],
  schrijven: ['schrijft', 'schreef', 'geschreven'],
  vragen: ['vraagt', 'vroeg', 'gevraagd'],
  maken: ['maakt', 'maakte', 'gemaakt'],
  kijken: ['kijkt', 'keek', 'gekeken'],
  luisteren: ['luistert', 'luisterde', 'geluisterd'],
  vertellen: ['vertelt', 'vertelde', 'verteld'],
  helpen: ['helpt', 'hielp', 'geholpen'],
  leren: ['leert', 'leerde', 'geleerd'],
  werken: ['werkt', 'werkte', 'gewerkt'],
  volgen: ['volgt', 'volgde', 'gevolgd'],
  bestellen: ['bestelt', 'bestelde', 'besteld'],
  invullen: ['vult in', 'vulde in', 'ingevuld'],
  inleveren: ['levert in', 'leverde in', 'ingeleverd'],
  sturen: ['stuurt', 'stuurde', 'gestuurd'],
  liggen: ['ligt', 'lag', 'gelegen'],
  rijden: ['rijdt', 'reed', 'gereden'],
  reizen: ['reist', 'reisde', 'gereisd'],
  opnemen: ['neemt op', 'nam op', 'opgenomen'],
  doorverbinden: ['verbindt door', 'verbond door', 'doorverbonden'],
  terugbellen: ['belt terug', 'belde terug', 'teruggebeld'],
  afspreken: ['spreekt af', 'sprak af', 'afgesproken'],
  inzetten: ['zet in', 'zette in', 'ingezet'],
  trakteren: ['trakteert', 'trakteerde', 'getrakteerd'],
  gebeuren: ['gebeurt', 'gebeurde', 'gebeurd'],
  meenemen: ['neemt mee', 'nam mee', 'meegenomen'],
  terugkomen: ['komt terug', 'kwam terug', 'teruggekomen'],
  bijhouden: ['houdt bij', 'hield bij', 'bijgehouden'],
  oefenen: ['oefent', 'oefende', 'geoefend'],
  parkeren: ['parkeert', 'parkeerde', 'geparkeerd'],
  inrijden: ['rijdt in', 'reed in', 'ingereden'],
  schoonmaken: ['maakt schoon', 'maakte schoon', 'schoongemaakt'],
  voorgaan: ['gaat voor', 'ging voor', 'voorgegaan'],
};

const VERB_EN = {
  zijn: 'to be',
  hebben: 'to have',
  worden: 'to become / be',
  kunnen: 'can / be able to',
  moeten: 'must / have to',
  willen: 'to want',
  mogen: 'may / be allowed to',
  hoeven: 'need to / have to',
  zullen: 'will / shall',
  gaan: 'to go',
  doen: 'to do',
  komen: 'to come',
  krijgen: 'to get / receive',
  geven: 'to give',
  nemen: 'to take',
  zien: 'to see',
  weten: 'to know',
  vinden: 'to find',
  lezen: 'to read',
  spreken: 'to speak',
  schrijven: 'to write',
  vragen: 'to ask',
  maken: 'to make / do',
  kijken: 'to look / watch',
  luisteren: 'to listen',
  vertellen: 'to tell / explain',
  helpen: 'to help',
  leren: 'to learn / study',
  werken: 'to work',
  volgen: 'to follow / take',
  bestellen: 'to order',
  invullen: 'to fill in',
  inleveren: 'to hand in / submit',
  sturen: 'to send',
  liggen: 'to lie / be located',
  rijden: 'to drive / run',
  reizen: 'to travel',
  opnemen: 'to answer / record',
  doorverbinden: 'to put through / connect',
  terugbellen: 'to call back',
  afspreken: 'to arrange / meet',
  inzetten: 'to deploy / use',
  trakteren: 'to treat',
  gebeuren: 'to happen',
  meenemen: 'to bring along',
  terugkomen: 'to come back',
  bijhouden: 'to keep / maintain',
  oefenen: 'to practise',
  parkeren: 'to park',
  inrijden: 'to drive into',
  schoonmaken: 'to clean',
  voorgaan: 'to come first',
};

const FORM_TO_INF = {};
Object.entries(VERBS).forEach(([inf, forms]) => {
  FORM_TO_INF[inf] = inf;
  forms.forEach(form => {
    if (!form) return;
    FORM_TO_INF[form.split(/\s+/)[0]] ||= inf;
  });
});
Object.assign(FORM_TO_INF, {
  ben: 'zijn', bent: 'zijn', waren: 'zijn',
  heb: 'hebben', hebt: 'hebben', hadden: 'hebben',
  kan: 'kunnen', kunt: 'kunnen', kun: 'kunnen', kon: 'kunnen', konden: 'kunnen',
  wil: 'willen', wilt: 'willen', wilde: 'willen', wilden: 'willen',
  mag: 'mogen', mocht: 'mogen', mochten: 'mogen',
  zou: 'zullen', zouden: 'zullen',
  ga: 'gaan', ging: 'gaan',
  doe: 'doen', deed: 'doen',
  krijg: 'krijgen', kreeg: 'krijgen', kregen: 'krijgen',
  geef: 'geven', gaf: 'geven',
  ligt: 'liggen', lag: 'liggen',
  loopt: 'lopen', liep: 'lopen',
  vul: 'invullen', lever: 'inleveren', hoor: 'horen',
  kijkt: 'kijken', bekijkt: 'bekijken', leert: 'leren',
  luistert: 'luisteren', vertelt: 'vertellen', volgt: 'volgen',
  trakteerde: 'trakteren', ingezet: 'inzetten',
  ingeschreven: 'inschrijven', ingesproken: 'inspreken',
  omgevallen: 'omvallen', schoongemaakt: 'schoonmaken',
  terugbelt: 'terugbellen',
});

const MANUAL = {
  kan: ['can / be able to', 'verb', 'kunnen'],
  kunt: ['can / be able to', 'verb', 'kunnen'],
  kunnen: ['can / be able to', 'verb', 'kunnen'],
  komende: ['coming, upcoming', 'adjective'],
  aankomende: ['upcoming, coming', 'adjective'],
  volgende: ['next', 'adjective'],
  nieuwe: ['new', 'adjective'],
  handige: ['useful', 'adjective'],
  groene: ['green', 'adjective'],
  drukke: ['busy', 'adjective'],
  goede: ['good', 'adjective'],
  kapotte: ['broken-down', 'adjective'],
  laatste: ['last', 'adjective'],
  belangrijke: ['important', 'adjective'],
  hele: ['very / whole', 'adjective'],
  fijne: ['nice', 'adjective'],
  warme: ['warm', 'adjective'],
  gesloten: ['closed', 'adjective'],
  getrouwd: ['married', 'adjective'],
  nodig: ['needed / necessary', 'adjective'],
};

function parseMarkdown(md) {
  const articleMatches = [...md.matchAll(/^##\s+(\d+)\.\s+(.+)$/gm)];
  return articleMatches.map((match, index) => {
    const examIndex = Number(match[1]);
    const rawTitle = match[2].trim();
    const start = match.index + match[0].length;
    const end = articleMatches[index + 1]?.index ?? md.length;
    const block = md.slice(start, end);
    const sentences = parseSentenceRows(block);
    const dictEntries = parseDictRows(block);
    return { examIndex, rawTitle, sentences, dictEntries };
  });
}

function parseSentenceRows(block) {
  const section = sectionBody(block, 'Sentence-by-sentence translation');
  const rows = tableRows(section);
  return rows
    .filter(cells => cells.length >= 3 && cells[1] !== 'Dutch' && cells[1])
    .map(cells => ({ nl: cells[1], en: cells[2] }));
}

function parseDictRows(block) {
  const section = sectionBody(block, 'Contextual word list');
  return tableRows(section).flatMap(cells => {
    if (cells[0] === 'Dutch word') return [];
    const pairs = [];
    for (let i = 0; i < cells.length; i += 2) {
      const nl = cleanKey(cells[i] || '');
      const en = (cells[i + 1] || '').trim();
      if (nl && en) pairs.push([nl, en]);
    }
    return pairs;
  });
}

function sectionBody(block, title) {
  const re = new RegExp(`^###\\s+${title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*$`, 'm');
  const match = block.match(re);
  if (!match) return '';
  const start = (match.index || 0) + match[0].length;
  const rest = block.slice(start);
  const next = rest.search(/^###\s+/m);
  return next >= 0 ? rest.slice(0, next) : rest;
}

function tableRows(text) {
  return text.split(/\r?\n/)
    .map(line => line.trim())
    .filter(line => line.startsWith('|') && !/^\|\s*-+/.test(line))
    .map(line => line.replace(/^\||\|$/g, '').split('|').map(cell => cell.trim()));
}

function cleanKey(text) {
  return String(text || '').toLowerCase().replace(/[“”]/g, '').trim();
}

function verbEntry(nl, en, inf) {
  const forms = VERBS[inf];
  if (!forms) return { nl, en, pos: 'verb' };
  return {
    nl,
    en,
    pos: 'verb',
    verb: { inf, hij: forms[0], past: forms[1], perfect: forms[2] },
  };
}

const md = fs.readFileSync(MD_PATH, 'utf8');
const articles = parseMarkdown(md);
if (!articles.length) throw new Error('No listening exam 2 articles parsed.');

const existingListenings = JSON.parse(fs.readFileSync(LISTENINGS_PATH, 'utf8'));
const withoutExam2 = existingListenings.filter(article => article.exam !== 'listen2');
const exam2Listenings = articles.map(article => ({
  id: `listen2-${article.examIndex}`,
  les: 200 + article.examIndex,
  exam: 'listen2',
  examIndex: article.examIndex,
  label: `L2.${article.examIndex}`,
  title: `L2.${article.examIndex} ${article.rawTitle}`,
  rawTitle: article.rawTitle,
  sentences: article.sentences,
}));
fs.writeFileSync(LISTENINGS_PATH, JSON.stringify([...withoutExam2, ...exam2Listenings], null, 2) + '\n');

const existingDict = JSON.parse(fs.readFileSync(DICT_PATH, 'utf8'));
const dictByKey = new Map(existingDict.map(entry => [cleanKey(entry.nl), entry]));
for (const article of articles) {
  for (const [nl, en] of article.dictEntries) {
    const inf = FORM_TO_INF[nl];
    const entry = inf ? verbEntry(nl, VERB_EN[inf] || en, inf) : { nl, en };
    dictByKey.set(nl, { ...entry, source: 'listening exam 2' });
  }
}
Object.entries(MANUAL).forEach(([nl, [en, pos, inf]]) => {
  dictByKey.set(nl, inf ? verbEntry(nl, en, inf) : { nl, en, pos });
});
const mergedDict = [...dictByKey.values()].sort((a, b) => a.nl.localeCompare(b.nl, 'nl'));
fs.writeFileSync(DICT_PATH, JSON.stringify(mergedDict, null, 2) + '\n');

console.log(`Imported ${exam2Listenings.length} listening exam 2 articles.`);
exam2Listenings.forEach(article => console.log(`${article.label}: ${article.sentences.length} sentences — ${article.rawTitle}`));
console.log(`Merged listening dictionary entries: ${mergedDict.length}`);
