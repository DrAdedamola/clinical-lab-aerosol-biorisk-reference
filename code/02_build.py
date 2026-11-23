#!/usr/bin/env python3
"""
02_build.py - Clinical Laboratory Aerosol Biorisk Reference

PLAIN LANGUAGE HEADER
This script does the arithmetic. It reads the scoring instrument, the agent
profiles and the seven step files, works out each score, and writes the result
tables plus a stats file that every document quotes from. You do not need to
open this file. If a number in the report looks wrong, the fix belongs in
data/raw/steps.yaml, not here.

Run:  python3 code/02_build.py
Reads:  instrument/instrument_v1.yaml, instrument/iso35001_clauses.csv,
        data/raw/agent_profiles.yaml, data/raw/steps.yaml, evidence/sources.yaml
Writes: data/processed/*.csv, report/stats.json
"""
import csv, json, os, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)
(ROOT / "report").mkdir(exist_ok=True)

def load(p):
    with open(ROOT / p) as f:
        return yaml.safe_load(f)

INSTR = load("instrument/instrument_v1.yaml")
PROFILES = load("data/raw/agent_profiles.yaml")["profiles"]
STEPS = load("data/raw/steps.yaml")["steps"]
SOURCES = load("evidence/sources.yaml")["sources"]
CLAUSES = {r["clause"]: r["title"]
           for r in csv.DictReader(open(ROOT / "instrument/iso35001_clauses.csv"))}

CREDIT = INSTR["composition"]["residual_biorisk_index"]["control_credit"]
BANDS = INSTR["composition"]["bands"]


# Items whose anchors run opposite to their dimension. Read from the instrument rather
# than hard-coded here, so the instrument file stays the single source of truth.
REVERSED = set(INSTR["dimension_A"].get("reverse_coded_items", []))
SCALE_MAX = 5


def mean(d, reverse=frozenset()):
    """Mean over scored items, applying (6 - x) to any reverse-coded item.

    NA items are excluded, never imputed. `reverse` names items whose anchors run
    opposite to their dimension; see dimension_A.aggregation_note in the instrument.
    """
    vals = []
    for k, v in d.items():
        if not isinstance(v, (int, float)):
            continue
        vals.append((SCALE_MAX + 1 - v) if k in reverse else v)
    if not vals:
        raise ValueError("no scored items")
    return sum(vals) / len(vals), len(vals)


def band(rbi):
    for b in BANDS:
        if b["min"] <= round(rbi, 2) <= b["max"]:
            return b["label"]
    raise ValueError(f"RBI {rbi} falls outside every band")


def rbi(iars, crs, scs):
    residual_release = max(1.0, iars - CREDIT * (crs - 1))
    return residual_release * scs, residual_release


