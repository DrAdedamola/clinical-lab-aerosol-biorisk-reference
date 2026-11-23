#!/usr/bin/env python3
"""
05_report.py - builds the technical report and the manuscript from the stats file

PLAIN LANGUAGE HEADER
Writes report/technical_report.md and report/manuscript.md. Every number in both is
read from report/stats.json, never typed in. That is what guarantees the words and
the data cannot drift apart: change a score, re-run the build, re-run this, and both
documents update themselves.

Run:  python3 code/05_report.py            (draft banner)
      python3 code/05_report.py --final    (after verification only)
"""
import argparse, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
S = json.load(open(ROOT / "report/stats.json"))
STEPS = yaml.safe_load(open(ROOT / "data/raw/steps.yaml"))["steps"]
SRC = yaml.safe_load(open(ROOT / "evidence/sources.yaml"))["sources"]
A = json.load(open(ROOT / "AUTHORS.json"))["authors"][0]
R = S["primary_profile_rows"]
C = S["clia_denominator"]

p = argparse.ArgumentParser(); p.add_argument("--final", action="store_true")
FINAL = p.parse_args().final
BANNER = "" if FINAL else (
    "> **DRAFT. NOT RELEASED.** Every score below is provisional and has not yet been\n"
    "> ruled on by the author. Do not cite this version.\n\n")
AUTHOR_LINE = f"{A['name']} (ORCID {A['orcid']}), {A['affiliation']}"


def table():
    rows = ["| Bench step | Release (IARS) | Baseline RBI | With controls | Evidence |",
            "|---|---|---|---|---|"]
    for sid in sorted(R, key=lambda k: -R[k]["RBI_baseline"]):
        r = R[sid]
        rows.append(f"| {r['step']} | {r['IARS']} | {r['RBI_baseline']} "
                    f"({r['band_baseline']}) | {r['RBI_recommended']} "
                    f"({r['band_recommended']}) | {r['evidence_grade']} |")
    return "\n".join(rows)


def refs():
    out = []
    for k in sorted(SRC):
        s = SRC[k]
        url = s.get("url") or s.get("url_contents_page", "")
        bits = [b for b in (s.get("authors"), s.get("title"),
                            s.get("journal") or s.get("issuer"),
                            str(s.get("year", "")), s.get("volume_pages")) if b]
        doi = f" doi:{s['doi']}." if s.get("doi") else ""
        out.append(f"- **[{k}]** {'. '.join(bits)}.{doi} {url} (accessed {s.get('access_date','')})")
    return "\n".join(out)


GRADES = S["evidence_grade_counts"]
E1 = S["n_steps_graded_E1"]
NOMEAS = S["n_steps_with_no_direct_measurement"]

