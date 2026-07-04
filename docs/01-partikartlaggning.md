# Kartläggning av riksdagspartierna inför valet 2026

Riksdagsvalet hålls **söndagen den 13 september 2026**. Åtta partier sitter i riksdagen. Nedan kartläggs varje parti: ideologisk hemvist, blocktillhörighet, profilfrågor och position på de åtta dimensioner som valkompassen bygger på (se `02-fragedesign.md`).

> **OBS:** Partiledaruppgifter och positioner speglar läget medio 2026. Positionerna är redaktionella bedömningar som **måste verifieras** mot valmanifest 2026 och partisvar innan lansering — se checklistan sist i dokumentet.

## Blocken

- **Vänsterblocket / de rödgröna:** Socialdemokraterna (S), Vänsterpartiet (V), Miljöpartiet (MP), Centerpartiet (C)*
- **Högerblocket / Tidöpartierna:** Moderaterna (M), Sverigedemokraterna (SD), Kristdemokraterna (KD), Liberalerna (L)

\* C definierar sig som liberalt mittenparti men har sedan 2022 samarbetat åt det rödgröna hållet. Blocktillhörighet inför 2026 bör bevakas.

---

## Partierna i korthet

### Socialdemokraterna (S)
- **Partiledare:** Magdalena Andersson (sedan 2021)
- **Ideologi:** Socialdemokrati
- **Profilfrågor:** Välfärd (sjukvård, skola, äldreomsorg), arbetsmarknad och trygghetssystem, ordning i välfärden (vinstbegränsningar), kriminalitetsbekämpning kombinerad med förebyggande arbete.
- **Ekonomi:** Center-vänster. Högre skatter för höga inkomster/kapital, mer resurser till offentlig välfärd.
- **Migration:** Stramare linje än historiskt; "ordning och reda", volymmål.
- **Typiska väljarkonflikter:** Väljare som gillar välfärdspolitiken men vill ha mjukare/stramare migrationspolitik.

### Moderaterna (M)
- **Partiledare:** Ulf Kristersson (sedan 2017), statsminister sedan 2022
- **Ideologi:** Liberalkonservatism
- **Profilfrågor:** Sänkta skatter, lag och ordning (hårdare straff, fler poliser), kärnkraft, arbetslinjen, restriktiv migration.
- **Ekonomi:** Höger. Skattesänkningar, bidragstak, privat drift i välfärden.
- **Klimat:** Teknikoptimism, kärnkraft som klimatlösning; lägre ambitioner för styrmedel som drabbar hushåll.

### Sverigedemokraterna (SD)
- **Partiledare:** Jimmie Åkesson (sedan 2005)
- **Ideologi:** Socialkonservatism, nationalism
- **Profilfrågor:** Kraftigt minskad invandring och återvandring, hårdare straff, nationell kultur och sammanhållning, sänkta drivmedelspriser, EU-skepsis.
- **Ekonomi:** Blandad — höger i skattefrågor men välfärdsvänlig retorik ("välfärdschauvinism").
- **Klimat:** Låg prioritet för klimatstyrmedel; kärnkraftsvänliga, motstånd mot vindkraftsutbyggnad till havs subventioner.

### Centerpartiet (C)
- **Partiledare:** Elisabeth Thand Ringqvist (sedan november 2025)
- **Ideologi:** Grön socialliberalism, agrar tradition
- **Profilfrågor:** Landsbygd och gröna näringar, företagande och avreglering, decentralisering, liberal migrationspolitik (relativt), marknadsbaserad klimatpolitik.
- **Ekonomi:** Center-höger. Sänkta arbetsgivaravgifter, avreglerad arbetsrätt, men mittenposition i välfärd.
- **Särart:** Enda tydligt liberala rösten i det rödgröna lägret; aldrig regera med SD som princip.

### Vänsterpartiet (V)
- **Partiledare:** Nooshi Dadgostar (sedan 2020)
- **Ideologi:** Socialism, feminism
- **Profilfrågor:** Stoppa vinster i välfärden, höjda skatter på kapital och höga inkomster, offentliga investeringar, hyresrätter, kortare arbetstid, klimatinvesteringar med statlig styrning.
- **Ekonomi:** Tydligast vänster. Stora offentliga investeringsprogram.
- **EU/NATO:** Historiskt kritiska; accepterar numera NATO-medlemskapet som faktum men EU-skeptisk vänsterprofil.

