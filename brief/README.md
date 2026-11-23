# Technical report: procedure inventory and evidence brief

**Aerosol-generating steps in routine clinical laboratory testing:
a procedure inventory and evidence brief**

Oyekunle Adedamola Oyeniyi · ORCID 0000-0002-1978-6133

`brief.pdf` is the compiled report, 11 pages, two-column.

## What this is, and how it differs from the preprint

This repository carries two written outputs.

- `preprint/` is the **instrument paper**. Its subject is the method: the
  anchored scoring items, the composition formula, the ISO 35001:2019 mapping,
  and the planned agreement study. Its reader is a methodologist.
- `brief/` is this **technical report**. Its subject is the findings as a
  practical inventory: what the seven bench steps are, what is known about
  each, how strong that knowledge is, and what controls the evidence supports.
  Its readers are laboratory practitioners, tuberculosis programmes, and
  bodies designing laboratory surveys.

The brief is intended to support comment on tuberculosis laboratory survey
practice, and Section VI and Table 2 are written for that use.

## Its principal contribution

Section IV assembles, on one logarithmic axis, every airborne concentration
measurement located for clinical laboratory bench work. That assembly does not
appear to exist elsewhere, and it is short: four conditions in which nothing
was recovered, two discrete values for acid-fast smear preparation, and three
simulated accident intensities. The point of the figure is coverage, not
ranking; the studies were not designed to be compared and the caption says so.

## Building it

```bash
python3 code/11_brief_figures.py   # three figures, seaborn, from project data
python3 code/12_brief.py           # compiles brief.pdf, needs pdflatex
```

Every number in the text and every figure is generated from the project's own
data files, so the report cannot disagree with the data behind it.

## Files

| File | Contents |
|---|---|
| `brief.tex` | Document root |
| `preamble.tex` | Layout, shared with the preprint |
| `title_block.tex` | Title, author, abstract, keywords |
| `sec01_intro.tex` | Introduction, purpose, TB relationship |
| `sec02_method.tex` | Scope, step definition, source identification, grading |
| `sec03_inventory.tex` | The seven steps, Table 1 |
| `sec04_measured.tex` | What has been measured, Figure 1 |
| `sec05_profile.tex` | Evidence profile, Figure 2 |
| `sec06_tb.tex` | The tuberculosis pathway, Figure 3 |
| `sec07_survey.tex` | Fourteen survey items, Table 2 |
| `sec08_limits.tex` | Limitations, conclusion, declarations |
| `sec09_refs.tex` | References |
| `figures/` | Figure PDFs and PNGs |

## Status

Derived from Clinical Laboratory Aerosol Biorisk Reference v1.1, after the
author's verification pass. Not yet deposited; no DOI. Target deposit
December 2026.
