# Frågedesign: vilka frågor behövs för att hitta rätt parti?

Målet med frågedesignen är **maximal särskiljningsförmåga med minimalt antal frågor**. Varje fråga ska bidra till att skilja minst två partier åt som annars skulle se likadana ut. Frågor där alla åtta partier tycker ungefär samma (t.ex. "sjukvården ska vara bra") är värdelösa och ska bort.

## De åtta dimensionerna

Svensk politik låter sig inte beskrivas på en enda vänster–höger-skala. Kompassen bygger på åtta dimensioner, valda för att de (a) förklarar de största skillnaderna mellan partierna och (b) motsvarar de sakområden väljare faktiskt röstar på:

| # | Dimension | Pol A (−2) | Pol B (+2) | Skiljer främst |
|---|-----------|-----------|-----------|----------------|
| 1 | **Ekonomi & skatter** | Mer omfördelning, högre skatt på höga inkomster | Lägre skatter, mer marknad | V/S ↔ M |
| 2 | **Migration & integration** | Generösare asyl- och anhörigpolitik | Restriktiv, återvandring | MP/V ↔ SD |
| 3 | **Klimat & miljö** | Skarpa mål och styrmedel nu | Lägre tempo, teknik löser det | MP ↔ SD/M |
| 4 | **Lag & ordning** | Förebyggande, sociala insatser | Straffskärpning, övervakning | V ↔ M/SD |
| 5 | **Välfärdens organisation** | Offentlig drift, vinstbegränsning | Privat drift, valfrihet | V/S ↔ M/C |
| 6 | **EU & internationellt** | Fördjupat EU-samarbete | Mindre överstatlighet | L ↔ SD |
| 7 | **Värderingar (GAL–TAN)** | Progressiv, individcentrerad | Traditionell, nationellt orienterad | MP/V/L ↔ KD/SD |
| 8 | **Energi & landsbygd** | Förnybar utbyggnad | Kärnkraftssatsning | MP ↔ KD/M/SD |

Dimension 7 (GAL–TAN) är avgörande: den fångar konflikter som vänster–höger missar helt, t.ex. varför en L-väljare och en SD-väljare kan tycka lika om skatter men helt olika om det mesta annat.

## Frågetyper

En sofistikerad kompass använder tre frågetyper i kombination:

### 1. Påståendefrågor (kärnan, ~28–32 st)

Likert-skala med fem steg plus möjlighet att avstå:

> "Skatten på höga inkomster bör höjas."
> ○ Instämmer helt ○ Instämmer delvis ○ Neutral/vet ej ○ Tar delvis avstånd ○ Tar helt avstånd ☐ Hoppa över

- Kodas −2 … +2. "Hoppa över" utesluter frågan ur matchningen (den räknas inte som neutral — viktig skillnad).
- 3–4 påståenden per dimension för robusthet (en enskild fråga kan misstolkas).

### 2. Viktningsfrågor (per fråga eller per dimension)

Efter varje påstående (eller per block): **"Hur viktig är denna fråga för dig?"** — Mycket viktig (vikt 2) / Ganska viktig (vikt 1) / Mindre viktig (vikt 0,5).

Detta är det som gör kompassen *sofistikerad*: en väljare för vilken migration avgör allt ska inte matchas som om klimat vägde lika tungt.

### 3. Prioriteringsfråga (1 st, i början eller slutet)

> "Välj de tre samhällsfrågor som är viktigast för dig när du röstar."
> (sjukvård, skola, lag och ordning, migration, klimat, ekonomi/skatter, försvar, äldreomsorg, energi, landsbygd, …)

Används för att (a) höja vikten på motsvarande dimensioner och (b) i resultatet visa "i dina tre viktigaste frågor tycker du mest som parti X".

## Principer för bra påståenden

1. **En sak per påstående.** Inte "skatten bör sänkas och bidragen stramas åt" — det är två frågor.
2. **Konkret, inte abstrakt.** "Vinstuttag ur skattefinansierade friskolor ska förbjudas" slår "vinster i välfärden är ett problem".
3. **Balanserad riktning.** Ungefär hälften av påståendena formuleras så att "instämmer" pekar åt vardera pol — annars belönas ja-sägande (acquiescence bias).
4. **Reell partiskillnad.** Varje påstående ska ha minst ett parti på vardera sidan om noll. Kör diskriminansanalys på frågebanken innan lansering och stryk frågor med låg spridning.
5. **Neutralt språk.** Undvik laddade ord ("massinvandring", "flumskola") — formuleringen får inte signalera vilket svar som är "rätt".
6. **Aktuella konfliktlinjer.** Frågorna ska handla om det som faktiskt skiljer partierna åt 2026: t.ex. angiverilag, visitationszoner, kärnkraftssubventioner, tiggeriförbud, arbetskraftsinvandringens lönegolv, Nato-samarbetets utformning, vinsttak i skolan.

## Rekommenderad struktur för användaren

1. **Intro** — 30 sek: så funkar det, anonymt, inget sparas.
2. **Prioriteringsfrågan** — sätter grundvikter.
3. **~30 påståenden** i slumpad ordning inom block, med viktknapp per fråga. Progressindikator. Beräknad tid: 7–10 min.
4. **Resultat** — rankad partilista med matchprocent, radardiagram per dimension, "största likhet/största skillnad" per parti, länk till källor.
5. **Fördjupning (valfritt)** — jämför två partier sida vid sida, se partiets faktiska svar/källa per fråga.

## Utkast till frågebank

Ett första utkast med 32 påståenden (4 per dimension) finns i [`data/questions.draft.json`](../data/questions.draft.json). Varje fråga har:

```json
{
  "id": "eco-01",
  "dimension": "economy",
  "text": "Skatten på höga inkomster bör höjas.",
  "reversed": false,
  "partyPositions": { "V": 2, "MP": 1, "S": 1, "C": -1, "L": -1, "KD": -2, "M": -2, "SD": -1 },
  "source": "ATT_VERIFIERA"
}
```

`reversed: true` markerar frågor där instämmande pekar mot höger/restriktiv/TAN-polen, så att kodningen kan vändas i matchningen. Fältet `source` ska före lansering ersättas med en riktig källhänvisning (manifest-sida, votering eller partisvar).
