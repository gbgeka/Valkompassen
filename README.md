# Valkompassen

En sofistikerad valkompass för riksdagsvalet i Sverige **13 september 2026**. Målet är att hjälpa väljare att hitta det parti som bäst matchar deras åsikter — inte bara på en vänster–höger-skala, utan över flera politiska dimensioner med viktning, prioriteringar och transparent metodik.

## Vad skiljer denna valkompass från andra?

1. **Flerdimensionell analys** — matchning sker över åtta politiska dimensioner (ekonomi, migration, klimat, trygghet, välfärd, EU, värderingar, energi/landsbygd), inte en endimensionell skala.
2. **Viktning** — användaren kan markera vilka frågor och områden som är viktigast, och matchningen tar hänsyn till det.
3. **Transparens** — varje partiposition är källbelagd (valmanifest, riksdagsvoteringar, partisvar) och användaren kan se *varför* ett parti matchar, nedbrutet per område.
4. **Osäkerhetsredovisning** — när ett parti saknar tydlig position redovisas det, i stället för att gissas.

## Projektstatus

| Fas | Innehåll | Status |
|-----|----------|--------|
| 1. Kartläggning | Partier, dimensioner, metodik | ✅ Klar (detta dokument + `docs/`) |
| 2. Frågebank | ~30 påståenden + partipositioner med källor | 🔜 Utkast finns i `data/questions.draft.json` |
| 3. Applikation | Webbapp (frontend + matchningsmotor) | ⬜ Ej påbörjad |
| 4. Validering | Testning mot partiernas egna svar | ⬜ Ej påbörjad |

## Dokumentation

- [`docs/01-partikartlaggning.md`](docs/01-partikartlaggning.md) — kartläggning av de åtta riksdagspartierna: ideologi, block, profilfrågor och positioner per dimension.
- [`docs/02-fragedesign.md`](docs/02-fragedesign.md) — vilka typer av frågor som behövs, de åtta dimensionerna, frågeformat och principer för bra påståenden.
- [`docs/03-matchningsalgoritm.md`](docs/03-matchningsalgoritm.md) — hur användarens svar matchas mot partierna (viktad distans, normalisering, resultatpresentation).
- [`docs/04-partiernas-program-2026-2030.md`](docs/04-partiernas-program-2026-2030.md) — kort sammanställning per parti: vad de står för och vill åstadkomma under mandatperioden 2026–2030.

## Data

- [`data/parties.json`](data/parties.json) — strukturerad partidata (namn, färg, ideologi, positioner per dimension).
- [`data/dimensions.json`](data/dimensions.json) — de åtta dimensionerna med skaländar.
- [`data/questions.draft.json`](data/questions.draft.json) — utkast till frågebank (~30 påståenden kopplade till dimensioner).

## Föreslagen teknikstack (fas 3)

- **Frontend:** React/Next.js eller SvelteKit, mobilanpassad (de flesta gör valkompasser i mobilen).
- **Matchningsmotor:** ren TypeScript-modul utan backend-beroende — all matchning kan ske klient-sidigt, ingen persondata behöver lämna webbläsaren.
- **Datakällor:** riksdagens öppna data (voteringar), partiernas valmanifest 2026, partisvar på enkät.

## Viktigt om datakvalitet

Partipositionerna i `data/parties.json` är ett **redaktionellt utgångsläge** baserat på partiernas politik t.o.m. början av 2026. Innan lansering måste varje position verifieras mot partiernas valmanifest för 2026 och helst mot direkta partisvar — se checklistan i `docs/01-partikartlaggning.md`.
