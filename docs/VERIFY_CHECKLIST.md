# Verification checklist

**COMPLETED 2026-10-29.** The author worked through this checklist and confirmed the
package. Version 1.0 was cut on that basis, the draft stamps were lifted, and the
publication gate passed with no blockers. The checklist is retained in the repository as
the record of what was checked and as the template for verifying release 2.

---

**Nothing in this project publishes until you have worked through this and said so.**

Your name goes on a permanent public record with a DOI. A wrong number in a Zenodo
release can be superseded but never erased. That is why this list exists and why I will
not go round it.

Total time: about four to six hours. You can do it in sittings. Tick each box.

---

## Part A — The scores are yours (2 to 3 hours)

This is the part only you can do. There are **100 provisional sub-scores** in this
release. I drafted every one. Until you rule on them they are my guesses wearing your
name.

Open `data/raw/steps.yaml`. For each of the seven steps you will find `iars` (5 items),
`crs_baseline` (4 items) and `crs_recommended` (4 items), each with a rationale beside it.
Open `instrument/instrument_v1.yaml` alongside it and read the anchor for each item.

- [ ] **A1. S01 Specimen reception** — 13 sub-scores. The one to argue with is `A2: 2`. I scored containment as "mostly open" on the grounds that leakage in transit is routine. If you think received containers should be scored as closed, this becomes `A2: 4`. **Note the direction:** A2 is reverse-coded inside the aggregation (v1.1), so raising the anchor number means more containment and *lowers* the release score. In v1.0 this ran the wrong way; the checklist text then asserted the opposite of what the code did, which is how the defect survived the first pass.
- [ ] **A2. S02 Centrifugation** — 13 sub-scores. The one to argue with is `A1: 5`. Centrifugation gets the top energy score, but the measured evidence says intact capped tubes release nothing. Decide whether the instrument should score energy applied, or energy escaping.
- [ ] **A3. S03 Cap removal** — 13 sub-scores. Check `A4: 5` (breathing-zone proximity at maximum, because hands come up to chest or face height) and `A2: 1`. A2 is the lowest containment anchor in the reference: this is the only step whose entire purpose is to remove containment, and after reverse-coding it contributes the maximum release value of 5. That single item is why S03's IARS is 4.0 rather than 3.2. Confirm you intend it.
- [ ] **A4. S04 Automated analysers** — 13 sub-scores. Check `crs_baseline` as a block. I assumed closed-tube sampling is available but not always configured. If you think most US core laboratories run closed-tube by default, `C1` goes to 4 and this row changes.
- [ ] **A5. S05 GeneXpert loading** — 13 sub-scores. Check `C1: 4` at baseline. I gave the closed cartridge a high engineering score even with no cabinet, because that is what the measurement supports. Confirm you are willing to publish that.
- [ ] **A6. S06 MALDI-TOF** — 13 sub-scores. Check `A3: 4`. Pure growth and positive-broth transfer are scored as enriched rather than maximum density. Decide whether a heavy plate sweep should be a 5.
- [ ] **A7. S07 Open culture work** — 13 sub-scores. Check `A1: 4`. Is flaming a wet loop high localised energy (4) or very high (5)? It changes the highest score in the reference.
- [ ] **A8. The three agent profiles** — 9 sub-scores in `data/raw/agent_profiles.yaml`. Check `P3.B2: 4` in particular: prophylaxis for the worked example exists but is prolonged and imperfect. Is 4 right, or 5?
- [ ] **A9. The control-credit weight.** Open `instrument/instrument_v1.yaml`, `composition.residual_biorisk_index.control_credit`. It is `0.8`. Perfect controls then cut the release term by 3.2 of a possible 4 points, never to zero. Keep, change, or ask me to run a sensitivity analysis showing how the step ordering moves at 0.5 and 1.0.
- [ ] **A10. The band cut points.** 4, 9, 14, 19. After the A2 correction S07 sits at 19.60, which is one tenth of a point inside **Very high**, and S06 at 17.73 is High. Both are now sensitive to a cut point you set by eye: moving the top boundary from 19 to 20 would drop S07 to High and change the headline sentence of the paper. Decide this deliberately, and consider asking me to run the sensitivity analysis before release 2 rather than after.
- [ ] **A11. The lineage statement.** `instrument/instrument_v1.yaml`, `meta.lineage`. This now describes the instrument's own structure — dimension A assesses, B characterises consequence, C and the evidence grade evaluate — and states that no training material is reproduced, paraphrased or relied on, and that the instrument claims to represent no particular organisation's methodology. **Read it and confirm it is what you want to say.** If you want your Sandia and DTRA training named as the source of the approach, that is your claim to make in your own words; say so and I will put it back. It is deliberately absent from the current text.

**After A1 to A11:** reply with your rulings, or edit `data/raw/steps.yaml` yourself and
tell me. I will re-run the build and the QA and show you what moved.

## Part B — The citations are real (1 to 2 hours)

Five named spot checks. Each takes about ten minutes. Open the URL, find the claim.

