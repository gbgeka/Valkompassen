# Bildkällor

## Partiledarfoton — Wikimedia Commons (hotlänkade)

Foton hotlänkas via `https://commons.wikimedia.org/wiki/Special:FilePath/<filnamn>?width=…`.
Samtliga är fritt licensierade (CC BY / CC BY-SA / motsvarande) — kontrollera exakt licens
och fotograf på respektive filsida före tryck/vidarespridning utanför webben.

| Person | Parti | Commons-fil |
|--------|-------|-------------|
| Magdalena Andersson | S | `Magdalena Andersson in 2022 (cropped).jpg` |
| Ulf Kristersson | M | `Ulf Kristersson January 2023.jpg` |
| Jimmie Åkesson | SD | `Jimmie Åkesson (cropped).jpg` |
| Elisabeth Thand Ringqvist | C | `ElisabethTR2.jpg` (Centerpartiet/Margoåå0, CC BY-SA 4.0) |
| Nooshi Dadgostar | V | `Nooshi Dadgostar (V) in 2021 (cropped).jpg` |
| Ebba Busch | KD | `Deputy Prime Minister of Sweden, Ebba Busch, in 2024.jpg` |
| Simona Mohamsson | L | `Simona Mohamsson June 2025 (cropped).jpg` |
| Amanda Lind | MP | `Amanda Lind in 2023.jpg` |
| Daniel Helldén | MP | `Daniel Helldén (MP) 2018.jpg` |

Filsida: `https://commons.wikimedia.org/wiki/File:<filnamn med _ i st.f. mellanslag>`

## Partisymboler

### Fritt licensierade på Commons (hotlänkade)

| Parti | Commons-fil |
|-------|-------------|
| V | `Vänsterpartiet logo.svg` |
| C | `Centerpartiet.svg` |
| L | `Liberals (Sweden) logo.svg` |
| KD | `Kd v1.svg` |
| M | `Moderata samlingspartiet Logo.svg` |

### Ej på Wikimedia Commons — lokalt lagrade officiella logotyper

**S (rosen), SD (blåsippan) och MP (maskrosen)** finns inte fritt licensierade på Wikimedia
Commons. Deras officiella logotyper lagras i stället lokalt i `assets/logos/` och pekas ut via
`logo`-fältet i `data/parties.json`:

| Parti | Lokal fil | Ursprung |
|-------|-----------|----------|
| S | `assets/logos/s.png` | logopedia-wikin (Socialdemokraternalogo2006-2010) |
| MP | `assets/logos/mp.svg` | finska Wikipedia (Miljöpartiet_logo) |
| SD | `assets/logos/sd.png` | TT Nyhetsbyrån |

Dessa logotyper är **varumärkesskyddade** — kontrollera partiernas riktlinjer före publik
lansering. Om en lokal fil saknas eller inte laddar faller kortet automatiskt tillbaka till ett
neutralt bokstavsmärke i partifärg (`onerror`).

Verifierad fallgrop: `Social Democratic Party logo (2021).svg` på Commons är **brittiska**
SDP — använd den inte.

## Storlekshantering

Alla logotyper renderas i en fast 64×64-ruta (`object-fit: contain`) på ljus platta så att
olika proportioner ser enhetliga ut; porträtt beskärs till 52×52-cirkel
(`object-fit: cover`). Thumbnails begärs i 128 px (2× för skärpa). Om en extern bild inte
laddar faller sidan tillbaka till platshållaren automatiskt (`onerror`).
