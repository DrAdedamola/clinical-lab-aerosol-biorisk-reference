#!/usr/bin/env python3
"""
10_preprint.py - builds the preprint PDF from LaTeX source

PLAIN LANGUAGE HEADER
Compiles preprint/preprint.tex into preprint/preprint.pdf. Run the figure script
first so the figures are current. Needs pdflatex. You do not need to run this
unless you have changed the manuscript text.

Run:  python3 code/09_preprint_figures.py && python3 code/10_preprint.py
"""
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "preprint"

if shutil.which("pdflatex") is None:
    sys.exit("pdflatex not found. Install a TeX distribution, or use the PDF already in preprint/.")

for i in (1, 2):                      # twice, so cross-references resolve
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "preprint.tex"],
                       cwd=PRE, capture_output=True, text=True)
errs = [l for l in r.stdout.splitlines() if l.startswith("! ")]
if errs:
    print("LaTeX reported errors:")
    for e in errs[:10]:
        print("  ", e)
    sys.exit(1)

for junk in ("aux", "log", "out"):
    for f in PRE.glob(f"*.{junk}"):
        f.unlink()
print(f"wrote {PRE / 'preprint.pdf'}")
