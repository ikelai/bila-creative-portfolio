#!/usr/bin/env python3
"""Generate the homepage and case pages from data/cases.json."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "data" / "cases.json"
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Karla:ital,wght@0,300;0,400;0,600;1,300&family=Noto+Sans+TC:wght@300;400;500;600&display=swap" rel="stylesheet">'
)


def esc(value: object, *, quote: bool = True) -> str:
    return html.escape(str(value), quote=quote)


def head(title: str, description: str, css: str, prefix: str = "") -> str:
    return f'''<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{css}">
</head>'''


def nav(prefix: str = "") -> str:
    return f'''<header class="top-nav">
<a class="logo" href="{prefix}index.html">BILA Creative<span class="logo-sub">必樂創意行銷</span></a>
<nav><a href="{prefix}works.html">Works</a><a href="{prefix}website-design.html">Website</a><a href="{prefix}services.html">Services</a><a href="{prefix}about.html">About</a><a href="{prefix}contact.html">Contact</a></nav>
</header>'''


def generate_index(cases: dict[str, dict]) -> str:
    selected = ("dell", "cathay", "chicony", "sakurayuki", "juheng", "laisen", "onpro", "yingsheng")
    cards: list[str] = []
    for number, slug in enumerate(selected, 1):
        case = cases[slug]
        cards.append(
            f'''<a class="home-work-card" href="work/{esc(slug)}.html">
<img src="{esc(case['hero'])}" alt="{esc(case['name'])}" loading="lazy">
<div><span>{number:02d} · {esc(case['kicker'])}</span><h3>{esc(case['name'])}</h3><p>{esc(case['role'])}</p></div>
</a>'''
        )
    return f'''{head('BILA Creative 必樂創意行銷 — 品牌、設計與數位整合', 'BILA Creative 將品牌、設計與數位整合為可被使用的商業成果。', 'assets/style.css')}
<body>
{nav()}
<main>
<section class="home-hero">
<img src="{esc(cases['dell']['hero'])}" alt="BILA Creative selected work">
<div class="home-hero-copy">
<p class="eyebrow">BILA CREATIVE · TAIPEI</p>
<h1>讓品牌、設計與數位，<em>真正被使用。</em></h1>
<p>我們為正在成長的品牌，整合品牌識別、網站與日常溝通，讓每個接觸點都能更清楚地傳達價值。</p>
<div class="home-actions"><a class="button button-light" href="#selected-work">View Projects</a><a class="text-link" href="contact.html">Start a Project →</a></div>
</div>
</section>
<section class="home-section" id="selected-work">
<div class="section-heading"><div><p class="eyebrow">SELECTED WORK</p><h2>作品先說話。</h2></div><a class="text-link" href="works.html">View all projects →</a></div>
<div class="home-work-grid">{''.join(cards)}</div>
</section>
<section class="home-section home-capabilities">
<p class="eyebrow">WHAT BILA DOES</p>
<h2>從第一個想法，<br>到每天都在使用的品牌體驗。</h2>
<div class="capability-grid">
<article><span>01</span><h3>Brand & Visual Identity</h3><p>品牌定位、識別系統與能夠長期運作的視覺語言。</p></article>
<article><span>02</span><h3>Web & Digital Experience</h3><p>品牌網站、活動網站與轉換導向的數位體驗。</p><a href="website-design.html">Explore website design →</a></article>
<article><span>03</span><h3>Campaign & Social Content</h3><p>把一次性的溝通，整理成可持續經營的內容與活動系統。</p></article>
<article><span>04</span><h3>Graphic & Communication</h3><p>型錄、包裝與企業溝通，把複雜資訊變成可理解的品牌資產。</p></article>
</div>
</section>
<section class="featured-case">
<img src="{esc(cases['cathay']['hero'])}" alt="{esc(cases['cathay']['name'])}" loading="lazy">
<div><p class="eyebrow">FEATURED CASE</p><h2>大型金融品牌的<br>年度數位溝通。</h2><p>從年度回顧網站到社群視覺，為國泰人壽建立連續、清楚且符合品牌標準的數位溝通。</p><a class="button" href="work/cathay.html">Explore the case</a></div>
</section>
<section class="home-section home-why">
<p class="eyebrow">WHY BILA</p>
<div class="why-grid"><h2>好看的設計，<br>只是開始。</h2><div><p>我們相信品牌不是一張主視覺，而是一連串被看見、被理解、被使用的經驗。</p><p>所以從策略、內容結構到最後的設計與製作，都以同一個商業問題為中心。</p><a class="text-link" href="about.html">How we work →</a></div></div>
</section>
<section class="home-section client-section">
<p class="eyebrow">SELECTED EXPERIENCE</p>
<div class="client-list"><span>Dell Technologies</span><span>國泰人壽</span><span>群光電子</span><span>ONPRO</span><span>RIZAP</span><span>鉅亨國際</span></div>
</section>
<section class="home-cta">
<p class="eyebrow">START A PROJECT</p><h2>有一個品牌、網站或設計專案正在規劃？</h2><a class="button button-light" href="contact.html">Tell us about it</a><a class="text-link" href="mailto:hello@bila.com.tw">hello@bila.com.tw</a>
</section>
</main>
</body></html>'''

def generate_not_found() -> str:
    return f'''{head('找不到頁面 — BILA Creative', '找不到這個 BILA Creative 頁面，請返回作品首頁繼續瀏覽。', 'assets/style.css')}
<body>
{nav()}
<main class="contact-page">
<p style="font-size:10px;letter-spacing:.22em;color:var(--soft)">ERROR · 404</p>
<h1 style="font-size:clamp(38px,6vw,84px);font-weight:300;line-height:1.08;margin:1rem 0">這一頁不在這裡。</h1>
<p style="font-size:13px;color:var(--soft)">網址可能已經更新，或這個頁面尚未建立。</p>
<a class="mail" href="index.html">返回作品首頁 →</a>
</main>
</body>
</html>'''


def image_tag(path: str) -> str:
    return f'<img src="../{esc(path)}" alt="" loading="lazy">'


def generate_case(slug: str, case: dict) -> str:
    stream: list[str] = []
    sections = case.get("brand_sections") or []
    if sections:
        for section in sections:
            stream.append(
                f'<div class="stream-section"><span class="ss-brand">{esc(section["brand"])}</span>'
                f'<span class="ss-tag">{esc(section.get("tag", ""))}</span></div>'
            )
            stream.extend(image_tag(path) for path in section.get("images") or section.get("gallery") or [])
    else:
        stream.extend(image_tag(path) for path in case.get("gallery") or [])
    meta = case["meta"]
    return f'''{head(f'{case["name"]} — BILA Creative', case['summary'], '../assets/style.css', '../')}
<body>
{nav('../')}
<section class="case-header">
<h1>{esc(case['name'])}<br><span style="color:var(--soft);font-size:.5em;font-weight:300">{esc(case['zh'])}</span></h1>
<div class="ch-role">{esc(case['role'])}</div>
<div class="ch-desc">{esc(case['summary'])}</div>
<div class="ch-meta">
<span>Client: {esc(meta['Client'])}</span>
<span>Scope: {esc(meta['Scope'])}</span>
<span>Scale: {esc(meta['Scale'])}</span>
</div>
</section>
<div class="image-stream">{"".join(stream)}</div>
<div class="case-footer">
<div class="cf-credit"><span>{esc(case['credit'])}</span><span>BILA Creative — 必樂創意行銷整合</span></div>
<a href="../index.html#{esc(slug)}">← 返回</a>
</div></body></html>'''


def outputs(cases: dict[str, dict]) -> dict[Path, str]:
    generated = {
        ROOT / "index.html": generate_index(cases),
        ROOT / "404.html": generate_not_found(),
    }
    generated.update({ROOT / "work" / f"{slug}.html": generate_case(slug, case) for slug, case in cases.items()})
    return generated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated pages are stale")
    args = parser.parse_args()
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    stale: list[Path] = []
    for path, content in outputs(cases).items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        print("Generated pages are stale:")
        for path in stale:
            print(f"- {path}")
        return 1
    print(f"{'Checked' if args.check else 'Generated'} {len(cases) + 2} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
