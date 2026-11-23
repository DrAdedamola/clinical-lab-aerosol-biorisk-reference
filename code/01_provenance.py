#!/usr/bin/env python3
"""
01_provenance.py - record where every source came from

PLAIN LANGUAGE HEADER
Writes data/raw/PROVENANCE.txt: for every source, the URL, the date it was opened,
and, where the file could be downloaded, its size and a fingerprint (SHA-256) so a
future reader can tell whether the source has changed since. You do not need to run
this; it has already been run and its output is committed.
"""
import hashlib, re, ssl, sys, urllib.request
from datetime import date
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SRC = yaml.safe_load(open(ROOT / "evidence/sources.yaml"))["sources"]
LOG = RAW / "PROVENANCE.txt"
FETCH = "--fetch" in sys.argv

# A run without --fetch must never downgrade a fingerprint that a previous run recorded.
# Overwriting sha256 lines with "NOT RETRIEVED" silently erases the provenance record,
# which is the one thing this file exists to preserve. Any existing digests are read back
# and reused unless this run actually re-fetches.
PRIOR = {}
if LOG.exists():
    key = None
    for line in LOG.read_text().splitlines():
        if re.fullmatch(r"[A-Z][A-Z0-9_]*", line.strip()):
            key = line.strip()
        elif key and line.strip().startswith("fingerprint  : sha256:"):
            PRIOR[key] = line.split("fingerprint  : ", 1)[1].strip()
        elif key and line.strip().startswith("bytes        :"):
            PRIOR[key + "::bytes"] = line.split("bytes        : ", 1)[1].strip()
if PRIOR and not FETCH:
    print(f"carrying forward {len([k for k in PRIOR if not k.endswith('::bytes')])} "
          f"existing fingerprint(s); re-run with --fetch to refresh them")

lines = [
    "PROVENANCE LOG - Clinical Laboratory Aerosol Biorisk Reference",
    f"Generated {date.today().isoformat()} by code/01_provenance.py",
    "",
    "Every source in evidence/sources.yaml, with the URL it was read from and the date.",
    "Where a fingerprint is recorded, the file was downloaded and hashed; where it says",
    "NOT RETRIEVED, the source was read in a browser and the URL is the record.",
    "",
    "Note on rediscovery: the CMS laboratory statistics file is published at a stable",
    "path but its CONTENTS are replaced each month. A reader checking this reference",
    "after September 2026 will find different numbers at the same URL. The figures used",
    "here are the September 2026 vintage, recorded in report/stats.json.",
    "",
    "-" * 78,
]

for key, s in sorted(SRC.items()):
    url = s.get("url") or s.get("url_contents_page") or ""
    lines += [f"{key}", f"  title        : {s.get('title','')}",
              f"  url          : {url}",
              f"  access_date  : {s.get('access_date','')}",
              f"  vintage      : {s.get('vintage', s.get('year',''))}",
              f"  terms_of_use : {s.get('terms_of_use','not stated by publisher')}"]
    digest = PRIOR.get(key, "NOT RETRIEVED (read in browser; URL is the record)")
    size = PRIOR.get(key + "::bytes", "")
    if size == "n/a":
        size = ""
    if FETCH and url:
        try:
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(url, timeout=25, context=ctx) as r:
                b = r.read()
            digest = "sha256:" + hashlib.sha256(b).hexdigest()
            size = f"{len(b)} bytes"
        except Exception as e:
            digest = f"NOT RETRIEVED ({type(e).__name__})"
    lines += [f"  bytes        : {size or 'n/a'}", f"  fingerprint  : {digest}", ""]

lines += ["-" * 78,
          "Sources identified but NOT verified at source, and therefore NOT cited:",
          *[f"  {k}" for k in yaml.safe_load(open(ROOT / 'evidence/sources.yaml'))['pending_verification']],
          ""]
LOG.write_text("\n".join(lines))
n_fp = sum(1 for l in lines if "fingerprint  : sha256:" in l)
print(f"wrote {LOG} ({len(SRC)} sources, {n_fp} with fingerprints)")
if not FETCH:
    print("run with --fetch to download each source and refresh its fingerprint")
