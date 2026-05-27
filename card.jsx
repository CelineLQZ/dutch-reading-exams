// Card components — WordCard (Learn/Review) and TestCard (Test mode)
const { useState: useStateW, useEffect: useEffectW, useRef: useRefW } = React;

function SpeakerIcon({ size = 16 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 5L6 9H3v6h3l5 4V5z"/>
      <path d="M15.5 8.5a5 5 0 010 7"/>
      <path d="M18.5 5.5a9 9 0 010 13"/>
    </svg>
  );
}

function ChevDown({ size = 12 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <path d="M6 9l6 6 6-6"/>
    </svg>
  );
}

function speak(text) { if (window.dutchTTS && text) window.dutchTTS.speak(text); }

function normalizeDictLookup(text) {
  return (text || '')
    .toLowerCase()
    .replace(/[.,!?;:"“”()]/g, '')
    .replace(/^'(.*)'$/, '$1')
    .trim();
}

function lookupDutchWord(token) {
  const dict = window.DutchDictionary || {};
  const key = normalizeDictLookup(token);
  if (!key) return null;
  return dict[key] || dict[key.replace(/'s$/, '')] || null;
}

function pickGrammarForm(forms, patterns) {
  return forms.find(f => {
    const label = String(f.label || '').toLowerCase();
    return patterns.some(pattern => pattern.test(label));
  });
}

function compactWordGrammar(word) {
  const forms = word.grammar?.forms || [];
  if (!forms.length) return [];

  const grammarKind = String(word.grammar?.kind || '').toLowerCase();
  const pos = String(word.pos || '').toLowerCase();

  if (grammarKind === 'noun' || pos.includes('noun')) {
    const plural = pickGrammarForm(forms, [/meervoud/, /plural/]);
    return plural ? [{ label: 'plural', nl: plural.nl }] : [];
  }

  if (grammarKind === 'verb' || pos.includes('verb')) {
    const ik = pickGrammarForm(forms, [/^ik$/]);
    const hij = pickGrammarForm(forms, [/^hij\b/, /hij\/zij/, /hij\/zij\/het/]);
    const past = pickGrammarForm(forms, [/^verleden$/, /^past$/]);
    const perfect = pickGrammarForm(forms, [/voltooid/, /perfect/]);

    return [
      ik && { label: 'ik', nl: ik.nl },
      hij && { label: 'hij', nl: hij.nl },
      past && { label: 'past', nl: past.nl },
      perfect && { label: 'perfect', nl: perfect.nl },
    ].filter(Boolean);
  }

  return [];
}

function ClickableDutchText({ text }) {
  const [selected, setSelected] = useStateW(null);
  const [inList, setInList] = useStateW(false);
  const parts = String(text || '').split(/([A-Za-zÀ-ÿ']+)/g);

  useEffectW(() => {
    if (!selected) return;
    const api = window.DutchStudyListAPI;
    setInList(api ? api.isInList(selected.token) : false);
  }, [selected]);

  const handleAdd = e => {
    e.stopPropagation();
    const api = window.DutchStudyListAPI;
    if (!api || !selected) return;
    const displayWord = (selected.entry.headword || selected.token).replace(/^(de|het|een)\s+/i, '');
    if (inList) { api.remove(selected.token); setInList(false); }
    else { api.add({ nl: displayWord, en: selected.entry.en, pos: selected.entry.pos, headword: selected.entry.headword }); setInList(true); }
  };

  return (
    <span className="dict-text">
      {parts.map((part, i) => {
        const entry = /^[A-Za-zÀ-ÿ']+$/.test(part) ? lookupDutchWord(part) : null;
        if (!entry) return <React.Fragment key={i}>{part}</React.Fragment>;
        return (
          <button
            key={i}
            type="button"
            className="dict-word"
            onPointerDown={e => e.stopPropagation()}
            onClick={e => { e.stopPropagation(); setSelected({ token: part, entry }); }}
          >
            {part}
          </button>
        );
      })}
      {selected && (
        <span className="dict-popover" onPointerDown={e => e.stopPropagation()}>
          <span className="dict-meaning">{selected.entry.en}</span>
          <span className="dict-popover-actions">
            <button type="button" className={'dict-add-btn' + (inList ? ' in-list' : '')} onClick={handleAdd}>
              {inList ? '✓ in deck' : '+ to deck'}
            </button>
            <button type="button" className="dict-close-btn" onClick={e => { e.stopPropagation(); setSelected(null); }} aria-label="Close">×</button>
          </span>
        </span>
      )}
    </span>
  );
}

// ── Sentence card (Reading learn / review) ───────────────────────
function SentenceCard({ word, mode, autoplay, isTop, dragState }) {
  const playedRef = useRefW(null);

  useEffectW(() => {
    if (!isTop || !autoplay) return;
    if (playedRef.current === word.nl) return;
    playedRef.current = word.nl;
    const t = setTimeout(() => speak(word.nl), 180);
    return () => clearTimeout(t);
  }, [isTop, word.nl, autoplay]);

  const grammarForms = word.grammar?.forms || [];

  return (
    <React.Fragment>
      {isTop && (
        <React.Fragment>
          <div className="stamp keep" style={{ opacity: dragState.keepOpacity }}>GOT IT</div>
          <div className="stamp forgot" style={{ opacity: dragState.forgotOpacity }}>AGAIN</div>
        </React.Fragment>
      )}

      <div className="card-top-row">
        <span className="les-tag">Article {word.les}</span>
        <span className="pos-tag">sentence</span>
      </div>

      <div className="sentence-study-card">
        <div className="sentence-number">{word.articleTitle || 'Reading'}</div>
        <div className="sentence-nl large"><ClickableDutchText text={word.nl} /></div>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <button
            className="speaker-btn"
            onPointerDown={e => e.stopPropagation()}
            onClick={e => { e.stopPropagation(); speak(word.nl); }}
            aria-label="Sentence pronunciation"
          ><SpeakerIcon size={16} /></button>
        </div>
        <div className="divider"></div>
        {mode !== 'test' && <div className="sentence-en large">{word.en}</div>}
      </div>

      {mode !== 'test' && grammarForms.length > 0 && (
        <div className="grammar-panel sentence-grammar-panel" onPointerDown={e => e.stopPropagation()}>
          <div className="sentence-grammar-title">Grammar</div>
          {grammarForms.map((f, i) => (
            <div className="sentence-grammar-row" key={i}>
              <span className="lab">{f.label}</span>
              <span className="form">{f.nl}</span>
            </div>
          ))}
        </div>
      )}
    </React.Fragment>
  );
}

// ── Word card (Learn / Review) ──────────────────────────
function WordCard({ word, mode, level, onLevelChange, autoplay, isTop, dragState, exampleMode = 'beginner', onExampleModeChange }) {
  const playedRef = useRefW(null);

  useEffectW(() => {
    if (!isTop || !autoplay) return;
    if (playedRef.current === word.nl) return;
    playedRef.current = word.nl;
    const t = setTimeout(() => speak(word.nl), 180);
    return () => clearTimeout(t);
  }, [isTop, word.nl, autoplay]);

  const exMap  = exampleMode === 'exam'
    ? (word.examExamples || word.examples || {})
    : (word.beginnerExamples || word.examples || {});
  const ex     = exMap.a1 || exMap.a0 || exMap.a2 || { nl: '—', en: '' };
  const hasEx  = ex.nl && ex.nl !== '—';
  const exampleTitle = word.deck === 'ar'
    ? 'From the exam text'
    : exampleMode === 'exam' && word.examExamples
      ? 'From the exam text'
      : 'Beginner example';
  const grammarRows = compactWordGrammar(word);
  const showExampleToggle = word.deck === 'common';

  return (
    <React.Fragment>
      {isTop && (
        <React.Fragment>
          <div className="stamp keep"   style={{ opacity: dragState.keepOpacity }}>GOT IT</div>
          <div className="stamp forgot" style={{ opacity: dragState.forgotOpacity }}>AGAIN</div>
        </React.Fragment>
      )}

      <div className="card-top-row">
        <span className="les-tag">Article {word.les}</span>
        {word.pos && <span className="pos-tag">{word.pos}</span>}
      </div>

      <div className="word-block">
        <div className={'word' + (word.type === 'sentence' ? ' sentence-word' : '')}>{word.nl}</div>
        {word.ipa && <div className="ipa">/{word.ipa}/</div>}
        <div style={{ marginTop: 10, display: 'flex', justifyContent: 'center' }}>
          <button
            className="speaker-btn"
            onPointerDown={e => e.stopPropagation()}
            onClick={e => { e.stopPropagation(); speak(word.nl); }}
            aria-label="Uitspreken"
          ><SpeakerIcon size={16} /></button>
        </div>
        {mode !== 'test' && <div className="meaning">{word.en}</div>}
      </div>

      <div className="divider"></div>

      <div className="example-block">
        {hasEx ? (
          <>
            {showExampleToggle ? (
              <div className="card-example-seg" onPointerDown={e => e.stopPropagation()}>
                {[{v:'beginner', lab:'Beginner'}, {v:'exam', lab:'Exam'}].map(o => (
                  <button
                    key={o.v}
                    type="button"
                    className={exampleMode === o.v ? 'active' : ''}
                    onClick={e => { e.stopPropagation(); onExampleModeChange?.(o.v); }}
                  >{o.lab}</button>
                ))}
              </div>
            ) : (
              <div className="sentence-grammar-title">{exampleTitle}</div>
            )}
            <div className="example-nl">
              <button
                className="speaker-btn small keep"
                onPointerDown={e => e.stopPropagation()}
                onClick={e => { e.stopPropagation(); speak(ex.nl); }}
                aria-label="Voorbeeld uitspreken"
              ><SpeakerIcon size={13} /></button>
              <span><ClickableDutchText text={ex.nl} /></span>
            </div>
            {ex.en && ex.en !== word.en && ex.en !== 'Original sentence from the mock exam.' && <div className="example-en">{ex.en}</div>}
          </>
        ) : (
          <div className="example-missing">
            Example not available yet.
          </div>
        )}
      </div>

      {grammarRows.length > 0 && mode !== 'test' && (
        <div className="grammar-card" onPointerDown={e => e.stopPropagation()}>
          <div className="grammar-card-title">Grammatica</div>
          {grammarRows.map((f, i) => (
            <div className="grammar-card-row" key={i}>
              <span className="lab">{f.label}</span>
              <span className="form">{f.nl}</span>
            </div>
          ))}
        </div>
      )}
    </React.Fragment>
  );
}

// ── Test card (multiple choice) ─────────────────────────
function TestCard({ word, choices, autoplay, isTop, dragState, onAnswered }) {
  const [picked, setPicked] = useStateW(null);
  const playedRef = useRefW(null);

  useEffectW(() => { setPicked(null); playedRef.current = null; }, [word.nl]);

  useEffectW(() => {
    if (!isTop || !autoplay || playedRef.current === word.nl) return;
    playedRef.current = word.nl;
    const t = setTimeout(() => speak(word.nl), 180);
    return () => clearTimeout(t);
  }, [isTop, word.nl, autoplay]);

  const handlePick = (e, choice) => {
    e.stopPropagation();
    if (picked) return;
    const correct = choice === word.en;
    setPicked({ choice, correct });
    setTimeout(() => onAnswered?.(correct), 800);
  };

  return (
    <React.Fragment>
      {isTop && (
        <React.Fragment>
          <div className="stamp keep"   style={{ opacity: dragState.keepOpacity }}>GOT IT</div>
          <div className="stamp forgot" style={{ opacity: dragState.forgotOpacity }}>AGAIN</div>
        </React.Fragment>
      )}

      <div className="card-top-row">
        <span className="les-tag">Article {word.les}</span>
        {word.pos && <span className="pos-tag">{word.pos}</span>}
      </div>

      <div className="word-block">
        <div className="word">{word.nl}</div>
        {word.ipa && <div className="ipa">/{word.ipa}/</div>}
        <div style={{ marginTop: 10, display: 'flex', justifyContent: 'center' }}>
          <button
            className="speaker-btn"
            onPointerDown={e => e.stopPropagation()}
            onClick={e => { e.stopPropagation(); speak(word.nl); }}
          ><SpeakerIcon size={16} /></button>
        </div>
      </div>

      <div style={{ fontSize: 11, fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--ink-faint)', marginTop: 12, textAlign: 'center' }}>
        {word.type === 'sentence' ? 'Choose the explanation' : 'What does it mean?'}
      </div>

      <div className="test-options" onPointerDown={e => e.stopPropagation()}>
        {choices.map((c, i) => {
          let cls = 'test-opt';
          if (picked) {
            cls += ' disabled';
            if (c === word.en)          cls += ' right';
            else if (picked.choice === c) cls += ' wrong';
          }
          return (
            <button key={c} className={cls} onClick={e => handlePick(e, c)}>
              <span className="letter">{String.fromCharCode(65 + i)}</span>
              <span>{c}</span>
            </button>
          );
        })}
      </div>
    </React.Fragment>
  );
}

window.WordCard  = WordCard;
window.SentenceCard = SentenceCard;
window.TestCard  = TestCard;
window.SpeakerIcon = SpeakerIcon;
window.ChevDown  = ChevDown;
