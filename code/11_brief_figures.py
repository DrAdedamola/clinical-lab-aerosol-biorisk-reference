#!/usr/bin/env python3
"""
11_brief_figures.py - figures for the procedure inventory and evidence brief

PLAIN LANGUAGE HEADER
Draws the three figures in the technical report. Every value is read from the
project's own data files, so a figure cannot disagree with the text. Sized for a
two-column page: 3.4 inches single column, 7.0 inches full width.

Run:  python3 code/11_brief_figures.py
"""
import csv, json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "brief" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

S = json.load(open(ROOT / "report/stats.json"))
STEPS = yaml.safe_load(open(ROOT / "data/raw/steps.yaml"))["steps"]
PRIM = S["primary_profile_rows"]
SCORES = list(csv.DictReader(open(ROOT / "data/processed/reference_scores.csv")))


def row(step_id, profile):
    """One scored row, by step and agent profile."""
    for r in SCORES:
        if r["step_id"] == step_id and r["agent_profile"] == profile:
            return r
    raise KeyError(f"{step_id} has no row for profile {profile}")

sns.set_theme(style="ticks", context="paper",
              rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8,
                  "ytick.major.width": 0.8, "font.family": "serif",
                  "font.serif": ["DejaVu Serif"], "axes.labelsize": 8.5,
                  "xtick.labelsize": 8, "ytick.labelsize": 8,
                  "legend.fontsize": 7.4, "axes.titlesize": 9})

NAVY, RUST, GREY, INK = "#1b4f72", "#b3471f", "#9aa0a6", "#202124"
TEAL, SAND = "#2a7f7f", "#c9a227"
SHORT = {"S01": "Specimen reception", "S02": "Centrifugation", "S03": "Cap removal",
         "S04": "Automated analysers", "S05": "GeneXpert loading",
         "S06": "MALDI-TOF identification", "S07": "Open culture work"}
GRADE_COL = {"E1": NAVY, "E2": "#4a7fa8", "E3": RUST, "E4": SAND, "E5": "#7a7a7a"}


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  {name}.pdf / .png")


