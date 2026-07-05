# Funktionsjämförelse med etablerade valkompasser

Jämförelse mot SVT:s valkompass 2026 (35 frågor, riksdag + lokala + kandidater), TV4/Aftonbladet/DN:s kompasser och internationella verktyg (Wahl-O-Mat, Political Compass). Uppdaterad juli 2026.

## Det vi redan har — och där vi ligger bra till

| Funktion | Vi | Kommentar |
|----------|-----|-----------|
| Viktning per fråga | ✅ | Tre nivåer (SVT har binärt "extra viktig") |
| Hoppa över fråga | ✅ | Exkluderas ur matchningen, räknas inte som neutral |
| Infotexter med för- och nackdelar | ✅ | **Starkare än de flesta** — SVT har korta förklaringar, sällan strukturerade pros/cons |
| Partiernas svar per fråga vs ditt | ✅ | Skalvy i "Se dina svar" |
| Ångra + nollställ + återuppta | ✅ | Sparas i localStorage |
| Integritet | ✅ | Ingen spårning, inget lämnar webbläsaren — tydlig USP |
| Metodtransparens | ✅ | Öppen källkod + dokumenterad algoritm |

## Luckor, prioriterade

### A. Snabba att bygga, hög effekt (befintlig data räcker)

1. **Resultat per ämnesområde** — stapel/radar per dimension: "du matchar M i ekonomi men V i klimat". Alla stora kompasser har någon form av detta. Dimensionsdatat finns redan.
2. **"Ni är överens i X av Y frågor"** + största samsyn/största skillnad per parti på resultatsidan (planerat i docs/03 §5).
3. **Dela resultat** — SVT m.fl. har social delning. Privacy-vänlig variant: koda resultatet i URL-fragmentet (`#r=...`), ingen server behövs.
4. **Prioriteringsfrågan** — "välj dina tre viktigaste områden" (docs/02 §3), ger dimensionsviktning och bättre resultatpresentation.
5. **Slumpad frågeordning inom område** — minskar ordningsbias, standard i seriösa kompasser.
6. **Jämför två partier sida vid sida** — fråga för fråga (planerat i docs/03 §5.4).

### B. Innehållsarbete (kräver redaktion/partikontakt)

7. **Källa per partiposition** — vår största lucka: alla positioner är `ATT_VERIFIERA`. SVT bygger på partienkäter. Åtgärd enligt checklistan i docs/01.
8. **Partiernas egna motiveringar per fråga** — SVT visar partiets kommentar till varje svar. Kräver enkätsvar från partierna (eller citat ur manifest med källa).
9. **Valfakta-sida** — hur man röstar, förtidsröstning, rösträtt, valdagen. Lågt hängande men kräver korrekt myndighetsinfo (val.se).

### C. Större byggen

10. **Ideologisk 2D-karta** — plotta dig och partierna på vänster–höger × GAL–TAN (data finns i dimensionerna). Pedagogiskt starkt, få svenska kompasser har det.
11. **Tillgänglighet och språk** — SVT erbjuder lättläst och flera språk; vi har bara standardsvenska. Även ARIA-genomgång och skärmläsartest.
12. **Osäkerhetsvisning** — flagga när ett partis position är svagt källbelagd (fältet finns förberett i datamodellen via `source`).

### D. Utom räckhåll för projektets storlek (medvetet bortvalda)

13. **Kandidatkompass** — SVT enkäterar tusentals riksdagskandidater. Kräver organisation vi inte har.
14. **Lokala kompasser** (kommun/region) — samma skäl: 290 kommuner × frågebank.

## Rekommenderad ordning

Fas A (1–6) före valrörelsens slutspurt — allt bygger på data som redan finns i `data/`. Punkt 7 (källverifiering) är dock **viktigast av allt** innan sidan marknadsförs: en valkompass med overifierade partipositioner får inte uppfattas som auktoritativ.
