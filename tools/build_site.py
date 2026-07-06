#!/usr/bin/env python3
"""Genererar index.html och test.html från data/ och docs/04.

Körs från repots rot:  python3 tools/build_site.py [artefakt-kopia.html]

- index.html: partisammanställning, stor grön "Gör testet"-knapp och ett
  resultatkort som visas om ett sparat resultat finns i localStorage.
- test.html: själva valkompasstestet. Frågor med infoknapp (förklaring +
  för-/nackdelar), viktning, hoppa över, matchning enligt
  docs/03-matchningsalgoritm.md (viktad L1-distans). Svar och resultat
  sparas i localStorage så att de kan ses igen senare.

Bildpolicy: se assets/KALLOR.md. Logotyper i fast 64x64-ruta
(object-fit:contain), porträtt i 64x64-cirkel (object-fit:cover),
onerror-fallback till platshållare.
"""
import json
import re
import sys

STORE_ANSWERS = 'vk_svar_v1'
STORE_RESULT = 'vk_resultat_v1'
MIN_ANSWERED = 15


def load_texts(path='docs/04-partiernas-program-2026-2030.md'):
    doc = open(path).read()
    texts = {}
    for m in re.finditer(r'## [^\n(]*\((\w+)\)\n(.*?)(?=\n## |\n---|\Z)', doc, re.S):
        pid, body = m.group(1), m.group(2)
        paras = [l.strip() for l in body.split('\n')
                 if l.strip() and not l.strip().startswith('<')]
        texts[pid] = ' '.join(paras)
    return texts


def md_to_html(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)


def luma_dark_text(color):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) > 150


def js_embed(obj):
    return json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


def logo_html(p):
    ph_fg = '#1a1a1a' if luma_dark_text(p['color']) else '#fff'
    fs = 30 if len(p['id']) == 1 else 22
    placeholder = (
        f'<svg class="ph" viewBox="0 0 64 64" role="img" aria-label="{p["name"]} symbol">'
        f'<circle cx="32" cy="32" r="30" fill="{p["color"]}"/>'
        f'<text x="32" y="33" text-anchor="middle" dominant-baseline="central" '
        f'font-family="Georgia,serif" font-weight="bold" font-size="{fs}" '
        f'fill="{ph_fg}">{p["id"]}</text></svg>')
    src = p.get('logoUrl') or p.get('logo')
    if src:
        return (f'<span class="logo-box">'
                f'<img src="{src}" alt="{p["name"]} logotyp" loading="lazy" '
                f'onerror="this.parentElement.classList.add(\'img-failed\')">'
                f'{placeholder}</span>')
    return f'<span class="logo-box no-media">{placeholder}</span>'


def leader_html(p, role):
    out = []
    for led in p['leaders']:
        initials = ''.join(w[0] for w in led['name'].split()[:2]).upper()
        placeholder = (
            f'<svg class="ph" viewBox="0 0 64 64" role="img" aria-label="{led["name"]}">'
            f'<circle cx="32" cy="32" r="30" fill="#e9e4dc"/>'
            f'<text x="32" y="35" text-anchor="middle" font-family="Georgia,serif" '
            f'font-weight="bold" font-size="22" fill="#6b6459">{initials}</text></svg>')
        out.append(
            f'<figure class="leader">'
            f'<span class="portrait" style="--pc:{p["color"]}">'
            f'<img src="{led["imageUrl"]}" alt="Porträtt: {led["name"]}" loading="lazy" '
            f'onerror="this.parentElement.classList.add(\'img-failed\')">'
            f'{placeholder}</span>'
            f'<figcaption><strong>{led["name"]}</strong><span>{role}</span></figcaption>'
            f'</figure>')
    return ''.join(out)


def card(p, texts):
    role = 'språkrör' if p['id'] == 'MP' else 'partiledare'
    return f'''<article class="party" id="{p['id'].lower()}" style="--pc:{p['color']}">
  <div class="party-head">
    {logo_html(p)}
    <div class="party-title">
      <h3>{p['name']}</h3>
      <p class="ideology">{' · '.join(p['ideology'])}</p>
    </div>
  </div>
  <div class="leaders">{leader_html(p, role)}</div>
  <p class="program">{md_to_html(texts[p['id']])}</p>
</article>'''


