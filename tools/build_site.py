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
    if p.get('logoUrl'):
        return (f'<span class="logo-box">'
                f'<img src="{p["logoUrl"]}" alt="{p["name"]} logotyp" loading="lazy" '
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
  S-, SD- och MP-symbolerna visas som neutrala märken i partifärg eftersom de officiella
  logotyperna inte är fritt licensierade. Texterna bygger på nyhetsrapportering och partiernas
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
    questions_js = js_embed([{
        'id': q['id'], 'dimension': dim_names[q['dimension']], 'text': q['text'],
        'info': q['info'], 'partyPositions': q['partyPositions']} for q in questions])

    return f'''<style>{CSS}</style>
<div class="wrap">
<header>
  <span class="eyebrow"><a href="index.html" style="color:inherit;text-decoration:none">← Valkompassen</a> · Testet</span>
</header>

<section id="v-start" class="startbox">
  <h1>Valkompasstestet</h1>
  <p class="lede" style="margin-inline:auto">32 påståenden om svensk politik. Svara på en femgradig skala,
  markera vilka frågor som är extra viktiga för dig, och tryck på infoknappen om du vill
  förstå frågan bättre — med för- och nackdelar för varje ståndpunkt.</p>
  <p class="small">Dina svar sparas bara lokalt i din webbläsare (localStorage) — inget skickas någonstans.
  Du kan när som helst komma tillbaka och se dina svar och ditt resultat.</p>
  <div id="start-buttons"></div>
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
  <h1>Ditt resultat</h1>
  <p class="small" id="r-meta"></p>
  <div id="r-warn"></div>
  <div id="r-list"></div>
  <p class="small">Matchningen bygger på viktad överensstämmelse fråga för fråga
  (se <a href="https://github.com/gbgeka/Valkompassen/blob/claude/swedish-voter-compass-42d6l8/docs/03-matchningsalgoritm.md">metodiken</a>).
  Partipositionerna är redaktionella utkast som verifieras mot valmanifest och partisvar före skarp lansering.</p>
  <div class="startrow">
    <button class="btn" id="r-review" type="button">Se dina svar</button>
    <button class="btn" id="r-redo" type="button">Gör om testet</button>
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
var LABELS = [[-2, 'Tar helt avstånd'], [-1, 'Tar delvis avstånd'], [0, 'Neutral / vet ej'],
              [1, 'Instämmer delvis'], [2, 'Instämmer helt']];
var WEIGHTS = [[0.5, 'Mindre viktig'], [1, 'Normal'], [2, 'Extra viktig']];
var KEY_A = '{STORE_ANSWERS}', KEY_R = '{STORE_RESULT}', MIN = {MIN_ANSWERED};
var DARKTEXT = ['#DDDD00', '#52BDEC'];

var answers = load(KEY_A) || {{}};
var idx = 0;
var hist = [];  // ångra-stack (per session): {{qid, idx, prev}}

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
  ['v-start', 'v-quiz', 'v-result', 'v-review'].forEach(function (v) {{
    el(v).classList.toggle('hidden', v !== view);
  }});
  window.scrollTo(0, 0);
}}

/* ---- matchning: viktad L1 enligt docs/03 ---- */
function computeScores() {{
  var rows = PARTIES.map(function (p) {{
    var num = 0, den = 0;
    QUESTIONS.forEach(function (q) {{
      var a = answers[q.id];
      if (!a || a.v === null || a.v === undefined) return;
      var w = a.w || 1;
      num += w * Math.abs(a.v - q.partyPositions[p.id]);
      den += w * 4;
    }});
    return {{ id: p.id, name: p.name, color: p.color,
             pct: den ? Math.round(100 * (1 - num / den)) : 0 }};
  }});
  rows.sort(function (a, b) {{ return b.pct - a.pct; }});
  return rows;
}}

/* ---- startvy ---- */
function renderStart() {{
  var box = el('start-buttons'); box.innerHTML = '';
  var res = load(KEY_R);
  var touched = touchedCount();
  function btn(txt, cls, fn) {{
    var b = document.createElement('button'); b.type = 'button';
    b.className = cls; b.textContent = txt; b.addEventListener('click', fn); return b;
  }}
  if (touched === 0) {{
    box.appendChild(btn('Starta testet', 'cta', function () {{ idx = 0; show('v-quiz'); renderQ(); }}));
  }} else {{
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
  }}
}}
function firstUnanswered() {{
  for (var i = 0; i < QUESTIONS.length; i++) if (!(QUESTIONS[i].id in answers)) return i;
  return 0;
}}
function restart(force) {{
  if (!force && touchedCount() > 0 &&
      !confirm('Detta nollställer testet: alla dina svar och ditt resultat raderas. Vill du fortsätta?')) return;
  localStorage.removeItem(KEY_A); localStorage.removeItem(KEY_R);
  answers = {{}}; hist = []; idx = 0; show('v-quiz'); renderQ();
}}

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
  var q = QUESTIONS[idx];
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
  var q = QUESTIONS[idx];
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
  var q = QUESTIONS[idx];
  pushHist(q.id);
  answers[q.id] = {{ v: null, w: answers[q.id] && answers[q.id].w || 1 }};
  save(KEY_A, answers); next();
}});

/* ---- resultatvy ---- */
function renderResult(saveIt) {{
  var n = answeredCount();
  var warn = el('r-warn'); warn.innerHTML = '';
  if (n < MIN) {{
    warn.innerHTML = '<div class="warn">Du har besvarat ' + n + ' frågor. Det behövs minst ' +
      MIN + ' för ett pålitligt resultat — <a href="#" id="warn-more">svara på fler frågor</a>.</div>';
    el('r-list').innerHTML = '';
    el('r-meta').textContent = '';
    show('v-result');
    el('warn-more').addEventListener('click', function (ev) {{
      ev.preventDefault(); idx = firstUnanswered(); show('v-quiz'); renderQ();
    }});
    return;
  }}
  var scores = computeScores();
  if (saveIt) {{
    save(KEY_R, {{ date: new Date().toISOString().slice(0, 10), answered: n,
                  total: QUESTIONS.length, scores: scores }});
  }}
  el('r-meta').textContent = n + ' av ' + QUESTIONS.length + ' frågor besvarade. ' +
    'Högre procent = större samsyn med partiet i dina viktade svar.';
  var list = el('r-list'); list.innerHTML = '';
  scores.forEach(function (s) {{
    var row = document.createElement('div'); row.className = 'score-row';
    var fg = DARKTEXT.indexOf(s.color) >= 0 ? '#1a1a1a' : '#fff';
    row.innerHTML = '<span class="pid" style="background:' + s.color + ';color:' + fg + '">' + s.id + '</span>' +
      '<span class="score-bar"><i style="width:' + s.pct + '%;background:' + s.color + '"></i></span>' +
      '<span class="pct">' + s.pct + ' %</span>';
    list.appendChild(row);
  }});
  show('v-result');
}}
el('r-redo').addEventListener('click', function () {{ restart(false); }});
el('r-review').addEventListener('click', renderReview);
el('rev-back').addEventListener('click', function () {{
  if (load(KEY_R)) renderResult(false); else {{ show('v-start'); renderStart(); }}
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
  QUESTIONS.forEach(function (q) {{ counts[statusOf(q)]++; }});

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
      for (var i = 0; i < QUESTIONS.length; i++) {{
        var st = statusOf(QUESTIONS[i]);
        if (st === 'missing' || st === 'skipped') {{ goTo(i); return; }}
      }}
    }});
    actions.appendChild(b);
  }}

  var STATUS_TXT = {{ answered: null, skipped: 'Hoppade över', missing: 'Obesvarad' }};
  var list = el('rev-list'); list.innerHTML = '';
  QUESTIONS.forEach(function (q, i) {{
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

/* ---- init: stöd direktlänkar från index ---- */
(function init() {{
  var h = location.hash;
  if (h === '#resultat' && load(KEY_R)) {{ renderResult(false); return; }}
  if (h === '#svar' && touchedCount() > 0) {{ renderReview(); return; }}
  if (h === '#om') {{ restart(true); return; }}
  renderStart(); show('v-start');
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
