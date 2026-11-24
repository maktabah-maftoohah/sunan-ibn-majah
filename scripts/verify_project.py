import json
from pathlib import Path

def test_project():
    root = Path(__file__).resolve().parent.parent
    assert (root / "index.html").exists(), "index.html missing"
    assert (root / "404.html").exists(), "404.html missing"
    assert (root / "AGENTS.md").exists(), "AGENTS.md missing"
    assert (root / ".nojekyll").exists(), ".nojekyll missing"
    assert (root / "manifest.webmanifest").exists(), "manifest.webmanifest missing"
    assert (root / "sw.js").exists(), "sw.js missing"
    assert (root / "icon.svg").exists(), "icon.svg missing"
    assert (root / "robots.txt").exists(), "robots.txt missing"
    assert (root / "sitemap.xml").exists(), "sitemap.xml missing"

    # Assets & Branding
    assert (root / "assets" / "og-banner.jpg").exists(), "og-banner.jpg missing"
    assert (root / "assets" / "logo.svg").exists(), "logo.svg missing"
    assert (root / "assets" / "logo.png").exists(), "logo.png missing"
    assert (root / "assets" / "logo-mark.svg").exists(), "logo-mark.svg missing"
    assert (root / "assets" / "logo-mark.png").exists(), "logo-mark.png missing"
    assert (root / "assets" / "github-avatar.png").exists(), "github-avatar.png missing"
    assert (root / "assets" / "site-banner.png").exists(), "site-banner.png missing"
    assert (root / "assets" / "icon-192.png").exists(), "icon-192.png missing"
    assert (root / "assets" / "icon-512.png").exists(), "icon-512.png missing"

    # Static OG stubs (Abd al-Baqi numbers)
    assert (root / "1" / "index.html").exists(), "Hadith 1 OG page stub missing"
    assert (root / "4341" / "index.html").exists(), "Hadith 4341 OG page stub missing"

    # Data files
    assert (root / "data" / "books.json").exists(), "books.json missing"
    assert (root / "data" / "collection.json").exists(), "collection.json missing"
    assert (root / "data" / "search-index.json").exists(), "search-index.json missing"
    assert (root / "data" / "numbering_index.json").exists(), "numbering_index.json missing"
    assert (root / "data" / "editions" / "manifest.json").exists(), "editions/manifest.json missing"

    with open(root / "data" / "books.json", "r", encoding="utf-8") as f:
        books = json.load(f)
        assert len(books) == 38, f"Expected 38 books, found {len(books)}"

    with open(root / "data" / "collection.json", "r", encoding="utf-8") as f:
        col = json.load(f)
        assert col.get("total_hadiths") == 4343, f"Expected 4343 hadiths, found {col.get('total_hadiths')}"
        assert col.get("default_numbering") == "abdul_baqi", "default_numbering must be abdul_baqi"

    print("Project structure & document verification PASSED for sunan-ibn-majah.")

if __name__ == "__main__":
    test_project()