CSS = '''
:root {
  --paper:#FAF8F2; --ink:#20242B; --ink-2:#5C6068; --line:#E2DDD0;
  --card:#FFFFFF; --accent:#F5C400; --accent-ink:#8A6D00; --chip:#F3EFE4;
  --logo-plate:#FDFCF8; --go:#1B7A3D; --go-hover:#166332; --go-ink:#fff;
  --pro:#1B7A3D; --con:#A83232;
}
@media (prefers-color-scheme: dark) {
  :root { --paper:#151920; --ink:#E7E3D9; --ink-2:#9BA0A8; --line:#2C323C;
          --card:#1C222B; --accent:#F5C400; --accent-ink:#E5C34D; --chip:#242B36;
          --logo-plate:#EDEAE2; --go:#2E9E54; --go-hover:#37B662; --go-ink:#0d1310;
          --pro:#4CBB74; --con:#E07B7B; }
}
:root[data-theme="dark"] { --paper:#151920; --ink:#E7E3D9; --ink-2:#9BA0A8; --line:#2C323C;
          --card:#1C222B; --accent:#F5C400; --accent-ink:#E5C34D; --chip:#242B36;
          --logo-plate:#EDEAE2; --go:#2E9E54; --go-hover:#37B662; --go-ink:#0d1310;
          --pro:#4CBB74; --con:#E07B7B; }
:root[data-theme="light"] { --paper:#FAF8F2; --ink:#20242B; --ink-2:#5C6068; --line:#E2DDD0;
          --card:#FFFFFF; --accent:#F5C400; --accent-ink:#8A6D00; --chip:#F3EFE4;
          --logo-plate:#FDFCF8; --go:#1B7A3D; --go-hover:#166332; --go-ink:#fff;
          --pro:#1B7A3D; --con:#A83232; }
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink);
  font:16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; }
.wrap { max-width:52rem; margin:0 auto; padding:2.5rem 1.25rem 4rem; }
.eyebrow { font:600 .72rem/1 ui-monospace, "SF Mono", Consolas, monospace;
  letter-spacing:.14em; text-transform:uppercase; color:var(--accent-ink);
  border-bottom:3px solid var(--accent); display:inline-block; padding-bottom:.45rem; }
h1 { font-family:Georgia, "Times New Roman", serif; font-size:clamp(1.9rem, 4.5vw, 2.7rem);
  line-height:1.15; margin:.9rem 0 .5rem; text-wrap:balance; }
.lede { color:var(--ink-2); max-width:38rem; margin:0 0 1.8rem; }
.facts { display:flex; flex-wrap:wrap; gap:.6rem 2rem; border-block:1px solid var(--line);
  padding:.9rem 0; margin-bottom:2rem; }
.facts div { font:500 .8rem/1.5 ui-monospace, "SF Mono", Consolas, monospace; color:var(--ink-2); }
.facts strong { display:block; color:var(--ink); font-size:1.05rem; font-variant-numeric:tabular-nums; }
.notice { background:var(--chip); border:1px solid var(--line); border-radius:6px;
  padding:.9rem 1.1rem; font-size:.92rem; margin-bottom:2.6rem; }
.notice strong { color:var(--accent-ink); }
h2.bloc { font-family:Georgia, serif; font-size:1.35rem; margin:2.6rem 0 .3rem; }
p.bloc-sub { margin:0 0 1.2rem; color:var(--ink-2); font-size:.9rem; }
.party { background:var(--card); border:1px solid var(--line); border-radius:8px;
  padding:1.4rem 1.5rem 1.2rem; margin-bottom:1.1rem; border-top:4px solid var(--pc); }
.party-head { display:flex; align-items:center; gap:1rem; }
.party-head h3 { font-family:Georgia, serif; margin:0; font-size:1.3rem; }
.ideology { margin:.1rem 0 0; font:500 .72rem/1.4 ui-monospace, monospace;
  letter-spacing:.08em; text-transform:uppercase; color:var(--ink-2); }
.logo-box { width:64px; height:64px; flex:none; display:flex; align-items:center;
  justify-content:center; background:var(--logo-plate); border:1px solid var(--line);
  border-radius:12px; padding:7px; }
.logo-box img { max-width:100%; max-height:100%; object-fit:contain; display:block; }
.logo-box .ph { display:none; width:100%; height:100%; }
.logo-box.no-media { background:none; border:none; padding:0; }
.logo-box.no-media .ph { display:block; }
.logo-box.img-failed img { display:none; }
.logo-box.img-failed .ph { display:block; }
.leaders { display:flex; flex-wrap:wrap; gap:.75rem 1.75rem; margin:1rem 0 .4rem; }
.leader { display:flex; align-items:center; gap:.65rem; margin:0; }
.portrait { width:64px; height:64px; flex:none; border-radius:50%;
  border:3px solid var(--pc); overflow:hidden; display:block; background:#e9e4dc; }
.portrait img { width:100%; height:100%; object-fit:cover; display:block; }
.portrait .ph { display:none; width:100%; height:100%; }
.portrait.img-failed img { display:none; }
.portrait.img-failed .ph { display:block; }
.leader figcaption { font-size:.85rem; line-height:1.35; }
.leader figcaption span { display:block; color:var(--ink-2); font-size:.75rem; }
.program { margin:.6rem 0 0; font-size:.95rem; }
footer { margin-top:3rem; border-top:1px solid var(--line); padding-top:1.2rem;
  font-size:.8rem; color:var(--ink-2); }
footer a { color:var(--accent-ink); }

/* --- CTA & resultatkort (index) --- */
.cta-block { margin:0 0 2.4rem; }
.cta { display:inline-block; background:var(--go); color:var(--go-ink);
  font-size:1.25rem; font-weight:700; padding:1rem 2.6rem; border-radius:12px;
  text-decoration:none; box-shadow:0 2px 0 rgba(0,0,0,.18); }
.cta:hover { background:var(--go-hover); }
.cta:focus-visible { outline:3px solid var(--accent); outline-offset:2px; }
.cta-sub { display:block; margin-top:.55rem; font-size:.82rem; color:var(--ink-2); }
.result-card { background:var(--card); border:1px solid var(--line); border-left:5px solid var(--go);
  border-radius:8px; padding:1.2rem 1.4rem; margin:0 0 2.4rem; }
.result-card h2 { font-family:Georgia, serif; font-size:1.15rem; margin:0 0 .2rem; }
.result-card .meta { font-size:.78rem; color:var(--ink-2); margin:0 0 .9rem; }
.result-links { margin-top:.9rem; font-size:.88rem; display:flex; gap:1.4rem; flex-wrap:wrap; }
.result-links a { color:var(--accent-ink); }

/* --- resultatstaplar (delas av index & test) --- */
.score-row { display:grid; grid-template-columns:2.4rem 1fr 3.2rem; gap:.7rem;
  align-items:center; margin:.45rem 0; }
.score-row .pid { font:700 .8rem/1 ui-monospace, monospace; text-align:center;
  padding:.32rem 0; border-radius:6px; }
.score-bar { background:var(--chip); border-radius:5px; height:14px; overflow:hidden; }
.score-bar i { display:block; height:100%; border-radius:5px; }
.score-row .pct { font:600 .88rem/1 ui-monospace, monospace; text-align:right;
  font-variant-numeric:tabular-nums; }

/* --- testsidan --- */
.progress { background:var(--chip); border-radius:99px; height:10px; margin:.5rem 0 1.5rem;
  overflow:hidden; border:1px solid var(--line); }
.progress i { display:block; height:100%; background:linear-gradient(90deg, var(--go), var(--go-hover));
  border-radius:99px; min-width:10px; }
.qmeta { display:flex; justify-content:space-between; align-items:baseline; gap:1rem;
  font:600 .7rem/1.4 ui-monospace, monospace;
  letter-spacing:.07em; text-transform:uppercase; color:var(--ink-2); }
.qmeta span:last-child { color:var(--accent-ink); white-space:nowrap; overflow:hidden;
  text-overflow:ellipsis; max-width:55%; }
.qcard { background:var(--card); border:1px solid var(--line); border-radius:14px;
  padding:1.7rem 1.7rem 1.4rem; box-shadow:0 1px 2px rgba(30,30,20,.05), 0 6px 18px rgba(30,30,20,.05); }
.qtext { font-family:Georgia, serif; font-size:1.4rem; line-height:1.35; margin:.1rem 0 1.1rem;
  text-wrap:balance; }
details.info { margin:0 0 1.3rem; border:1px solid var(--line); border-radius:10px;
  background:var(--chip); font-size:.9rem; }
details.info summary { cursor:pointer; padding:.7rem .9rem; font-weight:600;
  color:var(--accent-ink); list-style:none; display:flex; align-items:center; gap:.6rem; }
details.info summary::-webkit-details-marker { display:none; }
.info-badge { flex:none; width:21px; height:21px; border-radius:50%; background:var(--accent-ink);
  color:var(--chip); font:italic 700 13px/21px Georgia, serif; text-align:center; }
details.info summary .chev { margin-left:auto; flex:none; color:var(--ink-2); font-size:.72rem; }
details.info[open] summary .chev { transform:rotate(180deg); }
details.info[open] summary { border-bottom:1px solid var(--line); }
details.info .info-body { padding:.85rem .95rem 1rem; }
details.info .info-body > p { margin:0 0 .85rem; }
.proscons { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.proscons h4 { margin:0 0 .35rem; font-size:.78rem; text-transform:uppercase; letter-spacing:.06em; }
.proscons .pro h4 { color:var(--pro); } .proscons .con h4 { color:var(--con); }
.proscons ul { margin:0; padding-left:1.1rem; }
.proscons li { margin:.28rem 0; }
.answers { display:grid; gap:.55rem; margin:0 0 1.2rem; }
.answers button { display:flex; align-items:center; gap:.75rem; text-align:left; font-size:1rem;
  padding:.75rem .95rem; border-radius:10px; min-height:3.1rem;
  border:1.5px solid var(--line); background:var(--paper); color:var(--ink); cursor:pointer; }
.answers button::before { content:''; flex:none; width:20px; height:20px; border-radius:50%;
  border:2px solid var(--line); background:var(--card); font:700 13px/17px sans-serif;
  text-align:center; color:var(--go); }
.answers button:hover { border-color:var(--go); }
.answers button:hover::before { border-color:var(--go); }
.answers button:active { transform:scale(.99); }
.answers button.sel { border-color:var(--go); background:var(--go); color:var(--go-ink); font-weight:600; }
.answers button.sel::before { content:'✓'; border-color:#fff; background:#fff; }
.answers button:focus-visible { outline:3px solid var(--accent); outline-offset:1px; }
.weight { margin-bottom:1.3rem; font-size:.85rem; color:var(--ink-2); }
.weight > span:first-child { display:block; margin-bottom:.45rem; }
.weight .seg { display:flex; border:1.5px solid var(--line); border-radius:10px; overflow:hidden; }
.weight .seg button { flex:1; border:0; background:var(--paper); color:var(--ink-2);
  padding:.55rem .4rem; font-size:.84rem; cursor:pointer; white-space:nowrap; }
.weight .seg button + button { border-left:1.5px solid var(--line); }
.weight .seg button.sel { background:var(--accent); color:#3a2f00; font-weight:700; }
.qnav { display:grid; grid-template-columns:1fr 1fr; gap:.6rem; align-items:center; }
.qnav button, .btn { font-size:.95rem; padding:.7rem 1rem; border-radius:10px; cursor:pointer;
  border:1.5px solid var(--line); background:var(--card); color:var(--ink); }
.qnav button:disabled { opacity:.35; cursor:default; }
.btn-go, .qnav button.btn-go { background-color:var(--go); border-color:var(--go); color:var(--go-ink); font-weight:700; }
.btn-go:hover, .qnav button.btn-go:hover { background-color:var(--go-hover); border-color:var(--go-hover); }
.skip { grid-column:1 / -1; justify-self:center; background:none; border:none; color:var(--ink-2);
  text-decoration:underline; text-underline-offset:3px; cursor:pointer; font-size:.85rem;
  padding:.5rem .8rem; }
.skip:hover { color:var(--ink); }
@media (prefers-reduced-motion: no-preference) {
  .progress i { transition:width .25s ease; }
  .answers button, .qnav button, .weight .seg button { transition:border-color .12s ease,
    transform .08s ease; }
  details.info summary .chev { transition:transform .18s ease; }
}
/* --- prioritering --- */
.prio-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(13rem, 1fr)); gap:.6rem;
  margin:1.4rem 0; text-align:left; }
.prio-grid button { display:flex; align-items:center; gap:.6rem; padding:.75rem .9rem;
  border:1.5px solid var(--line); border-radius:10px; background:var(--card); color:var(--ink);
  font-size:.95rem; cursor:pointer; text-align:left; }
.prio-grid button::before { content:''; flex:none; width:19px; height:19px; border-radius:6px;
  border:2px solid var(--line); background:var(--paper); font:700 12px/16px sans-serif;
  text-align:center; color:var(--go-ink); }
.prio-grid button:hover { border-color:var(--go); }
.prio-grid button.sel { border-color:var(--go); background:rgba(27,122,61,.08); font-weight:600; }
.prio-grid button.sel::before { content:'✓'; background:var(--go); border-color:var(--go); }
.prio-grid button:disabled { opacity:.45; cursor:default; }

/* --- resultat: expanderbara partirader & områden --- */
.party-result { margin:.45rem 0; }
button.prh { display:grid; grid-template-columns:2.4rem 1fr 3.2rem 1rem; gap:.7rem; width:100%;
  align-items:center; background:none; border:none; padding:.15rem 0; cursor:pointer;
  color:var(--ink); font:inherit; text-align:left; }
button.prh .caret { font-size:.7rem; color:var(--ink-2); }
button.prh[aria-expanded="true"] .caret { transform:rotate(180deg); }
.pr-detail { margin:.4rem 0 .9rem 3.1rem; font-size:.88rem; border-left:3px solid var(--line);
  padding-left:.9rem; }
.pr-detail p { margin:.3rem 0; }
.pr-detail .q-quote { color:var(--ink-2); font-style:italic; }
.dimsec { border:1px solid var(--line); border-radius:8px; margin:.5rem 0; background:var(--card); }
.dimsec summary { cursor:pointer; padding:.65rem .9rem; display:flex; flex-wrap:wrap;
  gap:.3rem .8rem; align-items:baseline; list-style:none; }
.dimsec summary::-webkit-details-marker { display:none; }
.dimsec summary .dimname { font-weight:600; }
.dimsec summary .dimtop { color:var(--accent-ink); font-size:.88rem; }
.dimsec summary .dimn { color:var(--ink-2); font-size:.75rem; margin-left:auto; }
.dimsec .dimbody { padding:.2rem .9rem .7rem; border-top:1px solid var(--line); }
.share-row { display:flex; gap:.7rem; flex-wrap:wrap; margin:1.2rem 0; }
.shared-note { background:var(--chip); border:1px solid var(--accent); border-radius:8px;
  padding:.7rem 1rem; font-size:.9rem; margin:.8rem 0; }

/* --- jämför partier --- */
.cmp-selects { display:flex; gap:.7rem; align-items:center; flex-wrap:wrap; margin:1rem 0; }
.cmp-selects select { font-size:.95rem; padding:.55rem .7rem; border-radius:8px;
  border:1.5px solid var(--line); background:var(--card); color:var(--ink); }
.cmp-sum { margin:.4rem 0 1.1rem; display:flex; gap:.5rem; flex-wrap:wrap; }
.cmp-item { border-bottom:1px solid var(--line); padding:.75rem 0; }
.cmp-item .rq { font-size:.92rem; font-weight:600; }
.cmp-item.diff-big { border-left:4px solid var(--con); padding-left:.7rem; }
.cmp-chips { display:flex; gap:.45rem; flex-wrap:wrap; margin-top:.4rem; }
.cmp-chip { font:600 .78rem/1.3 ui-monospace, monospace; padding:.35rem .6rem; border-radius:6px; }
.cmp-chip.du { background:none; border:1.5px dashed var(--go); color:var(--ink); }

/* --- mobilfinput --- */
@media (max-width:600px) {
  .wrap { padding:1.3rem .85rem 3rem; }
  .qcard { padding:1.15rem 1rem 1rem; border-radius:12px; }
  .qtext { font-size:1.2rem; }
  .answers button { min-height:3rem; padding:.65rem .8rem; }
  .proscons { grid-template-columns:1fr; }
  .cta { display:block; text-align:center; }
  h1 { font-size:1.75rem; }
}
.warn { background:var(--chip); border:1px solid var(--accent); border-radius:8px;
  padding:.8rem 1rem; font-size:.9rem; margin:1rem 0; }
.qtools { display:flex; justify-content:flex-end; gap:.4rem; margin:-.7rem 0 .7rem; }
.qtools button { background:none; border:none; cursor:pointer; font-size:.8rem;
  color:var(--ink-2); text-decoration:underline; text-underline-offset:3px; padding:.3rem .5rem; }
.qtools button:hover { color:var(--ink); }
.qtools button:disabled { opacity:.35; cursor:default; text-decoration:none; }
.rev-summary { display:flex; flex-wrap:wrap; gap:.5rem; margin:.6rem 0 .9rem; }
.chip { display:inline-flex; align-items:center; gap:.35rem; font:600 .75rem/1 ui-monospace, monospace;
  padding:.38rem .7rem; border-radius:99px; border:1.5px solid var(--line); color:var(--ink-2);
  white-space:nowrap; }
.chip-ok { border-color:var(--pro); color:var(--pro); }
.chip-skip { border-color:var(--accent-ink); color:var(--accent-ink); }
.chip-none { border-color:var(--con); color:var(--con); }
.review-item { border-bottom:1px solid var(--line); padding:.9rem 0 .9rem .9rem;
  border-left:4px solid var(--line); margin-bottom:.15rem; }
.review-item.st-answered { border-left-color:var(--pro); }
.review-item.st-skipped { border-left-color:var(--accent); }
.review-item.st-missing { border-left-color:var(--con); background:var(--chip); border-radius:0 8px 8px 0; }
.review-item .rq { font-weight:600; }
.review-item .ra { font-size:.9rem; margin:.35rem 0 .3rem; display:flex; flex-wrap:wrap;
  gap:.4rem .8rem; align-items:center; }
.review-item .ra b { color:var(--accent-ink); }
.review-item .jump { background:none; border:none; cursor:pointer; font-size:.85rem;
  color:var(--accent-ink); text-decoration:underline; text-underline-offset:3px; padding:0; }
.spectrum { display:grid; grid-template-columns:repeat(5, 1fr); gap:4px; margin:.55rem 0 .15rem; }
.spec-col { min-height:2.1rem; border:1.5px dashed var(--line); border-radius:7px; padding:3px;
  display:flex; flex-wrap:wrap; gap:3px; align-content:flex-start; justify-content:center; }
.spec-col.me { border:2px solid var(--go); border-radius:7px; background:rgba(27,122,61,.07); }
.pmini { font:700 10px/1 ui-monospace, monospace; padding:4px 5px; border-radius:5px; }
.pmini.du { background:var(--go); color:var(--go-ink); }
.spec-axis { display:flex; justify-content:space-between; font:500 .68rem/1.3 ui-monospace, monospace;
  letter-spacing:.04em; text-transform:uppercase; color:var(--ink-2); margin-bottom:.55rem; }
.hidden { display:none !important; }
.startbox { text-align:center; padding:2.5rem 1rem; }
.startbox .cta { margin-top:1rem; border:none; cursor:pointer; }
.startbox p.small, p.small { font-size:.83rem; color:var(--ink-2); }
.startrow { display:flex; gap:.8rem; justify-content:center; flex-wrap:wrap; margin-top:1rem; }
'''


