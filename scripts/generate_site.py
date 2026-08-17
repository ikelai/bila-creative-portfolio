#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate BILA's public portfolio from the curated case manifest."""
from __future__ import annotations
import argparse, html, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data" / "cases.json"
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@300;400;500;600&family=Noto+Sans+TC:wght@300;400;500&display=swap" rel="stylesheet">')

def e(v): return html.escape(str(v), quote=True)
def head(title, description, prefix=""):
    return f'<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description)}"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">{FONT}<link rel="stylesheet" href="{prefix}assets/style.css"></head>'
def nav(prefix="", page=""):
    items=[("works.html","Projects"),("services.html","Services"),("about.html","Studio"),("contact.html","Contact")]
    links=''.join(f'<a class="{"is-current" if page==p else ""}" href="{prefix}{p}">{t}</a>' for p,t in items)
    return f'<header class="nav"><a class="wordmark" href="{prefix}index.html">BILA<span>CREATIVE STUDIO</span></a><nav>{links}</nav><a class="nav-contact" href="{prefix}contact.html">Start a project <i>↗</i></a></header>'
def footer(prefix=""):
    return f'<footer class="footer"><div><b>BILA Creative Studio</b><span>品牌、設計與數位整合</span></div><div>TAIPEI · TAIWAN<br>© 2026 BILA Creative</div><div><a href="{prefix}contact.html">New business ↗</a></div></footer>'
def image(path, alt=""):
    return f'<img src="{e(path)}" alt="{e(alt)}" loading="lazy">'

FEATURED=("dell","cathay","yingsheng","jufenzi")
def project_card(slug,c,index,prefix=""):
    pic = c["gallery"][3] if slug=="dell" and len(c["gallery"])>3 else c["hero"]
    return f'<a class="project-card" href="{prefix}work/{e(slug)}.html"><div class="project-image">{image(prefix+pic,c["name"])}</div><div class="project-meta"><span>{index:02d} / {e(c["kicker"])}</span><b>{e(c["name"])}</b><em>{e(c["role"])}</em><i>Explore ↗</i></div></a>'

def home(cases):
    featured=''.join(project_card(s,cases[s],i+1) for i,s in enumerate(FEATURED))
    return f'''{head("BILA Creative — 品牌、設計與數位整合", "BILA Creative Studio：以品牌、視覺與數位體驗，讓每一個商業溝通被看見、被理解、被使用。")}<body class="home">{nav()}<main><section class="home-hero"><div class="hero-copy"><p class="eyebrow">Independent creative studio / Taipei</p><h1>Make it<br><span>matter.</span></h1><p>把品牌、設計與數位整合成<br>真正能被使用的商業成果。</p><a class="text-link" href="#featured">Explore selected work <i>↓</i></a></div><div class="hero-art"><div class="hero-art-image">{image("images/dell/dell-03-20230608_DELL_Q2-DM_20面_FA_demo.jpg","Dell Technologies brochure system")}</div><p>Selected work<br><b>Dell Technologies</b></p></div></section><section class="intro"><p class="eyebrow">What BILA does</p><h2>We give brands<br>something <em>clear</em> to say<br>and a way to say it.</h2><div><p>從一次關鍵的品牌識別，到每天都在運作的網站、內容與活動，我們把策略、視覺與製作放在同一個思考裡。</p><a class="text-link" href="services.html">Our capabilities <i>↗</i></a></div></section><section class="featured" id="featured"><div class="section-top"><p class="eyebrow">Selected projects</p><a class="text-link" href="works.html">View all projects <i>↗</i></a></div><div class="featured-grid">{featured}</div></section><section class="principle"><p class="eyebrow">A useful point of view</p><div><h2>Creative work<br>should do more<br>than <em>look good.</em></h2><p>它必須能在真實的商業情境裡工作：讓品牌更一致、訊息更容易被理解、下一次溝通更快發生。</p></div></section><section class="closing"><p class="eyebrow">Let’s work together</p><h2>有一個想清楚<br>的品牌，<em>正在等你。</em></h2><a class="button" href="contact.html">Start a conversation <i>↗</i></a></section></main>{footer()}</body></html>'''

def case(slug,c):
    blocks=''.join(f'<section class="case-copy"><p class="eyebrow">{e(x["h"])}</p><div>{"".join(f"<p>{e(p)}</p>" for p in x.get("p",[]))}{("<ul>"+"".join(f"<li>{e(u)}</li>" for u in x.get("ul") or [])+"</ul>") if x.get("ul") else ""}</div></section>' for x in c.get("blocks",[]))
    gallery=''.join(f'<figure class="gallery-item gallery-{i%3}">{image("../"+p,c["name"])}</figure>' for i,p in enumerate(c.get("gallery",[])))
    meta=''.join(f'<div><span>{e(k)}</span><b>{e(v)}</b></div>' for k,v in c["meta"].items())
    return f'''{head(c["name"]+" — BILA Creative", c["summary"], "../")}<body class="case">{nav("../", "works.html")}<main><section class="case-hero"><div><p class="eyebrow">Project / {e(c["kicker"])}</p><h1>{e(c["name"])}</h1><p class="case-role">{e(c["role"])}</p></div><div class="case-hero-image">{image("../"+c["hero"],c["name"])}</div></section><section class="case-summary"><p class="eyebrow">Overview</p><h2>{e(c["summary"])}</h2><div class="case-facts">{meta}</div></section>{blocks}<section class="gallery">{gallery}</section><section class="next-case"><p class="eyebrow">Next step</p><h2>有一個複雜的問題？<br><em>一起把它變清楚。</em></h2><a class="button" href="../contact.html">Start a conversation <i>↗</i></a></section></main>{footer("../")}</body></html>'''

