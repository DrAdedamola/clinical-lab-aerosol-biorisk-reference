# Next steps

What each release adds, so that a v1.0 is understood as a first step rather than a
finished thing.

## Release 1 — Scoring instrument v1.0 (ready now, pending your verification)

The instrument, the ISO 35001:2019 clause mapping, the codebook, the provenance log and
the scoring rules. Zenodo DOI.

## Release 2 — Reference scores and control sets (ready now, same gate)

Scores for the seven bench steps under three agent profiles, with cited sources and
recommended control sets. Adds, before release:

- A **systematic literature search** with a recorded strategy, dates, databases and a
  screening log, to replace the targeted search used here. This is the single biggest
  upgrade available and it would let the project claim completeness, which it currently
  cannot.
- A **sensitivity analysis** on the control-credit weight (0.5, 0.8, 1.0) and the band cut
  points, showing how far the step ordering moves. At present both are asserted.
- Resolution of the pending source in `evidence/sources.yaml`.

## Release 3 — Sentinel laboratory module (scaffold built)

The same scoring applied to the rule-out and referral steps of the ASM Sentinel Level
Clinical Laboratory Protocols. Five steps are defined in `sentinel/sentinel_module.yaml`.
Needs: reading the current agent-specific protocols at source, and a decision on how to
score SL03, which controls consequence rather than release and does not fit the instrument
as written. That decision is itself a methodological contribution.

## Release 4 — Inter-rater agreement study

Protocol registered in advance at `scenarios/AGREEMENT_PROTOCOL.md`; analysis code written
and self-tested at `code/06_agreement.py`. Needs: a second rater, and 22 more scenario
vignettes drafted from the source register to reach n = 25. Until this is done, every score
in the reference is one person's reading and the project says so plainly.

## Beyond

- **The measurement study the reference argues for.** Release 2 identifies automated
  analysers as research priority 1: highest throughput, grade E5. A collaboration with a
  core laboratory and an aerosol group would produce the first measurement and the strongest
  possible citation of this reference, by its own author.
- **A public comment.** The CLIA framework and federal biosafety guidance are periodically
  open for comment. The evidence-gap finding is exactly the kind of technical input those
  dockets ask for.
- **A conference package.** ABSA International and ASM Microbe both take abstracts on
  exactly this. The figures already exist.
- **Translation into a usable form.** The instrument as a YAML file serves other
  researchers. A one-page scoring sheet a bench supervisor can print serves laboratories,
  and that is who the project is for.
