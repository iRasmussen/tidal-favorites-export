# TIDAL Favorites Export

Et Python-script, der eksporterer gemte numre, album og kunstnere fra **Min musiksamling** i TIDAL.

Du kan lære mere om Python i [Python-vejledningen](https://www.w3schools.com/python/) hos W3Schools.

Eksporten gemmes lokalt som både struktureret JSON og en læsbar tekstfil. Hver kørsel får sin egen mappe med et UTC-tidsstempel.

> Projektet anvender det uofficielle Python-bibliotek `tidalapi` og er ikke udviklet, godkendt eller understøttet af TIDAL.

## Funktioner

- Eksporterer gemte numre, album og kunstnere.
- Henter hele samlingen i sideinddelte portioner.
- Bevarer danske og andre internationale tegn i UTF-8.
- Gemmer data som både JSON og almindelig tekst.
- Opretter en særskilt tidsstemplet mappe for hver kørsel.
- Overskriver ikke tidligere eksporter.

## Krav

- Python 3.9 eller nyere
- Et aktivt TIDAL-login
- Internetforbindelse under eksporten

## Installation

Klon repositoryet, og gå ind i projektmappen:

```bash
git clone https://github.com/iRasmussen/tidal-favorites-export.git
cd tidal-favorites-export
```

Opret et virtuelt Python-miljø:

```bash
python3 -m venv .venv
```

Aktivér miljøet på macOS eller Linux:

```bash
source .venv/bin/activate
```

Installér afhængighederne:

```bash
python3 -m pip install -r requirements.txt
```

## Brug

Start eksporten fra projektets rodmappe:

```bash
python3 export_tidal_favorites.py
```

Scriptet åbner et OAuth-login til TIDAL. Efter godkendelsen hentes de gemte numre, album og kunstnere.

Når eksporten er færdig, viser Terminal antallet af eksporterede elementer og placeringen af de to outputfiler.

## Resultatfiler

Hver kørsel opretter en tidsstemplet mappe under `output/`:

```text
output/
└── 2026-08-10T120500Z/
    ├── tidal_favorites.json
    └── tidal_favorites.txt
```

Mappenavnet følger et kompakt ISO 8601-format:

```text
ÅÅÅÅ-MM-DDTHHMMSSZ
```

`Z` betyder, at tidspunktet er angivet i UTC (Coordinated Universal Time), en fælles tidsstandard uafhængig af lokale tidszoner.

### Sådan foregår eksporten

1. Scriptet beder TIDAL om et login. OAuth åbner en sikker godkendelse hos TIDAL, så scriptet kan få adgang til din samling uden at bede om din adgangskode.
2. Scriptet henter numre, album og kunstnere i sideinddelte portioner. Sideinddeling betyder, at samlingen hentes i mindre bidder i stedet for én stor forespørgsel.
3. Når alle sider er hentet, gemmes dataene i JSON og tekst i en ny mappe under `output/`.

### Forventet resultat

Terminalen viser først login- og hentevejledninger. Når eksporten er færdig, vises en oversigt, for eksempel:

```text
Eksport gennemført
Numre:      125
Album:      18
Kunstnere:  9
JSON:       output/2026-08-10T120500Z/tidal_favorites.json
Tekst:      output/2026-08-10T120500Z/tidal_favorites.txt
```

Antallene afhænger af din samling. Tekstfilens overskrifter er `Numre`, `Album` og `Kunstnere`; JSON-filens nøgler er fortsat `tracks`, `albums` og `artists`.

### Fejlsøgning og kontrol efter kørslen

- **Login åbner ikke eller bliver ikke godkendt:** Følg linket, som vises i Terminal, gennemfør godkendelsen i browseren, og prøv igen. Kontrollér, at du logger ind på den ønskede TIDAL-konto.
- **Hentningen fejler eller stopper:** Kontrollér internetforbindelsen, og prøv igen. Fejl fra login eller netværk vises i Terminal; hvis problemet fortsætter, notér fejlmeddelelsen.
- **En kategori viser 0:** Det kan betyde, at der ikke er gemt noget i den kategori på kontoen. Kontrollér samlingen i TIDAL.
- **Kontrollér en gennemført eksport:** Find den nyeste tidsstemplede mappe i `output/`. Tjek, at begge filer findes, at JSON-filen kan åbnes og indeholder `tracks`, `albums` og `artists`, og at antallene passer med oversigten i Terminal. Tekstfilen giver en letlæselig kontrol af titler og navne.

### JSON

`tidal_favorites.json` indeholder tre samlinger:

```json
{
  "tracks": [],
  "albums": [],
  "artists": []
}
```

Formatet er velegnet til videre behandling, søgning og sammenligning mellem eksporter.

### Tekst

`tidal_favorites.txt` indeholder en almindeligt læsbar oversigt med:

- antal gemte numre under overskriften `Numre`
- numrenes titel, kunstner og album
- antal gemte album under overskriften `Album`
- albummets titel og kunstner
- antal gemte kunstnere under overskriften `Kunstnere`
- kunstnernes navne

## Projektstruktur

```text
tidal-favorites-export/
├── export_tidal_favorites.py
├── output/
│   └── .gitkeep
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── requirements.txt
└── VERSION
```

- `export_tidal_favorites.py`: Selve eksportscriptet.
- `output/`: Lokale, genererede eksportfiler.
- `requirements.txt`: Projektets Python-afhængigheder.
- `CHANGELOG.md`: Ændringer mellem offentliggjorte versioner.
- `VERSION`: Projektets aktuelle versionsnummer.

## Privatliv og sikkerhed

Indholdet af `output/` versionsstyres ikke.

Eksportfilerne kan afspejle personlige musikvaner og bør gennemgås, før de deles med andre. Følgende må ikke lægges i repositoryet:

- eksporterede musikdata
- adgangstokens
- sessionsdata
- loginoplysninger
- lokale miljøfiler

Projektets `.gitignore` udelukker blandt andet:

```text
output/*
.env
.venv/
```

Filen `output/.gitkeep` bevarer den tomme outputmappe i Git uden at medtage dens indhold.

## Begrænsninger

- Projektet eksporterer metadata, ikke musik- eller billedfiler.
- Projektet anvender et uofficielt API-bibliotek.
- Ændringer i TIDAL eller `tidalapi` kan påvirke scriptets funktion.
- Eksporten er et lokalt øjebliksbillede og synkroniseres ikke automatisk.

## Version

Version: 1008a

Se [CHANGELOG.md](CHANGELOG.md) for ændringer mellem versionerne.

## Licens

Projektets egen kildekode udgives under MIT-licensen. Se LICENSE.

TIDAL-navnet og metadata fra tjenesten tilhører deres respektive rettighedshavere.
