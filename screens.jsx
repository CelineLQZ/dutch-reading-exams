// Screens: Register, Home, Deck, Test, Done, UserSwitcher
const { useState: useStateS, useRef: useRefS, useMemo: useMemoS, useEffect: useEffectS } = React;

/* ── Icon helpers ─────────────────────────────────── */
function CloseIcon()   { return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6L6 18"/><path d="M6 6l12 12"/></svg>; }
function CheckIcon()   { return <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3"   strokeLinecap="round" strokeLinejoin="round"><path d="M5 12l5 5L20 7"/></svg>; }
function XIcon()       { return <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3"   strokeLinecap="round" strokeLinejoin="round"><path d="M18 6L6 18"/><path d="M6 6l12 12"/></svg>; }
function PlayIcon()    { return <svg width="18" height="18" viewBox="0 0 24 24" fill="white" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>; }
function GearIcon()    { return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>; }
function ChevDownS()   { return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="M6 9l6 6 6-6"/></svg>; }

function initial(name) { return (name || '?').trim().charAt(0).toUpperCase(); }

function shuffleArr(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/* ── Register ─────────────────────────────────────── */
function RegisterScreen({ existingUsers, onCreate, onPickExisting }) {
  const [name, setName] = useStateS('');
  const trimmed = name.trim();
  const submit = () => { if (trimmed) onCreate(trimmed); };
  return (
    <div className="app-screen">
      <div className="register">
        <div className="hero">
          <div className="flag">🇳🇱</div>
          <h1>Lezen</h1>
          <p>Practice Dutch exam words<br/>and reading sentences.</p>
        </div>
        <label className="field-label">Your name</label>
        <input className="text-input" autoFocus placeholder="e.g. Alex" value={name}
          onChange={e => setName(e.target.value)} onKeyDown={e => e.key === 'Enter' && submit()} maxLength={24} />
        <button className="primary-btn" disabled={!trimmed} onClick={submit}>Start learning</button>
        {existingUsers.length > 0 && (
          <div className="existing-users">
            <div className="field-label" style={{ marginBottom: 8 }}>Or continue as</div>
            {existingUsers.map(u => (
              <div key={u} className="user-row" onClick={() => onPickExisting(u)}>
                <div className="user-avatar">{initial(u)}</div>
                <div className="name">{u}</div>
                <div className="chev">›</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

/* ── User Switcher (bottom sheet) ────────────────── */
function UserSwitcher({ users, active, onPick, onAdd, onDelete, onClose }) {
  const [adding, setAdding] = useStateS(false);
  const [newName, setNewName] = useStateS('');
  const submit = () => {
    const t = newName.trim();
    if (!t) return;
    onAdd(t); setNewName(''); setAdding(false);
  };
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="sheet" onClick={e => e.stopPropagation()}>
        <div className="sheet-handle"></div>
        <h2>Switch user</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {users.map(u => (
            <div key={u} style={{
              background: u === active ? 'var(--paper-2)' : 'var(--paper)',
              border: u === active ? '2px solid var(--brand)' : '1px solid var(--line)',
              borderRadius: 14, padding: '12px 14px',
              display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer'
            }} onClick={() => onPick(u)}>
              <div className="user-avatar">{initial(u)}</div>
              <div style={{ flex: 1, fontWeight: 700, fontSize: 15 }}>{u}</div>
              {u === active
                ? <div style={{ fontSize: 10, fontWeight: 800, color: 'var(--brand)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>active</div>
                : <button onClick={e => { e.stopPropagation(); if (confirm(`Delete ${u}?`)) onDelete(u); }}
                    style={{ background: 'transparent', border: 'none', color: 'var(--ink-faint)', fontSize: 18, padding: 4, cursor: 'pointer' }}>×</button>
              }
            </div>
          ))}
        </div>
        {adding ? (
          <div style={{ marginTop: 14 }}>
            <input className="text-input" autoFocus placeholder="New name" value={newName}
              onChange={e => setNewName(e.target.value)} onKeyDown={e => e.key === 'Enter' && submit()} maxLength={24} />
            <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
              <button className="ghost-btn" style={{ flex: 1, margin: 0 }} onClick={() => { setAdding(false); setNewName(''); }}>Cancel</button>
              <button className="primary-btn" style={{ flex: 1, margin: 0 }} disabled={!newName.trim()} onClick={submit}>Add</button>
            </div>
          </div>
        ) : (
          <button className="ghost-btn" onClick={() => setAdding(true)} style={{ marginTop: 14 }}>+ Add another user</button>
        )}
      </div>
    </div>
  );
}

/* ── Home ────────────────────────────────────────── */
function LegacyHomeScreen({ user, stats, sentenceStats, prefs, lessons, articles, wordCategories, onPickMode, onPickContent, onChangePrefs, onSwitchUser, onShowSettings, continueSession, onContinue }) {
  const [lesOpen, setLesOpen] = useStateS(false);
  const [categoryOpen, setCategoryOpen] = useStateS(false);
  const [testCountDraft, setTestCountDraft] = useStateS(String(prefs.testCount || 100));
  const activeStats = prefs.contentType === 'sentences' ? sentenceStats : stats;
  const activeUnit = prefs.contentType === 'sentences' ? 'sentences' : 'words';
  const allWordCount = wordCategories.reduce((sum, c) => sum + c.count, 0);
  const allArticleCount = articles.reduce((sum, a) => sum + (prefs.contentType === 'sentences' ? a.sentenceCount : a.wordCount), 0);
  const currentArticle = articles.find(a => a.les === prefs.les);
  const currentLesLabel = prefs.les === 'all'
    ? `All articles · ${activeStats.total} ${activeUnit}`
    : `Article ${prefs.les} · ${currentArticle?.title || ''}`;
  const currentCategory = wordCategories.find(c => c.id === prefs.category);
  const currentCategoryLabel = prefs.category === 'all'
    ? `All categories · ${allWordCount} words`
    : `${currentCategory?.label || prefs.category} · ${currentCategory?.count || 0} words`;
  const applyTestCount = value => {
    const n = Number.parseInt(value, 10);
    const clamped = Number.isFinite(n) ? Math.max(20, Math.min(1200, n)) : 100;
    setTestCountDraft(String(clamped));
    onChangePrefs({ testCount: clamped });
  };

  return (
    <div className="app-screen">
      <div className="topbar">
        <div style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 18, letterSpacing: '-0.01em' }}>
          🇳🇱&nbsp;&nbsp;Lezen
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <div className="mode-pill"><span className="dot"></span>{activeStats.total} {activeUnit}</div>
          <button className="iconbtn" onClick={onShowSettings} title="Instellingen"><GearIcon /></button>
        </div>
      </div>

      <div className="home">
        {/* Greeting */}
        <div className="home-greet" onClick={onSwitchUser}>
          <div className="user-avatar">{initial(user)}</div>
          <div className="who">
            <div className="hi">Hallo, {user}!</div>
            <div className="sw">Tap to switch user</div>
          </div>
          <div style={{ color: 'var(--ink-faint)', fontSize: 22 }}>⇅</div>
        </div>

        {/* Stats */}
        <div className="stats-row">
          <div className="stat-card brand"><div className="num">{activeStats.total}</div><div className="lbl">Total</div></div>
          <div className="stat-card keep"><div className="num">{activeStats.learned}</div><div className="lbl">Learned</div></div>
          <div className="stat-card forgot"><div className="num">{activeStats.forgotten}</div><div className="lbl">Review</div></div>
        </div>

        {/* Continue banner */}
        {continueSession && (
          <div className="continue-banner" onClick={onContinue}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="label">Continue</div>
              <div className="title">
                {continueSession.mode === 'test' ? 'Test in progress'
                 : continueSession.mode === 'review' ? 'Review session'
                 : 'Learning session'}
              </div>
              <div className="progress">
                <span style={{ width: `${Math.round((continueSession.cursor / continueSession.words.length) * 100)}%` }}></span>
              </div>
            </div>
            <div className="play"><PlayIcon /></div>
          </div>
        )}

        <div className="section-h"><h3>Content</h3></div>
        <div className="seg" style={{ marginBottom: 14 }}>
          {[{v:'words',lab:'Words'},{v:'sentences',lab:'Sentences'}].map(o => (
            <div key={o.v} className={'opt' + (prefs.contentType === o.v ? ' active' : '')}
              onClick={() => onPickContent ? onPickContent(o.v) : onChangePrefs({ contentType: o.v, filterMode: o.v === 'sentences' ? 'article' : prefs.filterMode })}>{o.lab}</div>
          ))}
        </div>

        {prefs.contentType === 'words' && (
          <>
            <div className="section-h"><h3>Filter type</h3></div>
            <div className="seg" style={{ marginBottom: 14 }}>
              {[{v:'article',lab:'Article'},{v:'category',lab:'Category'}].map(o => (
                <div key={o.v} className={'opt' + (prefs.filterMode === o.v ? ' active' : '')}
                  onClick={() => onChangePrefs({ filterMode: o.v })}>{o.lab}</div>
              ))}
            </div>
          </>
        )}

        {/* Article/category dropdown */}
        <div className="section-h"><h3>{prefs.contentType === 'words' && prefs.filterMode === 'category' ? 'Category' : 'Article'}</h3></div>
        {prefs.contentType === 'words' && prefs.filterMode === 'category' ? (
          <div className={'dropdown' + (categoryOpen ? ' open' : '')}>
            <button type="button" className="dropdown-trigger" onClick={() => setCategoryOpen(o => !o)}>
              <span className="dropdown-value">{currentCategoryLabel}</span>
              <span className="dropdown-chev"><ChevDownS /></span>
            </button>
            {categoryOpen && (
              <div className="dropdown-menu">
                <div className={'dropdown-item' + (prefs.category === 'all' ? ' active' : '')}
                  onClick={() => { onChangePrefs({ category: 'all' }); setCategoryOpen(false); }}>
                  <span>All categories</span>
                  <span className="dropdown-count">{allWordCount}</span>
                </div>
                {wordCategories.map(c => (
                  <div key={c.id}
                    className={'dropdown-item' + (prefs.category === c.id ? ' active' : '')}
                    onClick={() => { onChangePrefs({ category: c.id }); setCategoryOpen(false); }}>
                    <span>{c.label}</span>
                    <span className="dropdown-count">{c.count}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
        <div className={'dropdown' + (lesOpen ? ' open' : '')}>
          <button type="button" className="dropdown-trigger" onClick={() => setLesOpen(o => !o)}>
            <span className="dropdown-value">{currentLesLabel}</span>
            <span className="dropdown-chev"><ChevDownS /></span>
          </button>
          {lesOpen && (
            <div className="dropdown-menu">
              <div className={'dropdown-item' + (prefs.les === 'all' ? ' active' : '')}
                onClick={() => { onChangePrefs({ les: 'all' }); setLesOpen(false); }}>
                <span>All articles</span>
                <span className="dropdown-count">{allArticleCount}</span>
              </div>
              {articles.map(a => (
                <div key={a.les}
                  className={'dropdown-item' + (prefs.les === a.les ? ' active' : '')}
                  onClick={() => { onChangePrefs({ les: a.les }); setLesOpen(false); }}>
                  <span>Article {a.les}: {a.title}</span>
                  <span className="dropdown-count">{prefs.contentType === 'sentences' ? a.sentenceCount : a.wordCount}</span>
                </div>
              ))}
            </div>
          )}
        </div>
        )}

        {/* Modes */}
        <div className="section-h" style={{ marginTop: 18 }}><h3>Modes</h3></div>
        <div className="mode-list">
          <div className="mode-card learn" onClick={() => onPickMode('study')}>
            <div className="glyph">📖</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="title">Study</div>
              <div className="desc">Swipe through selected {activeUnit}.</div>
            </div>
            <div className="chev">›</div>
          </div>
          <div className="mode-card review" onClick={() => onPickMode('review')}>
            <div className="glyph">🔁</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="title">Review</div>
              <div className="desc">{activeStats.forgotten ? `${activeStats.forgotten} ${activeUnit.slice(0, -1)}${activeStats.forgotten === 1 ? '' : 's'} to retry` : 'Nothing to review yet'}</div>
            </div>
            <div className="chev">›</div>
          </div>
          <div className="mode-card test" onClick={() => onPickMode('test')}>
            <div className="glyph">✓</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="title">Test</div>
              <div className="desc">{prefs.contentType === 'sentences' ? 'Pick the English explanation.' : 'Guess the meaning — no hints.'}</div>
            </div>
            <div className="chev">›</div>
          </div>
        </div>

        {/* Test count (only relevant when testing all words) */}
        {prefs.les === 'all' && !(prefs.contentType === 'words' && prefs.filterMode === 'category' && prefs.category !== 'all') && (
          <>
            <div className="section-h" style={{ marginTop: 18 }}><h3>Test count</h3></div>
            <div className="test-count-row">
              <input className="number-input" type="number" inputMode="numeric"
                min="20" max="1200" step="10" value={testCountDraft}
                onChange={e => setTestCountDraft(e.target.value)}
                onBlur={e => applyTestCount(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') e.currentTarget.blur(); }} />
              <div className="count-hint">20-1200</div>
            </div>
          </>
        )}

        {/* Order */}
        <div className="section-h"><h3>Order</h3></div>
        <div className="seg" style={{ marginBottom: 14 }}>
          {[{v:'random',lab:'Random'},{v:'course',lab:'By lesson'}].map(o => (
            <div key={o.v} className={'opt' + (prefs.order === o.v ? ' active' : '')}
              onClick={() => onChangePrefs({ order: o.v })}>{o.lab}</div>
          ))}
        </div>

      </div>
    </div>
  );
}

function LegacyWordsPickScreen({ wordCategories, statsByCategory, articles, prefs, onBack, onPickAll, onPickCategory, onPickArticle }) {
  const [mode, setMode] = useStateS('category');
  const orderedCategories = ['verb', 'noun', 'preposition', 'question', 'time', 'phrase', 'pronoun', 'adverb', 'adjective', 'grammar', 'other'];
  const categories = wordCategories.slice().sort((a, b) => {
    const ai = orderedCategories.indexOf(a.id);
    const bi = orderedCategories.indexOf(b.id);
    return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
  });

  return (
    <div className="app-screen">
      <div className="topbar">
        <button className="iconbtn" onClick={onBack}><CloseIcon /></button>
        <div className="mode-pill"><span className="dot"></span>Words</div>
        <div style={{ width: 38 }}></div>
      </div>
      <div className="home pick-screen">
        <div className="seg">
          <div className={'opt' + (mode === 'all' ? ' active' : '')} onClick={() => { setMode('all'); onPickAll(); }}>All</div>
          <div className={'opt' + (mode === 'article' ? ' active' : '')} onClick={() => setMode('article')}>Article</div>
          <div className={'opt' + (mode === 'category' ? ' active' : '')} onClick={() => setMode('category')}>Category</div>
        </div>

        {mode === 'article' ? (
          <>
            <div className="section-h"><h3>Articles</h3></div>
            <div className="pick-list">
              {articles.map(a => (
                <div key={a.les} className="mode-card pick-row" onClick={() => onPickArticle(a.les)}>
                  <div className="glyph reading">{a.les}</div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div className="title">Article {a.les}</div>
                    <div className="desc">{a.title} · {a.wordCount} words</div>
                  </div>
                  <div className="chev">›</div>
                </div>
              ))}
            </div>
          </>
        ) : (
          <>
            <div className="section-h"><h3>Categories</h3></div>
            <div className="pick-grid">
              {categories.map(c => {
                const s = statsByCategory[c.id] || { total: c.count, learned: 0 };
                const pct = s.total ? Math.round((s.learned / s.total) * 100) : 0;
                return (
                  <div key={c.id} className="pick-card" onClick={() => onPickCategory(c.id)}>
                    <div className="pick-card-title">{c.label}</div>
                    <div className="pick-card-count">{c.count} words</div>
                    <div className="mini-progress"><span style={{ width: `${pct}%` }}></span></div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function LegacySentencesPickScreen({ readings, statsByArticle, onBack, onPickArticle }) {
  const rows = readings.map(r => {
    const s = statsByArticle[r.id] || { total: r.sentences?.length || 0, learned: 0 };
    return { ...r, stats: s, pct: s.total ? Math.round((s.learned / s.total) * 100) : 0 };
  });
  const resume = rows.find(r => r.stats.learned > 0 && r.stats.learned < r.stats.total) || rows[0];

  return (
    <div className="app-screen">
      <div className="topbar">
        <button className="iconbtn" onClick={onBack}><CloseIcon /></button>
        <div className="mode-pill"><span className="dot"></span>Sentences</div>
        <div style={{ width: 38 }}></div>
      </div>
      <div className="home pick-screen">
        {resume && (
          <div className="continue-banner pick-continue" onClick={() => onPickArticle(resume.les)}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="label">Continue</div>
              <div className="title">{resume.title}</div>
              <div className="desc-light">Sentence {Math.min(resume.stats.learned + 1, resume.stats.total)}/{resume.stats.total}</div>
              <div className="progress"><span style={{ width: `${resume.pct}%` }}></span></div>
            </div>
            <div className="play"><PlayIcon /></div>
          </div>
        )}

        <div className="section-h"><h3>All articles</h3></div>
        <div className="pick-list">
          {rows.map(r => (
            <div key={r.id} className="mode-card pick-row" onClick={() => onPickArticle(r.les)}>
              <div className="glyph reading">{r.stats.total}</div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div className="title">{r.title}</div>
                <div className="desc">{r.stats.total} sentences</div>
                <div className="mini-progress"><span style={{ width: `${r.pct}%` }}></span></div>
              </div>
              <div className="chev">›</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function SessionModeList({ selected, order, onOrder, onStart, reviewCount = 0, unit = 'items' }) {
  if (!selected) {
    return (
      <div className="empty-hint-card">
        Choose the content you want to practice first.
      </div>
    );
  }
  return (
    <>
      <div className="section-h"><h3>Modes</h3></div>
      <div className="mode-list">
        <div className="mode-card learn" onClick={() => onStart('study')}>
          <div className="glyph">📖</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div className="title">Study</div>
            <div className="desc">Swipe through {selected.label}.</div>
          </div>
          <div className="chev">›</div>
        </div>
        <div className="mode-card review" onClick={() => onStart('review')}>
          <div className="glyph">🔁</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div className="title">Review</div>
            <div className="desc">{reviewCount ? `${reviewCount} ${unit} to retry` : 'Nothing to review yet'}</div>
          </div>
          <div className="chev">›</div>
        </div>
        <div className="mode-card test" onClick={() => onStart('test')}>
          <div className="glyph">✓</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div className="title">Test</div>
            <div className="desc">Dutch → English, 4 choices.</div>
          </div>
          <div className="chev">›</div>
        </div>
      </div>

      <div className="section-h"><h3>Order</h3></div>
      <div className="seg" style={{ marginBottom: 14 }}>
        {[{v:'course',lab:'By order'},{v:'random',lab:'Random'}].map(o => (
          <div key={o.v} className={'opt' + (order === o.v ? ' active' : '')}
            onClick={() => onOrder(o.v)}>{o.lab}</div>
        ))}
      </div>
    </>
  );
}

function HomeScreen({ user, stats, sentenceStats, onPickContent, onSwitchUser, onShowSettings, continueSession, onContinue }) {
  return (
    <div className="app-screen">
      <div className="topbar">
        <div style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 18, letterSpacing: '-0.01em' }}>
          🇳🇱&nbsp;&nbsp;Lezen
        </div>
        <button className="iconbtn" onClick={onShowSettings} title="Instellingen"><GearIcon /></button>
      </div>

      <div className="home">
        <div className="home-greet" onClick={onSwitchUser}>
          <div className="user-avatar">{initial(user)}</div>
          <div className="who">
            <div className="hi">Hallo, {user}!</div>
            <div className="sw">Tap to switch user</div>
          </div>
          <div style={{ color: 'var(--ink-faint)', fontSize: 22 }}>⇅</div>
        </div>

        <div className="stats-row">
          <div className="stat-card brand"><div className="num">{stats.total}</div><div className="lbl">Words</div></div>
          <div className="stat-card keep"><div className="num">{sentenceStats.total}</div><div className="lbl">Sentences</div></div>
          <div className="stat-card forgot"><div className="num">{stats.forgotten + sentenceStats.forgotten}</div><div className="lbl">Review</div></div>
        </div>

        {continueSession && (
          <div className="continue-banner" onClick={onContinue}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="label">Continue</div>
              <div className="title">Learning session</div>
              <div className="progress">
                <span style={{ width: `${Math.round((continueSession.cursor / continueSession.words.length) * 100)}%` }}></span>
              </div>
            </div>
            <div className="play"><PlayIcon /></div>
          </div>
        )}

        <div className="section-h"><h3>Choose content</h3></div>
        <div className="mode-list">
          <div className="mode-card learn" onClick={() => onPickContent('words')}>
            <div className="glyph">▣</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="title">Words</div>
              <div className="desc">Pick a deck by article or category.</div>
            </div>
            <div className="chev">›</div>
          </div>
          <div className="mode-card reading" onClick={() => onPickContent('sentences')}>
            <div className="glyph">¶</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="title">Sentences</div>
              <div className="desc">Pick an article and read sentence by sentence.</div>
            </div>
            <div className="chev">›</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function WordsPickScreen({ wordCategories, statsByCategory, articles, prefs, onBack, onStartDeck }) {
  const allDeck = { id: 'all', label: 'all words', reviewCount: 0, patch: { filterMode: 'article', les: 'all', category: 'all' } };
  const [mode, setMode] = useStateS('all');
  const [selected, setSelected] = useStateS(allDeck);
  const [order, setOrder] = useStateS(prefs.order || 'course');
  const [articleOrder, setArticleOrder] = useStateS('asc');
  const [articleLes, setArticleLes] = useStateS('');
  const [wordLimit, setWordLimit] = useStateS(String(prefs.wordLimit || ''));
  const [lesFrom, setLesFrom] = useStateS(String(prefs.lesFrom || ''));
  const [lesTo, setLesTo] = useStateS(String(prefs.lesTo || ''));
  const orderedCategories = ['verb', 'noun', 'preposition', 'question', 'other'];
  const categories = wordCategories.slice().sort((a, b) => {
    const ai = orderedCategories.indexOf(a.id);
    const bi = orderedCategories.indexOf(b.id);
    return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
  });
  const articleOptions = articles
    .filter(a => a.wordCount > 0)
    .slice()
    .sort((a, b) => articleOrder === 'asc' ? a.les - b.les : b.les - a.les);
  const pick = deck => setSelected(deck);
  const start = action => {
    if (!selected) return;
    const custom = selected.id === 'all' ? { wordLimit, lesFrom, lesTo } : { wordLimit: '', lesFrom: '', lesTo: '' };
    onStartDeck(action, { ...selected.patch, ...custom, order });
  };
  const changeContent = () => {
    setSelected(null);
    setArticleLes('');
  };
  const pickArticleValue = value => {
    const les = Number(value);
    const article = articles.find(a => a.les === les);
    setArticleLes(value);
    if (article) {
      pick({ id: `article-${article.les}`, label: article.title, reviewCount: 0, patch: { filterMode: 'article', les: article.les, category: 'all' } });
    }
  };

  return (
    <div className="app-screen">
      <div className="topbar">
        <button className="iconbtn" onClick={onBack}><CloseIcon /></button>
        <div className="mode-pill"><span className="dot"></span>Words</div>
        <div style={{ width: 38 }}></div>
      </div>
      <div className="home pick-screen">
        <div className="seg">
          <div className={'opt' + (mode === 'all' ? ' active' : '')} onClick={() => { setMode('all'); pick(allDeck); }}>All</div>
          <div className={'opt' + (mode === 'article' ? ' active' : '')} onClick={() => { setMode('article'); changeContent(); }}>Article</div>
          <div className={'opt' + (mode === 'category' ? ' active' : '')} onClick={() => { setMode('category'); changeContent(); }}>Category</div>
        </div>

        {selected && (
          <div className="selected-deck-pill">
            Selected: <strong>{selected.label}</strong>
            <button type="button" onClick={changeContent}>Change</button>
          </div>
        )}

        {selected?.id === 'all' && (
          <div className="custom-filter-card">
            <div className="section-h"><h3>Customize all words</h3></div>
            <div className="inline-input-grid">
              <label>
                <span>Words</span>
                <input className="number-input compact" inputMode="numeric" type="number" min="1" max="1200"
                  placeholder="All" value={wordLimit} onChange={e => setWordLimit(e.target.value)} />
              </label>
              <label>
                <span>From article</span>
                <input className="number-input compact" inputMode="numeric" type="number" min="1" max="40"
                  placeholder="1" value={lesFrom} onChange={e => setLesFrom(e.target.value)} />
              </label>
              <label>
                <span>To article</span>
                <input className="number-input compact" inputMode="numeric" type="number" min="1" max="40"
                  placeholder="40" value={lesTo} onChange={e => setLesTo(e.target.value)} />
              </label>
            </div>
          </div>
        )}

        <SessionModeList selected={selected} order={order} onOrder={setOrder}
          reviewCount={selected?.reviewCount || 0} unit="words" onStart={start} />

        {!selected && mode === 'article' ? (
          <>
            <div className="section-h pick-heading-row">
              <h3>Pick article</h3>
              <button className="sort-toggle-btn" type="button"
                onClick={() => setArticleOrder(o => o === 'asc' ? 'desc' : 'asc')}>
                {articleOrder === 'asc' ? '↑' : '↓'}
              </button>
            </div>
            <select className="select-input" value={articleLes} onChange={e => pickArticleValue(e.target.value)}>
              <option value="">Choose an article</option>
              {articleOptions.map(a => (
                <option key={a.les} value={a.les}>Article {a.les}: {a.title} · {a.wordCount} words</option>
              ))}
            </select>
          </>
        ) : !selected && mode === 'category' ? (
          <>
            <div className="section-h"><h3>Pick category</h3></div>
            <div className="pick-grid">
              {categories.map(c => {
                const s = statsByCategory[c.id] || { total: c.count, learned: 0, forgotten: 0 };
                const pct = s.total ? Math.round((s.learned / s.total) * 100) : 0;
                return (
                  <div key={c.id} className={'pick-card' + (selected?.id === `category-${c.id}` ? ' selected' : '')}
                    onClick={() => pick({ id: `category-${c.id}`, label: c.label, reviewCount: s.forgotten, patch: { filterMode: 'category', category: c.id, les: 'all' } })}>
                    <div className="pick-card-title">{c.label}</div>
                    <div className="pick-card-count">{c.count} words</div>
                    <div className="mini-progress"><span style={{ width: `${pct}%` }}></span></div>
                  </div>
                );
              })}
            </div>
          </>
        ) : null}

      </div>
    </div>
  );
}

function SentencesPickScreen({ readings, statsByArticle, prefs, onBack, onStartArticle }) {
  const [selected, setSelected] = useStateS(null);
  const [order, setOrder] = useStateS(prefs.order || 'course');
  const [articleOrder, setArticleOrder] = useStateS('asc');
  const [articleLes, setArticleLes] = useStateS('');
  const rows = readings.map(r => {
    const s = statsByArticle[r.id] || { total: r.sentences?.length || 0, learned: 0, forgotten: 0 };
    return { ...r, stats: s, pct: s.total ? Math.round((s.learned / s.total) * 100) : 0 };
  });
  const articleOptions = rows.slice().sort((a, b) => articleOrder === 'asc' ? a.les - b.les : b.les - a.les);
  const resume = rows.find(r => r.stats.learned > 0 && r.stats.learned < r.stats.total) || rows[0];
  const pick = r => {
    setArticleLes(String(r.les));
    setSelected({ id: r.id, label: r.title, reviewCount: r.stats.forgotten, les: r.les });
  };
  const start = action => selected && onStartArticle(action, selected.les, order);
  const changeContent = () => {
    setSelected(null);
    setArticleLes('');
  };
  const pickArticleValue = value => {
    const les = Number(value);
    const article = rows.find(r => r.les === les);
    if (article) pick(article);
    else changeContent();
  };

  return (
    <div className="app-screen">
      <div className="topbar">
        <button className="iconbtn" onClick={onBack}><CloseIcon /></button>
        <div className="mode-pill"><span className="dot"></span>Sentences</div>
        <div style={{ width: 38 }}></div>
      </div>
      <div className="home pick-screen">
        {resume && (
          <div className="continue-banner pick-continue" onClick={() => pick(resume)}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="label">Continue</div>
              <div className="title">{resume.title}</div>
              <div className="desc-light">Sentence {Math.min(resume.stats.learned + 1, resume.stats.total)}/{resume.stats.total}</div>
              <div className="progress"><span style={{ width: `${resume.pct}%` }}></span></div>
            </div>
            <div className="play"><PlayIcon /></div>
          </div>
        )}

        {selected && (
          <div className="selected-deck-pill">
            Selected: <strong>{selected.label}</strong>
            <button type="button" onClick={changeContent}>Change</button>
          </div>
        )}

        <SessionModeList selected={selected} order={order} onOrder={setOrder}
          reviewCount={selected?.reviewCount || 0} unit="sentences" onStart={start} />

        {!selected && (
          <>
            <div className="section-h"><h3>Pick article</h3></div>
            <div className="seg mini-seg">
              {[{v:'asc',lab:'1 → 40'},{v:'desc',lab:'40 → 1'}].map(o => (
                <div key={o.v} className={'opt' + (articleOrder === o.v ? ' active' : '')}
                  onClick={() => setArticleOrder(o.v)}>{o.lab}</div>
              ))}
            </div>
            <select className="select-input" value={articleLes} onChange={e => pickArticleValue(e.target.value)}>
              <option value="">Choose an article</option>
              {articleOptions.map(r => (
                <option key={r.id} value={r.les}>Article {r.les}: {r.title} · {r.stats.total} sentences</option>
              ))}
            </select>
          </>
        )}

      </div>
    </div>
  );
}

/* ── Deck (Learn / Review) ───────────────────────── */
function DeckScreen({ mode, words, level, onLevelChange, autoplay, onExit, onSwipe, progressOffset = 0 }) {
  const deckRef = useRefS(null);
  const [cursor, setCursor] = useStateS(0);
  const [internalLevel, setInternalLevel] = useStateS(level);
  const totalWords = progressOffset + words.length;

  if (!words.length) {
    return (
      <div className="app-screen">
        <div className="topbar">
          <div className="iconbtn" onClick={onExit}><CloseIcon /></div>
          <div className="mode-pill"><span className="dot"></span>{mode}</div>
          <div style={{ width: 38 }}></div>
        </div>
        <div className="empty-state">
          <div className="big">🎉</div>
          <div className="title">Nothing here</div>
          <div className="desc">{mode === 'review' ? 'No words to review yet. Try Learn mode first.' : 'All caught up!'}</div>
          <button className="primary-btn" style={{ maxWidth: 220 }} onClick={onExit}>Back home</button>
        </div>
      </div>
    );
  }

  const done = cursor >= words.length;
  const pct  = totalWords ? Math.round(((progressOffset + cursor) / totalWords) * 100) : 0;
  const swipe = (dir) => deckRef.current?.swipe(dir);
  const sentenceMode = words[0]?.type === 'sentence' || mode.startsWith('sentence') || mode === 'reading';
  const modeLabel = sentenceMode
    ? (mode.includes('review') ? 'Sentence Review' : 'Sentences')
    : (mode === 'review' ? 'Review' : 'Learn');

  return (
    <div className="app-screen">
      <div className="topbar">
        <div className="iconbtn" onClick={onExit}><CloseIcon /></div>
        <div className="mode-pill">
          <span className="dot" style={{ background: mode === 'review' ? 'var(--forgot)' : 'var(--brand)' }}></span>
          {modeLabel}
        </div>
        <div className="counter">{Math.min(progressOffset + cursor + 1, totalWords)}/{totalWords}</div>
      </div>
      {!done && <div className="progressbar"><span style={{ width: pct + '%' }}></span></div>}
      <div className="deck-stage">
        {!done ? (
          <SwipeDeck ref={deckRef} items={words}
            onSwipe={(i, dir, item) => { setCursor(i + 1); onSwipe?.(item, dir, i + 1); }}
            renderCard={(w, i, isTop, dragState) => (
              sentenceMode ? (
                <SentenceCard word={w} mode={mode} autoplay={autoplay} isTop={isTop} dragState={dragState} />
              ) : (
                <WordCard word={w} mode={mode} level={internalLevel}
                  onLevelChange={lv => { setInternalLevel(lv); onLevelChange?.(lv); }}
                  autoplay={autoplay} isTop={isTop} dragState={dragState} />
              )
            )}
          />
        ) : (
          <div className="empty-state">
            <div className="big">🎉</div>
            <div className="title">Session done!</div>
            <div className="desc">Nice work. Come back tomorrow to keep your streak alive.</div>
            <button className="primary-btn" style={{ maxWidth: 220 }} onClick={onExit}>Back home</button>
          </div>
        )}
      </div>
      {!done && (
        <div className="deck-actions">
          <button className="act-btn forgot" onClick={() => swipe('left')}  aria-label="Don't know"><XIcon /></button>
          <button className="act-btn keep"   onClick={() => swipe('right')} aria-label="Got it"><CheckIcon /></button>
        </div>
      )}
    </div>
  );
}

/* ── Reading screen ──────────────────────────────── */
function ReadingScreen({ readings, autoplay, onExit }) {
  const [articleId, setArticleId] = useStateS(readings[0]?.id || null);
  const [sentenceIndex, setSentenceIndex] = useStateS(0);
  const current = readings.find(r => r.id === articleId) || readings[0];
  const sentences = current?.sentences || [];
  const activeSentence = sentences[sentenceIndex];

  useEffectS(() => {
    if (!current || !autoplay) return;
    const sentence = current.sentences?.[sentenceIndex]?.nl;
    if (sentence && window.dutchTTS) {
      const t = setTimeout(() => window.dutchTTS.speak(sentence), 220);
      return () => clearTimeout(t);
    }
  }, [current?.id, sentenceIndex, autoplay]);

  if (!current) {
    return (
      <div className="app-screen">
        <div className="topbar">
          <div className="iconbtn" onClick={onExit}><CloseIcon /></div>
          <div className="mode-pill"><span className="dot"></span>Reading</div>
          <div style={{ width: 38 }}></div>
        </div>
        <div className="empty-state">
          <div className="big">📖</div>
          <div className="title">No readings yet</div>
          <button className="primary-btn" style={{ maxWidth: 220 }} onClick={onExit}>Back home</button>
        </div>
      </div>
    );
  }

  const pickArticle = (id) => {
    setArticleId(id);
    setSentenceIndex(0);
  };
  const goPrev = () => setSentenceIndex(i => Math.max(0, i - 1));
  const goNext = () => setSentenceIndex(i => Math.min(sentences.length - 1, i + 1));
  const pct = sentences.length ? Math.round(((sentenceIndex + 1) / sentences.length) * 100) : 0;

  return (
    <div className="app-screen">
      <div className="topbar">
        <div className="iconbtn" onClick={onExit}><CloseIcon /></div>
        <div className="mode-pill"><span className="dot"></span>Reading</div>
        <div className="counter">{sentenceIndex + 1}/{sentences.length}</div>
      </div>
      <div className="progressbar"><span style={{ width: pct + '%' }}></span></div>
      <div className="reading-screen">
        <div className="article-tabs">
          {readings.map(r => (
            <button key={r.id}
              className={'article-tab' + (r.id === current.id ? ' active' : '')}
              onClick={() => pickArticle(r.id)}>
              {r.les}. {r.title}
            </button>
          ))}
        </div>

        <div className="reading-card-wrap">
          <div className="reading-card">
            <div className="reading-card-top">
              <div>
                <div className="lesson-chip">Article {current.les}</div>
                <h2>{current.title}</h2>
              </div>
              <button className="speaker-btn"
                onClick={() => activeSentence && window.dutchTTS?.speak(activeSentence.nl)}
                aria-label="Sentence pronunciation">
                <SpeakerIcon size={16} />
              </button>
            </div>

            {activeSentence && (
              <div className="reading-sentence">
                <div className="sentence-number">Sentence {sentenceIndex + 1}</div>
                <div className="sentence-nl large">{activeSentence.nl}</div>
                <div className="divider"></div>
                <div className="sentence-en large">{activeSentence.en}</div>
              </div>
            )}
          </div>
        </div>

        <div className="reading-actions">
          <button className="ghost-nav-btn" onClick={goPrev} disabled={sentenceIndex === 0}>Previous</button>
          <button className="primary-nav-btn" onClick={goNext} disabled={sentenceIndex >= sentences.length - 1}>Next</button>
        </div>
      </div>
    </div>
  );
}

/* ── Test screen ─────────────────────────────────── */
function TestScreen({ words, allWords, autoplay, maxQuestions, onWrongWord, onExit, onComplete }) {
  const deckRef = useRefS(null);
  const [cursor, setCursor] = useStateS(0);
  const [score, setScore]   = useStateS({ right: 0, wrong: 0 });
  const [wrongWords, setWrongWords] = useStateS([]);
  const quizKey = useMemoS(
    () => words.map(w => `${w.les}|${w.nl}|${w.en}`).join('~') + `::${maxQuestions ?? 'all'}`,
    [words, maxQuestions]
  );

  const quiz = useMemoS(() => {
    const cap  = maxQuestions != null ? maxQuestions : words.length;
    const pool = shuffleArr(words).slice(0, Math.min(cap, words.length));
    return pool.map(w => {
      const distractors = shuffleArr(allWords.filter(x => x.en !== w.en)).slice(0, 3).map(x => x.en);
      return { word: w, choices: shuffleArr([w.en, ...distractors]) };
    });
  }, [words, allWords, maxQuestions]);
  const sentenceMode = words[0]?.type === 'sentence';

  useEffectS(() => {
    setCursor(0);
    setScore({ right: 0, wrong: 0 });
    setWrongWords([]);
    deckRef.current?.reset?.();
  }, [quizKey]);

  if (!quiz.length) {
    return (
      <div className="app-screen">
        <div className="topbar">
          <div className="iconbtn" onClick={onExit}><CloseIcon /></div>
          <div className="mode-pill"><span className="dot" style={{ background: 'var(--keep)' }}></span>{sentenceMode ? 'Sentence Test' : 'Test'}</div>
          <div style={{ width: 38 }}></div>
        </div>
        <div className="empty-state">
          <div className="big">📭</div>
          <div className="title">{sentenceMode ? 'No sentences yet' : 'No words yet'}</div>
          <div className="desc">{sentenceMode ? 'Choose another article filter or try again.' : 'Learn a few words first, then test yourself.'}</div>
          <button className="primary-btn" style={{ maxWidth: 220 }} onClick={onExit}>Back home</button>
        </div>
      </div>
    );
  }

  const done  = cursor >= quiz.length;
  const total = quiz.length;
  const pct   = total ? Math.round((cursor / total) * 100) : 0;

  if (done) {
    return <DoneScreen right={score.right} wrong={score.wrong} wrongWords={wrongWords} onExit={onExit}
      onRetry={wrongWords.length ? () => onComplete?.(wrongWords) : null} />;
  }

  return (
    <div className="app-screen">
      <div className="topbar">
        <div className="iconbtn" onClick={onExit}><CloseIcon /></div>
        <div className="mode-pill"><span className="dot" style={{ background: 'var(--keep)' }}></span>{sentenceMode ? 'Sentence Test' : 'Test'}</div>
        <div className="counter">{cursor + 1}/{total}</div>
      </div>
      <div className="progressbar"><span style={{ width: pct + '%' }}></span></div>
      <div className="deck-stage">
        <SwipeDeck ref={deckRef} items={quiz}
          onSwipe={(i) => setCursor(i + 1)}
          renderCard={(q, i, isTop, dragState) => (
            <TestCard word={q.word} choices={q.choices} autoplay={autoplay} isTop={isTop} dragState={dragState}
              onAnswered={correct => {
                setScore(s => ({ right: s.right + (correct ? 1 : 0), wrong: s.wrong + (correct ? 0 : 1) }));
                if (!correct) {
                  setWrongWords(ws => [...ws, q.word]);
                  onWrongWord?.(q.word);
                }
                deckRef.current?.swipe(correct ? 'right' : 'left');
              }}
            />
          )}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          marginTop: 14, padding: '0 6px', fontSize: 12, fontWeight: 800,
          textTransform: 'uppercase', letterSpacing: '0.08em' }}>
          <span style={{ color: 'var(--forgot)' }}>✗ {score.wrong}</span>
          <span style={{ color: 'var(--ink-faint)' }}>Tap an answer</span>
          <span style={{ color: 'var(--keep)' }}>{score.right} ✓</span>
        </div>
      </div>
    </div>
  );
}

/* ── Done screen ─────────────────────────────────── */
function DoneScreen({ right, wrong, wrongWords, onExit, onRetry }) {
  const total = right + wrong;
  const pct   = total ? Math.round((right / total) * 100) : 0;
  const title = pct >= 90 ? 'Geweldig!' : pct >= 70 ? 'Goed gedaan!' : pct >= 40 ? 'Bijna!' : 'Blijf oefenen!';
  const desc  = pct >= 90 ? 'Practically a native speaker.'
    : pct >= 70 ? 'Solid result. Tomorrow nail the rest.'
    : pct >= 40 ? 'A few more rounds and these stick.'
    : 'Every swipe counts. Try once more.';
  return (
    <div className="app-screen">
      <div className="topbar">
        <div className="iconbtn" onClick={onExit}><CloseIcon /></div>
        <div className="mode-pill"><span className="dot" style={{ background: 'var(--keep)' }}></span>Done</div>
        <div style={{ width: 38 }}></div>
      </div>
      <div className="empty-state">
        <div className="score-circle" style={{ '--p': pct + '%' }}>
          <div className="inner">
            <div style={{ textAlign: 'center' }}>
              <div className="pct">{pct}%</div>
              <div className="lab">{right}/{total} right</div>
            </div>
          </div>
        </div>
        <div className="score-breakdown">
          <span className="right">✓ {right} correct</span>
          <span className="wrong">✗ {wrong} wrong</span>
        </div>
        <div className="title" style={{ marginTop: 12 }}>{title}</div>
        <div className="desc">{desc}</div>
        <div className="button-row">
          {onRetry && (
            <button className="primary-btn" type="button" onClick={onRetry}>
              Retry {wrongWords.length} wrong word{wrongWords.length === 1 ? '' : 's'}
            </button>
          )}
          <button type="button" className={onRetry ? 'ghost-btn' : 'primary-btn'} style={{ margin: 0 }} onClick={onExit}>Back home</button>
        </div>
      </div>
    </div>
  );
}

window.RegisterScreen = RegisterScreen;
window.UserSwitcher   = UserSwitcher;
window.HomeScreen     = HomeScreen;
window.WordsPickScreen = WordsPickScreen;
window.SentencesPickScreen = SentencesPickScreen;
window.DeckScreen     = DeckScreen;
window.ReadingScreen  = ReadingScreen;
window.TestScreen     = TestScreen;
window.DoneScreen     = DoneScreen;
