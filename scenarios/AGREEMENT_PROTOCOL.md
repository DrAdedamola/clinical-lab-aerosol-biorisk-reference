# Inter-rater agreement protocol

**Status: REGISTERED PROTOCOL, NOT YET RUN. Deferred to release 4.**

This protocol is published *before* any rating is done, so that the analysis cannot be
chosen after the results are seen. That is the whole point of writing it down first.

## Why this exists

A scoring instrument that only its author can apply is not an instrument, it is an
opinion with a number attached. The test is whether two people, working independently
from the same written anchors and the same published scenario, land on the same score.
Until that is measured, every score in this reference is one person's judgement.

## What gets rated

Published, openly accessible accounts of real clinical laboratory exposure events and
aerosol studies, each rewritten as a standardised scenario vignette of roughly 150 to
250 words. Vignettes contain only what the published source states. Where the source is
silent on something the instrument asks about, the vignette says so explicitly, and the
rater records NA. Inventing detail to make a vignette scorable would be fabricating data.

Scenario set: `scenarios/scenarios.yaml`. Target n = 25 vignettes drawn from the source
register, with the step mix weighted toward S06 and S07 because that is where the
published incident literature is.

## Raters

Two raters, scoring independently, with no contact about scores until both rating sheets
are locked and committed.

- **Rater 1:** Oyekunle Adedamola Oyeniyi.
- **Rater 2:** to be recruited. Must be a laboratory biosafety practitioner or a clinical
  microbiologist who was not involved in writing the instrument.

Rater 2 is trained only by reading `instrument/instrument_v1.yaml` and
`docs/CODEBOOK.md`. No verbal coaching, no worked examples beyond those printed in the
instrument. If the written anchors are not enough, that is a finding about the
instrument, and it is the finding worth having.

## Procedure

1. Both raters receive the same shuffled scenario file and a blank rating form
   (`scenarios/rating_form_blank.csv`).
2. Each rater scores all 12 instrument items for every vignette, independently.
3. Each locked sheet is committed to the repository before the other is opened. The git
   history is the evidence that the ratings were independent.
4. `code/06_agreement.py` computes the statistics. No scores are revised afterwards.
5. Disagreements are reconciled in a logged discussion *after* the statistics are
   computed and reported. Reconciliation informs instrument v1.1. It never changes the
   reported agreement.

## Statistics, fixed in advance

- **Primary:** Gwet's AC2 with ordinal (linear) weights, per item and pooled, with 95%
  confidence intervals.
- **Secondary:** linearly weighted Cohen's kappa, per item and pooled.
- **Also reported:** raw exact agreement, agreement within one point, the proportion of
  NA, and band agreement on the final RBI.

Gwet's AC2 is primary because these scores will cluster in the middle of the scale, and
kappa is unstable under that clustering. Reporting kappa alongside is what lets a reader
see that for themselves rather than taking it on trust.

## Pre-declared interpretation

No threshold is declared as "success". The agreement coefficient is reported as a
property of the instrument, whatever it is. An instrument with modest agreement,
honestly reported, is more useful than one with excellent agreement obtained by letting
the raters talk first.

Per-item results drive instrument v1.1: any item whose agreement is markedly below the
rest has an anchor problem, and the anchor gets rewritten.

## What will be published

The vignettes, both rating sheets, the analysis script, and the results, together. A
reader who disagrees with the agreement figure can recompute it from the same files.

## Deviations

Any deviation from this protocol is recorded in `scenarios/DEVIATIONS.md` with the date
and the reason, before the analysis is run.