# ------------------------------------------------------------------ Figure 1
def fig1_measured():
    """
    Every measured airborne concentration located for clinical bench work,
    on one logarithmic axis. The central exhibit of the brief.
    """
    # (label, values, kind, source)
    #   kind 'nd'  = not detected, plotted as an upper bound at the detection limit
    #   kind 'pts' = discrete measured values, plotted individually
    #   kind 'rng' = a reported range
    rows = [
        ("Tube opening\n(blood, spiked)",               None,        "nd",  "Dubuis 2021"),
        ("Centrifugation, closed cap\n(blood, spiked)", None,        "nd",  "Dubuis 2021"),
        ("GeneXpert sample preparation\n(sputum, TB)",  None,        "nd",  "Banada 2010"),
        ("GeneXpert cartridge processing\n(sputum, TB)",None,        "nd",  "Banada 2010"),
        ("AFB smear preparation\n(sputum, TB)",         [16, 325],   "pts", "Banada 2010"),
        ("Centrifugal tube rupture\n(simulated)",       [10, 100],   "rng", "Liu 2023"),
        ("Dropped container\n(simulated)",              [1e3, 1e4],  "rng", "Liu 2023"),
        ("Accidental injection\n(simulated)",           [1e3, 1e4],  "rng", "Liu 2023"),
    ]
    LOD = 4.0
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ys = np.arange(len(rows))[::-1]

    for y, (lab, vals, kind, src) in zip(ys, rows):
        if kind == "nd":
            ax.plot([1.05, LOD], [y, y], color=GREY, lw=1.1, ls=":", zorder=2)
            ax.scatter([LOD], [y], marker="<", s=42, color=GREY, zorder=3)
            ax.text(LOD * 1.45, y, "not detected", va="center", ha="left",
                    fontsize=7.2, color=GREY, style="italic")
        elif kind == "pts":
            ax.scatter(vals, [y] * len(vals), s=46, color=RUST, zorder=3,
                       edgecolor="white", lw=0.9)
            ax.text(max(vals) * 1.5, y, " and ".join(f"{v:.0f}" for v in vals),
                    va="center", ha="left", fontsize=7.2, color=RUST)
        else:
            lo, hi = vals
            ax.plot([lo, hi], [y, y], color=RUST, lw=3.0,
                    solid_capstyle="round", zorder=3)
            txt = (f"{lo:.0f}\u2013{hi:.0f}" if hi < 1e3
                   else "$10^{3}$\u2013$10^{4}$")
            ax.text(hi * 1.5, y, txt, va="center", ha="left",
                    fontsize=7.2, color=RUST)

    ax.axvline(LOD, color=GREY, lw=0.8, ls="--", zorder=1)
    ax.annotate("detection limit 4 CFU/m$^3$", xy=(LOD, -0.62),
                xytext=(LOD * 2.6, -0.62), fontsize=6.9, color=GREY,
                va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))

    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.6, linespacing=1.25)
    ax.set_xscale("log")
    ax.set_xlim(1.05, 6e4)
    ax.set_xlabel("Airborne concentration recovered (CFU m$^{-3}$, logarithmic)")
    ax.set_ylim(-1.05, len(rows) - 0.35)

    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(left=False)
    ax.grid(axis="x", color="#e8e8e8", lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    for y, r in zip(ys, rows):
        ax.text(1.005, y, r[3], transform=ax.get_yaxis_transform(),
                va="center", ha="left", fontsize=6.8, color=INK)
    ax.text(1.005, len(rows) - 0.35, "Source", transform=ax.get_yaxis_transform(),
            va="center", ha="left", fontsize=6.8, color=INK, weight="bold")
    save(fig, "fig1_measured_concentrations")


# ------------------------------------------------------------------ Figure 2
def fig2_evidence_profile():
    """Release intensity against evidence grade, per step in the inventory."""
    fig, ax = plt.subplots(figsize=(3.4, 3.2))
    order = sorted(STEPS, key=lambda s: -PRIM[s]["IARS"])
    ys = np.arange(len(order))[::-1]
    for y, sid in zip(ys, order):
        g = STEPS[sid]["evidence_grade"]
        ax.barh(y, PRIM[sid]["IARS"], height=0.55,
                color=GRADE_COL[g], zorder=3, edgecolor="white", lw=0.8)
        ax.text(PRIM[sid]["IARS"] + 0.09, y, g, va="center", fontsize=7.4,
                color=GRADE_COL[g], weight="bold")
    ax.set_yticks(ys)
    ax.set_yticklabels([SHORT[s] for s in order], fontsize=7.6)
    ax.set_xlim(0, 5.5); ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xlabel("Inherent aerosol release score (1–5)")
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(left=False)
    ax.grid(axis="x", color="#e8e8e8", lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    handles = [Line2D([], [], marker="s", ls="", ms=6, color=GRADE_COL[g],
                      label=f"{g}") for g in ("E1", "E2", "E3", "E5")]
    ax.legend(handles=handles, frameon=False, ncol=4, loc="upper center",
              bbox_to_anchor=(0.5, 1.13), handletextpad=0.3, columnspacing=1.0)
    save(fig, "fig2_evidence_profile")


# ------------------------------------------------------------------ Figure 3
def fig3_tb_pathway():
    """The steps a pulmonary TB specimen passes through, and what is known."""
    path = ["S01", "S03", "S05", "S02", "S07", "S06"]
    labels = ["Specimen\nreception", "Cap removal /\naliquoting",
              "GeneXpert\nloading", "Centrifugation\n(digestion)",
              "Open culture\nwork", "MALDI-TOF\nidentification"]
    fig, ax = plt.subplots(figsize=(7.0, 2.1))
    xs = np.arange(len(path))
    for x, sid, lab in zip(xs, path, labels):
        g = STEPS[sid]["evidence_grade"]
        r = row(sid, "P3")          # TB is a low-dose inhalational hazard
        rbi, band = float(r["RBI_baseline"]), r["RBI_baseline_band"]
        ax.scatter(x, 0, s=1500, color=GRADE_COL[g], zorder=3,
                   edgecolor="white", lw=2.0)
        ax.text(x, 0, g, ha="center", va="center", color="white",
                fontsize=9.5, weight="bold", zorder=4)
        ax.text(x, 0.40, lab, ha="center", va="bottom", fontsize=7.6,
                color=INK, linespacing=1.25)
        ax.text(x, -0.40, f"RBI {rbi:g}", ha="center", va="top",
                fontsize=7.4, color=INK)
        ax.text(x, -0.60, band, ha="center", va="top",
                fontsize=6.9, color=GREY)
        if x < len(path) - 1:
            ax.annotate("", xy=(x + 0.72, 0), xytext=(x + 0.28, 0),
                        arrowprops=dict(arrowstyle="-|>", color="#c4c4c4", lw=1.2))
    # No explanatory note inside the figure: the LaTeX caption carries it, and
    # at print width an in-figure note of this length is unreadable.
    ax.set_xlim(-0.6, len(path) - 0.4); ax.set_ylim(-0.95, 0.95)
    ax.axis("off")
    save(fig, "fig3_tb_pathway")


if __name__ == "__main__":
    print("brief figures:")
    fig1_measured(); fig2_evidence_profile(); fig3_tb_pathway()
