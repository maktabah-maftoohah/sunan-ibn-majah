#!/usr/bin/env python3
"""
scripts/generate_branding.py
Generates the official Maktabah Maftoohah visual identity for Sunan Ibn Majah:
1. assets/logo-mark.svg & logo-mark.png (512x512 Standalone Emblem)
2. assets/github-avatar.svg, github-avatar.png, avatar.png (512x512 Circle-Safe GitHub Avatar)
3. assets/logo.svg & logo.png (800x200 Horizontal Brand Lockup)
4. assets/site-banner.svg & site-banner.png (1280x640 GitHub Repository Social Preview)
5. assets/og-banner.jpg (1280x640 High-Res Open Graph Banner)
6. assets/icon-192.png & icon-512.png (PWA Manifest Icons)
7. root icon.svg
"""

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

CHROME_EXEC = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
PLAYWRIGHT_DIR = "D:/RepoTools/GitHub/maktabah-maftoohah/al-quran/node_modules"

def build_logo_mark_svg() -> str:
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Background Gradient (Deep Emerald Forest) -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#064e3b" />
      <stop offset="50%" stop-color="#043829" />
      <stop offset="100%" stop-color="#021c14" />
    </linearGradient>

    <!-- Regal Gold Gradient -->
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef3c7" />
      <stop offset="25%" stop-color="#fde68a" />
      <stop offset="50%" stop-color="#f59e0b" />
      <stop offset="75%" stop-color="#d97706" />
      <stop offset="100%" stop-color="#92400e" />
    </linearGradient>

    <!-- Mint Emerald Glow Radial -->
    <radialGradient id="mintAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.4" />
      <stop offset="60%" stop-color="#047857" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#064e3b" stop-opacity="0" />
    </radialGradient>

    <!-- Book Page Gradient -->
    <linearGradient id="pageGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#fef9c3" />
      <stop offset="48%" stop-color="#ffffff" />
      <stop offset="52%" stop-color="#e2e8f0" />
      <stop offset="100%" stop-color="#fef9c3" />
    </linearGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&amp;family=Inter:wght@600;700;800&amp;display=swap');
      .ar-title { font-family: 'Amiri', 'Traditional Arabic', serif; font-weight: 700; }
      .latin-brand { font-family: 'Inter', -apple-system, sans-serif; }
    </style>
  </defs>

  <!-- Base Rounded Container (Squircle) -->
  <rect width="512" height="512" rx="108" fill="url(#bgGrad)" />
  <rect width="496" height="496" x="8" y="8" rx="100" fill="none" stroke="url(#goldGrad)" stroke-width="2.5" stroke-opacity="0.85" />
  <rect width="480" height="480" x="16" y="16" rx="92" fill="none" stroke="#34d399" stroke-width="1" stroke-opacity="0.4" />

  <!-- Ambient Mint Aura -->
  <circle cx="256" cy="240" r="190" fill="url(#mintAura)" />

  <!-- Outer Islamic 8-Point Geometric Star (Rub el Hizb) Background -->
  <g transform="translate(256, 240)" opacity="0.25" stroke="url(#goldGrad)" stroke-width="2" fill="none">
    <rect x="-140" y="-140" width="280" height="280" rx="20" />
    <rect x="-140" y="-140" width="280" height="280" rx="20" transform="rotate(45)" />
    <circle r="152" stroke="#34d399" stroke-width="1.5" stroke-dasharray="6 6" />
  </g>

  <!-- Central Open Hadith Tome / Manuscript -->
  <g id="HadithBook" transform="translate(256, 225)">
    <!-- Book Drop Shadow -->
    <ellipse cx="0" cy="98" rx="130" ry="16" fill="#000000" opacity="0.45" />

    <!-- Open Book Cover (Leather Moroccan Emerald) -->
    <path d="M-132,78 Q-66,94 0,82 Q66,94 132,78 L138,-52 Q66,-36 0,-48 Q-66,-36 -138,-52 Z" 
          fill="#065f46" stroke="url(#goldGrad)" stroke-width="3" />

    <!-- Book Inner Pages (Cream & White Parchment) -->
    <path d="M-124,70 Q-62,84 0,74 Q62,84 124,70 L130,-44 Q62,-30 0,-40 Q-62,-30 -130,-44 Z" 
          fill="url(#pageGrad)" stroke="#cbd5e1" stroke-width="1" />

    <!-- Book Spine Center Fold & Shading -->
    <path d="M-6,-40 Q0,-42 6,-40 L6,74 Q0,76 -6,74 Z" fill="#94a3b8" opacity="0.6" />
    <line x1="0" y1="-41" x2="0" y2="75" stroke="#047857" stroke-width="2" />

    <!-- Manuscript Text Ruling Lines (Gold Ink) -->
    <line x1="-105" y1="-18" x2="-22" y2="-12" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="-110" y1="2" x2="-22" y2="8" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="-105" y1="22" x2="-22" y2="28" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="-95" y1="42" x2="-35" y2="48" stroke="#d97706" stroke-width="2" stroke-linecap="round" opacity="0.6" />

    <line x1="22" y1="-12" x2="105" y2="-18" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="22" y1="8" x2="110" y2="2" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="22" y1="28" x2="105" y2="22" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="35" y1="48" x2="95" y2="42" stroke="#d97706" stroke-width="2" stroke-linecap="round" opacity="0.6" />

    <!-- Silk Bookmark Ribbon -->
    <path d="M-5,-42 Q-3,10 8,88 L22,96 L16,84 Q4,10 5,-42 Z" fill="#d97706" stroke="#b45309" stroke-width="1" />
    <polygon points="8,88 22,96 17,90 22,84" fill="#fbbf24" />
  </g>

  <!-- Arabic Calligraphy Inscription -->
  <text x="256" y="375" text-anchor="middle" class="ar-title" font-size="46" fill="url(#goldGrad)" letter-spacing="1">سُنَنُ ابْنِ مَاجَه</text>

  <!-- Subtitle Ribbon Badge -->
  <g transform="translate(256, 432)">
    <rect x="-145" y="-18" width="290" height="34" rx="10" fill="#064e3b" stroke="url(#goldGrad)" stroke-width="1.5" />
    <circle cx="-120" cy="-1" r="3" fill="#fbbf24" />
    <circle cx="120" cy="-1" r="3" fill="#fbbf24" />
    <text x="0" y="5" text-anchor="middle" class="latin-brand" font-size="14.5" font-weight="700" fill="#34d399" letter-spacing="2.5">MAKTABAH MAFTOOHAH</text>
  </g>
