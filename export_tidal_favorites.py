#!/usr/bin/env python3
import json
from pathlib import Path
import tidalapi

OUT = Path("output")
OUT.mkdir(exist_ok=True)

def item_to_dict(item):
    d = {}
    for key in ["id", "name", "title"]:
        if hasattr(item, key):
            try:
                d[key] = getattr(item, key)
            except Exception:
                pass
    if hasattr(item, "artist") and item.artist:
        try:
            d["artist"] = getattr(item.artist, "name", None)
        except Exception:
            pass
    if hasattr(item, "album") and item.album:
        try:
            d["album"] = getattr(item.album, "name", None)
        except Exception:
            pass
    return d

def export_favorites(collection, fetch_fn, kind, limit=1000):
    offset = 0
    items = []
    while True:
        batch = fetch_fn(limit, offset)
        if not batch:
            break
        for x in batch:
            items.append(item_to_dict(x))
        offset += limit
    return items

def main():
    session = tidalapi.Session()
    session.login_oauth_simple()
    favorites = tidalapi.Favorites(session, session.user.id)

    tracks = export_favorites(favorites, favorites.tracks, "tracks")
    albums = export_favorites(favorites, favorites.albums, "albums")
    artists = export_favorites(favorites, favorites.artists, "artists")

    data = {
        "tracks": tracks,
        "albums": albums,
        "artists": artists,
    }

    (OUT / "tidal_favorites.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    lines = []
    lines.append(f"Tracks: {len(tracks)}")
    for t in tracks:
        lines.append(
            f"{t.get('name', '')} — {t.get('artist', '')} — {t.get('album', '')}"
        )

    lines.append("")
    lines.append(f"Albums: {len(albums)}")
    for a in albums:
        lines.append(f"{a.get('name', '')} — {a.get('artist', '')}")

    lines.append("")
    lines.append(f"Artists: {len(artists)}")
    for a in artists:
        lines.append(a.get("name", ""))

    (OUT / "tidal_favorites.txt").write_text("\n".join(lines), encoding="utf-8")

    print("Done")
    print(f"Tracks:  {len(tracks)}")
    print(f"Albums:  {len(albums)}")
    print(f"Artists: {len(artists)}")

if __name__ == "__main__":
    main()
