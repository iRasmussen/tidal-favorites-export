import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from export_tidal_favorites import export_favorites, item_to_dict, write_json, write_text


class ExportFavoritesTests(unittest.TestCase):
    def test_fetches_all_pages_until_api_returns_empty_list(self):
        pages = {
            0: [SimpleNamespace(id=1, name="Sang 1")],
            2: [SimpleNamespace(id=2, name="Sang 2")],
            4: [],
        }
        calls = []

        def fetch(limit, offset):
            calls.append((limit, offset))
            return pages[offset]

        result = export_favorites(fetch, page_size=2)

        self.assertEqual(calls, [(2, 0), (2, 2), (2, 4)])
        self.assertEqual(result, [{"id": 1, "name": "Sang 1"}, {"id": 2, "name": "Sang 2"}])

    def test_item_to_dict_includes_available_artist_and_album_names(self):
        item = SimpleNamespace(
            id=42,
            title="Blå",
            artist=SimpleNamespace(name="Björk"),
            album=SimpleNamespace(name="Debut"),
        )

        self.assertEqual(
            item_to_dict(item),
            {"id": 42, "title": "Blå", "artist": "Björk", "album": "Debut"},
        )

    def test_writes_json_and_text_as_utf8(self):
        data = {
            "tracks": [{"name": "Blå", "artist": "Björk", "album": "Debut"}],
            "albums": [{"name": "Debut", "artist": "Björk"}],
            "artists": [{"name": "Björk"}],
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_directory = Path(temporary_directory)
            json_file = write_json(output_directory, data)
            text_file = write_text(
                output_directory,
                data["tracks"],
                data["albums"],
                data["artists"],
            )

            self.assertEqual(json.loads(json_file.read_text(encoding="utf-8")), data)
            self.assertIn("Björk", text_file.read_text(encoding="utf-8"))
            self.assertIn("Blå | Björk | Debut", text_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