</svg>'''

def build_github_avatar_svg() -> str:
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <clipPath id="circleClip">
      <circle cx="256" cy="256" r="256" />
    </clipPath>

    <linearGradient id="avBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#064e3b" />
      <stop offset="50%" stop-color="#043829" />
      <stop offset="100%" stop-color="#021c14" />
    </linearGradient>

    <linearGradient id="avGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a" />
      <stop offset="35%" stop-color="#f59e0b" />
      <stop offset="70%" stop-color="#d97706" />
      <stop offset="100%" stop-color="#78350f" />
    </linearGradient>

    <radialGradient id="avGlow" cx="50%" cy="45%" r="48%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.4" />
      <stop offset="65%" stop-color="#047857" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#064e3b" stop-opacity="0" />
    </radialGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&amp;family=Inter:wght@600;700;800&amp;display=swap');
      .ar-avatar { font-family: 'Amiri', 'Traditional Arabic', serif; font-weight: 700; }
      .latin-avatar { font-family: 'Inter', -apple-system, sans-serif; font-weight: 800; }
    </style>
  </defs>

  <g clip-path="url(#circleClip)">
    <rect width="512" height="512" fill="url(#avBg)" />

    <circle cx="256" cy="256" r="248" fill="none" stroke="url(#avGold)" stroke-width="4" stroke-opacity="0.9" />
    <circle cx="256" cy="256" r="236" fill="none" stroke="#34d399" stroke-width="1.5" stroke-opacity="0.4" stroke-dasharray="8 6" />

    <circle cx="256" cy="220" r="160" fill="url(#avGlow)" />

    <g transform="translate(256, 185) scale(0.88)">
      <ellipse cx="0" cy="85" rx="110" ry="14" fill="#000000" opacity="0.45" />

      <path d="M-115,68 Q-58,82 0,72 Q58,82 115,68 L120,-45 Q58,-32 0,-42 Q-58,-32 -120,-45 Z" 
            fill="#065f46" stroke="url(#avGold)" stroke-width="3" />

      <path d="M-108,60 Q-54,72 0,64 Q54,72 108,60 L113,-38 Q54,-26 0,-35 Q-54,-26 -113,-38 Z" 
            fill="#fefce8" stroke="#cbd5e1" stroke-width="1" />

      <line x1="0" y1="-35" x2="0" y2="65" stroke="#047857" stroke-width="2" />

      <line x1="-92" y1="-14" x2="-20" y2="-9" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />
      <line x1="-96" y1="4" x2="-20" y2="9" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />
      <line x1="-92" y1="22" x2="-20" y2="27" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />

      <line x1="20" y1="-9" x2="92" y2="-14" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />
      <line x1="20" y1="9" x2="96" y2="4" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />
      <line x1="20" y1="27" x2="92" y2="22" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />

      <path d="M-4,-36 Q-2,8 6,76 L18,84 L14,72 Q3,8 4,-36 Z" fill="#d97706" stroke="#b45309" stroke-width="1" />
    </g>

    <text x="256" y="340" text-anchor="middle" class="ar-avatar" font-size="44" fill="url(#avGold)">سُنَنُ ابْنِ مَاجَه</text>
    <text x="256" y="380" text-anchor="middle" class="latin-avatar" font-size="16.5" fill="#f8fafc" letter-spacing="3.5">SUNAN IBN MAJAH</text>

    <g transform="translate(256, 422)">
      <rect x="-115" y="-14" width="230" height="28" rx="8" fill="#064e3b" stroke="#34d399" stroke-width="1.2" />
      <circle cx="-95" cy="0" r="2.5" fill="#fbbf24" />
      <circle cx="95" cy="0" r="2.5" fill="#fbbf24" />
      <text x="0" y="5" text-anchor="middle" class="latin-avatar" font-size="11" fill="#34d399" letter-spacing="2">MAKTABAH MAFTOOHAH</text>
    </g>
  </g>
</svg>'''

