# Codebook

Every file and every column, defined. If a number appears anywhere in this project,
its definition is here.

---

## data/processed/reference_scores.csv

One row per bench step per applicable agent profile. 17 rows.

| Column | Definition |
|---|---|
| `step_id` | S01 to S07. The step identifier used throughout. |
| `step_name` | Full name, from `data/raw/steps.yaml`. |
| `agent_profile` | P1, P2 or P3. See `data/raw/agent_profiles.yaml`. |
| `agent_profile_name` | Plain name of the profile. |
| `is_primary_profile` | True where this profile is the realistic operating case for the step. Headline figures use these rows only. |
| `IARS` | Inherent Aerosol Release Score. Mean of items A1 to A5 **with A2 reverse-coded as (6 − A2)**, because A2 is anchored on containment and a high raw value is a low-release condition. 1 to 5, two decimals. A property of the step, before any control. |
| `IARS_items_scored` | How many of the five release items were scored. Always 5 in this release. Present so that any future NA is visible rather than hidden in a mean. |
| `SCS` | Scenario Consequence Score. Mean of B1, B2, B3 for this agent profile. 1 to 5. |
| `CRS_baseline` | Control Reliability Score under common current practice. Mean of C1 to C4. 1 to 5. Higher means more reliable. |
| `CRS_recommended` | Control Reliability Score with the recommended control set applied. |
| `residual_release_baseline` | `max(1, IARS - 0.8 x (CRS_baseline - 1))`. The release term after credit for baseline controls. |
| `residual_release_recommended` | The same with `CRS_recommended`. |
| `RBI_baseline` | `residual_release_baseline x SCS`. 1 to 25. |
| `RBI_baseline_band` | Low, Moderate, Elevated, High or Very high. Cut points 4, 9, 14, 19. |
| `RBI_recommended` | `residual_release_recommended x SCS`. |
| `RBI_recommended_band` | Band for the recommended state. |
| `RBI_reduction` | `RBI_baseline - RBI_recommended`. What the recommendation is worth for this step and profile. |
| `evidence_grade` | E1 to E5. **Never an input to any score.** |
| `conditionality` | `none`, `failure-conditional` or `technique-conditional`. Whether the evidence splits between the step done as intended and the step done with a named failure. |
| `status` | Release marker. Names the instrument version and the date the scores were ruled on. |

## data/processed/control_sets.csv

One row per recommended control. 76 rows.

| Column | Definition |
|---|---|
| `step_id`, `step_name` | The step the control belongs to. |
| `control_category` | `engineering`, `cabinet_use`, `ppe` or `administrative`. Categories are ordered by the hierarchy of controls, not alphabetically. |
| `control_number` | Position within its category for that step. Not a priority ranking. |
| `control` | The recommendation, in full. |

## data/processed/evidence_table.csv

One row per cited finding. 13 rows.

| Column | Definition |
|---|---|
| `step_id`, `step_name` | The step the finding bears on. |
| `finding` | What the source reports, paraphrased. |
| `direction` | `positive` (supports release or harm), `negative` (found none), `gap` (source states no evidence exists), `control recommendation`, or `not yet admissible`. |
| `source_key` | Key into `evidence/sources.yaml`. |
| `source_title`, `source_url`, `access_date` | Resolved from the source register. A row reading PENDING VERIFICATION is deliberately not citable. |

## data/processed/step_iso35001_map.csv and instrument/iso35001_map.csv

| Column | Definition |
|---|---|
| `element` / `step_id` | The instrument element (IARS, A1, C3, EG...) or the bench step. |
| `level` | `dimension` or `item`, for the instrument map only. |
| `iso35001_clause` | Clause number, e.g. `6.1.3`. |
| `iso35001_clause_title` | Clause title, from `instrument/iso35001_clauses.csv`. **Numbers and titles only. No text of the standard is reproduced anywhere in this project.** |

## report/stats.json

The only place any document may take a number from. Written by `code/02_build.py`.
If a figure in the report disagrees with this file, the report is wrong.

Keys include `n_steps`, `n_scored_rows`, `n_instrument_items`, `n_controls`,
`n_sources`, `evidence_grade_counts`, `n_steps_with_no_direct_measurement`,
`control_credit`, `profile_scs`, `primary_profile_rows`, `max_rbi_baseline`,
`mean_rbi_reduction`, and `clia_denominator`.

## data/processed/qa_report.txt

Output of `code/03_qa.py`. Read it before trusting anything. It confirms the arithmetic
and the referencing. It does not confirm that any score is correct.

## Source files, for completeness

- `instrument/instrument_v1.yaml` — the instrument: dimensions, items, anchors, formula, bands, evidence grades, scoring rules.
- `instrument/iso35001_clauses.csv` — the clause index, 62 rows, numbers and titles.
- `data/raw/steps.yaml` — step definitions, boundaries, sub-scores, rationale, evidence, controls.
- `data/raw/agent_profiles.yaml` — the three agent profiles and their B scores.
- `evidence/sources.yaml` — the source register, plus a register of sources identified but not verified and therefore not citable.
- `sentinel/sentinel_module.yaml` — release 3 scaffold. Definitions only, no scores.
- `scenarios/scenarios.yaml` — vignettes for the agreement study. Seed set.