def build():
    scores_rows, control_rows, evidence_rows, map_rows = [], [], [], []
    profile_scs = {}
    for pid, p in PROFILES.items():
        m, n = mean({k: p[k] for k in ("B1", "B2", "B3")})
        profile_scs[pid] = round(m, 4)

    for sid, s in STEPS.items():
        iars_m, iars_n = mean(s["iars"], reverse=REVERSED)
        crs_b, _ = mean(s["crs_baseline"])
        crs_r, _ = mean(s["crs_recommended"])

        for pid in s["applicable_profiles"]:
            scs = profile_scs[pid]
            rbi_b, rel_b = rbi(iars_m, crs_b, scs)
            rbi_r, rel_r = rbi(iars_m, crs_r, scs)
            scores_rows.append({
                "step_id": sid,
                "step_name": s["name"],
                "agent_profile": pid,
                "agent_profile_name": PROFILES[pid]["name"],
                "is_primary_profile": pid == s["primary_profile"],
                "IARS": round(iars_m, 2),
                "IARS_items_scored": iars_n,
                "IARS_reverse_coded_items": "|".join(sorted(REVERSED)) or "none",
                "SCS": round(scs, 2),
                "CRS_baseline": round(crs_b, 2),
                "CRS_recommended": round(crs_r, 2),
                "residual_release_baseline": round(rel_b, 2),
                "residual_release_recommended": round(rel_r, 2),
                "RBI_baseline": round(rbi_b, 2),
                "RBI_baseline_band": band(rbi_b),
                "RBI_recommended": round(rbi_r, 2),
                "RBI_recommended_band": band(rbi_r),
                "RBI_reduction": round(rbi_b - rbi_r, 2),
                "evidence_grade": s["evidence_grade"],
                "conditionality": s["conditionality"],
                "status": "released v1.0, author-ruled 2026-10-29",
            })

        for category, items in s["controls"].items():
            for i, text in enumerate(items, 1):
                control_rows.append({
                    "step_id": sid, "step_name": s["name"],
                    "control_category": category, "control_number": i,
                    "control": text,
                })

        for f in s.get("evidence_findings", []):
            src = f["source"]
            meta = SOURCES.get(src, {})
            evidence_rows.append({
                "step_id": sid, "step_name": s["name"],
                "finding": f["finding"], "direction": f["direction"],
                "source_key": src,
                "source_title": meta.get("title", "PENDING VERIFICATION - NOT CITABLE"),
                "source_url": meta.get("url", meta.get("url_contents_page", "")),
                "access_date": meta.get("access_date", ""),
            })

        for c in s["iso35001_clauses"]:
            if c not in CLAUSES:
                raise KeyError(f"{sid} maps to clause {c}, which is not in the clause index")
            map_rows.append({
                "step_id": sid, "step_name": s["name"],
                "iso35001_clause": c, "iso35001_clause_title": CLAUSES[c],
            })

    # instrument element -> clause map
    elem_rows = []
    for dim in ("dimension_A", "dimension_B", "dimension_C"):
        d = INSTR[dim]
        for c in d["iso35001_clauses"]:
            elem_rows.append({"element": d["code"], "element_name": d["name"],
                              "level": "dimension", "iso35001_clause": c,
                              "iso35001_clause_title": CLAUSES[c]})
        for ikey, item in d["items"].items():
            for c in item["iso35001_clauses"]:
                elem_rows.append({"element": ikey, "element_name": item["name"],
                                  "level": "item", "iso35001_clause": c,
                                  "iso35001_clause_title": CLAUSES[c]})
    for c in INSTR["evidence_grade"]["iso35001_clauses"]:
        elem_rows.append({"element": "EG", "element_name": "Evidence Grade",
                          "level": "dimension", "iso35001_clause": c,
                          "iso35001_clause_title": CLAUSES[c]})

    def write(name, rows):
        if not rows:
            return
        with open(OUT / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"  wrote {name}: {len(rows)} rows")

    write("reference_scores.csv", scores_rows)
    write("control_sets.csv", control_rows)
    write("evidence_table.csv", evidence_rows)
    write("step_iso35001_map.csv", map_rows)
    with open(ROOT / "instrument" / "iso35001_map.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(elem_rows[0].keys()))
        w.writeheader(); w.writerows(elem_rows)
    print(f"  wrote instrument/iso35001_map.csv: {len(elem_rows)} rows")

    # ---- stats file: the only place documents may take numbers from ----
    prim = [r for r in scores_rows if r["is_primary_profile"]]
    grades = {}
    for s in STEPS.values():
        grades[s["evidence_grade"]] = grades.get(s["evidence_grade"], 0) + 1
    stats = {
        "status": "RELEASED",
        "instrument_version": INSTR["meta"]["version"],
        "n_steps": len(STEPS),
        "n_agent_profiles": len(PROFILES),
        "n_scored_rows": len(scores_rows),
        "n_instrument_items": sum(len(INSTR[d]["items"]) for d in
                                  ("dimension_A", "dimension_B", "dimension_C")),
        "reverse_coded_items": sorted(REVERSED),
        "n_controls": len(control_rows),
        "n_evidence_findings": len(evidence_rows),
        "n_sources": len(SOURCES),
        "n_distinct_iso_clauses_mapped": len({r["iso35001_clause"] for r in elem_rows}
                                             | {r["iso35001_clause"] for r in map_rows}),
        "control_credit": CREDIT,
        "evidence_grade_counts": dict(sorted(grades.items())),
        "n_steps_graded_E1": grades.get("E1", 0),
        "n_steps_with_no_direct_measurement": sum(
            1 for s in STEPS.values() if s["evidence_grade"] in ("E3", "E4", "E5")),
        "n_steps_conditional": sum(1 for s in STEPS.values()
                                   if s["conditionality"] != "none"),
        "profile_scs": profile_scs,
        "primary_profile_rows": {
            r["step_id"]: {
                "step": r["step_name"], "profile": r["agent_profile"],
                "IARS": r["IARS"], "SCS": r["SCS"],
                "RBI_baseline": r["RBI_baseline"], "band_baseline": r["RBI_baseline_band"],
                "RBI_recommended": r["RBI_recommended"],
                "band_recommended": r["RBI_recommended_band"],
                "evidence_grade": r["evidence_grade"],
            } for r in prim},
        "max_rbi_baseline": max(r["RBI_baseline"] for r in scores_rows),
        "max_rbi_baseline_step": max(scores_rows, key=lambda r: r["RBI_baseline"])["step_id"],
        "mean_rbi_reduction": round(
            sum(r["RBI_reduction"] for r in scores_rows) / len(scores_rows), 2),
        "clia_denominator": {
            "source": "CMS2026",
            "labs_registered_total": 301284,
            "certificate_of_compliance": 15214,
            "certificate_of_accreditation": 15542,
            "vintage": "September 2026",
            "note": "Compliance plus accreditation certificates are the non-waived, "
                    "moderate- and high-complexity settings where these bench steps occur.",
        },
    }
    stats["clia_denominator"]["non_waived_certificates"] = (
        stats["clia_denominator"]["certificate_of_compliance"]
        + stats["clia_denominator"]["certificate_of_accreditation"])
    with open(ROOT / "report" / "stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  wrote report/stats.json: {len(stats)} keys")
    return stats


if __name__ == "__main__":
    print("Building reference scores...")
    st = build()
    print(f"\nDone. {st['n_steps']} steps, {st['n_scored_rows']} scored rows, "
          f"{st['n_controls']} controls, {st['n_sources']} sources.")