def build_logo_horizontal_svg() -> str:
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="800" height="200">
  <defs>
    <linearGradient id="logoCardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#064e3b" />
      <stop offset="50%" stop-color="#043829" />
      <stop offset="100%" stop-color="#021c14" />
    </linearGradient>

    <linearGradient id="goldHdr" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef3c7" />
      <stop offset="40%" stop-color="#f59e0b" />
      <stop offset="100%" stop-color="#d97706" />
    </linearGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&amp;family=Inter:wght@400;600;700;800&amp;display=swap');
      .ar-hdr { font-family: 'Amiri', 'Traditional Arabic', serif; font-weight: 700; }
      .latin-title { font-family: 'Inter', -apple-system, sans-serif; font-weight: 800; }
      .latin-sub { font-family: 'Inter', -apple-system, sans-serif; font-weight: 600; }
    </style>
  </defs>

  <rect width="800" height="200" rx="28" fill="url(#logoCardBg)" />
  <rect width="794" height="194" x="3" y="3" rx="25" fill="none" stroke="url(#goldHdr)" stroke-width="1.5" stroke-opacity="0.4" />

  <g transform="translate(30, 25)">
    <!-- Book Mini Emblem -->
    <rect width="150" height="150" rx="32" fill="#043829" stroke="url(#goldHdr)" stroke-width="2" />
    <circle cx="75" cy="75" r="55" fill="#10b981" fill-opacity="0.15" />
    <text x="75" y="90" text-anchor="middle" class="ar-hdr" font-size="52" fill="url(#goldHdr)">ماجه</text>
  </g>

  <g transform="translate(210, 50)">
    <text x="0" y="30" class="latin-title" font-size="34" fill="#ffffff" letter-spacing="-0.5">SUNAN IBN MAJAH</text>
    <text x="0" y="62" class="ar-hdr" font-size="30" fill="url(#goldHdr)">سُنَنُ ابْنِ مَاجَه — الإمام محمد بن يزيد القزويني</text>
    <text x="0" y="95" class="latin-sub" font-size="14.5" fill="#34d399" letter-spacing="1.5">MAKTABAH MAFTOOHAH &bull; KUTUB AS-SITTAH (38 KITAB &bull; 4,343 HADIS)</text>
  </g>