def build_index(parties_by_id, texts):
    rodgrona, tido = ['S', 'V', 'MP', 'C'], ['M', 'SD', 'KD', 'L']
    return f'''<style>{CSS}</style>
<div class="wrap">
<header>
  <span class="eyebrow">Valkompassen · Riksdagsvalet 2026</span>
  <h1>Hitta partiet som tycker som du</h1>
  <p class="lede">Valkompassen matchar dina åsikter mot de åtta riksdagspartierna
  inför valet den 13 september 2026 — över åtta politiska dimensioner, med
  förklaringar till varje fråga. Nedan hittar du också en sammanställning av
  vad varje parti står för och vill åstadkomma 2026–2030.</p>
  <div class="cta-block">
    <a class="cta" href="test.html">Gör testet</a>
    <span class="cta-sub">32 frågor · cirka 8 minuter · svaren sparas bara i din webbläsare</span>
  </div>
  <section id="mitt-resultat" class="result-card hidden" aria-label="Ditt sparade resultat">
    <h2>Ditt resultat</h2>
    <p class="meta" id="res-meta"></p>
    <div id="res-list"></div>
    <div class="result-links">
      <a href="test.html#resultat">Se hela resultatet</a>
      <a href="test.html#svar">Se dina svar</a>
      <a href="test.html#jamfor">Jämför partier</a>
      <a href="test.html#om">Gör om testet</a>
    </div>
  </section>
  <div class="facts">
    <div>Valdag<strong>13 sep 2026</strong></div>
    <div>Riksdagspartier<strong>8</strong></div>
    <div>Mandat<strong>349</strong></div>
    <div>Riksdagsspärr<strong>4&nbsp;%</strong></div>
  </div>
  <div class="notice"><strong>Sverigelöftet (mars 2026):</strong> SD:s och L:s avtal om fortsatt
  samarbete — alla fyra Tidöpartier ska ingå i regeringen vid valseger, en euro-utredning
  genomförs och en folkomröstning om euron hålls på valdagen 2030.</div>
</header>

<h2 class="bloc">De rödgröna</h2>
<p class="bloc-sub">Socialdemokraterna, Vänsterpartiet, Miljöpartiet — samt Centerpartiet, som samarbetar åt det rödgröna hållet men definierar sig som liberalt mittenparti.</p>
{''.join(card(parties_by_id[pid], texts) for pid in rodgrona)}

<h2 class="bloc">Tidöpartierna</h2>
<p class="bloc-sub">Moderaterna, Sverigedemokraterna, Kristdemokraterna och Liberalerna — regeringsunderlaget sedan 2022, med ambition att regera i fyrpartiregering efter valet.</p>
{''.join(card(parties_by_id[pid], texts) for pid in tido)}

<footer>
  <p>Partiledarfoton och fritt licensierade partisymboler:
  <a href="https://commons.wikimedia.org">Wikimedia Commons</a> (CC-licenser, källor per bild i
  <a href="https://github.com/gbgeka/Valkompassen/blob/claude/swedish-voter-compass-42d6l8/assets/KALLOR.md">assets/KALLOR.md</a>).
  S, SD och MP visas med egenritade stiliserade symboler (ros, maskros och blåsippa) eftersom
  de officiella logotyperna inte är fritt licensierade. Texterna bygger på nyhetsrapportering och partiernas
  utspel t.o.m. juli 2026. Del av projektet
  <a href="https://github.com/gbgeka/Valkompassen">Valkompassen</a>.</p>
</footer>
</div>
<script>
(function () {{
  var raw = localStorage.getItem('{STORE_RESULT}');
  if (!raw) return;
  var res; try {{ res = JSON.parse(raw); }} catch (e) {{ return; }}
  if (!res || !res.scores || !res.scores.length) return;
  document.getElementById('mitt-resultat').classList.remove('hidden');
  document.getElementById('res-meta').textContent =
    'Gjort ' + res.date + ' · ' + res.answered + ' av ' + res.total + ' frågor besvarade';
  var list = document.getElementById('res-list');
  res.scores.slice(0, 3).forEach(function (s) {{
    var row = document.createElement('div'); row.className = 'score-row';
    var dark = ['#DDDD00', '#52BDEC'].indexOf(s.color) >= 0;
    row.innerHTML = '<span class="pid" style="background:' + s.color + ';color:' +
      (dark ? '#1a1a1a' : '#fff') + '">' + s.id + '</span>' +
      '<span class="score-bar"><i style="width:' + s.pct + '%;background:' + s.color + '"></i></span>' +
      '<span class="pct">' + s.pct + ' %</span>';
    list.appendChild(row);
  }});
}})();
</script>'''


