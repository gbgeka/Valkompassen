#!/usr/bin/env python3
"""Verifierar att alla bild-URL:er och lokala bildfiler fungerar.

Körs i CI (deploy-workflowet) där utgående nätverk är öppet:
    python3 tools/check_images.py

Kontrollerar att varje extern bild i data/parties.json svarar 200 med en
bild-content-type (Special:FilePath följer redirect till upload.wikimedia.org),
och att lokala platshållarfiler finns. Avslutar med felkod om något brister,
vilket stoppar deployen.
"""
import json
import os
import sys
import urllib.request

OK, FAIL = 0, 0


def check_url(label, url):
    global OK, FAIL
    req = urllib.request.Request(url, method='GET', headers={
        'User-Agent': 'Valkompassen-bildkontroll/1.0 (github.com/gbgeka/Valkompassen)'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ctype = r.headers.get('Content-Type', '')
            size = len(r.read())
            if r.status == 200 and ctype.startswith('image/') and size > 500:
                print(f'  OK   {label}: {ctype}, {size} B')
                OK += 1
            else:
                print(f'  FEL  {label}: status={r.status} type={ctype} size={size}')
                FAIL += 1
    except Exception as e:
        print(f'  FEL  {label}: {e}')
        FAIL += 1


def check_local(label, path):
    global OK, FAIL
    if os.path.isfile(path) and os.path.getsize(path) > 100:
        print(f'  OK   {label}: lokal fil, {os.path.getsize(path)} B')
        OK += 1
    else:
        print(f'  FEL  {label}: saknas eller tom ({path})')
        FAIL += 1


def main():
    data = json.load(open('data/parties.json'))
    print('== Logotyper ==')
    for p in data['parties']:
        if p.get('logoUrl'):
            check_url(f'{p["id"]} logotyp', p['logoUrl'])
        else:
            check_local(f'{p["id"]} logotyp (platshållare)', p['logo'])
    print('== Partiledarporträtt ==')
    for p in data['parties']:
        for led in p['leaders']:
            check_url(f'{p["id"]} {led["name"]}', led['imageUrl'])
    print(f'\nResultat: {OK} OK, {FAIL} fel')
    sys.exit(1 if FAIL else 0)


if __name__ == '__main__':
    main()
