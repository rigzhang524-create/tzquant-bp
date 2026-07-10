#!/usr/bin/env python3
"""Generate a PDF from index.html, excluding video assets."""
import os
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
HTML_PATH = BASE_DIR / "index.html"
TEMP_HTML_PATH = BASE_DIR / "index_for_pdf.html"
PDF_PATH = BASE_DIR / "TzQuant_Investor_Deck.pdf"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def prepare_html():
    text = HTML_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "lxml")

    # Remove all <video> elements and the poster play button.
    for video in soup.find_all("video"):
        video.decompose()
    for btn in soup.find_all(class_="poster-play"):
        btn.decompose()

    # The original HTML uses <div class="section-inner"> but the CSS expects
    # <div class="section-inner two-col"> for the combined Business+Market
    # section. Add the missing class so the two columns render side-by-side.
    combined = soup.find("section", id="business")
    if combined:
        inner = combined.find("div", class_="section-inner")
        if inner and "two-col" not in (inner.get("class") or []):
            inner["class"] = (inner.get("class") or []) + ["two-col"]

    # Remove the original screen stylesheet and inject a print-optimised one.
    link = soup.find("link", rel="stylesheet")
    if link:
        link.decompose()

    style = soup.new_tag("style")
    style.string = """
/* Reset */
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 14px; }
body { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif; color: #1d1d1f; line-height: 1.5; background: #fff; }
img { max-width: 100%; height: auto; display: block; }
ul { list-style: none; }
a { color: inherit; text-decoration: none; }

/* Hide interactive/header/footer elements */
.site-header, .menu-toggle, .lang-toggle, .header-cta, .poster-play, video, .hero-links, .site-footer { display: none !important; }

/* Layout */
.hero { padding: 40px 0 20px; text-align: center; }
.hero-content { max-width: 100%; padding: 0 16px; margin-bottom: 16px; }
.hero h1 { font-size: 1.8rem; font-weight: 700; margin-bottom: 10px; line-height: 1.2; }
.hero-subhead { font-size: 0.95rem; color: #6e6e73; margin-bottom: 16px; }
.hero-media { display: none !important; }

.quote-section { padding: 18px 16px; background: #fafafc; border-top: 1px solid #e8e8ed; border-bottom: 1px solid #e8e8ed; text-align: center; }
.quote-section blockquote { font-size: 1rem; font-style: italic; font-weight: 500; line-height: 1.5; margin-bottom: 10px; }
.quote-section cite { font-size: 0.8rem; color: #6e6e73; }

.section { padding: 18px 16px; page-break-inside: avoid; }
.section-inner { max-width: 100%; }
.section-head { text-align: center; margin-bottom: 14px; }
.eyebrow { display: block; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #0071e3; margin-bottom: 6px; }
.section-head h2 { font-size: 1.4rem; font-weight: 700; line-height: 1.2; }
.section-subhead { font-size: 0.85rem; color: #6e6e73; margin-top: 6px; }

.opportunity { background: #f5f5f7; }
.opportunity-body p { font-size: 0.82rem; margin-bottom: 8px; }
.opportunity-body p.expand { font-size: 0.8rem; color: #6e6e73; border-left: 2px solid #0071e3; padding-left: 10px; margin: 8px 0; }
.opportunity-body p.secondary { font-size: 0.82rem; }
.metrics-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px 8px; margin-top: 14px; }
.metric { text-align: center; }
.metric-value { display: block; font-size: 1.15rem; font-weight: 700; }
.metric-label { font-size: 0.65rem; color: #6e6e73; }

.solution-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.solution-card { background: #f5f5f7; border-radius: 10px; padding: 12px; }
.solution-card.wide { grid-column: span 2; text-align: center; }
.solution-card span { font-size: 0.9rem; font-weight: 700; display: block; margin-bottom: 2px; }
.solution-card p { font-size: 0.75rem; color: #6e6e73; }

.strategic-note { font-size: 0.78rem; font-style: italic; text-align: center; margin-bottom: 14px; padding: 0 8px; }
.competitor-table-wrap { overflow-x: visible; }
.competitor-table { width: 100%; min-width: auto; border-collapse: collapse; font-size: 0.72rem; background: #f5f5f7; border-radius: 10px; }
.competitor-table th, .competitor-table td { padding: 8px 4px; text-align: center; border-bottom: 1px solid #e8e8ed; }
.competitor-table td:first-child { text-align: left; font-weight: 600; padding-left: 8px; }
.competitor-table .yes { color: #2d8a3e; font-weight: 600; }
.competitor-table .yes.strong { color: #1e6b2e; }
.competitor-table .partial { color: #d68a00; }
.competitor-table .no { color: #c41c1c; }
.competitor-table tr.highlight { background: rgba(0,113,227,0.06); }
.competitor-legend { display: flex; justify-content: center; gap: 10px; font-size: 0.65rem; color: #6e6e73; margin: 10px 0; }
.competitor-summary { background: #f5f5f7; border-radius: 10px; padding: 12px; text-align: center; }
.competitor-summary p { font-size: 0.75rem; color: #6e6e73; line-height: 1.5; }

.why-now-layout { display: grid; grid-template-columns: 1fr; gap: 12px; }
.why-now-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.why-now-card { background: #f5f5f7; border: 1px solid #e8e8ed; border-radius: 10px; padding: 10px; }
.why-now-icon { width: 24px; height: 24px; color: #0071e3; margin-bottom: 6px; }
.why-now-card h3 { font-size: 0.8rem; font-weight: 600; margin-bottom: 4px; }
.why-now-card p { font-size: 0.68rem; color: #6e6e73; line-height: 1.4; }
.why-now-flow { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; gap: 6px; padding: 10px; background: #f5f5f7; border-radius: 10px; }
.flow-item { font-size: 0.7rem; font-weight: 500; padding: 4px 10px; background: #fff; border: 1px solid #e8e8ed; border-radius: 999px; }
.flow-item.highlight { background: #0071e3; color: #fff; }
.flow-arrow { transform: rotate(90deg); font-size: 0.7rem; color: #6e6e73; }
.why-now-closing { text-align: center; margin-top: 12px; }
.closing-lead { font-size: 0.95rem; font-weight: 700; }
.closing-sub { font-size: 0.75rem; color: #6e6e73; }

.traction { background: #f5f5f7; text-align: center; }
.traction-metrics { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 12px; }
.traction-metric { background: #fff; border-radius: 10px; padding: 10px; }
.metric-number { font-size: 1.2rem; font-weight: 700; }
.traction-summary { font-size: 0.78rem; color: #6e6e73; margin-bottom: 14px; }
.growth-sixmonths h3 { font-size: 0.65rem; color: #6e6e73; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
.growth-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 10px; }
.growth-metric { background: #fff; border-radius: 10px; padding: 8px; }
.growth-value { font-size: 1.1rem; font-weight: 700; color: #0071e3; }
.growth-label { font-size: 0.65rem; color: #6e6e73; }
.growth-curve { height: 60px; background: #fff; border-radius: 10px; }
.traction-quote { font-size: 0.85rem; font-weight: 500; margin: 14px 0 6px; }
.traction-cite { font-size: 0.75rem; color: #6e6e73; }

.workflow-flow { display: flex; justify-content: center; gap: 8px; margin-bottom: 14px; font-size: 0.7rem; font-weight: 600; color: #86868b; }
.workflow-step { padding: 4px 10px; background: #f5f5f7; border-radius: 999px; }
.workflow-arrow { color: #0071e3; }
.product-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
.product-card { background: #f5f5f7; border-radius: 10px; overflow: hidden; display: flex; flex-direction: row; }
.product-media { width: 30%; min-height: 100%; }
.product-media img { width: 100%; height: 100%; object-fit: cover; }
.product-info { width: 70%; padding: 10px; }
.product-info h3 { font-size: 0.85rem; margin-bottom: 2px; }
.product-lead { font-size: 0.72rem; color: #6e6e73; margin-bottom: 6px; }
.product-points li { font-size: 0.68rem; padding-left: 14px; position: relative; margin-bottom: 2px; }
.product-points li::before { content: '✓'; position: absolute; left: 0; color: #0071e3; font-weight: bold; }
.product-outcome { padding-top: 6px; border-top: 1px solid #e8e8ed; margin-top: 6px; }
.outcome-label { font-size: 0.7rem; font-weight: 700; }

.advantage { background: #f5f5f7; }
.advantage-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.advantage-card { background: #fff; border-radius: 10px; padding: 12px; }
.advantage-card h3 { font-size: 0.85rem; margin-bottom: 4px; }
.advantage-card p { font-size: 0.7rem; color: #6e6e73; line-height: 1.4; }
.moat-subtitle { font-size: 0.78rem; font-style: italic; color: #6e6e73; text-align: center; margin-bottom: 14px; }
.moat-quote-box { background: #fff; border: 1px solid #e8e8ed; border-radius: 10px; padding: 12px; margin-top: 14px; }
.moat-quote-box p { font-size: 0.75rem; font-style: italic; line-height: 1.5; }

.roadmap-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
.roadmap-card { background: #f5f5f7; border-radius: 10px; padding: 10px; }
.roadmap-status { font-size: 0.6rem; font-weight: 700; color: #86868b; text-transform: uppercase; display: block; margin-bottom: 4px; }
.roadmap-status.done { color: #2d8a3e; }
.roadmap-card h3 { font-size: 0.82rem; margin-bottom: 2px; }
.roadmap-card p { font-size: 0.68rem; color: #6e6e73; line-height: 1.4; }

.combined .section-inner { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.market-col { padding-top: 0; margin-top: 0; border-top: none; }
.design-logic { font-size: 0.75rem; font-style: italic; color: #6e6e73; text-align: center; margin-bottom: 10px; }
.business-list, .market-list { display: flex; flex-direction: column; gap: 8px; }
.business-item h3, .market-value { font-size: 0.9rem; font-weight: 700; }
.business-item p, .market-item p { font-size: 0.68rem; color: #6e6e73; }
.market-label { font-size: 0.55rem; font-weight: 700; color: #86868b; text-transform: uppercase; }

.team { background: #f5f5f7; }
.team-grid { display: flex; flex-direction: column; gap: 8px; }
.team-card { background: #fff; border-radius: 10px; padding: 10px; display: flex; gap: 10px; align-items: flex-start; }
.member-photo { width: 1.6cm; height: 1.6cm; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.member-header { display: flex; align-items: baseline; gap: 6px; margin-bottom: 2px; }
.team-card h3 { font-size: 1rem; }
.member-role { font-size: 0.72rem; color: #0071e3; font-weight: 600; }
.member-tagline { font-size: 0.72rem; color: #6e6e73; margin-bottom: 4px; }
.member-highlights { display: flex; flex-direction: column; gap: 2px; }
.member-highlights li { display: flex; gap: 4px; font-size: 0.65rem; color: #6e6e73; }
.member-highlights li strong, .member-highlights li .highlight-label { font-size: 0.62rem; font-weight: 700; background: #f5f5f7; padding: 1px 4px; border-radius: 3px; min-width: 28px; text-align: center; }

.contact { text-align: center; padding-bottom: 20px; }
.contact h2 { font-size: 1.5rem; }
.contact h2 strong { color: #1d1d1f; }
.funding-plan { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 14px 0; }
.fund-block { background: #f5f5f7; border-radius: 8px; padding: 8px; text-align: center; }
.fund-block h3 { font-size: 0.6rem; color: #6e6e73; text-transform: uppercase; margin-bottom: 6px; }
.fund-block > p, .fund-allocations li, .fund-milestones li { font-size: 0.68rem; }
.fund-pct { display: inline-block; width: 28px; padding: 1px 0; background: #0071e3; color: #fff; border-radius: 999px; font-size: 0.55rem; font-weight: 700; }
.fund-value { font-size: 1rem; font-weight: 700; }
.contact-email { font-size: 1rem; color: #0071e3; font-weight: 600; }
.contact-location { font-size: 0.7rem; color: #6e6e73; }

h1, h2, h3 { page-break-after: avoid; }
p, li { orphans: 3; widows: 3; }
img { page-break-inside: avoid; }
"""
    soup.head.append(style)

    TEMP_HTML_PATH.write_text(str(soup), encoding="utf-8")
    return TEMP_HTML_PATH


def generate_pdf(html_path: Path, pdf_path: Path):
    if not os.path.exists(CHROME_PATH):
        print(f"Chrome not found at {CHROME_PATH}", file=sys.stderr)
        sys.exit(1)

    cmd = [
        CHROME_PATH,
        "--headless=old",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_path}",
        f"file://{html_path}",
    ]
    subprocess.run(cmd, check=True)


def main():
    print("Preparing HTML without video assets...")
    html_path = prepare_html()
    print(f"Saved temporary HTML to {html_path}")

    print("Generating PDF with Chrome headless...")
    generate_pdf(html_path, PDF_PATH)
    print(f"PDF saved to {PDF_PATH}")


if __name__ == "__main__":
    main()
