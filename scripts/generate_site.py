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
<nav><a href="{prefix}works.html">Works</a><a href="{prefix}services.html">Services</a><a href="{prefix}about.html">About</a><a href="{prefix}contact.html">Contact</a></nav>
</header>'''


def generate_index(cases: dict[str, dict]) -> str:
    featured = ("dell", "cathay", "yingsheng")
    media = {
        "dell": (
            "images/dell/dell-06-00-封面.jpg",
            "images/dell/dell-05-2021_DELL_Q1平面型錄_設計完稿_OL_FA-0604_1.jpg",
        ),
        "cathay": (
            "images/cathay/cathay-01-2025_國泰人壽_banner_0119_02-主視覺篇_入口網站_550x2.jpg",
            "images/cathay/cathay-03-2025_國泰人壽_banner_0119_02-主視覺篇_FB_1080x10.jpg",
        ),
        "yingsheng": (
            "images/yingsheng/yingsheng-01-迎盛-BLIKSEN-型錄設計方案書_1204-01.jpg",
            "images/yingsheng/yingsheng-05-30-LOGO.jpg",
        ),
    }
    stories: list[str] = []
    for index, slug in enumerate(featured, 1):
        case = cases[slug]
        primary, secondary = media[slug]
        stories.append(f'''<article class="editorial-case" id="{esc(slug)}">
<div class="editorial-case-no">0{index}</div>
<div class="editorial-case-copy"><p class="editorial-kicker">{esc(case['kicker'])}</p>
<h2>{esc(case['name'])}</h2><p class="editorial-zh">{esc(case['zh'])}</p>
<p class="editorial-role">{esc(case['role'])}</p>
<p class="editorial-summary">{esc(case['summary'])}</p>
<a class="editorial-link" href="work/{esc(slug)}.html">閱讀案例 <span>→</span></a></div>
<div class="editorial-media"><img src="{esc(primary)}" alt="{esc(case['name'])} 作品選圖"><img class="editorial-secondary" src="{esc(secondary)}" alt="" loading="lazy"></div>
</article>''')
    return f'''{head('BILA Creative 必樂創意行銷 — Selected Works', 'BILA Creative 精選案例：Dell Technologies、國泰人壽與迎盛 BLIKSEN 的品牌與數位溝通設計。', 'assets/style.css')}
<body class="editorial-body">
{nav()}
<main>
<section class="editorial-intro"><p class="editorial-index">BILA CREATIVE / SELECTED WORKS / 2026</p>
<h1>設計不是把畫面<br>塞得更滿。<br><em>是讓品牌被看懂。</em></h1>
<div class="editorial-intro-bottom"><p>必樂以設計系統、數位體驗與長期製作能力，幫品牌把複雜的事情說清楚。</p><a href="#dell">向下閱讀 <span>↓</span></a></div></section>
<section class="editorial-statement"><p>三個案例，三種尺度：全球科技品牌的在地化系統、金融品牌的年度數位溝通，以及 B2B 企業的識別與型錄重整。</p></section>
<section class="editorial-cases">{"".join(stories)}</section>
<section class="editorial-closing"><p class="editorial-index">BILA CREATIVE / TAIPEI</p><h2>有一件事值得<br><em>重新說清楚？</em></h2><a class="editorial-link" href="contact.html">開始一個專案 <span>→</span></a></section>
</main></body></html>'''


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
