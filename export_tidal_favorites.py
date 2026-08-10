#!/usr/bin/env python3
"""Eksportér favoritter fra Min musiksamling i TIDAL.

Scriptet henter gemte numre, album og kunstnere via det uofficielle
Python-bibliotek tidalapi.

Hver kørsel opretter en tidsstemplet mappe under output/ med:

- tidal_favorites.json
- tidal_favorites.txt

Eksempel:

    output/2026-08-10T103045Z/
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import tidalapi


OUTPUT_ROOT = Path("output")
PAGE_SIZE = 1000


def create_output_directory() -> Path:
    """Opret og returnér en UTC-tidsstemplet mappe til denne eksport.

    Det kompakte ISO 8601-format gør mapperne kronologisk sorterbare:

        2026-08-10T103045Z
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    output_directory = OUTPUT_ROOT / timestamp
    output_directory.mkdir(parents=True, exist_ok=False)
    return output_directory


def get_attribute(item: Any, attribute: str) -> Any:
    """Hent en attribut uden at afbryde eksporten ved API-afvigelser."""
    try:
        return getattr(item, attribute, None)
    except Exception:
        return None


def item_to_dict(item: Any) -> dict[str, Any]:
    """Omsæt et TIDAL-objekt til en enkel, JSON-egnet ordbog.

    Forskellige objekttyper anvender ikke nødvendigvis de samme
    attributter. Funktionen medtager derfor kun værdier, som faktisk
    findes på det pågældende objekt.
    """
    result: dict[str, Any] = {}

    for attribute in ("id", "name", "title"):
        value = get_attribute(item, attribute)
        if value is not None:
            result[attribute] = value

    artist = get_attribute(item, "artist")
    if artist is not None:
        result["artist"] = get_attribute(artist, "name")

    album = get_attribute(item, "album")
    if album is not None:
        result["album"] = get_attribute(album, "name")

    return result


def export_favorites(
    fetch_function: Callable[[int, int], list[Any]],
    page_size: int = PAGE_SIZE,
) -> list[dict[str, Any]]:
    """Hent alle favoritter fra en sideinddelt TIDAL-funktion.

    Der hentes op til ``page_size`` elementer ad gangen. Hentningen
    fortsætter, indtil API'et returnerer en tom liste.
    """
    offset = 0
    exported_items: list[dict[str, Any]] = []

    while True:
        batch = fetch_function(page_size, offset)

        if not batch:
            break

        exported_items.extend(item_to_dict(item) for item in batch)
        offset += page_size

    return exported_items


def write_json(
    output_directory: Path,
    data: dict[str, list[dict[str, Any]]],
) -> Path:
    """Skriv den komplette eksport som UTF-8-kodet JSON."""
    output_file = output_directory / "tidal_favorites.json"

    output_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return output_file


def write_text(
    output_directory: Path,
    tracks: list[dict[str, Any]],
    albums: list[dict[str, Any]],
    artists: list[dict[str, Any]],
) -> Path:
    """Skriv en læsbar tekstoversigt over den komplette eksport."""
    lines: list[str] = []

    lines.append(f"Tracks: {len(tracks)}")
    for track in tracks:
        lines.append(
            " | ".join(
                (
                    str(track.get("name", "")),
                    str(track.get("artist", "")),
                    str(track.get("album", "")),
                )
            )
        )

    lines.append("")
    lines.append(f"Albums: {len(albums)}")
    for album in albums:
        lines.append(
            " | ".join(
                (
                    str(album.get("name", "")),
                    str(album.get("artist", "")),
                )
            )
        )

    lines.append("")
    lines.append(f"Artists: {len(artists)}")
    for artist in artists:
        lines.append(str(artist.get("name", "")))

    output_file = output_directory / "tidal_favorites.txt"
    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return output_file


def main() -> None:
    """Log ind, hent favoritter og skriv eksportfilerne."""
    print("Åbner login til TIDAL...")
    print("Åbn linket herunder (højreklik og vælg Åbn link).")
    print("Nu skulle du se et browservindue, hvori du kan logge ind på din konto.")
    print("Når browseren har godkendt dig hos TIDAL, hentes dine foretrukne numre, album og kunstnere.")

    session = tidalapi.Session()
    session.login_oauth_simple()

    favorites = tidalapi.Favorites(session, session.user.id)

    print("Henter gemte numre...")
    tracks = export_favorites(favorites.tracks)

    print("Henter gemte album...")
    albums = export_favorites(favorites.albums)

    print("Henter gemte kunstnere...")
    artists = export_favorites(favorites.artists)

    data = {
        "tracks": tracks,
        "albums": albums,
        "artists": artists,
    }

    output_directory = create_output_directory()
    json_file = write_json(output_directory, data)
    text_file = write_text(output_directory, tracks, albums, artists)

    print("")
    print("Eksport gennemført")
    print(f"Numre:      {len(tracks)}")
    print(f"Album:      {len(albums)}")
    print(f"Kunstnere:  {len(artists)}")
    print(f"JSON:       {json_file}")
    print(f"Tekst:      {text_file}")


if __name__ == "__main__":
    main()