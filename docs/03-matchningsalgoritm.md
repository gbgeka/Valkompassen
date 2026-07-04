# Matchningsalgoritm

Hur användarens svar omvandlas till en rankad partilista. Designmål: rättvis, förklarbar, robust mot obesvarade frågor — och helt körbar i webbläsaren (ingen persondata lämnar klienten).

## 1. Indata

- **Användarsvar:** per fråga *i*: svar `uᵢ ∈ {−2, −1, 0, +1, +2}` eller `hoppad`, samt frågevikt `wᵢ ∈ {0.5, 1, 2}`.
- **Partipositioner:** per fråga *i* och parti *p*: `aᵢₚ ∈ {−2 … +2}`, med källa. Saknar partiet tydlig position markeras frågan `okänd` för det partiet.
- **Prioriterade områden:** upp till tre dimensioner som får dimensionsvikt `Wd = 1.5` (övriga `1.0`).

## 2. Grundformel: viktad normaliserad likhet

För varje parti *p* beräknas ett likhetsvärde över alla frågor som varken användaren hoppat över eller partiet saknar position i:

```
likhet(p) = 1 − Σᵢ (wᵢ · Wd(i) · |uᵢ − aᵢₚ|) / Σᵢ (wᵢ · Wd(i) · dmax)
```

där `dmax = 4` (största möjliga avstånd, från −2 till +2). Resultatet blir 0–1 och presenteras som **matchprocent**.

**Varför Manhattan-avstånd (L1) i stället för Euklidiskt (L2)?** L1 straffar många små skillnader lika mycket som få stora — det speglar bättre hur väljare resonerar ("vi tycker olika i tio frågor" väger tyngre än "vi tycker väldigt olika i en"). L2 skulle premiera partier som är lagom fel överallt.

## 3. Hantering av bortfall

- **Användaren hoppar över en fråga** → frågan utesluts ur både täljare och nämnare för alla partier. Nämnaren normaliserar, så partier jämförs rättvist.
- **Partiet saknar position** → frågan utesluts för det partiet, men resultatet flaggas: om >20 % av användarens besvarade frågor saknar partiposition visas en osäkerhetsmarkering ("matchningen mot parti X bygger på färre frågor").
- **Minst 15 besvarade frågor** krävs för att visa resultat alls — annars uppmanas användaren att svara på fler.

## 4. Neutrala svar

`uᵢ = 0` ("neutral") behandlas som ett riktigt svar: ett parti med stark position (±2) får avstånd 2 mot en neutral användare. Det är avsiktligt — en väljare utan åsikt i migrationsfrågan ska inte matchas med ett parti vars hela profil är migration.

## 5. Resultatpresentation

1. **Rankad lista** med matchprocent per parti. Visa alla åtta — inte bara toppresultatet — så att användaren ser hur nära det är.
2. **Radar-/stapeldiagram per dimension:** användarens position vs. topp-3-partiernas, så det syns *var* man är överens.
3. **"Största likhet / största skillnad":** för valfritt parti, de tre frågor där avståndet är minst respektive störst.
4. **Jämförelseläge:** två partier sida vid sida, fråga för fråga, med källa per partiposition.
5. **Osäkerhetsmarkering** enligt §3.

## 6. Validering innan lansering

- **Självtest:** mata in varje partis egna positioner som "användarsvar" — partiet ska då matcha sig självt till ~100 % och blocksyskonen därnäst. Om inte: frågebanken eller positionerna är felkodade.
- **Diskriminanstest:** stryk frågor där alla partier hamnar inom ±1 av varandra (låg särskiljning).
- **Känslighetsanalys:** små ändringar i en enskild fråga ska inte kasta om topp-3 — annars är frågebanken för liten.
- **Panel:** låt testpersoner med känd partisympati köra kompassen och jämför utfallet.

## 7. Implementationsskiss (fas 3)

```ts
type Answer = { questionId: string; value: -2|-1|0|1|2; weight: 0.5|1|2 } | { questionId: string; skipped: true };

function match(answers: Answer[], party: Party, priorities: DimensionId[]): MatchResult {
  // filtrera hoppade frågor och frågor där partiet saknar position,
  // summera viktade L1-avstånd, normalisera mot max, returnera
  // { score, questionsUsed, coverage, perDimension }
}
```

Motorn ska vara en ren, sidoeffektsfri TypeScript-modul med full testtäckning — den är hjärtat i produkten och den del som måste vara bevisbart korrekt.