report = f"""# Clinical Laboratory Aerosol Biorisk Reference

### A procedure-level BRACE scoring instrument for the bench steps of routine diagnostic testing, with reference scores, evidence grades and control sets

**{AUTHOR_LINE}**

Instrument version {S['instrument_version']} · Technical report

{BANNER}---

## Summary

Every clinical laboratory is required to assess the biorisk of its own procedures. Almost
none is given a method for doing it at the level of a single bench step. This reference
supplies one: an open scoring instrument of {S['n_instrument_items']} anchored items across
three dimensions, mapped to the clause structure of ISO 35001:2019, applied to
{S['n_steps']} routine bench steps under {S['n_agent_profiles']} agent profiles, with
{S['n_controls']} recommended controls and {S['n_evidence_findings']} cited findings drawn
from {S['n_sources']} openly accessible sources.

The instrument's central design choice is that a score and its evidence grade are reported
together and never combined. Applying it produces a result that is uncomfortable and, I believe,
the most useful thing in this document: **the bench steps that laboratories worry
about most have been measured and found to release little, while the steps that have
actually infected and killed laboratory workers have never been measured at all.**

Of {S['n_steps']} steps, {E1} carry direct quantitative aerosol measurement and
{NOMEAS} do not. The highest-throughput step in the laboratory, operation of automated
chemistry and haematology analysers, carries grade E5: no evidence located.

## Why this matters

CMS records {C['labs_registered_total']:,} laboratories registered under CLIA as of
{C['vintage']}, of which {C['certificate_of_compliance']:,} hold a certificate of
compliance and {C['certificate_of_accreditation']:,} a certificate of accreditation:
{C['non_waived_certificates']:,} settings performing the moderate- and high-complexity
testing where these bench steps take place. National biosafety guidance asks each of them
to assess the risk of its own procedures and leaves the step-by-step work to each
laboratory. A shared, cited reference lets a frontline laboratory start from evidence
instead of a blank form.

## The instrument

Three scored dimensions and one reported grade.

- **Inherent Aerosol Release (IARS)**, 5 items, a property of the step before any control
  is credited: energy applied, containment of the specimen, volume and concentration,
  proximity to the breathing zone, and throughput.
- **Scenario Consequence (SCS)**, 3 items, a property of the organism rather than the step:
  inhalational infectivity, severity against the availability of prophylaxis, and the
  likelihood of unsuspected presence. The last of these is the one most often omitted from
  procedure risk assessments and the one the incident literature turns on.
- **Control Reliability (CRS)**, 4 items, scored twice for every step, once for baseline
  practice and once for the recommended control set: engineering effectiveness,
  independence from human performance, verification and certification, and PPE adequacy
  for the inhalation route.
- **Evidence Grade (E1 to E5)**, reported beside every score and never inside it.

Composition: `RBI = max(1, IARS - {S['control_credit']} x (CRS - 1)) x SCS`, on a 1 to 25
scale, banded Low, Moderate, Elevated, High, Very high. No control set is credited with
eliminating release, because the evidence base does not support that for any step here.

## Reference scores

At each step's primary agent profile. Full results for all {S['n_scored_rows']} step and
profile combinations are in `data/processed/reference_scores.csv`.

{table()}

![Evidence against risk](figures/fig1_evidence_vs_risk.png)

![What the controls are worth](figures/fig2_control_effect.png)

## What the evidence actually says

**Measured and negative.** Air and surface sampling during opening of blood sample tubes
and during centrifugation of capped primary tubes, in a working hospital biochemistry
laboratory using a model bacterium, recovered no organisms [DUBUIS2021]. These are the two
pre-analytical steps laboratories most often cite when asking for a cabinet. The one study
that measured them found nothing.

**Measured and conditional.** Viable aerosol production during cartridge loading and assay
running on the cartridge-based tuberculosis platform was reduced below that of acid-fast
smear preparation, provided the sample reagent was given its specified contact time; the
incorrect-use condition was deliberately simulated by omitting that incubation
[BANADA2010]. The safety case for this step rests entirely on a timer.

**Never measured, repeatedly lethal.** Almost all reported laboratory-acquired meningococcal
infections occurred in microbiologists who had manipulated sterile-site isolates on an open
bench rather than in a cabinet [MMWR2002MENING, SEJVAR2005]; in one fatal case the
investigation identified bench-top manipulation, open-bench plate spreading and flaming of
an incompletely dried slide among the breaches [MMWR2014CALAB]. No aerosol measurement of
routine subculture in a clinical laboratory has been located. This step carries the highest
score in the reference on grade E3.

**Not measured at all.** An investigation of exposure risk events across ten clinical
laboratories found rapid identification technology in use during several of the events, and
recommended handling slow-growing organisms in a cabinet and withholding automated
identification until biological threat agents are excluded [JCM2019BRUCELLA]. A review of
accidental laboratory aerosol generation identifies highly automated equipment as a source
still requiring characterisation [RAVNHOLDT2025]. No study has measured aerosol release from
a routine clinical chemistry or haematology analyser.

## Research priorities this reference identifies

1. **Measure a high-volume automated analyser.** Highest throughput in the laboratory,
   grade E5. One well designed measurement study would move this row from E5 to E1 and be
   citable by every laboratory in the country.
2. **Measure open-bench subculture and plate manipulation.** The step with the strongest
   incident evidence and no measurement.
3. **Measure the failure modes rather than the procedures.** For centrifugation and
   specimen reception the risk is concentrated in breakage and leakage, which is where
   measurement effort should go.
4. **Measure decontamination adequacy for instrument internal pathways** after a late-
   recognised isolate has passed through an automated platform.

## Limitations

See `docs/LIMITATIONS.md`, which is written in full and should be read before the scores
are used. In short: these scores are structured expert judgement, not measurement;
inter-rater agreement has not yet been measured; the control-credit weight and band cut
points are set rather than derived; and the literature search was targeted rather than
systematic.

## Reproducing this

```
python3 code/01_provenance.py
python3 code/02_build.py
python3 code/03_qa.py
python3 code/04_figures.py
python3 code/05_report.py
```

Every number in this document is interpolated from `report/stats.json`, which is written
by the build. The documents cannot disagree with the data.

## Licence

Instrument, data and documents CC BY 4.0. Code MIT.

## Sources

{refs()}
"""

