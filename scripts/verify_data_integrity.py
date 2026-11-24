import json
import os
from pathlib import Path

def test_data_integrity():
    root = Path(__file__).resolve().parent.parent
    hadiths_dir = root / "data" / "hadiths"

    assert hadiths_dir.exists(), "data/hadiths/ directory missing"

    total_hadiths = 0
    book_files = sorted(hadiths_dir.glob("*.json"))
    assert len(book_files) == 38, f"Expected 38 book files (00 to 37), found {len(book_files)}"

    for bf in book_files:
        with open(bf, "rb") as raw_f:
            bom_check = raw_f.read(3)
            assert bom_check != b"\xef\xbb\xbf", f"UTF-8 BOM detected in {bf.name}"

        with open(bf, "r", encoding="utf-8") as f:
            hadiths = json.load(f)

        assert len(hadiths) > 0, f"Empty book file: {bf.name}"

        for h in hadiths:
            total_hadiths += 1
            assert h.get("collection_id") == "sunan-ibn-majah", f"Invalid collection_id in {h}"
            assert "hadith_number" in h, f"Missing hadith_number in {h}"
            assert "book_number" in h, f"Missing book_number in {h}"
            assert 0 <= h["book_number"] <= 37, f"Book number out of bounds: {h['book_number']}"
            assert "arabic" in h and len(h["arabic"].strip()) > 0, f"Empty arabic text in Hadith #{h.get('hadith_number')}"
            assert "book_title" in h and "ar" in h["book_title"] and "ms" in h["book_title"], f"Incomplete book_title in {h}"
            assert "gradings" in h and len(h["gradings"]) > 0, f"Missing gradings in Hadith #{h.get('hadith_number')}"
            assert "translations" in h, f"Missing translations in Hadith #{h.get('hadith_number')}"

            # Verify numbering systems
            num_obj = h.get("numbering")
            assert num_obj is not None, f"Missing numbering object in Hadith #{h.get('hadith_number')}"
            assert "abdul_baqi" in num_obj, f"Missing abdul_baqi numbering in Hadith #{h.get('hadith_number')}"
            assert "in_book" in num_obj, f"Missing in_book numbering in Hadith #{h.get('hadith_number')}"
            assert "darussalam" in num_obj, f"Missing darussalam numbering in Hadith #{h.get('hadith_number')}"
            assert "alamiyah" in num_obj, f"Missing alamiyah numbering in Hadith #{h.get('hadith_number')}"
            assert "universal" in num_obj, f"Missing universal numbering in Hadith #{h.get('hadith_number')}"

    assert total_hadiths == 4343, f"Expected 4343 hadiths in total, found {total_hadiths}"

    # Verify books.json
    books_file = root / "data" / "books.json"
    with open(books_file, "r", encoding="utf-8") as f:
        books = json.load(f)
    assert len(books) == 38, f"Expected 38 books in books.json, found {len(books)}"
    assert sum(b["hadith_count"] for b in books) == 4343, "Total book hadith_count sum mismatch"

    # Verify search-index.json
    s_idx = root / "data" / "search-index.json"
    with open(s_idx, "r", encoding="utf-8") as f:
        tokens = json.load(f)
    assert len(tokens) == 4343, f"Expected 4343 tokens in search-index.json, found {len(tokens)}"

    # Verify numbering_index.json
    num_idx_file = root / "data" / "numbering_index.json"
    assert num_idx_file.exists(), "numbering_index.json missing"
    with open(num_idx_file, "r", encoding="utf-8") as f:
        num_data = json.load(f)
    assert num_data.get("default_numbering") == "abdul_baqi", "Default numbering must be abdul_baqi"
    assert len(num_data.get("abdul_baqi_to_universal", {})) == 4343, "abdul_baqi_to_universal count mismatch"

    print("Data integrity verification PASSED! All 4,343 hadiths across 38 books verified with 'Abd al-Baqi default numbering conforming to Maktabah Maftoohah schema.")

if __name__ == "__main__":
    test_data_integrity()
