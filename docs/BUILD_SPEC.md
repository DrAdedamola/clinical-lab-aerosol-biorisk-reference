# Build spec v1.0

Written before any code. If the project changes shape, this file changes first.

```
PROJECT:   Clinical Laboratory Aerosol Biorisk Reference
           Archetypes: (4) benchmark/scoring instrument + (7) evidence map
                       + (9) technical report. Three stacked, one build.

QUESTION:  For each of seven routine bench steps in a clinical diagnostic
           laboratory, what is actually known about infectious aerosol release,
           how strong is that evidence, and what control set does the evidence
           support?

SOURCES:   Open literature (PubMed Central, open-access journals) on aerosol
           measurement during laboratory procedures and on laboratory-acquired
           infections; CDC BMBL 6th edition; WHO Laboratory Biosafety Manual
           4th edition; CDC MMWR laboratory exposure reports; ASM/APHL Sentinel
           Level Clinical Laboratory Protocols (free PDFs, asm.org); CMS CLIA
           laboratory statistics (September 2026); ISO 35001:2019 clause
           numbers and titles only, taken from the publicly posted contents
           page of the standard. Every source free to access. No ISO text is
           reproduced; no paywalled full text is relied on for a scored claim.

UNIT:      One bench step (procedure), as defined in data/raw/steps.yaml.
           Seven steps in the core reference; the sentinel module adds steps
           drawn from the ASM rule-out and referral algorithms.

MEASURES:
  IARS  Inherent Aerosol Release Score. Mean of five anchored sub-scores
        (energy applied, specimen containment, volume and concentration,
        breathing-zone proximity, throughput). 1 to 5.
  SCS   Scenario Consequence Score. Mean of three anchored sub-scores
        (inhalational infectious dose, prophylaxis and treatment availability,
        likelihood of unsuspected presence). 1 to 5. Agent-dependent, so it is
        a scenario parameter, not a property of the step.
  CRS   Control Reliability Score. Mean of four anchored sub-scores
        (engineering control effectiveness, independence from human
        performance, verification and certification, PPE adequacy). 1 to 5.
  RBI   Residual Biorisk Index = max(1, IARS - 0.8 x (CRS - 1)) x SCS.
        Range 1 to 25. Banded Low / Moderate / Elevated / High / Very high.
  EG    Evidence Grade, E1 to E5. Reported beside every score, never averaged
        into it. E1 direct quantitative measurement of this step; E2
        quantitative measurement of a closely analogous step; E3 epidemiological
        or incident evidence linking the step to infection; E4 authoritative
        guidance or expert consensus only; E5 no evidence located.

OUTPUTS:
  instrument/instrument_v1.yaml        machine-readable scoring instrument
  instrument/iso35001_map.csv          element to ISO 35001 clause mapping
  docs/CODEBOOK.md                     every field defined
  data/processed/reference_scores.csv  the seven steps scored
  data/processed/control_sets.csv      recommended controls per step
  data/processed/evidence_table.csv    every cited finding, per step
  data/processed/qa_report.txt         quality checks
  scenarios/scenarios.yaml             published exposure scenarios to rate
  scenarios/rating_form_blank.csv      what each rater fills in
  data/processed/agreement_results.*   inter-rater agreement (after real rating)
  report/stats.json                    every number any document quotes
  report/technical_report.md|.pdf      the citable write-up

VENUES:    GitHub repository; Zenodo versioned DOI (instrument v1.0, then
           reference scores, then sentinel module); a preprint or an
           open-access biosafety or laboratory-medicine journal for the
           instrument-and-agreement paper; conference abstract (ABSA
           International, ASM Microbe) as a secondary output.

VERIFY POINTS (the author personally rules on each):
  V1  The seven step definitions and their boundaries.
  V2  Every sub-score anchor wording.
  V3  Every provisional score for all seven steps.
  V4  The RBI formula's control-credit weight (0.8 per CRS point) and the band
      cut points.
  V5  Whether SCS is fixed at a reference agent profile or reported across
      three profiles.
  V6  Every citation checked against its source.
  V7  The BRACE lineage statement: how the instrument's elements correspond to
      what was taught in the Sandia workshops. This is the author's own
      knowledge, not something I can source.
  V8  The second rater's identity and the agreement results.

LICENSE:   Code MIT. Data, instrument and documents CC BY 4.0.

DECISIONS (author, 2026-10-29):
  D1  Three agent profiles reported side by side, not one. Each step also
      carries a primary profile, the realistic operating case.
  D2  The inter-rater agreement study is deferred to release 4. The protocol is
      registered in advance and the analysis code is written and self-tested;
      no agreement figure is published without a real second rater.
  D3  Both a technical report and a journal manuscript draft are produced.
  D4  CC BY 4.0 for instrument, data and documents; MIT for code.

ASSUMPTIONS (proceeding on these until corrected):
  A1  The "automated chemistry and hematology analyzers" item is one step with
      two sub-contexts, as the brief describes it.
  A2  The scoring assumes US CLIA moderate- and high-complexity settings.
  A3  Agreement statistic is Gwet's AC2 with ordinal weights, with weighted
      Cohen's kappa reported alongside, because kappa is unstable when ratings
      cluster in one category and these scores will cluster.
```
