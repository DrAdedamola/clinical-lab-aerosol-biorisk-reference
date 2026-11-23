# Preprint

`preprint.pdf` is the manuscript. Everything else here builds it.

## Files

| File | What it is |
|---|---|
| `preprint.pdf` | The manuscript, 10 pages, two-column. This is the file you submit. |
| `preprint.tex` | Master file. It pulls in the pieces below. |
| `preamble.tex` | Page geometry, fonts, section styling. |
| `title_block.tex` | Title, author, abstract, keywords. |
| `sec_intro_methods.tex` | Sections I and II. |
| `sec_results.tex` | Section III. |
| `sec_discussion.tex` | Sections IV and V, and the back matter. |
| `sec_tables.tex` | Tables 1 to 4. |
| `sec_figures.tex` | Figure blocks and captions. |
| `sec_refs.tex` | The reference list. |
| `figures/` | Figures as PDF (used by LaTeX) and PNG (for slides and the web). |

## Rebuilding

```bash
python3 code/09_preprint_figures.py   # redraw the figures from stats.json
python3 code/10_preprint.py           # compile the PDF
```

Every number in the manuscript was taken from `report/stats.json` and checked against
`data/processed/reference_scores.csv` at the time of writing. If you change a score,
re-run `code/02_build.py` first, then check that the figures in the text still match.

## Where it is going

medRxiv. See `docs/PUBLISH_GUIDE.md` for the submission steps. You submit this yourself:
a preprint submission is an attestation that the work is yours, which is not something
that can be delegated.
