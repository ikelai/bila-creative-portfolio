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
    sections: list[str] = []
    dots: list[str] = []
    for slug, case in cases.items():
        dots.append(f'<a href="#{esc(slug)}" class="dot"></a>')
        sections.append(
            f'''<section class="case-section" id="{esc(slug)}">
<img class="cs-bg" src="{esc(case['hero'])}" alt="{esc(case['name'])}">
<div class="cs-info">
<div class="cs-role">{esc(case['role'])}</div>
<div class="cs-client">{esc(case['name'])}</div>
<div class="cs-tag">{esc(case['zh'])} · {esc(case['kicker'])}</div>
</div>
<a class="cs-link" href="work/{esc(slug)}.html">View Project →</a>
</section>'''
        )
    dot_nav = "".join(dots)
    section_html = "".join(sections)
    return f'''{head('BILA Creative 必樂創意行銷 — BILA Creative', '品牌設計、網站、社群與創意整合作品集 — Dell Technologies、國泰人壽、群光電子等品牌。', 'assets/style.css')}
<body>
{nav()} 
<nav class="scroll-hint" aria-label="案例導航">{dot_nav}</nav>
{section_html}
<script>
(function(){{
 var dots=document.querySelectorAll('.scroll-hint .dot');
 var sections=document.querySelectorAll('.case-section');
 function update(){{
  var i=0; sections.forEach(function(s,idx){{ var r=s.getBoundingClientRect(); if(r.top<window.innerHeight*.5)i=idx; }});
  dots.forEach(function(d,idx){{ d.classList.toggle('active',idx===i); }});
 }}
 window.addEventListener('scroll',update,{{passive:true}});
 update();
}})();
</script></body></html>'''.replace("</header> \n", "</header>\n")


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
    generated = {ROOT / "index.html": generate_index(cases)}
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
    print(f"{'Checked' if args.check else 'Generated'} {len(cases) + 1} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