</svg>'''

def build_site_banner_svg() -> str:
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" width="1280" height="640">
  <defs>
    <linearGradient id="sbBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#022c22" />
      <stop offset="40%" stop-color="#064e3b" />
      <stop offset="80%" stop-color="#043829" />
      <stop offset="100%" stop-color="#011812" />
    </linearGradient>

    <linearGradient id="sbGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef3c7" />
      <stop offset="25%" stop-color="#fde68a" />
      <stop offset="50%" stop-color="#f59e0b" />
      <stop offset="75%" stop-color="#d97706" />
      <stop offset="100%" stop-color="#92400e" />
    </linearGradient>

    <radialGradient id="sbAura" cx="35%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.3" />
      <stop offset="70%" stop-color="#064e3b" stop-opacity="0.05" />
      <stop offset="100%" stop-color="#022c22" stop-opacity="0" />
    </radialGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&amp;family=Inter:wght@400;500;600;700;800;900&amp;display=swap');
      .sb-ar-large { font-family: 'Amiri', 'Traditional Arabic', serif; font-weight: 700; }
      .sb-latin-hero { font-family: 'Inter', -apple-system, sans-serif; font-weight: 900; }
      .sb-latin-sub { font-family: 'Inter', -apple-system, sans-serif; font-weight: 600; }
      .sb-pill { font-family: 'Inter', -apple-system, sans-serif; font-weight: 700; }
    </style>
  </defs>

  <rect width="1280" height="640" fill="url(#sbBg)" />
  <circle cx="450" cy="320" r="480" fill="url(#sbAura)" />

  <!-- Outer Frame -->
  <rect width="1248" height="608" x="16" y="16" rx="28" fill="none" stroke="url(#sbGold)" stroke-width="2.5" stroke-opacity="0.7" />
  <rect width="1224" height="584" x="28" y="28" rx="20" fill="none" stroke="#34d399" stroke-width="1" stroke-opacity="0.3" />

  <!-- Left: Main Logo Emblem -->
  <g transform="translate(100, 140)">
    <rect width="360" height="360" rx="80" fill="#043829" stroke="url(#sbGold)" stroke-width="3" />
    <circle cx="180" cy="180" r="130" fill="#10b981" fill-opacity="0.15" />
    <text x="180" y="210" text-anchor="middle" class="sb-ar-large" font-size="110" fill="url(#sbGold)">ماجه</text>
  </g>

  <!-- Right: Titles & Badges -->
  <g transform="translate(530, 160)">
    <!-- Heritage Badge -->
    <g transform="translate(0, 0)">
      <rect width="360" height="36" rx="18" fill="#047857" fill-opacity="0.5" stroke="#34d399" stroke-width="1.2" />
      <text x="180" y="23" text-anchor="middle" class="sb-pill" font-size="13" fill="#6ee7b7" letter-spacing="2">🌙 ZERO-BUILD ISLAMIC HERITAGE</text>
    </g>

    <text x="0" y="100" class="sb-latin-hero" font-size="56" fill="#ffffff" letter-spacing="-1">SUNAN IBN MAJAH</text>
    <text x="0" y="170" class="sb-ar-large" font-size="52" fill="url(#sbGold)">سُنَنُ ابْنِ مَاجَه (المُصَنَّف)</text>

    <text x="0" y="230" class="sb-latin-sub" font-size="20" fill="#cbd5e1" line-height="1.5">
      Koleksi Hadis Lengkap (38 Kitab &bull; 4,343 Hadis) &bull; Takhrij Ulama
    </text>
    <text x="0" y="265" class="sb-latin-sub" font-size="18" fill="#34d399">
      Piawaian Penomoran: Muhammad Fu'ad 'Abd al-Baqi (Default Sejagat)
    </text>

    <!-- Stat Pills -->
    <g transform="translate(0, 310)">
      <rect width="160" height="42" rx="12" fill="#064e3b" stroke="url(#sbGold)" stroke-width="1" />
      <text x="80" y="27" text-anchor="middle" class="sb-pill" font-size="14.5" fill="#fde68a">38 Kitab</text>

      <rect x="180" width="180" height="42" rx="12" fill="#064e3b" stroke="url(#sbGold)" stroke-width="1" />
      <text x="270" y="27" text-anchor="middle" class="sb-pill" font-size="14.5" fill="#fde68a">4,343 Hadis</text>

      <rect x="380" width="220" height="42" rx="12" fill="#064e3b" stroke="#34d399" stroke-width="1" />
      <text x="490" y="27" text-anchor="middle" class="sb-pill" font-size="14" fill="#34d399">Kutub as-Sittah</text>
    </g>
  </g>
</svg>'''