### Kristdemokraterna (KD)
- **Partiledare:** Ebba Busch (sedan 2015)
- **Ideologi:** Kristdemokrati, socialkonservatism
- **Profilfrågor:** Sjukvård (statligt huvudmannaskap), familjepolitik (valfrihet för familjer), äldreomsorg, hårdare straff, kärnkraft.
- **Ekonomi:** Höger. Skattesänkningar för pensionärer och familjer.
- **Värderingar:** Traditionellt/konservativt på GAL–TAN-skalan, familjen som bas.

### Liberalerna (L)
- **Partiledare:** Simona Mohamsson (sedan juni 2025)
- **Ideologi:** Socialliberalism
- **Profilfrågor:** Skolan (kunskapsfokus, statlig skola), integration med krav, EU-vänlighet (mest EU-positiva partiet), kärnkraft, individens frihet.
- **Ekonomi:** Center-höger.
- **Särart:** Liberala värderingar (GAL-sidan) kombinerat med regeringssamarbete som vilar på SD — spänning som många väljare vill få belyst.

### Miljöpartiet (MP)
- **Språkrör:** Amanda Lind och Daniel Helldén (sedan 2023/2024)
- **Ideologi:** Grön ideologi
- **Profilfrågor:** Klimatomställning (skarpa utsläppsmål, styrmedel), biologisk mångfald, avveckla fossila subventioner, human migrationspolitik, psykisk hälsa.
- **Ekonomi:** Center-vänster med grön investeringsprofil.
- **Energi:** Förnybart framför kärnkraft — tydligast anti-kärnkraft.

---

## Positionsmatris (utgångsläge, skala −2 … +2)

Skalorna definieras i `data/dimensions.json`. Negativt värde = vänster/generös/hög ambition-polen, positivt = höger/restriktiv/låg prioritet-polen (se respektive dimension). Detta är **utgångsvärden att verifiera**, inte facit.

| Dimension | V | MP | S | C | L | KD | M | SD |
|---|---|---|---|---|---|---|---|---|
| Ekonomi (omfördelning ↔ marknad) | −2 | −1 | −1 | +1 | +1 | +1 | +2 | +1 |
| Migration (generös ↔ restriktiv) | −1 | −2 | +1 | −1 | 0 | +1 | +1 | +2 |
| Klimat (hög ambition ↔ låg prioritet) | −1 | −2 | −1 | −1 | 0 | +1 | +1 | +2 |
| Lag & ordning (förebyggande ↔ straffskärpning) | −2 | −1 | 0 | 0 | +1 | +1 | +2 | +2 |
| Välfärd (offentlig drift ↔ privat valfrihet) | −2 | −1 | −1 | +1 | +1 | +1 | +2 | 0 |
| EU (mer integration ↔ mindre överstatlighet) | +1 | −1 | 0 | −1 | −2 | 0 | 0 | +2 |
| Värderingar GAL–TAN (progressiv ↔ traditionell) | −2 | −2 | −1 | −1 | −1 | +1 | +1 | +2 |
| Energi (förnybart ↔ kärnkraft) | −1 | −2 | 0 | 0 | +1 | +2 | +2 | +2 |

### Kända spänningar som frågorna bör fånga

- **S vs V/MP om migration** — de rödgröna är splittrade; en migrationsfråga skiljer dem tydligt åt.
- **SD:s ekonomiska mittenprofil** — SD avviker från M/KD i t.ex. a-kassa och pensioner; rena skattefrågor räcker inte för att skilja SD från M.
- **C:s mellanposition** — liberal ekonomi + grön politik + generös migration; C fångas bara om kompassen har fler dimensioner än vänster–höger.
- **L:s EU-vänlighet** — mest EU-positiva partiet; en Euro/EU-fördjupningsfråga isolerar L.
- **KD vs M** — skiljs bäst av värderings- och familjepolitiska frågor samt sjukvårdens huvudmannaskap.
- **V vs S** — vinster i välfärden och skattenivåer skiljer dem tydligast.

## Verifieringschecklista före lansering

- [ ] Läs och koda respektive partis **valmanifest 2026** mot varje påstående i frågebanken.
- [ ] Komplettera med **riksdagsvoteringar** (riksdagens öppna data, `data.riksdagen.se`) där manifestet är vagt.
- [ ] Skicka **enkät till partikanslierna** med exakt samma påståenden som användarna får — partisvar är guldstandard.
- [ ] Dokumentera **källa per parti och fråga** i `data/` (fältet `source` i frågebanken).
- [ ] Låt minst två personer oberoende koda positionerna och jämför (interbedömarreliabilitet).
- [ ] Bevaka partiledarbyten och blockbyten fram till valdagen.
