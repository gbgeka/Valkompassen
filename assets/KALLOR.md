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

### Ej på Wikimedia Commons — hotlänkas från externa källor

**S (rosen), SD (blåsippan) och MP (maskrosen)** finns inte fritt licensierade på Wikimedia
Commons. Deras officiella logotyper hotlänkas i stället från externa källor via `logoUrl` i
`data/parties.json`:

| Parti | Källa (logoUrl) |
|-------|-----------------|
| S | logopedia-wikin (`static.wikia.nocookie.net/logopedia/…/Socialdemokraternalogo2006-2010.png`) |
| MP | finska Wikipedia (`upload.wikimedia.org/wikipedia/fi/…/Miljöpartiet_logo.svg`) |
| SD | TT Nyhetsbyrån (`via.tt.se/data/images/…`) |

Dessa logotyper är **varumärkesskyddade** — kontrollera partiernas riktlinjer före publik
lansering. Om en extern bild inte laddar faller kortet automatiskt tillbaka till ett neutralt
bokstavsmärke i partifärg (`onerror`). Som lokal reserv finns dessutom egenritade, stiliserade
symboler (`assets/logos/s.svg`, `sd.svg`, `mp.svg`) — originalillustrationer, inte officiella
logotypfiler; de används om `logoUrl` tas bort så att `logo`-fältet tar över.

Verifierad fallgrop: `Social Democratic Party logo (2021).svg` på Commons är **brittiska**
SDP — använd den inte.

## Storlekshantering

Alla logotyper renderas i en fast 64×64-ruta (`object-fit: contain`) på ljus platta så att
olika proportioner ser enhetliga ut; porträtt beskärs till 52×52-cirkel
(`object-fit: cover`). Thumbnails begärs i 128 px (2× för skärpa). Om en extern bild inte
laddar faller sidan tillbaka till platshållaren automatiskt (`onerror`).