def render_with_playwright(tasks):
    print("=== Step 2: Rendering High-Resolution PNG/JPG Assets via Playwright ===")
    chrome_path = CHROME_EXEC.replace("\\", "/")
    node_script = f"""
const path = require('path');
const fs = require('fs');
const {{ chromium }} = require('{PLAYWRIGHT_DIR}/playwright');

(async () => {{
  console.log('Launching headless browser...');
  const browser = await chromium.launch({{
    executablePath: '{chrome_path}'
  }});
  const tasks = {json.dumps(tasks)};

  for (const t of tasks) {{
    console.log(`Rendering ${{t.output}} (${{t.width}}x${{t.height}})...`);
    const page = await browser.newPage({{
      viewport: {{ width: t.width, height: t.height }},
      deviceScaleFactor: t.scale || 1
    }});
    
    await page.goto('file:///' + t.input.replace(/\\\\/g, '/'));
    await page.waitForTimeout(400);
    
    const opts = {{ path: t.output }};
    if (t.type === 'jpeg') {{
      opts.type = 'jpeg';
      opts.quality = t.quality || 95;
    }}
    await page.screenshot(opts);
    await page.close();
  }}

  await browser.close();
  console.log('All Playwright rendering finished successfully!');
}})();
"""
    tmp_js = ROOT / "scripts" / ".render_tmp.cjs"
    tmp_js.write_text(node_script, encoding="utf-8")
    
    try:
        res = subprocess.run(["node", str(tmp_js)], capture_output=True, text=True, check=True)
        print(res.stdout)
    except Exception as e:
        print("Playwright render error or skipped:", e)
    finally:
        if tmp_js.exists():
            tmp_js.unlink()

def main():
    print("=== Step 1: Generating High-Precision Vector SVG Assets ===")

    # 1. assets/logo-mark.svg
    logo_mark_svg = build_logo_mark_svg()
    (ASSETS / "logo-mark.svg").write_text(logo_mark_svg, encoding="utf-8")
    (ROOT / "icon.svg").write_text(logo_mark_svg, encoding="utf-8")
    print("  • Generated assets/logo-mark.svg and root icon.svg (512x512)")

    # 2. assets/github-avatar.svg
    github_avatar_svg = build_github_avatar_svg()
    (ASSETS / "github-avatar.svg").write_text(github_avatar_svg, encoding="utf-8")
    print("  • Generated assets/github-avatar.svg (512x512 Circle-Safe)")

    # 3. assets/logo.svg
    logo_svg = build_logo_horizontal_svg()
    (ASSETS / "logo.svg").write_text(logo_svg, encoding="utf-8")
    print("  • Generated assets/logo.svg (800x200)")

    # 4. assets/site-banner.svg
    site_banner_svg = build_site_banner_svg()
    (ASSETS / "site-banner.svg").write_text(site_banner_svg, encoding="utf-8")
    print("  • Generated assets/site-banner.svg (1280x640)")

    # Step 2: Render raster PNGs and JPGs
    render_tasks = [
        {
            "input": str(ASSETS / "logo-mark.svg"),
            "output": str(ASSETS / "logo-mark.png"),
            "width": 512,
            "height": 512,
            "scale": 1
        },
        {
            "input": str(ASSETS / "github-avatar.svg"),
            "output": str(ASSETS / "github-avatar.png"),
            "width": 512,
            "height": 512,
            "scale": 1
        },
        {
            "input": str(ASSETS / "github-avatar.svg"),
            "output": str(ASSETS / "avatar.png"),
            "width": 512,
            "height": 512,
            "scale": 1
        },
        {
            "input": str(ASSETS / "logo-mark.svg"),
            "output": str(ASSETS / "icon-192.png"),
            "width": 192,
            "height": 192,
            "scale": 1
        },
        {
            "input": str(ASSETS / "logo-mark.svg"),
            "output": str(ASSETS / "icon-512.png"),
            "width": 512,
            "height": 512,
            "scale": 1
        },
        {
            "input": str(ASSETS / "logo.svg"),
            "output": str(ASSETS / "logo.png"),
            "width": 800,
            "height": 200,
            "scale": 2
        },
        {
            "input": str(ASSETS / "site-banner.svg"),
            "output": str(ASSETS / "site-banner.png"),
            "width": 1280,
            "height": 640,
            "scale": 2
        },
        {
            "input": str(ASSETS / "site-banner.svg"),
            "output": str(ASSETS / "og-banner.jpg"),
            "width": 1280,
            "height": 640,
            "scale": 1,
            "type": "jpeg",
            "quality": 95
        }
    ]

    render_with_playwright(render_tasks)
    print("\n>>> ALL BRANDING ASSETS GENERATED FOR SUNAN IBN MAJAH! <<<")

if __name__ == "__main__":
    main()
