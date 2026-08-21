# TIDAL Favorites Export

Et Python-script, der eksporterer gemte numre, album og kunstnere fra **Min musiksamling** i TIDAL.

Du kan lære om Python på [Python Tutorial](https://www.w3schools.com/python/) hos W3Schools.


Eksporten gemmes lokalt som både struktureret JSON og en læsbar tekstfil. Hver kørsel placeres i sin egen UTC-tidsstemplede mappe.

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

## Output

Hver kørsel opretter en UTC-tidsstemplet mappe under `output/`:

```text
output/
└── 2026-08-10T120500Z/
    ├── tidal_favorites.json
    └── tidal_favorites.txt
```

Tidsstemplet følger et kompakt ISO 8601-format:

```text
ÅÅÅÅ-MM-DDTHHMMSSZ
```

`Z` angiver, at tidspunktet er registreret i UTC.

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

- antal gemte numre
- numrenes titel, kunstner og album
- antal gemte album
- albummets titel og kunstner
- antal gemte kunstnere
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

Version: 0810a

Se [CHANGELOG.md](CHANGELOG.md) for ændringer mellem versionerne.

## Licens

Projektets egen kildekode udgives under MIT-licensen. Se LICENSE.

TIDAL-navnet og metadata fra tjenesten tilhører deres respektive rettighedshavere.
