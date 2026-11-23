#!/usr/bin/env python3
"""
12_brief.py - builds the technical report PDF from LaTeX source

PLAIN LANGUAGE HEADER
Compiles brief/brief.tex into brief/brief.pdf, the procedure inventory and
evidence brief. Run the figure script first so the figures are current. Needs
pdflatex. You do not need to run this unless you have changed the text.

Run:  python3 code/11_brief_figures.py && python3 code/12_brief.py
"""
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BR = ROOT / "brief"

if shutil.which("pdflatex") is None:
    sys.exit("pdflatex not found. Install a TeX distribution, or use the PDF already in brief/.")

for _ in range(3):                    # three passes: refs, then cross-refs settle
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "brief.tex"],
                       cwd=BR, capture_output=True, text=True)
errs = [l for l in r.stdout.splitlines() if l.startswith("! ")]
if errs:
    print("LaTeX reported errors:")
    for e in errs[:10]:
        print("  ", e)
    sys.exit(1)

undef = [l for l in r.stdout.splitlines()
         if "undefined" in l.lower() and "warning" in l.lower()]
if undef:
    print("Warning: undefined references remain:")
    for u in undef[:6]:
        print("  ", u.strip())

for junk in ("aux", "log", "out", "toc"):
    for f in BR.glob(f"*.{junk}"):
        f.unlink()
print(f"wrote {BR / 'brief.pdf'}")
