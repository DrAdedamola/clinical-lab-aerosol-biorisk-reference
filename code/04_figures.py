#!/usr/bin/env python3
"""
04_figures.py - figures, built from report/stats.json only

PLAIN LANGUAGE HEADER
Draws the two figures for the report. Every number comes from report/stats.json,
so a figure can never disagree with the text. Figures are stamped DRAFT until you
pass --final, which only happens after you have verified the package.

Run:  python3 code/04_figures.py            (draft, stamped)
      python3 code/04_figures.py --final    (after verification only)
"""
import argparse, json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / "report" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
S = json.load(open(ROOT / "report" / "stats.json"))
ROWS = S["primary_profile_rows"]

BLUE, ORANGE, INK, MUTED = "#1b5e9e", "#c25708", "#1a1a1a", "#6b6b6b"
GRADE_X = {"E1": 1, "E2": 2, "E3": 3, "E4": 4, "E5": 5}
GRADE_LABEL = {1: "E1\ndirect\nmeasurement", 2: "E2\nanalogous\nmeasurement",
               3: "E3\nincident\nevidence", 4: "E4\nguidance\nonly", 5: "E5\nno evidence\nlocated"}
SHORT = {"S01": "Specimen\nreception", "S02": "Centrifugation", "S03": "Cap removal",
         "S04": "Automated\nanalysers", "S05": "GeneXpert\nloading",
         "S06": "MALDI-TOF\nidentification", "S07": "Open culture\nwork"}


def stamp(fig, final):
    if not final:
        fig.text(0.5, 0.5, "DRAFT", fontsize=78, color="#cccccc", alpha=0.35,
                 ha="center", va="center", rotation=28, zorder=0)


def fig1(final):
    """The inversion: how much is known, against how much risk there is."""
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    stamp(fig, final)
    # spread points that share an evidence grade so neither marks nor labels collide
    by_grade = {}
    for sid, r in ROWS.items():
        by_grade.setdefault(r["evidence_grade"], []).append(sid)
    for grade, sids in by_grade.items():
        sids.sort(key=lambda s: ROWS[s]["RBI_baseline"])
        n = len(sids)
        for j, sid in enumerate(sids):
            r = ROWS[sid]
            x = GRADE_X[grade] + (j - (n - 1) / 2) * 0.30
            y = r["RBI_baseline"]
            ax.scatter(x, y, s=190, color=BLUE, zorder=3, edgecolor="white", linewidth=1.6)
            # alternate label side when a grade column is crowded
            if n == 1:
                dx, dy, ha, va = 0, 17, "center", "bottom"
            elif j == n - 1:
                dx, dy, ha, va = 14, -4, "left", "center"
            elif j == 0:
                dx, dy, ha, va = 0, -20, "center", "top"
            else:
                dx, dy, ha, va = 0, 17, "center", "bottom"
            ax.annotate(SHORT[sid].replace("\n", " "), (x, y), textcoords="offset points",
                        xytext=(dx, dy), ha=ha, va=va, fontsize=8.8, color=INK)
    ax.axhspan(9.01, 25, color=ORANGE, alpha=0.07, zorder=0)
    ax.text(0.58, 20.8, "Elevated or higher", fontsize=8.5, color=ORANGE,
            ha="left", va="center")
    ax.set_xlim(0.4, 5.75); ax.set_ylim(0, 22)
    ax.set_xticks(list(GRADE_LABEL)); ax.set_xticklabels(GRADE_LABEL.values(), fontsize=8.5)
    ax.set_xlabel("Strength of the evidence base for this step  \u2192  weaker",
                  fontsize=10, color=MUTED, labelpad=10)
    ax.set_ylabel("Residual Biorisk Index under baseline practice\n(1 to 25 scale)",
                  fontsize=10, color=MUTED)
    ax.set_title("The steps that have caused infection are the ones nobody has measured",
                 fontsize=12.5, color=INK, pad=14, loc="left")
    ax.grid(axis="y", color="#e6e6e6", linewidth=0.8, zorder=0)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"): ax.spines[sp].set_color("#cccccc")
    ax.tick_params(colors=MUTED, labelsize=9)
    fig.text(0.013, 0.015, "Each point is one bench step at its primary agent profile. "
             f"Instrument v{S['instrument_version']}, Oyeniyi OA, 2026. CC BY 4.0.",
             fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(FIGS / "fig1_evidence_vs_risk.png", dpi=220)
    plt.close(fig)


def fig2(final):
    """What the recommended control set is worth, step by step."""
    order = sorted(ROWS, key=lambda k: ROWS[k]["RBI_baseline"])
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    stamp(fig, final)
    for i, sid in enumerate(order):
        r = ROWS[sid]
        ax.plot([r["RBI_recommended"], r["RBI_baseline"]], [i, i],
                color="#d6d6d6", linewidth=2.4, zorder=1, solid_capstyle="round")
        ax.scatter(r["RBI_baseline"], i, s=135, color=ORANGE, zorder=3,
                   edgecolor="white", linewidth=1.5,
                   label="Baseline practice" if i == 0 else None)
        ax.scatter(r["RBI_recommended"], i, s=135, color=BLUE, zorder=3,
                   edgecolor="white", linewidth=1.5,
                   label="With recommended controls" if i == 0 else None)
        ax.text(r["RBI_baseline"] + 0.45, i, f"{r['evidence_grade']}", va="center",
                fontsize=8, color=MUTED)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([SHORT[s].replace("\n", " ") for s in order], fontsize=9.5, color=INK)
    ax.set_xlim(0, 19); ax.set_xlabel("Residual Biorisk Index (1 to 25 scale)",
                                      fontsize=10, color=MUTED, labelpad=8)
    ax.set_title("What the recommended control set is worth, step by step",
                 fontsize=12.5, color=INK, pad=14, loc="left")
    ax.legend(frameon=False, fontsize=9, loc="lower right", labelcolor=INK)
    ax.grid(axis="x", color="#e6e6e6", linewidth=0.8, zorder=0)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#cccccc")
    ax.tick_params(colors=MUTED, labelsize=9, left=False)
    fig.text(0.013, 0.015, "Letters to the right of each baseline point are the evidence "
             f"grade. Mean reduction {S['mean_rbi_reduction']} points. "
             f"Instrument v{S['instrument_version']}, Oyeniyi OA, 2026. CC BY 4.0.",
             fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(FIGS / "fig2_control_effect.png", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--final", action="store_true")
    a = p.parse_args()
    fig1(a.final); fig2(a.final)
    print(f"figures written to {FIGS} ({'FINAL' if a.final else 'DRAFT-stamped'})")
