#!/usr/bin/env python3
"""
07_publish_gate.py - refuses to let unfinished work out of the door

PLAIN LANGUAGE HEADER
Scans the whole project for things that must not be published: DRAFT stamps,
[VERIFY] tags, placeholder brackets, and anything that looks like a password or
token. If it finds any, it stops and lists them. It cannot check whether a score is
correct; only you can do that (docs/VERIFY_CHECKLIST.md).

Run:  python3 code/07_publish_gate.py
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", ".ipynb_checkpoints"}
# This file necessarily contains the patterns it searches for.
SELF = Path(__file__).name
# The checklist and protocol are *about* the draft state and keep their markers.
ALLOWED = {"docs/VERIFY_CHECKLIST.md", "docs/START_HERE.md", "docs/NEXT_STEPS.md",
           "scenarios/AGREEMENT_PROTOCOL.md", "docs/PUBLISH_GUIDE.md"}

# Scripts legitimately contain the words DRAFT and VERIFY because they implement the
# draft machinery. Content blockers skip code/; the secret scan never skips anything.
CODE_EXEMPT = {"VERIFY tag", "DRAFT marker", "placeholder", "unfilled bracket"}

# The secret scan runs on EVERY file, including those exempt from content blockers.
# PUBLISH_GUIDE.md is the file most likely to have a pasted token in it, and it was
# previously skipped wholesale, which defeated the point of the scan.
SECRET = ("possible secret", re.compile(
    r"(gh[pousr]_[A-Za-z0-9]{20,}|"
    r"(ZENODO|ZENODO_SANDBOX|GITHUB)_TOKEN\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{8,}|"
    r"api[_-]?key\s*[:=]\s*['\"]\S+)", re.I))

BLOCKERS = [
    ("VERIFY tag",       re.compile(r"\[VERIFY[-\w]*\]")),
    ("author ruling pending", re.compile(r"\[AUTHOR-RULING-PENDING\]")),
    ("DRAFT marker",     re.compile(r"\bDRAFT\b")),
    ("placeholder",      re.compile(r"\[(insert|TBD|TODO|XXX|FIXME)[^\]]*\]", re.I)),
    ("unfilled bracket", re.compile(r"<[A-Z_]{3,}>")),
]

hits = []
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or any(d in p.parts for d in SKIP_DIRS):
        continue
    rel = p.relative_to(ROOT).as_posix()
    if p.suffix.lower() in {".png", ".jpg", ".pdf", ".docx", ".xlsx", ".zip"}:
        continue
    try:
        text = p.read_text(errors="ignore")
    except Exception:
        continue
    exempt_file = rel in ALLOWED or p.name == SELF
    for line_no, line in enumerate(text.splitlines(), 1):
        # The secret scan runs first and is never skipped, for any file.
        if p.name != SELF and SECRET[1].search(line):
            hits.append((SECRET[0], rel, line_no, "<redacted: possible credential>"))
        if exempt_file:
            continue
        for name, rx in BLOCKERS:
            if name in CODE_EXEMPT and rel.startswith("code/"):
                continue
            if rx.search(line):
                hits.append((name, rel, line_no, line.strip()[:110]))

print("=" * 78)
print("PUBLICATION GATE")
print("=" * 78)
if not hits:
    print("\nNo blockers found in the files scanned.\n")
    print("The mechanical half is clear. The human half is not scriptable:")
    print("  - every score ruled on by the author")
    print("  - every citation checked against its source")
    print("  - the README and abstract written in the author's own voice")
    print("  - the author's explicit statement that they stand behind it")
    print("\nSee docs/VERIFY_CHECKLIST.md. Do not publish until that is done.\n")
    sys.exit(0)

by_kind = {}
for name, rel, ln, txt in hits:
    by_kind.setdefault(name, []).append((rel, ln, txt))
print(f"\nREFUSING TO PROCEED. {len(hits)} blocker(s) in "
      f"{len({h[1] for h in hits})} file(s).\n")
for name, rows in by_kind.items():
    print(f"{name} ({len(rows)}):")
    for rel, ln, txt in rows[:12]:
        print(f"   {rel}:{ln}  {txt}")
    if len(rows) > 12:
        print(f"   ... and {len(rows) - 12} more")
    print()
print("Resolve these, then run this script again.")
print("Figures: re-run `python3 code/04_figures.py --final` to remove the watermark.")
sys.exit(1)