- [ ] **B1. CLIA numbers.** Open https://www.cms.gov/files/document/laboratory-statistics.pdf — look for the September 2026 table. You should see Laboratories Registered 301,284, Compliance 15,214, Accreditation 15,542. Confirm those three match `report/stats.json` → `clia_denominator`. Note while you are there that Washington State is CLIA-exempt with 8,106 laboratories, which is worth a sentence in the relevance paragraph.
- [ ] **B2. The negative measurement.** Open https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8097034/ — confirm that the four procedures include opening blood sample tubes and centrifugation, and that bacteria were not recovered in any air or surface sample. Then confirm the S02 and S03 rows in `data/processed/evidence_table.csv` say that and no more than that.
- [ ] **B3. The GeneXpert finding.** Open https://jcm.asm.org/content/48/10/3551 — confirm two things: that infectious-aerosol risk with correct sample reagent use was reduced below that of smear preparation, and that incorrect use was simulated by skipping the recommended incubation. The second point is the one the whole S05 control set hangs on.
- [ ] **B4. The open-bench evidence.** Open https://www.cdc.gov/mmwr/preview/mmwrhtml/mm5107a1.htm and https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6335a2.htm — confirm the three findings quoted in the S07 rows of the evidence table. Pay particular attention to whether I have overstated anything.
- [ ] **B5. The evidence gap.** Open https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12415171/ — confirm that the review identifies automated laboratory equipment as needing characterisation. This single sentence is the basis for grading S04 as E5 and calling it research priority 1. If it does not say that, the strongest claim in the project comes out.
- [ ] **B6. The excluded claim.** `evidence/sources.yaml` → `pending_verification.CUNNINGHAM_PATEL`. I found this at second hand and would not cite it. Either locate and read the primary article and promote it, or leave it out. Do not let it in on the strength of the secondary source.
- [ ] **B7. Read every other row** of `data/processed/evidence_table.csv` against its URL. There are 13 rows. You have done 8 above.

## Part C — The arithmetic (20 minutes)

- [ ] **C1.** Open `data/processed/qa_report.txt`. Confirm it ends "RESULT: all checks passed."
- [ ] **C2.** Pick one row of `data/processed/reference_scores.csv` and do it by hand. Take S07/P3. The raw A items are 4, 1, 5, 5, 4; A2 reverse-codes as 6 − 1 = 5, giving 4, 5, 5, 5, 4, so IARS is 23/5 = 4.6. SCS is the mean of 5, 4, 5 = 4.67. CRS baseline is the mean of 2, 1, 2, 1 = 1.5. So `max(1, 4.6 − 0.8 × 0.5) × 4.67 = 4.2 × 4.67 = 19.60`. Confirm the file says 19.6. **Do this one by hand even if you skip the rest of Part C** — it is the step that exposes the reverse-coding, and the pre-correction version of this item gave a lower figure for S07 without anyone noticing the direction was wrong.
- [ ] **C3.** Reproduce the whole build. Either run it yourself:
      ```
      cd clinical-lab-aerosol-biorisk-reference
      python3 code/02_build.py && python3 code/03_qa.py && python3 code/04_figures.py
      ```
      and confirm `git status` shows no change to the committed outputs — or ask me, in a
      fresh session, to rebuild from scratch and compare the headline numbers. Either
      satisfies this step.
- [ ] **C4.** Run `python3 code/06_agreement.py --selftest` and confirm all assertions pass.

## Part D — The words are yours (30 minutes)

- [ ] **D1.** Rewrite the README summary paragraph in your own voice. Mine is a placeholder.
- [ ] **D2.** Rewrite the technical report abstract in your own voice. If writing is not how you like to work, say so and we will do it line by line out loud, but the final words must be ones you would actually say.
- [ ] **D3.** Read `docs/LIMITATIONS.md` end to end. Add anything I have missed. Remove nothing to make the project look stronger.
- [ ] **D4.** Read `docs/TALK_TRACK.md` aloud, on a timer. If a sentence is not one you would say to a colleague, change it.

## Part E — Identity and licence (10 minutes)

- [ ] **E1.** `AUTHORS.json` — your name exactly as it should appear, ORCID 0000-0002-1978-6133, affiliation "Independent Researcher, Pullman, Washington, USA". Confirm all three. This file feeds the README, the citation file, the Zenodo record and the manuscript, so one error propagates everywhere.
- [ ] **E2.** Confirm CC BY 4.0 for the instrument, data and documents, MIT for code.
- [ ] **E3.** Confirm you are content that the agreement study is deferred to release 4, and that the sentinel module ships as a definitions-only scaffold.

## Part F — The gate

- [ ] **F1.** Run `python3 code/07_publish_gate.py`. It refuses while any DRAFT stamp, `[VERIFY]` tag or placeholder remains. Resolve what it finds.
- [ ] **F2.** Re-run figures with `--final` to strip the DRAFT watermark.
- [ ] **F3.** Say, in your own words, that you have checked this and stand behind it.

Then we publish.
