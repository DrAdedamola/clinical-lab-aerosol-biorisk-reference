# Clinical Laboratory Aerosol Biorisk Reference

**Status: Released v1.1, 2026-10-29.** Verified by the author. DOI pending first deposit.
Instrument version 1.1 · Supersedes v1.0, withdrawn before deposit

An open, step-by-step evidence base and scoring reference for the bench steps of routine
diagnostic testing that can generate infectious aerosols.

---

## What this is, in plain words

Every clinical laboratory in the United States is told to assess the risk of its own
procedures. Nobody is told how to do it for a single step at the bench. This project takes
seven everyday bench steps, says what is actually known about each one releasing germs into
the air, grades how strong that evidence is, gives each step a score, and recommends a set
of controls. Everything is cited to a source anyone can open for free.

The headline finding is an inversion. The steps laboratories worry about most, uncapping
tubes and spinning centrifuges, have been measured and found to release little. The steps
that have actually infected and killed laboratory workers, open-bench culture work above
all, have never been measured at all. And the highest-throughput step in the whole
laboratory, running specimens on automated chemistry and haematology analysers, has no
located evidence of any kind.

## The seven bench steps

| ID | Step | Evidence grade |
|---|---|---|
| S01 | Specimen reception and accessioning | E2 analogous measurement |
| S02 | Centrifugation of primary specimen tubes | E1 direct measurement |
| S03 | Cap removal, decapping and aliquoting | E1 direct measurement |
| S04 | Automated chemistry and haematology analyser operation | **E5 no evidence located** |
| S05 | GeneXpert cartridge loading | E1 direct measurement |
| S06 | MALDI-TOF target preparation and identification | E3 incident evidence |
| S07 | Open-tube and open-plate culture work | E3 incident evidence |

## How to run it

Requires Python 3 with `pyyaml` and `matplotlib`.

```bash
python3 code/01_provenance.py      # record where every source came from
python3 code/02_build.py           # compute every score, write the tables and stats.json
python3 code/03_qa.py              # quality checks; read data/processed/qa_report.txt
python3 code/04_figures.py         # figures (add --final only after verification)
python3 code/05_report.py          # technical report and manuscript, built from stats.json
python3 code/06_agreement.py --selftest   # check the agreement arithmetic
python3 code/07_publish_gate.py    # refuses while any draft marker remains
python3 code/08_pdf.py             # typeset PDF of the technical report (needs pandoc)
python3 code/09_preprint_figures.py # preprint figures, seaborn style
python3 code/10_preprint.py        # compile the preprint PDF (needs pdflatex)
```

Scripts are numbered in run order and each is runnable on its own. A stranger running them
top to bottom from this README gets the committed outputs.

## Where to start reading

| If you want to | Open |
|---|---|
| Understand the project in five minutes | `docs/START_HERE.md` |
| Use the instrument on your own bench | `instrument/instrument_v1.yaml` |
| See the scores | `data/processed/reference_scores.csv` |
| See the controls | `data/processed/control_sets.csv` |
| Check a claim | `data/processed/evidence_table.csv` and `evidence/sources.yaml` |
| Know what every column means | `docs/CODEBOOK.md` |
| Know what this cannot do | `docs/LIMITATIONS.md` |
| Look up a term | `docs/GLOSSARY.md` |
| Read the preprint | `preprint/preprint.pdf` |
| Read the shorter write-up | `report/technical_report.pdf` or `.md` |
| See what changed and what is known to be missing | `RELEASE_NOTES.md` |

## Sources

All openly accessible. Full register with URLs and access dates in `evidence/sources.yaml`;
fingerprints and retrieval record in `data/raw/PROVENANCE.txt`.

Principal sources: CMS CLIA laboratory statistics (September 2026); CDC BMBL 6th edition;
WHO Laboratory Biosafety Manual 4th edition; ASM/APHL Sentinel Level Clinical Laboratory
Protocols; and the peer-reviewed aerosol-measurement and laboratory-acquired-infection
literature.

**On ISO 35001:2019:** this project reproduces clause numbers and titles only, as a
structural index, taken from the publicly posted contents page. No requirement text,
figure or definition from the standard appears anywhere in this repository. You do not
need to buy the standard to use this reference.

## Version history

**v1.1** supersedes **v1.0**, which was withdrawn before deposit. Item A2 (containment) is
reverse-coded inside the aggregation: in v1.0 better containment raised the release score.
Anchor wording is unchanged, so rating sheets completed against v1.0 anchors remain valid.
Five evidence corrections were applied at the same time. See `RELEASE_NOTES.md`.

## Releases planned

1. Scoring instrument v1.0, with ISO 35001:2019 clause mapping.
2. Reference scores and control sets for the seven bench steps, with cited sources.
3. Sentinel laboratory module, applying the same scoring to rule-out and referral steps.
4. Inter-rater agreement study on published exposure scenarios.

Protocol for release 4 is registered in advance at `scenarios/AGREEMENT_PROTOCOL.md`.

## Licence

Instrument, data and documents: CC BY 4.0. Code: MIT. See `LICENSE`.

## Citation

See `CITATION.cff`. A DOI will be minted on first release and added here.

## Author

Oyekunle Adedamola Oyeniyi, Independent Researcher, Pullman, Washington, USA.
ORCID [0000-0002-1978-6133](https://orcid.org/0000-0002-1978-6133).

## How this was made

Built with AI assistance for code, data wrangling, literature triage and drafting
mechanics. Every analytic decision, every score and every citation is the author's, checked
against its source. The verification checklist that gates release is at
`docs/VERIFY_CHECKLIST.md`.
