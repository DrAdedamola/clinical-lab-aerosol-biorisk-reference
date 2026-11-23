#!/usr/bin/env python3
"""
08_pdf.py - renders report/technical_report.md to a typeset PDF

PLAIN LANGUAGE HEADER
Turns the technical report into a PDF you can attach to an email or upload to Zenodo.
Run code/05_report.py first so the markdown is current. Needs pandoc and weasyprint.

Run:  python3 code/08_pdf.py
"""
import subprocess, tempfile
from pathlib import Path
from weasyprint import HTML, CSS

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report"
CSS_TEXT = """
@page { size: A4; margin: 22mm 20mm;
        @bottom-center { content: counter(page); font: 9pt Georgia, serif; color: #777; } }
body { font: 10.5pt/1.55 Georgia, 'DejaVu Serif', serif; color: #1a1a1a; }
h1 { font-size: 20pt; line-height: 1.25; margin: 0 0 6pt; }
h3 { font-size: 12pt; font-weight: normal; font-style: italic; color: #444; margin: 0 0 14pt; }
h2 { font-size: 13.5pt; margin: 22pt 0 7pt; border-bottom: 1px solid #ddd; padding-bottom: 3pt;
     break-after: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 9.5pt; margin: 10pt 0; }
th, td { border-bottom: 1px solid #e2e2e2; padding: 5pt 7pt; text-align: left; vertical-align: top; }
th { border-bottom: 1.5px solid #999; font-size: 9pt; text-transform: uppercase; letter-spacing: .4pt; }
img { max-width: 100%; margin: 12pt 0; }
code, pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt; background: #f6f6f6; }
pre { padding: 8pt; border-left: 3px solid #ddd; white-space: pre-wrap; }
a { color: #1b5e9e; text-decoration: none; word-break: break-word; }
ul { padding-left: 16pt; } li { margin-bottom: 4pt; }
hr { border: none; border-top: 1px solid #ddd; margin: 14pt 0; }
"""

with tempfile.TemporaryDirectory() as tmp:
    frag = Path(tmp) / "body.html"
    subprocess.run(["pandoc", str(REPORT / "technical_report.md"), "-t", "html5",
                    "-o", str(frag)], check=True)
    page = Path(tmp) / "page.html"
    page.write_text('<!doctype html><html><head><meta charset="utf-8"></head><body>'
                    + frag.read_text() + "</body></html>")
    out = REPORT / "technical_report.pdf"
    HTML(str(page), base_url=str(REPORT)).write_pdf(str(out), stylesheets=[CSS(string=CSS_TEXT)])
    print(f"wrote {out}")
