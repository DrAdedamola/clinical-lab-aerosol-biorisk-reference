#!/usr/bin/env python3
"""
06_agreement.py - inter-rater agreement for the scoring instrument

PLAIN LANGUAGE HEADER
This script answers one question: when two people score the same scenario without
talking to each other, how often do they agree? It computes Gwet's AC2 (the primary
measure, chosen in advance) and weighted Cohen's kappa (reported alongside), per
instrument item and pooled.

It refuses to run on made-up data. Pass --selftest to check the arithmetic against a
clearly labelled synthetic fixture; the output of a self-test is stamped so it can never
be mistaken for a result.

Run on real ratings:
    python3 code/06_agreement.py --rater1 scenarios/ratings_rater1.csv \
                                 --rater2 scenarios/ratings_rater2.csv
Check the maths:
    python3 code/06_agreement.py --selftest
"""
import argparse, csv, json, math, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATS = [1, 2, 3, 4, 5]


def ordinal_weights(cats):
    """Linear disagreement weights: adjacent scores are nearly agreement, 1 vs 5 is not."""
    k = len(cats) - 1
    return {(a, b): 1 - abs(a - b) / k for a in cats for b in cats}


W = ordinal_weights(CATS)


def _paired(r1, r2):
    """Pairs where BOTH raters gave a numeric score. NA on either side is excluded and counted."""
    keys = set(r1) & set(r2)
    pairs, na = [], 0
    for k in sorted(keys):
        a, b = r1[k], r2[k]
        if a is None or b is None:
            na += 1
        else:
            pairs.append((a, b))
    return pairs, na


def observed_agreement(pairs):
    return sum(W[p] for p in pairs) / len(pairs)


def gwet_ac2(pairs):
    """Gwet's AC2 with ordinal weights. Primary measure, declared in advance."""
    n = len(pairs)
    if n < 2:
        return None, None
    pa = observed_agreement(pairs)
    pi = {c: sum((a == c) + (b == c) for a, b in pairs) / (2 * n) for c in CATS}
    q = len(CATS)
    tw = sum(W[(a, b)] for a in CATS for b in CATS)
    pe = (tw / (q * (q - 1))) * sum(pi[c] * (1 - pi[c]) for c in CATS)
    if abs(1 - pe) < 1e-12:
        return None, None
    ac2 = (pa - pe) / (1 - pe)
    # variance by the linearisation estimator
    terms = []
    for a, b in pairs:
        pa_i = W[(a, b)]
        pe_i = (tw / (q * (q - 1))) * sum(
            pi[c] * (1 - pi[c]) + ((a == c) + (b == c)) / 2 - pi[c] for c in CATS)
        terms.append((pa_i - pe) / (1 - pe) - 2 * (1 - ac2) * (pe_i - pe) / (1 - pe))
    m = sum(terms) / n
    var = sum((t - m) ** 2 for t in terms) / (n * (n - 1))
    se = math.sqrt(max(var, 0))
    return ac2, (ac2 - 1.96 * se, ac2 + 1.96 * se)


def weighted_kappa(pairs):
    """Linearly weighted Cohen's kappa. Secondary, reported for comparison."""
    n = len(pairs)
    pa = observed_agreement(pairs)
    m1 = {c: sum(a == c for a, _ in pairs) / n for c in CATS}
    m2 = {c: sum(b == c for _, b in pairs) / n for c in CATS}
    pe = sum(W[(a, b)] * m1[a] * m2[b] for a in CATS for b in CATS)
    return None if abs(1 - pe) < 1e-12 else (pa - pe) / (1 - pe)


def read_ratings(path):
    out = defaultdict(dict)
    for r in csv.DictReader(open(path)):
        v = (r["score_1_to_5_or_NA"] or "").strip()
        if v == "":
            continue
        out[r["item"]][r["scenario_id"]] = None if v.upper() == "NA" else int(v)
    return out


