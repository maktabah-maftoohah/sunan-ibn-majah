#!/usr/bin/env python3
"""
scripts/generate_og_pages.py
Generates static Open Graph preview and redirect stubs for all hadiths in Sunan Ibn Majah
using Muhammad Fu'ad 'Abd al-Baqi canonical numbering (Default: 1 to 4341 + sub-hadiths).
Enables rich unfurling on WhatsApp, Facebook, Telegram, Twitter/X, Discord, and search engines
while redirecting human visitors into the SPA reading view with smooth scroll & highlight.
Also updates robots.txt and sitemap.xml.
"""

import html
import json
import os
import shutil
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
HADITHS_DIR = ROOT_DIR / "data" / "hadiths"

def clean_og_pages():
    cleaned = 0
    for entry in ROOT_DIR.iterdir():
        if entry.is_dir() and (entry.name.isdigit() or entry.name.replace('.', '', 1).isdigit()):
            shutil.rmtree(entry)
            cleaned += 1
    print(f"Cleaned {cleaned} generated hadith directory trees.")

def main():
    if "--clean" in sys.argv:
        clean_og_pages()
        return

    start_time = time.time()
    base_url = "https://maktabah-maftoohah.github.io/sunan-ibn-majah"
    banner_url = f"{base_url}/assets/og-banner.jpg"

    total_hadiths = 0
    hadith_files = sorted(HADITHS_DIR.glob("*.json"))
    sitemap_entries = [
        f"""  <url>
    <loc>{base_url}/</loc>
    <xhtml:link rel="alternate" hreflang="ms" href="{base_url}/?lang=ms" />
    <xhtml:link rel="alternate" hreflang="en" href="{base_url}/?lang=en" />
    <xhtml:link rel="alternate" hreflang="ar" href="{base_url}/?lang=ar" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{base_url}/" />
    <lastmod>{time.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]

    print(f"Scanning {len(hadith_files)} book shard files...")

    for hf in hadith_files:
        with open(hf, "r", encoding="utf-8") as f:
            hadiths = json.load(f)

        for h in hadiths:
            # Default numbering is Muhammad Fu'ad 'Abd al-Baqi
            ab_val = h.get("numbering", {}).get("abdul_baqi") or h.get("hadith_number")
            if ab_val is None:
                continue

            h_str = str(int(ab_val)) if isinstance(ab_val, (int, float)) and float(ab_val).is_integer() else str(ab_val)

            target_dir = ROOT_DIR / h_str
            target_dir.mkdir(parents=True, exist_ok=True)
            out_file = target_dir / "index.html"

            book_title_ms = h.get("book_title", {}).get("ms") or f"Kitab {h.get('book_number')}"
            book_title_ar = h.get("book_title", {}).get("ar") or ""
            in_book = h.get("in_book_number")
            in_book_text = f" : Hadis {in_book}" if in_book else ""

            ar_text = h.get("arabic", "").strip()
            ar_snippet = (ar_text[:140] + "...") if len(ar_text) > 140 else ar_text

            trans_ms = h.get("translations", {}).get("ms") or h.get("translations", {}).get("en") or ""
            trans_snippet = (trans_ms[:180] + "...") if len(trans_ms) > 180 else trans_ms

            page_title = f"Sunan Ibn Majah #{h_str} ('Abd al-Baqi) — Maktabah Maftoohah"
            og_title = f"Sunan Ibn Majah #{h_str} ({book_title_ms})"
            og_desc = f"{ar_snippet} — {trans_snippet}"
            og_url = f"{base_url}/{h_str}/"

            gradings_str = ", ".join([f"{g.get('scholar')}: {g.get('grade')}" for g in h.get("gradings", [])])

            redirect_target = f"../?ref={h_str}"

            html_content = f"""<!DOCTYPE html>
<html lang="ms">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(page_title)}</title>

  <!-- Open Graph & Twitter Social Card Meta Tags -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Maktabah Maftoohah — Sunan Ibn Majah">
  <meta property="og:title" content="{html.escape(og_title)}">
  <meta property="og:description" content="{html.escape(og_desc)}">
  <meta property="og:image" content="{banner_url}">
  <meta property="og:image:secure_url" content="{banner_url}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html.escape(og_title)}">
  <meta property="og:url" content="{og_url}">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(og_title)}">
  <meta name="twitter:description" content="{html.escape(og_desc)}">
  <meta name="twitter:image" content="{banner_url}">

  <!-- SEO Canonical & Hreflang Alternates -->
  <link rel="canonical" href="{og_url}">
  <link rel="alternate" hreflang="ms" href="{base_url}/?ref={h_str}&amp;lang=ms">
  <link rel="alternate" hreflang="en" href="{base_url}/?ref={h_str}&amp;lang=en">
  <link rel="alternate" hreflang="ar" href="{base_url}/?ref={h_str}&amp;lang=ar">
  <link rel="alternate" hreflang="x-default" href="{og_url}">

  <!-- Schema.org JSON-LD Structured Data for Crawlers & LLMs -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "{og_url}"
    }},
    "headline": "{html.escape(og_title)}",
    "description": "{html.escape(og_desc)}",
    "image": "{banner_url}",
    "inLanguage": "ms",
    "author": {{
      "@type": "Person",
      "name": "Imam Ibn Majah (محمد بن يزيد القزويني)"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Maktabah Maftoohah",
      "url": "https://maktabah-maftoohah.github.io/"
    }},
    "articleSection": "{html.escape(book_title_ms)}",
    "keywords": "Hadis, Sunan Ibn Majah, Abd al-Baqi, Kutub as-Sittah, Maktabah Maftoohah, Takhrij, Sahih"
  }}
  </script>

  <!-- Instant SPA redirection with search-engine fallback -->
  <meta http-equiv="refresh" content="0; url={redirect_target}">
  <script>
    window.location.replace("{redirect_target}");
  </script>