def works(cases):
    cards=''.join(project_card(s,c,i+1) for i,(s,c) in enumerate(cases.items()))
    return f'''{head("Projects — BILA Creative", "BILA Creative selected projects.")}<body>{nav(page="works.html")}<main><section class="page-hero"><p class="eyebrow">Selected projects</p><h1>Different brands.<br><em>One standard of care.</em></h1><p>從科技、金融到生活品牌，我們讓複雜的溝通變得有感、好用並且一致。</p></section><section class="all-projects">{cards}</section></main>{footer()}</body></html>'''

def services():
    data=[("01","Brand identity","讓品牌在每一個觸點都被一致地認出與理解。"),("02","Web & digital","以內容、使用情境與商業目標為核心，打造真正可用的數位體驗。"),("03","Campaign & social","把一次溝通做成能在不同平台持續工作的內容系統。"),("04","Editorial & communication","把複雜資訊整理成有清晰層次、值得閱讀的企業溝通。")]
    rows=''.join(f'<div class="service-row"><span>{n}</span><h2>{t}</h2><p>{d}</p></div>' for n,t,d in data)
    return f'''{head("Services — BILA Creative", "BILA Creative services: brand, web, campaign and communication.")}<body>{nav(page="services.html")}<main><section class="page-hero"><p class="eyebrow">Capabilities</p><h1>A practical<br><em>creative partner.</em></h1><p>擅長把品牌需求從模糊的想法，帶到可以落地、維持與延伸的設計系統。</p></section><section class="service-list">{rows}</section><section class="closing"><p class="eyebrow">Start here</p><h2>不知道從哪裡開始？<br><em>先把問題說出來。</em></h2><a class="button" href="contact.html">Talk to BILA <i>↗</i></a></section></main>{footer()}</body></html>'''
def about(): return f'''{head("Studio — BILA Creative", "About BILA Creative Studio.")}<body>{nav(page="about.html")}<main><section class="page-hero"><p class="eyebrow">The studio</p><h1>Clarity is<br><em>a creative act.</em></h1></section><section class="studio-copy"><p>我們是位於台北的創意工作室，服務從全球科技品牌到在地企業與生活品牌。</p><p>我們相信一個好設計不只是畫面漂亮，而是能讓人快速理解品牌、讓團隊容易繼續工作、讓每一次溝通都往前一步。</p><a class="text-link" href="contact.html">Work with us <i>↗</i></a></section></main>{footer()}</body></html>'''
def contact(): return f'''{head("Contact — BILA Creative", "Contact BILA Creative Studio.")}<body>{nav(page="contact.html")}<main><section class="contact-hero"><p class="eyebrow">New business / collaboration</p><h1>Let’s make<br>something <em>matter.</em></h1><p>告訴我們你正在面對的品牌、網站或溝通問題。我們會先理解，再一起決定最合適的開始方式。</p><a class="contact-mail" href="mailto:hello@bila.com.tw">hello@bila.com.tw <i>↗</i></a></section></main>{footer()}</body></html>'''
def not_found(): return f'''{head("Page not found — BILA Creative", "This BILA page could not be found.")}<body>{nav()}<main><section class="contact-hero"><p class="eyebrow">Error / 404</p><h1>這一頁<br><em>不在這裡。</em></h1><a class="button" href="index.html">Back to home <i>↗</i></a></section></main>{footer()}</body></html>'''
def outputs(cases):
    out={ROOT/"index.html":home(cases),ROOT/"works.html":works(cases),ROOT/"services.html":services(),ROOT/"about.html":about(),ROOT/"contact.html":contact(),ROOT/"404.html":not_found()}; out.update({ROOT/"work"/(s+".html"):case(s,c) for s,c in cases.items()}); return out
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--check",action="store_true"); args=parser.parse_args(); cases=json.loads(CASES.read_text(encoding="utf-8")); stale=[]
    for p,content in outputs(cases).items():
        if args.check:
            if not p.exists() or p.read_text(encoding="utf-8")!=content: stale.append(p.relative_to(ROOT))
        else: p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding="utf-8")
    if stale: print("Generated pages are stale:",*map(str,stale),sep="\n- "); return 1
    print(f"{'Checked' if args.check else 'Generated'} {len(outputs(cases))} pages"); return 0
if __name__=="__main__": sys.exit(main())