def build_test(parties, questions, dimensions):
    dim_names = {d['id']: d['name'] for d in dimensions}
    parties_js = js_embed([{'id': p['id'], 'name': p['name'], 'color': p['color']}
                           for p in parties])
    dims_js = js_embed([{'id': d['id'], 'name': d['name']} for d in dimensions])
    questions_js = js_embed([{
        'id': q['id'], 'dim': q['dimension'], 'dimension': dim_names[q['dimension']],
        'text': q['text'], 'info': q['info'], 'partyPositions': q['partyPositions']}
        for q in questions])

    return f'''<style>{CSS}</style>
<div class="wrap">
<header>
  <span class="eyebrow"><a href="index.html" style="color:inherit;text-decoration:none">← Valkompassen</a> · Testet</span>
</header>

<section id="v-start" class="startbox hidden">
  <h1>Välkommen tillbaka</h1>
  <p class="lede" style="margin-inline:auto">Dina tidigare svar finns sparade lokalt i din webbläsare.
  Fortsätt där du var, titta på resultatet eller börja om från början.</p>
  <div id="start-buttons"></div>
</section>

<section id="v-prio" class="hidden">
  <h1>Vad är viktigast för dig?</h1>
  <p class="lede">Välj upp till tre samhällsområden som väger tyngst när du röstar —
  frågor inom dem får större inverkan på matchningen. Sedan väntar 32 påståenden (cirka 8 minuter)
  med svar på en femgradig skala. Markera gärna extra viktiga frågor, och tryck på infoknappen
  när du vill förstå en fråga bättre — med för- och nackdelar för varje ståndpunkt.</p>
  <p class="small">Dina svar sparas bara lokalt i din webbläsare — inget skickas någonstans.
  Du kan när som helst komma tillbaka, se dina svar och ändra dem.</p>
  <div class="prio-grid" id="prio-grid"></div>
  <div class="startrow">
    <button class="cta" id="prio-done" type="button" style="border:none;cursor:pointer">Starta frågorna</button>
  </div>
  <div class="startrow">
    <button class="skip" id="prio-skip" type="button">Hoppa över — vikta alla områden lika</button>
  </div>
</section>

<section id="v-quiz" class="hidden">
  <div class="qmeta"><span id="q-step"></span><span id="q-dim"></span></div>
  <div class="progress"><i id="q-bar" style="width:0%"></i></div>
  <div class="qtools">
    <button id="q-undo" type="button" disabled>↶ Ångra senaste</button>
    <button id="q-reset" type="button">Nollställ testet</button>
  </div>
  <div class="qcard">
    <p class="qtext" id="q-text"></p>
    <details class="info" id="q-info">
      <summary><span class="info-badge">i</span>Om frågan — för- och nackdelar<span class="chev">▼</span></summary>
      <div class="info-body">
        <p id="q-expl"></p>
        <div class="proscons">
          <div class="pro"><h4>Skäl för</h4><ul id="q-pros"></ul></div>
          <div class="con"><h4>Skäl emot</h4><ul id="q-cons"></ul></div>
        </div>
      </div>
    </details>
    <div class="answers" id="q-answers" role="group" aria-label="Svarsalternativ"></div>
    <div class="weight">
      <span>Hur viktig är frågan för dig?</span>
      <span class="seg" id="q-weight"></span>
    </div>
    <div class="qnav">
      <button id="q-prev" type="button">← Föregående</button>
      <button id="q-next" type="button">Nästa →</button>
      <button class="skip" id="q-skip" type="button">Hoppa över frågan</button>
    </div>
  </div>
</section>

<section id="v-result" class="hidden">
  <h1 id="r-title">Ditt resultat</h1>
  <p class="small" id="r-meta"></p>
  <div id="r-shared-note"></div>
  <div id="r-warn"></div>
  <div id="r-list"></div>
  <p class="small" id="r-hint"></p>
  <div class="share-row" id="r-share-row">
    <button class="btn" id="r-share" type="button">Kopiera resultatlänk</button>
    <button class="btn" id="r-compare" type="button">Jämför två partier</button>
  </div>
  <div id="r-dims-wrap">
    <h2 class="bloc" style="margin-top:1.8rem">Så matchar du per område</h2>
    <div id="r-dims"></div>
  </div>
  <p class="small">Matchningen bygger på viktad överensstämmelse fråga för fråga
  (se <a href="https://github.com/gbgeka/Valkompassen/blob/claude/swedish-voter-compass-42d6l8/docs/03-matchningsalgoritm.md">metodiken</a>).
  Partipositionerna är redaktionella utkast som verifieras mot valmanifest och partisvar före skarp lansering.</p>
  <div class="startrow" id="r-own-actions">
    <button class="btn" id="r-review" type="button">Se dina svar</button>
    <button class="btn" id="r-redo" type="button">Gör om testet</button>
    <a class="btn" href="index.html" style="text-decoration:none">Till startsidan</a>
  </div>
</section>

<section id="v-compare" class="hidden">
  <h1>Jämför två partier</h1>
  <p class="small">Fråga för fråga, sida vid sida. Rader med stor åsiktsskillnad (minst två steg) markeras.
  Ditt eget svar visas när det finns.</p>
  <div class="cmp-selects">
    <select id="cmp-a" aria-label="Parti A"></select>
    <span>mot</span>
    <select id="cmp-b" aria-label="Parti B"></select>
  </div>
  <div class="cmp-sum" id="cmp-sum"></div>
  <div id="cmp-list"></div>
  <div class="startrow">
    <button class="btn" id="cmp-back" type="button">← Tillbaka</button>
    <a class="btn" href="index.html" style="text-decoration:none">Till startsidan</a>
  </div>
</section>

<section id="v-review" class="hidden">
  <h1>Dina svar</h1>
  <p class="small">Sparade lokalt i din webbläsare. Öppna infoknappen för att läsa om frågan igen,
  eller tryck på Ändra/Svara för att hoppa till frågan.</p>
  <div id="rev-summary" class="rev-summary"></div>
  <div id="rev-actions" class="startrow" style="justify-content:flex-start"></div>
  <div id="rev-list"></div>
  <div class="startrow">
    <button class="btn" id="rev-back" type="button">← Tillbaka</button>
    <a class="btn" href="index.html" style="text-decoration:none">Till startsidan</a>
  </div>
</section>

<footer><p>Inga kakor, ingen spårning — svaren lagras enbart i din egen webbläsare
och försvinner om du rensar webbplatsdata. Del av projektet
<a href="https://github.com/gbgeka/Valkompassen">Valkompassen</a>.</p></footer>
</div>

<script>
var PARTIES = {parties_js};
var QUESTIONS = {questions_js};
var DIMS = {dims_js};
var LABELS = [[-2, 'Tar helt avstånd'], [-1, 'Tar delvis avstånd'], [0, 'Neutral / vet ej'],
              [1, 'Instämmer delvis'], [2, 'Instämmer helt']];
var WEIGHTS = [[0.5, 'Mindre viktig'], [1, 'Normal'], [2, 'Extra viktig']];
var KEY_A = '{STORE_ANSWERS}', KEY_R = '{STORE_RESULT}', MIN = {MIN_ANSWERED};
var KEY_P = 'vk_prio_v1', KEY_O = 'vk_ordning_v1';
var PRIO_BOOST = 1.5;
var DARKTEXT = ['#DDDD00', '#52BDEC'];
var PBYID = {{}};
PARTIES.forEach(function (p) {{ PBYID[p.id] = p; }});
var QBYID = {{}};
QUESTIONS.forEach(function (q) {{ QBYID[q.id] = q; }});

var answers = load(KEY_A) || {{}};
var idx = 0;
var hist = [];  // ångra-stack (per session): {{qid, idx, prev}}

/* slumpad frågeordning inom varje område; sparas så numrering är stabil */
function ensureOrder() {{
  var o = load(KEY_O);
  if (o && o.length === QUESTIONS.length) return o;
  o = [];
  DIMS.forEach(function (d) {{
    var g = QUESTIONS.filter(function (q) {{ return q.dim === d.id; }}).map(function (q) {{ return q.id; }});
    for (var i = g.length - 1; i > 0; i--) {{
      var j = Math.floor(Math.random() * (i + 1));
      var t = g[i]; g[i] = g[j]; g[j] = t;
    }}
    o = o.concat(g);
  }});
  save(KEY_O, o);
  return o;
}}
var ORDER = ensureOrder();
function getQ(i) {{ return QBYID[ORDER[i]]; }}
function prio() {{ return load(KEY_P) || []; }}

function load(k) {{ try {{ return JSON.parse(localStorage.getItem(k)); }} catch (e) {{ return null; }} }}
function save(k, v) {{ localStorage.setItem(k, JSON.stringify(v)); }}
function el(id) {{ return document.getElementById(id); }}
function answeredCount() {{
  return QUESTIONS.filter(function (q) {{
    var a = answers[q.id]; return a && a.v !== null && a.v !== undefined;
  }}).length;
}}
function touchedCount() {{ return Object.keys(answers).length; }}

function show(view) {{
  ['v-start', 'v-prio', 'v-quiz', 'v-result', 'v-review', 'v-compare'].forEach(function (v) {{
    el(v).classList.toggle('hidden', v !== view);
  }});
  window.scrollTo(0, 0);
}}

/* ---- matchning: viktad L1 enligt docs/03, med områdesprioritering ---- */
function effWeight(q, a) {{
  var w = a.w || 1;
  if (prio().indexOf(q.dim) >= 0) w *= PRIO_BOOST;
  return w;
}}
function computeScores(dimId) {{
  var rows = PARTIES.map(function (p) {{
    var num = 0, den = 0, n = 0;
    QUESTIONS.forEach(function (q) {{
      if (dimId && q.dim !== dimId) return;
      var a = answers[q.id];
      if (!a || a.v === null || a.v === undefined) return;
      var w = effWeight(q, a);
      num += w * Math.abs(a.v - q.partyPositions[p.id]);
      den += w * 4;
      n++;
    }});
    return {{ id: p.id, name: p.name, color: p.color, n: n,
             pct: den ? Math.round(100 * (1 - num / den)) : 0 }};
  }});
  rows.sort(function (a, b) {{ return b.pct - a.pct; }});
  return rows;
}}
/* överensstämmelse per parti: samma svar / nära / störst samsyn & skillnad */
function agreeStats(pid) {{
  var same = 0, near = 0, n = 0, best = null, worst = null;
  QUESTIONS.forEach(function (q) {{
    var a = answers[q.id];
    if (!a || a.v === null || a.v === undefined) return;
    n++;
    var pv = q.partyPositions[pid];
    var d = Math.abs(a.v - pv);
    if (d === 0) {{
      same++;
      if (!best || Math.abs(a.v) > Math.abs(best.v)) best = {{ q: q, v: a.v }};
    }} else if (d === 1) near++;
    if (!worst || d > worst.d) worst = {{ q: q, d: d, u: a.v, pv: pv }};
  }});
  return {{ same: same, near: near, n: n, best: best, worst: worst }};
}}

/* ---- startvy: visas bara för återvändande besökare med sparade svar ---- */
function renderStart() {{
  var box = el('start-buttons'); box.innerHTML = '';
  var res = load(KEY_R);
  var touched = touchedCount();
  function btn(txt, cls, fn) {{
    var b = document.createElement('button'); b.type = 'button';
    b.className = cls; b.textContent = txt; b.addEventListener('click', fn); return b;
  }}
  var row = document.createElement('div'); row.className = 'startrow';
  if (touched < QUESTIONS.length) {{
    row.appendChild(btn('Fortsätt (' + touched + ' av ' + QUESTIONS.length + ')', 'cta', function () {{
      idx = firstUnanswered(); show('v-quiz'); renderQ();
    }}));
  }}
  if (res) row.appendChild(btn('Se resultat', 'btn', function () {{ renderResult(false); }}));
  row.appendChild(btn('Se dina svar', 'btn', function () {{ renderReview(); }}));
  row.appendChild(btn('Nollställ testet', 'btn', function () {{ restart(false); }}));
  box.appendChild(row);
  show('v-start');
}}
function firstUnanswered() {{
  for (var i = 0; i < ORDER.length; i++) if (!(ORDER[i] in answers)) return i;
  return 0;
}}
function restart(force) {{
  if (!force && touchedCount() > 0 &&
      !confirm('Detta nollställer testet: alla dina svar och ditt resultat raderas. Vill du fortsätta?')) return;
  localStorage.removeItem(KEY_A); localStorage.removeItem(KEY_R);
  localStorage.removeItem(KEY_P); localStorage.removeItem(KEY_O);
  answers = {{}}; hist = []; idx = 0;
  ORDER = ensureOrder();
  renderPrio();
}}

/* ---- prioritering: första steget för nya besökare ---- */
function renderPrio() {{
  var grid = el('prio-grid'); grid.innerHTML = '';
  var sel = prio().slice();
  DIMS.forEach(function (d) {{
    var b = document.createElement('button'); b.type = 'button';
    b.textContent = d.name;
    function refresh() {{
      b.classList.toggle('sel', sel.indexOf(d.id) >= 0);
      b.disabled = sel.length >= 3 && sel.indexOf(d.id) < 0;
    }}
    b.addEventListener('click', function () {{
      var i = sel.indexOf(d.id);
      if (i >= 0) sel.splice(i, 1); else if (sel.length < 3) sel.push(d.id);
      grid.querySelectorAll('button').forEach(function (btn2, k) {{
        btn2.classList.toggle('sel', sel.indexOf(DIMS[k].id) >= 0);
        btn2.disabled = sel.length >= 3 && sel.indexOf(DIMS[k].id) < 0;
      }});
    }});
    refresh();
    grid.appendChild(b);
  }});
  el('prio-done').onclick = function () {{ save(KEY_P, sel); startQuiz(); }};
  el('prio-skip').onclick = function () {{ save(KEY_P, []); startQuiz(); }};
  show('v-prio');
}}
function startQuiz() {{ idx = firstUnanswered(); show('v-quiz'); renderQ(); }}

/* ---- ångra ---- */
function snapshot(qid) {{
  return answers[qid] ? JSON.parse(JSON.stringify(answers[qid])) : null;
}}
function pushHist(qid) {{
  hist.push({{ qid: qid, idx: idx, prev: snapshot(qid) }});
  if (hist.length > 200) hist.shift();
}}
function undo() {{
  var h = hist.pop();
  if (!h) return;
  if (h.prev) answers[h.qid] = h.prev; else delete answers[h.qid];
  save(KEY_A, answers);
  idx = h.idx;
  show('v-quiz'); renderQ();
}}
el('q-undo').addEventListener('click', undo);
el('q-reset').addEventListener('click', function () {{ restart(false); }});

/* ---- frågevy ---- */
function renderQ() {{
  var q = getQ(idx);
  var a = answers[q.id] || {{}};
  el('q-step').textContent = 'Fråga ' + (idx + 1) + ' av ' + QUESTIONS.length;
  el('q-dim').textContent = q.dimension;
  el('q-bar').style.width = Math.round(100 * idx / QUESTIONS.length) + '%';
  el('q-text').textContent = q.text;
  el('q-info').removeAttribute('open');
  el('q-expl').textContent = q.info.explanation;
  ['pros', 'cons'].forEach(function (kind) {{
    var ul = el('q-' + kind); ul.innerHTML = '';
    q.info[kind].forEach(function (t) {{
      var li = document.createElement('li'); li.textContent = t; ul.appendChild(li);
    }});
  }});
  var ans = el('q-answers'); ans.innerHTML = '';
  LABELS.forEach(function (pair) {{
    var b = document.createElement('button'); b.type = 'button';
    b.textContent = pair[1];
    if (a.v === pair[0]) b.className = 'sel';
    b.addEventListener('click', function () {{ pick(pair[0]); }});
    ans.appendChild(b);
  }});
  var seg = el('q-weight'); seg.innerHTML = '';
  var w = a.w || 1;
  WEIGHTS.forEach(function (pair) {{
    var b = document.createElement('button'); b.type = 'button';
    b.textContent = pair[1];
    if (w === pair[0]) b.className = 'sel';
    b.addEventListener('click', function () {{
      pushHist(q.id);
      var cur = answers[q.id] || {{}}; cur.w = pair[0]; answers[q.id] = cur;
      save(KEY_A, answers); renderQ();
    }});
    seg.appendChild(b);
  }});
  el('q-prev').disabled = idx === 0;
  el('q-next').textContent = (idx === QUESTIONS.length - 1) ? 'Visa resultat' : 'Nästa →';
  el('q-next').classList.toggle('btn-go', q.id in answers);
  el('q-next').disabled = !(q.id in answers);
  el('q-undo').disabled = hist.length === 0;
}}
function pick(v) {{
  var q = getQ(idx);
  pushHist(q.id);
  var cur = answers[q.id] || {{}};
  cur.v = v; if (!cur.w) cur.w = 1;
  answers[q.id] = cur; save(KEY_A, answers);
  renderQ();
}}
function next() {{
  if (idx < QUESTIONS.length - 1) {{ idx++; renderQ(); }}
  else renderResult(true);
}}
el('q-prev').addEventListener('click', function () {{ if (idx > 0) {{ idx--; renderQ(); }} }});
el('q-next').addEventListener('click', next);
el('q-skip').addEventListener('click', function () {{
  var q = getQ(idx);
  pushHist(q.id);
  answers[q.id] = {{ v: null, w: answers[q.id] && answers[q.id].w || 1 }};
  save(KEY_A, answers); next();
}});

/* ---- resultatvy ---- */
function fgFor(color) {{ return DARKTEXT.indexOf(color) >= 0 ? '#1a1a1a' : '#fff'; }}
function scoreRowHtml(s) {{
  return '<span class="pid" style="background:' + s.color + ';color:' + fgFor(s.color) + '">' + s.id + '</span>' +
    '<span class="score-bar"><i style="width:' + s.pct + '%;background:' + s.color + '"></i></span>' +
    '<span class="pct">' + s.pct + ' %</span>';
}}
function partyDetailHtml(s) {{
  var st = agreeStats(s.id);
  var html = '<p><strong>Samma svar i ' + st.same + ' av ' + st.n + '</strong> besvarade frågor, ' +
    'ett steg ifrån i ' + st.near + '.</p>';
  if (st.best) {{
    html += '<p>Störst samsyn: <span class="q-quote">”' + st.best.q.text + '”</span> — ni svarar båda <b>' +
      labelFor(st.best.v).toLowerCase() + '</b>.</p>';
  }}
  if (st.worst && st.worst.d >= 2) {{
    html += '<p>Störst skillnad: <span class="q-quote">”' + st.worst.q.text + '”</span> — du: <b>' +
      labelFor(st.worst.u).toLowerCase() + '</b>, ' + s.id + ': <b>' + labelFor(st.worst.pv).toLowerCase() + '</b>.</p>';
  }}
  return html;
}}
function renderDims() {{
  var wrap = el('r-dims'); wrap.innerHTML = '';
  DIMS.forEach(function (d) {{
    var rows = computeScores(d.id);
    var nAns = rows[0] ? rows[0].n : 0;
    var det = document.createElement('details'); det.className = 'dimsec';
    var starred = prio().indexOf(d.id) >= 0 ? ' ★' : '';
    if (nAns === 0) {{
      det.innerHTML = '<summary><span class="dimname">' + d.name + starred +
        '</span><span class="dimn">inga besvarade frågor</span></summary>';
      wrap.appendChild(det);
      return;
    }}
    var top = rows.slice(0, 3).map(function (s) {{ return s.id + ' ' + s.pct + ' %'; }}).join(' · ');
    det.innerHTML = '<summary><span class="dimname">' + d.name + starred + '</span>' +
      '<span class="dimtop">' + top + '</span>' +
      '<span class="dimn">' + nAns + ' av 4 frågor</span></summary>';
    var body = document.createElement('div'); body.className = 'dimbody';
    rows.forEach(function (s) {{
      var row = document.createElement('div'); row.className = 'score-row';
      row.innerHTML = scoreRowHtml(s);
      body.appendChild(row);
    }});
    det.appendChild(body);
    wrap.appendChild(det);
  }});
}}
function encodeShare(res) {{
  var payload = {{ d: res.date, a: res.answered, t: res.total,
                  s: res.scores.map(function (x) {{ return [x.id, x.pct]; }}) }};
  return btoa(unescape(encodeURIComponent(JSON.stringify(payload))))
    .replace(/\\+/g, '-').replace(/\\//g, '_').replace(/=+$/, '');
}}
function decodeShare(str) {{
  try {{
    var json = decodeURIComponent(escape(atob(str.replace(/-/g, '+').replace(/_/g, '/'))));
    var p = JSON.parse(json);
    return {{ date: p.d, answered: p.a, total: p.t,
             scores: p.s.map(function (x) {{
               var party = PBYID[x[0]] || {{ name: x[0], color: '#888' }};
               return {{ id: x[0], name: party.name, color: party.color, pct: x[1] }};
             }}) }};
  }} catch (e) {{ return null; }}
}}
function renderResult(saveIt, shared) {{
  el('r-shared-note').innerHTML = '';
  el('r-warn').innerHTML = '';
  var scores, n, total;

  if (shared) {{
    el('r-title').textContent = 'Delat resultat';
    el('r-meta').textContent = 'Gjort ' + shared.date + ' · ' + shared.answered + ' av ' +
      shared.total + ' frågor besvarade.';
    el('r-shared-note').innerHTML = '<div class="shared-note">Det här är någon annans resultat, ' +
      'delat via länk. <a href="test.html">Gör testet själv</a> så får du ditt eget.</div>';
    el('r-own-actions').classList.add('hidden');
    el('r-share-row').classList.add('hidden');
    el('r-dims-wrap').classList.add('hidden');
    el('r-hint').textContent = '';
    scores = shared.scores;
  }} else {{
    el('r-title').textContent = 'Ditt resultat';
    el('r-own-actions').classList.remove('hidden');
    el('r-share-row').classList.remove('hidden');
    el('r-dims-wrap').classList.remove('hidden');
    n = answeredCount(); total = QUESTIONS.length;
    if (n < MIN) {{
      el('r-warn').innerHTML = '<div class="warn">Du har besvarat ' + n + ' frågor. Det behövs minst ' +
        MIN + ' för ett pålitligt resultat — <a href="#" id="warn-more">svara på fler frågor</a>.</div>';
      el('r-list').innerHTML = ''; el('r-meta').textContent = '';
      el('r-dims').innerHTML = ''; el('r-hint').textContent = '';
      el('r-share-row').classList.add('hidden');
      show('v-result');
      el('warn-more').addEventListener('click', function (ev) {{
        ev.preventDefault(); idx = firstUnanswered(); show('v-quiz'); renderQ();
      }});
      return;
    }}
    scores = computeScores();
    if (saveIt) {{
      save(KEY_R, {{ date: new Date().toISOString().slice(0, 10), answered: n,
                    total: total, scores: scores }});
    }}
    var pnames = prio().map(function (id) {{
      var d = DIMS.filter(function (x) {{ return x.id === id; }})[0];
      return d ? d.name : id;
    }});
    el('r-meta').textContent = n + ' av ' + total + ' frågor besvarade. ' +
      'Högre procent = större samsyn med partiet i dina viktade svar.' +
      (pnames.length ? ' Prioriterade områden (★): ' + pnames.join(', ') + '.' : '');
    el('r-hint').textContent = 'Tryck på en partirad för detaljer: hur många frågor ni svarar lika på, och var ni skiljer er mest.';
  }}

  var list = el('r-list'); list.innerHTML = '';
  scores.forEach(function (s) {{
    if (shared) {{
      var row = document.createElement('div'); row.className = 'score-row';
      row.innerHTML = scoreRowHtml(s);
      list.appendChild(row);
      return;
    }}
    var box = document.createElement('div'); box.className = 'party-result';
    var head = document.createElement('button');
    head.type = 'button'; head.className = 'prh'; head.setAttribute('aria-expanded', 'false');
    head.innerHTML = scoreRowHtml(s) + '<span class="caret">▼</span>';
    var detail = document.createElement('div'); detail.className = 'pr-detail hidden';
    head.addEventListener('click', function () {{
      var nowHidden = detail.classList.toggle('hidden');
      head.setAttribute('aria-expanded', String(!nowHidden));
      if (!nowHidden && !detail.innerHTML) detail.innerHTML = partyDetailHtml(s);
    }});
    box.appendChild(head); box.appendChild(detail);
    list.appendChild(box);
  }});

  if (!shared) renderDims();
  show('v-result');
}}

/* ---- dela resultat ---- */
el('r-share').addEventListener('click', function () {{
  var res = load(KEY_R);
  if (!res) return;
  var url = location.origin + location.pathname + '#r=' + encodeShare(res);
  var btn = el('r-share');
  function done() {{
    btn.textContent = 'Länk kopierad ✓';
    setTimeout(function () {{ btn.textContent = 'Kopiera resultatlänk'; }}, 2500);
  }}
  if (navigator.share) {{
    navigator.share({{ title: 'Mitt valkompassresultat', url: url }}).catch(function () {{}});
  }} else if (navigator.clipboard && navigator.clipboard.writeText) {{
    navigator.clipboard.writeText(url).then(done);
  }} else {{
    window.prompt('Kopiera länken:', url);
  }}
}});
el('r-compare').addEventListener('click', function () {{ renderCompare(null, null); }});

/* ---- jämför två partier ---- */
function fillCompareSelect(sel, chosen) {{
  sel.innerHTML = '';
  PARTIES.forEach(function (p) {{
    var o = document.createElement('option');
    o.value = p.id; o.textContent = p.name;
    if (p.id === chosen) o.selected = true;
    sel.appendChild(o);
  }});
}}
function renderCompare(aId, bId) {{
  var res = load(KEY_R);
  if (!aId || !bId) {{
    if (res && res.scores.length >= 2) {{ aId = res.scores[0].id; bId = res.scores[1].id; }}
    else {{ aId = 'S'; bId = 'M'; }}
  }}
  fillCompareSelect(el('cmp-a'), aId);
  fillCompareSelect(el('cmp-b'), bId);
  el('cmp-a').onchange = el('cmp-b').onchange = function () {{
    renderCompare(el('cmp-a').value, el('cmp-b').value);
  }};
  var A = PBYID[aId], B = PBYID[bId];
  var same = 0, near = 0;
  var list = el('cmp-list'); list.innerHTML = '';
  QUESTIONS.forEach(function (q) {{
    var av = q.partyPositions[aId], bv = q.partyPositions[bId];
    var d = Math.abs(av - bv);
    if (d === 0) same++; else if (d === 1) near++;
    var item = document.createElement('div');
    item.className = 'cmp-item' + (d >= 2 ? ' diff-big' : '');
    var chips = '<span class="cmp-chip" style="background:' + A.color + ';color:' + fgFor(A.color) + '">' +
      aId + ': ' + labelFor(av) + '</span>' +
      '<span class="cmp-chip" style="background:' + B.color + ';color:' + fgFor(B.color) + '">' +
      bId + ': ' + labelFor(bv) + '</span>';
    var ua = answers[q.id];
    if (ua && ua.v !== null && ua.v !== undefined) {{
      chips += '<span class="cmp-chip du">Du: ' + labelFor(ua.v) + '</span>';
    }}
    item.innerHTML = '<div class="rq">' + q.text + '</div><div class="cmp-chips">' + chips + '</div>';
    list.appendChild(item);
  }});
  el('cmp-sum').innerHTML =
    '<span class="chip chip-ok">Samma svar i ' + same + ' av ' + QUESTIONS.length + '</span>' +
    '<span class="chip chip-skip">Ett steg ifrån i ' + near + '</span>' +
    '<span class="chip chip-none">Längre isär i ' + (QUESTIONS.length - same - near) + '</span>';
  show('v-compare');
}}
el('cmp-back').addEventListener('click', function () {{
  if (load(KEY_R)) renderResult(false); else if (touchedCount() > 0) renderStart(); else renderPrio();
}});
el('r-redo').addEventListener('click', function () {{ restart(false); }});
el('r-review').addEventListener('click', renderReview);
el('rev-back').addEventListener('click', function () {{
  if (load(KEY_R)) renderResult(false); else renderStart();
}});

/* ---- granska svar ---- */
function labelFor(v) {{
  if (v === null || v === undefined) return 'Hoppade över';
  for (var i = 0; i < LABELS.length; i++) if (LABELS[i][0] === v) return LABELS[i][1];
  return '?';
}}
function weightFor(w) {{
  for (var i = 0; i < WEIGHTS.length; i++) if (WEIGHTS[i][0] === w) return WEIGHTS[i][1];
  return 'Normal';
}}
function statusOf(q) {{
  var a = answers[q.id];
  if (!a) return 'missing';
  if (a.v === null || a.v === undefined) return 'skipped';
  return 'answered';
}}
function goTo(i) {{ idx = i; show('v-quiz'); renderQ(); }}
function renderReview() {{
  var counts = {{ answered: 0, skipped: 0, missing: 0 }};
  ORDER.forEach(function (qid) {{ counts[statusOf(QBYID[qid])]++; }});

  el('rev-summary').innerHTML =
    '<span class="chip chip-ok">✓ ' + counts.answered + ' besvarade</span>' +
    '<span class="chip chip-skip">↷ ' + counts.skipped + ' överhoppade</span>' +
    '<span class="chip chip-none">○ ' + counts.missing + ' obesvarade</span>';

  var actions = el('rev-actions'); actions.innerHTML = '';
  if (counts.missing + counts.skipped > 0) {{
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'btn btn-go';
    b.textContent = 'Svara på nästa obesvarade fråga';
    b.addEventListener('click', function () {{
      for (var i = 0; i < ORDER.length; i++) {{
        var st = statusOf(QBYID[ORDER[i]]);
        if (st === 'missing' || st === 'skipped') {{ goTo(i); return; }}
      }}
    }});
    actions.appendChild(b);
  }}

  var STATUS_TXT = {{ answered: null, skipped: 'Hoppade över', missing: 'Obesvarad' }};
  var list = el('rev-list'); list.innerHTML = '';
  ORDER.forEach(function (qid, i) {{
    var q = QBYID[qid];
    var a = answers[q.id];
    var st = statusOf(q);
    var item = document.createElement('div');
    item.className = 'review-item st-' + st;
    var ansHtml;
    if (st === 'answered') {{
      ansHtml = 'Ditt svar: <b>' + labelFor(a.v) + '</b> <span>· vikt: ' + weightFor(a.w || 1) + '</span>';
    }} else {{
      ansHtml = '<b>' + STATUS_TXT[st] + '</b>';
    }}
    item.innerHTML = '<div class="rq">' + (i + 1) + '. ' + q.text + '</div>' +
      '<div class="ra">' + ansHtml + '</div>';

    // partiernas svar på skalan, ditt eget markerat
    var spec = document.createElement('div'); spec.className = 'spectrum';
    [-2, -1, 0, 1, 2].forEach(function (v) {{
      var col = document.createElement('div'); col.className = 'spec-col';
      col.title = labelFor(v);
      if (st === 'answered' && a.v === v) {{
        col.classList.add('me');
        var du = document.createElement('span'); du.className = 'pmini du';
        du.textContent = 'DU'; col.appendChild(du);
      }}
      PARTIES.forEach(function (p) {{
        if (q.partyPositions[p.id] !== v) return;
        var b = document.createElement('span'); b.className = 'pmini';
        b.textContent = p.id; b.title = p.name + ': ' + labelFor(v);
        b.style.background = p.color;
        b.style.color = DARKTEXT.indexOf(p.color) >= 0 ? '#1a1a1a' : '#fff';
        col.appendChild(b);
      }});
      spec.appendChild(col);
    }});
    item.appendChild(spec);
    var axis = document.createElement('div'); axis.className = 'spec-axis';
    axis.innerHTML = '<span>← Tar helt avstånd</span><span>Instämmer helt →</span>';
    item.appendChild(axis);

    var jump = document.createElement('button');
    jump.type = 'button'; jump.className = 'jump';
    jump.textContent = (st === 'answered') ? 'Ändra svar' : 'Svara på frågan';
    jump.addEventListener('click', function () {{ goTo(i); }});
    item.querySelector('.ra').appendChild(jump);
    var det = document.createElement('details'); det.className = 'info';
    det.innerHTML = '<summary><span class="info-badge">i</span>Om frågan<span class="chev">▼</span></summary>';
    var body = document.createElement('div'); body.className = 'info-body';
    var pr = q.info.pros.map(function (t) {{ return '<li>' + t + '</li>'; }}).join('');
    var co = q.info.cons.map(function (t) {{ return '<li>' + t + '</li>'; }}).join('');
    body.innerHTML = '<p>' + q.info.explanation + '</p>' +
      '<div class="proscons"><div class="pro"><h4>Skäl för</h4><ul>' + pr + '</ul></div>' +
      '<div class="con"><h4>Skäl emot</h4><ul>' + co + '</ul></div></div>';
    det.appendChild(body);
    item.appendChild(det);
    list.appendChild(item);
  }});
  show('v-review');
}}

/* ---- init: direktlänkar + val av första vy ---- */
(function init() {{
  var h = location.hash;
  if (h.indexOf('#r=') === 0) {{
    var sharedRes = decodeShare(h.slice(3));
    if (sharedRes) {{ renderResult(false, sharedRes); return; }}
  }}
  if (h === '#resultat' && load(KEY_R)) {{ renderResult(false); return; }}
  if (h === '#svar' && touchedCount() > 0) {{ renderReview(); return; }}
  if (h === '#jamfor') {{ renderCompare(null, null); return; }}
  if (h === '#om') {{ restart(true); return; }}
  if (touchedCount() === 0 && !load(KEY_R)) {{ renderPrio(); return; }}
  renderStart();
}})();
</script>'''


def wrap_page(title, body):
    return ('<!doctype html>\n<html lang="sv">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')


def build():
    pdata = json.load(open('data/parties.json'))
    parties = pdata['parties']
    parties_by_id = {p['id']: p for p in parties}
    questions = json.load(open('data/questions.draft.json'))['questions']
    dimensions = json.load(open('data/dimensions.json'))['dimensions']
    texts = load_texts()

    index_body = build_index(parties_by_id, texts)
    open('index.html', 'w').write(wrap_page('Valkompassen · Riksdagsvalet 2026', index_body))
    print(f'index.html skriven')

    test_body = build_test(parties, questions, dimensions)
    open('test.html', 'w').write(wrap_page('Gör testet · Valkompassen 2026', test_body))
    print(f'test.html skriven')

    if len(sys.argv) > 1:
        art = '<title>Partierna 2026–2030 · Valkompassen</title>\n' + index_body + '\n'
        open(sys.argv[1], 'w').write(art)
        print(f'artefaktkopia skriven: {sys.argv[1]}')


if __name__ == '__main__':
    build()