</head>
<body style="font-family: system-ui, -apple-system, sans-serif; background: #041b14; color: #f8fafc; padding: 2rem; max-width: 800px; margin: 0 auto; line-height: 1.8;">
  <div style="background: #09261d; border: 1px solid #14533d; border-radius: 12px; padding: 2rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #14533d; padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
      <span style="background: #047857; color: #ffffff; padding: 0.25rem 0.75rem; border-radius: 6px; font-weight: 700; font-size: 0.9rem;">
        Sunan Ibn Majah #{h_str} (Piawaian 'Abd al-Baqi)
      </span>
      <span style="color: #6ee7b7; font-size: 0.85rem;">Kitab {h.get('book_number')}{in_book_text}</span>
    </div>

    <h2 style="color: #f59e0b; margin-top: 0; font-size: 1.15rem;">{html.escape(book_title_ms)} ({html.escape(book_title_ar)})</h2>

    <p dir="rtl" style="font-family: 'Amiri', serif; font-size: 1.6rem; line-height: 2.2; color: #f8fafc; text-align: right; margin: 1.5rem 0; border-bottom: 1px dashed #14533d; padding-bottom: 1.5rem;">
      {html.escape(ar_text)}
    </p>

    <div style="margin: 1.25rem 0;">
      <h3 style="color: #34d399; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Terjemahan Bahasa Melayu:</h3>
      <p style="color: #cbd5e1; font-size: 1rem;">{html.escape(trans_ms)}</p>
    </div>

    <div style="margin: 1rem 0; font-size: 0.85rem; color: #94a3b8;">
      <strong>Takhrij Ulama:</strong> {html.escape(gradings_str)}
    </div>

    <p style="margin-top: 2rem; font-size: 0.9rem; text-align: center;">
      <a href="{redirect_target}" style="display: inline-block; background: #047857; color: #ffffff; text-decoration: none; padding: 0.65rem 1.25rem; border-radius: 8px; font-weight: 600;">
        Buka dalam Pembaca Digital Maktabah Maftoohah &rarr;
      </a>
    </p>
  </div>
</body>
</html>
"""
            out_file.write_text(html_content, encoding="utf-8")
            total_hadiths += 1

            sitemap_entries.append(f"""  <url>
    <loc>{og_url}</loc>
    <xhtml:link rel="alternate" hreflang="ms" href="{base_url}/?ref={h_str}&amp;lang=ms" />
    <xhtml:link rel="alternate" hreflang="en" href="{base_url}/?ref={h_str}&amp;lang=en" />
    <xhtml:link rel="alternate" hreflang="ar" href="{base_url}/?ref={h_str}&amp;lang=ar" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{og_url}" />
    <lastmod>{time.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    # Write sitemap.xml
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(sitemap_entries)}
</urlset>
"""
    (ROOT_DIR / "sitemap.xml").write_text(sitemap_content, encoding="utf-8")
    print(f"  • Generated sitemap.xml with {len(sitemap_entries)} URLs")

    # Update robots.txt
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml
"""
    (ROOT_DIR / "robots.txt").write_text(robots_content, encoding="utf-8")
    print("  • Updated robots.txt")

    elapsed = time.time() - start_time
    print(f"\n[SUCCESS] Generated {total_hadiths} static OG preview pages for Sunan Ibn Majah in {elapsed:.2f}s.")

if __name__ == "__main__":
    main()