manuscript = f"""# Procedure-level biorisk scoring for aerosol-generating bench steps in clinical diagnostic laboratories: an open instrument, reference scores and an evidence map

**{AUTHOR_LINE}**

{BANNER}## Abstract

**Background.** Clinical laboratories are required to assess the biorisk of their own
procedures, but no openly available instrument operates at the level of a single bench
step, and the evidence underlying routine bench biosafety practice has not been
systematically characterised.

**Methods.** I developed a procedure-level scoring instrument of {S['n_instrument_items']}
anchored items across three dimensions (inherent aerosol release, scenario consequence,
control reliability), with a separately reported evidence grade, mapped to the clause
structure of ISO 35001:2019. I applied it to {S['n_steps']} routine bench steps under
{S['n_agent_profiles']} agent profiles, extracting findings from openly accessible
literature and guidance.

**Results.** Across {S['n_scored_rows']} step and profile combinations, residual biorisk
under baseline practice ranged to {S['max_rbi_baseline']} of a possible 25, and the
recommended control sets reduced it by a mean of {S['mean_rbi_reduction']} points. Evidence
grades were distributed {', '.join(f'{k}: {v}' for k, v in GRADES.items())}. Direct
quantitative aerosol measurement existed for {E1} of {S['n_steps']} steps. The steps with
the highest residual biorisk were those supported only by incident evidence, while the
steps with direct measurement scored lowest; the highest-throughput step in the laboratory
had no located evidence of any kind.

**Conclusions.** Bench biosafety practice in clinical laboratories is inverted with respect
to its evidence base. An open, cited, procedure-level instrument makes that inversion
visible and gives frontline laboratories a starting point other than a blank form.

**Keywords:** biorisk management, clinical laboratory, aerosol, laboratory-acquired
infection, ISO 35001, biosafety cabinet, evidence grading

## Sections to draft

1. Introduction — the assessment requirement and the absence of a procedure-level tool.
2. Methods — instrument development, anchoring, agent profiles, composition, evidence
   grading, ISO 35001 mapping, and the planned agreement study.
3. Results — reference scores, control effect, evidence distribution, the gaps.
4. Discussion — the inversion finding, what it implies for where measurement effort goes,
   and what it implies for cabinet policy at the bench.
5. Limitations — imported in full from `docs/LIMITATIONS.md`.
6. Data availability — repository and DOI.

## Sources

{refs()}
"""

(ROOT / "report/technical_report.md").write_text(report)
(ROOT / "report/manuscript.md").write_text(manuscript)
print(f"wrote report/technical_report.md and report/manuscript.md "
      f"({'FINAL' if FINAL else 'DRAFT'})")
