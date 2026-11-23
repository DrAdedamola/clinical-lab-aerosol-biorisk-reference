# Limitations

Written before the discussion section of any paper, so that the paper cannot outrun it.

1. **The scores are expert judgement, not measurement.** The instrument makes judgement
   structured, explicit and arguable. It does not make it empirical. Any reader who
   disagrees with a sub-score can see exactly which anchor was applied and argue with it,
   which is the point, but the number is still a judgement.

2. **Inter-rater agreement has not yet been measured.** Until it is, every score in this
   release is one person's reading of the anchors. The protocol is registered in
   `scenarios/AGREEMENT_PROTOCOL.md` and the analysis code is written and self-tested, but
   no rating has been done. Readers should treat the scores accordingly.

3. **The evidence base is thin, and that is the finding rather than a flaw in the method.**
   Of seven steps, three carry direct measurement, two rest on incident reports with no
   aerosol measurement at all, one rests on guidance alone, and one has no located evidence
   of any kind. Nothing the instrument does can manufacture evidence that does not exist.

4. **The negative measurements were obtained with the controls already in place, and
   that is what they are evidence for.** This is the most consequential reading error the
   reference could invite, so it is stated plainly. In the pre-analytical study, the
   centrifugation run used closed-cap swing-bucket containment and the tubes were opened
   behind a plexiglass panel. The result therefore shows that the recommended controls
   work. It does not show that an uncontrolled bench is adequate, and it must not be
   cited to that effect. The study also had a stated detection limit of 4 CFU per cubic
   metre: "nothing was recovered" means "nothing above 4 CFU per cubic metre was
   recovered", which is not the same as nothing released. Add to this a model bacterium
   at a chosen concentration, one laboratory, and correct technique throughout, and a
   single negative study is not clearance for a procedure.

5. **The control-credit weight and the band cut points are set by the author, not
   derived.** The instrument reduces the release term by 0.8 points for each point of
   control reliability, and the bands are drawn at 4, 9, 14 and 19. Neither choice is
   empirical. Sensitivity of the step ordering to the control credit has now been tested
   at 0.5, 0.8 and 1.0 and the ordering is robust across that range, so this is a
   limitation on the absolute values rather than on the ranking. Band membership near a
   cut point remains sensitive by construction.

5a. **The headline is more sensitive to primary-profile assignment than to any parameter
   in the formula.** Each step is reported at one primary agent profile, and that
   assignment is a judgement, not a calculation. Because the consequence score multiplies
   the whole expression, moving a step between profiles moves its index far more than any
   plausible change to the control credit does: the same step reads very differently at a
   profile score of 1.67 than at 4.67. The ordering in the headline table is therefore an
   artefact of profile assignment as much as of the scores themselves, and a reader who
   disagrees with an assignment should read the full results across all profiles in
   `data/processed/reference_scores.csv` rather than the primary-profile table.

6. **Agent profiles are stylised.** Three profiles stand in for an enormous diversity of
   organisms. A laboratory with a specific organism in mind should score dimension B for
   that organism rather than take a profile off the shelf.

7. **The reference describes US CLIA moderate- and high-complexity practice.** Equipment,
   staffing and regulation differ elsewhere. The instrument should transfer; the baseline
   control scores almost certainly do not.

8. **Baseline control scores describe common practice as reported in the literature and in
   guidance, not a surveyed sample.** No survey of what laboratories actually do was
   conducted. A baseline score is therefore a characterisation, not an estimate.

9. **Throughput is scored per operator per shift, which varies enormously** between a small
   rural laboratory and a core laboratory running thousands of specimens a day. The same
   step can legitimately score 3 in one and 5 in the other.

10. **ISO 35001 mapping is structural, not a conformity assessment.** The mapping says which
    clause an element speaks to. It does not assert that applying the instrument makes a
    laboratory conformant, and this project is not a certification scheme.

11. **The literature search was not systematic.** Sources were identified by targeted
    searching, not by a registered systematic search with a recorded strategy and a
    screening log. An evidence map claiming completeness would need that; this release does
    not claim it. A systematic search is scheduled for release 2.

12. **One claim material to the MALDI-TOF control set is excluded** because it was found
    only at second hand. It is recorded in `evidence/sources.yaml` under
    `pending_verification` rather than cited, and the S06 control set is therefore more
    cautious than the full evidence may warrant. For the same reason this release names no
    standard designation or interval for biological safety cabinet certification, and
    instead requires each laboratory to record the standard and interval it applies.

13. **The sentinel module is a scaffold.** Its steps are defined; it carries no scores, and
    should not be cited as though it did. One of its steps, exposure assessment after
    retrospective recognition, controls consequence rather than release and will be scored
    on a separate scale in release 3 rather than forced into this instrument.

14. **No numeric wait interval is given for opening a centrifuge or its sealed buckets.**
    No interval in the located evidence is derived from measurement of a clinical
    centrifuge. A number stated here would acquire an authority the evidence does not
    support, so the control requires the laboratory to set, record and justify its own.
