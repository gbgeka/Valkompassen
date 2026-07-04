# Bildkällor och ersättningsplan

## Status: platshållare

Bilderna i `assets/logos/` och `assets/leaders/` är **egengenererade SVG-platshållare** (logotypmärke med partibokstav i partiets färg, respektive porträttsilhuett med initialer). De är inte partiernas officiella logotyper eller foton.

Skälet: utvecklingsmiljöns nätverkspolicy blockerar externa bildkällor (Wikimedia Commons, partiernas webbplatser, TT), så riktiga bilder kunde inte hämtas automatiskt.

## Så ersätts de med riktiga bilder

Behåll filnamnen — dokument och `data/parties.json` pekar på dem.

### Partiloggor (`assets/logos/<id>.svg`)

Hämta officiella logotyper från respektive partis pressrum/grafiska profil:

| Fil | Parti | Pressrum |
|-----|-------|----------|
| `s.svg` | Socialdemokraterna | socialdemokraterna.se/press |
| `m.svg` | Moderaterna | moderaterna.se/press |
| `sd.svg` | Sverigedemokraterna | sd.se/press |
| `c.svg` | Centerpartiet | centerpartiet.se/press |
| `v.svg` | Vänsterpartiet | vansterpartiet.se/press |
| `kd.svg` | Kristdemokraterna | kristdemokraterna.se/press |
| `l.svg` | Liberalerna | liberalerna.se/press |
| `mp.svg` | Miljöpartiet | mp.se/press |

**OBS juridik:** partiloggor är varumärkesskyddade. Användning i en valkompass (nyhets-/upplysningssammanhang) är normalt okontroversiell, men kontrollera respektive partis riktlinjer för användning av grafiskt material innan publik lansering.

### Partiledarporträtt (`assets/leaders/<namn>.svg`)

Fritt licensierade porträtt finns på Wikimedia Commons (sök på namnet, välj CC BY/CC BY-SA-licensierad bild, ange fotograf enligt licensen) eller använd partiernas pressbilder (oftast fria för redaktionell användning med fotografangivelse):

- Magdalena Andersson (S), Ulf Kristersson (M), Jimmie Åkesson (SD), Elisabeth Thand Ringqvist (C), Nooshi Dadgostar (V), Ebba Busch (KD), Simona Mohamsson (L), Amanda Lind & Daniel Helldén (MP).

När en riktig bild läggs in: uppdatera denna fil med **källa, fotograf och licens** per bild.