def analyse(r1, r2, label):
    items = sorted(set(r1) & set(r2))
    rows, all_pairs, total_na = [], [], 0
    for it in items:
        pairs, na = _paired(r1[it], r2[it])
        total_na += na
        all_pairs += pairs
        if not pairs:
            continue
        ac2, ci = gwet_ac2(pairs)
        rows.append({
            "item": it, "n_pairs": len(pairs), "n_na_excluded": na,
            "exact_agreement": round(sum(a == b for a, b in pairs) / len(pairs), 3),
            "within_one_point": round(sum(abs(a - b) <= 1 for a, b in pairs) / len(pairs), 3),
            "gwet_ac2": None if ac2 is None else round(ac2, 3),
            "gwet_ac2_ci_low": None if ci is None else round(ci[0], 3),
            "gwet_ac2_ci_high": None if ci is None else round(ci[1], 3),
            "weighted_kappa": (lambda k: None if k is None else round(k, 3))(weighted_kappa(pairs)),
        })
    pooled_ac2, pooled_ci = gwet_ac2(all_pairs)
    return {
        "label": label,
        "n_items": len(rows), "n_pairs_total": len(all_pairs),
        "n_na_excluded_total": total_na,
        "pooled_exact_agreement": round(sum(a == b for a, b in all_pairs) / len(all_pairs), 3),
        "pooled_within_one_point": round(sum(abs(a - b) <= 1 for a, b in all_pairs) / len(all_pairs), 3),
        "pooled_gwet_ac2": None if pooled_ac2 is None else round(pooled_ac2, 3),
        "pooled_gwet_ac2_ci": None if pooled_ci is None else [round(pooled_ci[0], 3), round(pooled_ci[1], 3)],
        "pooled_weighted_kappa": (lambda k: None if k is None else round(k, 3))(weighted_kappa(all_pairs)),
        "per_item": rows,
    }


def selftest():
    """Synthetic fixture. NOT A RESULT. Checks the maths against known boundary cases."""
    print("SELF-TEST ON SYNTHETIC FIXTURE DATA - THESE ARE NOT RESULTS\n")
    ident = [(c, c) for c in CATS] * 5
    ac2, _ = gwet_ac2(ident)
    print(f"  perfect agreement      -> AC2 = {ac2:.3f}  (expected 1.000)")
    assert abs(ac2 - 1.0) < 1e-9, "perfect agreement must give AC2 = 1"
    near = [(3, 3), (3, 4), (4, 4), (2, 3), (3, 3), (4, 3), (3, 2), (4, 4), (3, 3), (2, 2)]
    ac2n, cin = gwet_ac2(near)
    print(f"  realistic clustered    -> AC2 = {ac2n:.3f} "
          f"[{cin[0]:.3f}, {cin[1]:.3f}], weighted kappa = {weighted_kappa(near):.3f}")
    print("  note: kappa is markedly lower than AC2 on clustered ratings. This is the")
    print("        documented behaviour that made AC2 the pre-declared primary measure.")
    opp = [(1, 5), (5, 1)] * 5
    ac2o, _ = gwet_ac2(opp)
    print(f"  maximal disagreement   -> AC2 = {ac2o:.3f}  (expected negative)")
    assert ac2o < 0, "maximal disagreement must give a negative coefficient"
    r1 = {"A1": {"SC1": 3, "SC2": None}}
    r2 = {"A1": {"SC1": 4, "SC2": 2}}
    p, na = _paired(r1["A1"], r2["A1"])
    print(f"  NA handling            -> {len(p)} pair(s) used, {na} excluded, none imputed")
    assert na == 1 and len(p) == 1
    print("\n  All self-test assertions passed. The arithmetic is sound.")
    print("  NO REAL RATINGS EXIST YET. See scenarios/AGREEMENT_PROTOCOL.md.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rater1"); ap.add_argument("--rater2")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--label", default="release-4 agreement study")
    a = ap.parse_args()
    if a.selftest:
        selftest(); sys.exit(0)
    if not (a.rater1 and a.rater2):
        print("No rating files given. This script will not invent data.\n"
              "Run with --selftest to check the arithmetic, or supply two rating files.\n"
              "See scenarios/AGREEMENT_PROTOCOL.md.")
        sys.exit(2)
    res = analyse(read_ratings(a.rater1), read_ratings(a.rater2), a.label)
    out = ROOT / "data/processed/agreement_results.json"
    json.dump(res, open(out, "w"), indent=2)
    with open(ROOT / "data/processed/agreement_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(res["per_item"][0].keys()))
        w.writeheader(); w.writerows(res["per_item"])
    print(json.dumps({k: v for k, v in res.items() if k != "per_item"}, indent=2))
    print(f"\nwritten to {out}")
