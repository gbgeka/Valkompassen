#!/usr/bin/env python3
"""Genererar index.html (GitHub Pages) från data/parties.json och docs/04.

Körs från repots rot:  python3 tools/build_site.py [artefakt-kopia.html]

Bildpolicy:
- Partiledarfoton och fritt licensierade partisymboler hotlänkas från
  Wikimedia Commons (Special:FilePath). Saknas fri logotyp (S, SD, MP)
  renderas ett platshållarmärke med partibokstaven i partifärg.
- Alla logotyper ritas i en fast 64x64-ruta med object-fit:contain på en
  ljus platta, så att olika proportioner får enhetlig visuell storlek.
- Porträtt beskärs till 52x52-cirkel med object-fit:cover.
- onerror-fallback: om en extern bild inte laddar visas platshållaren.
"""
import json
import re
import sys


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
  --logo-plate:#FDFCF8;
}
@media (prefers-color-scheme: dark) {
  :root { --paper:#151920; --ink:#E7E3D9; --ink-2:#9BA0A8; --line:#2C323C;
          --card:#1C222B; --accent:#F5C400; --accent-ink:#E5C34D; --chip:#242B36;
          --logo-plate:#EDEAE2; }
}
:root[data-theme="dark"] { --paper:#151920; --ink:#E7E3D9; --ink-2:#9BA0A8; --line:#2C323C;
          --card:#1C222B; --accent:#F5C400; --accent-ink:#E5C34D; --chip:#242B36;
          --logo-plate:#EDEAE2; }
:root[data-theme="light"] { --paper:#FAF8F2; --ink:#20242B; --ink-2:#5C6068; --line:#E2DDD0;
          --card:#FFFFFF; --accent:#F5C400; --accent-ink:#8A6D00; --chip:#F3EFE4;
          --logo-plate:#FDFCF8; }
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
.portrait { width:52px; height:52px; flex:none; border-radius:50%;
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
'''


def build():
    data = json.load(open('data/parties.json'))
    parties = {p['id']: p for p in data['parties']}
    texts = load_texts()
    rodgrona, tido = ['S', 'V', 'MP', 'C'], ['M', 'SD', 'KD', 'L']

    body = f'''<style>{CSS}</style>
<div class="wrap">
<header>
  <span class="eyebrow">Valkompassen · Riksdagsvalet 2026</span>
  <h1>Vad partierna vill åstadkomma 2026–2030</h1>
  <p class="lede">Kort sammanställning av de åtta riksdagspartiernas program inför valet:
  vad de står för och vad de lovar väljarna den kommande mandatperioden.
  Baserad på valplattformar och vallöften kända t.o.m. juli 2026.</p>
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
{''.join(card(parties[pid], texts) for pid in rodgrona)}

<h2 class="bloc">Tidöpartierna</h2>
<p class="bloc-sub">Moderaterna, Sverigedemokraterna, Kristdemokraterna och Liberalerna — regeringsunderlaget sedan 2022, med ambition att regera i fyrpartiregering efter valet.</p>
{''.join(card(parties[pid], texts) for pid in tido)}

<footer>
  <p>Partiledarfoton och fritt licensierade partisymboler:
  <a href="https://commons.wikimedia.org">Wikimedia Commons</a> (CC-licenser, källor per bild i
  <a href="https://github.com/gbgeka/Valkompassen/blob/claude/swedish-voter-compass-42d6l8/assets/KALLOR.md">assets/KALLOR.md</a>).
  S-, SD- och MP-symbolerna visas som neutrala märken i partifärg eftersom de officiella
  logotyperna inte är fritt licensierade. Texterna bygger på nyhetsrapportering och partiernas
  utspel t.o.m. juli 2026. Del av projektet
  <a href="https://github.com/gbgeka/Valkompassen">Valkompassen</a>.</p>
</footer>
</div>'''

    full = ('<!doctype html>\n<html lang="sv">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>Partierna 2026–2030 · Valkompassen</title>\n</head>\n<body>\n'
            + body + '\n</body>\n</html>\n')
    open('index.html', 'w').write(full)
    print(f'index.html skriven ({len(full)} tecken)')

    if len(sys.argv) > 1:
        art = '<title>Partierna 2026–2030 · Valkompassen</title>\n' + body + '\n'
        open(sys.argv[1], 'w').write(art)
        print(f'artefaktkopia skriven: {sys.argv[1]}')


if __name__ == '__main__':
    build()
