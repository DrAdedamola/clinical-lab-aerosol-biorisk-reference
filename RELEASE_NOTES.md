# Release notes

## v1.0 — 2026-10-29

First release. Verified by the author and cut from a clean rebuild that reproduced every
committed output.

**Contains**

- Procedure-level BRACE scoring instrument v1.0: 12 anchored items across three scored
  dimensions, plus a separately reported evidence grade, with explicit scoring rules.
- ISO 35001:2019 clause mapping: 62-clause index, 32 instrument-element references,
  56 step references. Clause numbers and titles only; no text of the standard.
- Reference scores for seven bench steps under three agent profiles: 17 scored rows.
- 76 recommended controls, grouped by the hierarchy of controls.
- 12 cited findings from 16 openly accessible sources, with URLs, access dates and
  retrieval fingerprints.
- Sentinel laboratory module scaffold: five steps defined, deliberately unscored.
- Inter-rater agreement protocol, registered in advance, with self-tested analysis code.
- Technical report and journal manuscript draft, both built from `report/stats.json`.

**Decisions recorded in this release**

- Three agent profiles are reported side by side; each step also carries a primary
  profile, the realistic operating case.
- The control-credit weight (0.8) and band cut points (4, 9, 14, 19) are author-set and
  asserted, not derived. Sensitivity analysis is scheduled for release 2.
- No numeric wait interval is given for opening a centrifuge or its sealed buckets,
  because none in the located evidence is derived from measurement of a clinical
  centrifuge.
- No standard designation or interval is named for cabinet certification, because neither
  was confirmed at source. The controls require each laboratory to record its own.
- One claim material to the MALDI-TOF control set is held in the pending register and
  excluded from every score, because it was found only at second hand.
- The sentinel step covering exposure assessment after retrospective recognition will be
  scored on a separate consequence-mitigation scale in release 3, not forced into an
  instrument built to score release.

**Known gaps, stated rather than hidden**

- Inter-rater agreement has not been measured. Every score is one rater's reading.
- The literature search was targeted, not systematic.
- Baseline control scores characterise common practice as described in the literature and
  guidance; no survey of laboratories was conducted.

**Not yet done**

Nothing has been deposited. No DOI exists. `docs/PUBLISH_GUIDE.md` has the steps.

## v1.1 — 2026-10-29

Corrections arising from the author's verification pass, and the preprint.

**Scoring defect corrected**

Item A2 (containment of the specimen during the step) is anchored 1 = fully open through
5 = fully closed, while dimension A aggregates as a plain mean in which a higher value
means more release. The item was being aggregated untransformed, so better containment was
*raising* the release score. The instrument now declares A2 as reverse-coded and applies
`A2' = 6 - A2` inside the aggregation; the published anchor wording is unchanged, and the
item carries an explicit direction note modelled on the one B2 already had.

Five of seven steps moved. Scores at the primary agent profile, before and after:

| Step | Was | Now |
|---|---|---|
| Specimen reception | 5.00 Moderate | 5.67 Moderate |
| Centrifugation | 4.67 Moderate | 4.67 Moderate (unchanged) |
| Cap removal | 5.00 Moderate | 6.33 Moderate |
| Automated analysers | 3.33 Low | 3.33 Low (unchanged) |
| GeneXpert loading | 8.40 Moderate | 10.27 Elevated |
| MALDI-TOF identification | 14.00 Elevated | 17.73 High |
| Open culture work | 15.87 High | **19.60 Very high** |

The correction raises the open-bench steps the reference is about. Verification checklist
items A1, A3 and A10 were rewritten, having been drafted against the broken arithmetic.

**Evidence corrections**

1. The centrifuge rotor-leak finding attributed to Ravnholdt et al. was struck; it is not
   in that review. Replaced with what the review does say. The quantitative comparison
   moved to Liu et al. 2023 and is now stated in the correct direction: centrifugal tube
   rupture at roughly 10–100 CFU/m³, *below* the 10³–10⁴ CFU/m³ of drops and injection.
   The failure-conditional flag on centrifugation is retained but now rests on the
   breakage literature and guidance.
2. The specimen-reception drop claim, previously asserted in prose with no row behind it,
   now has its own evidence row cited to Liu et al., graded E2 with the inference stated
   (30 mL of concentrated suspension in a research laboratory, not clinical specimens).
   S01 moved from E4 to E2.
3. Containment conditions added to the centrifugation and cap-removal rows: closed-cap
   swing-bucket rotor, plexiglass panel, detection limit 4 CFU/m³. The negative result is
   evidence that the recommended controls work, not that the baseline is adequate, and
   LIMITATIONS item 4 now says so. SC002's `silent_on` list corrected.
4. The second GeneXpert finding was pulled pending the Banada methods section; the
   abstract describes no simulated incorrect-use condition, and the sterilisation variable
   is the reagent-to-sputum ratio rather than contact time. E1 retained on the bioaerosol
   comparison alone, now stated at full strength (0 CFU/m³ against 16 and 325 CFU/m³ for
   smear preparation). The control widened from a bench timer to reagent ratio, dispensing
   and contact time; the claim that a timer is the single control the safety case depends
   on was dropped.
5. The MALDI-TOF trigger was rebuilt. In three of the four exposure events the initial
   Gram stain suggested streptococci, so the previous Gram-stain prompt would have failed
   to fire and the stated failure mode was wrong. Replaced with a blanket rule on
   slow-growing blood culture isolates irrespective of stain appearance, plus a clinical
   and travel history cue.

**Added**

- `preprint/` — the manuscript as a 10-page two-column preprint, with four figures.
- `code/09_preprint_figures.py`, `code/10_preprint.py`.

**Counts after correction:** 18 evidence findings (from 13), 78 controls (from 76),
15 sources, 21 QA checks passing, 0 failing.
