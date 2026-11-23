#!/usr/bin/env python3
"""
09_preprint_figures.py - figures for the preprint, seaborn style

PLAIN LANGUAGE HEADER
Draws the four figures that appear in the preprint. Every value is read from
report/stats.json and the processed tables, so a figure can never disagree with
the text. Sized for a two-column page: single-column figures are 3.4 inches wide,
full-width figures 7.0 inches.

Run:  python3 code/09_preprint_figures.py
"""
import csv, json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "preprint" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

S = json.load(open(ROOT / "report/stats.json"))
ROWS = list(csv.DictReader(open(ROOT / "data/processed/reference_scores.csv")))
STEPS = yaml.safe_load(open(ROOT / "data/raw/steps.yaml"))["steps"]
INSTR = yaml.safe_load(open(ROOT / "instrument/instrument_v1.yaml"))
REV = set(INSTR["dimension_A"].get("reverse_coded_items", []))
PRIM = S["primary_profile_rows"]

sns.set_theme(style="ticks", context="paper",
              rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8,
                  "ytick.major.width": 0.8, "font.family": "serif",
                  "font.serif": ["DejaVu Serif"], "axes.labelsize": 8.5,
                  "xtick.labelsize": 8, "ytick.labelsize": 8,
                  "legend.fontsize": 7.6, "axes.titlesize": 9})

NAVY, RUST, GREY, INK = "#1b4f72", "#b3471f", "#9aa0a6", "#202124"
BAND_EDGES = [(1, 4, "Low"), (4, 9, "Moderate"), (9, 14, "Elevated"),
              (14, 19, "High"), (19, 25, "Very high")]
SHORT = {"S01": "Specimen\nreception", "S02": "Centrifugation", "S03": "Cap removal",
         "S04": "Automated\nanalysers", "S05": "GeneXpert\nloading",
         "S06": "MALDI-TOF\nidentification", "S07": "Open culture\nwork"}
FLAT = {k: v.replace("\n", " ") for k, v in SHORT.items()}
GX = {"E1": 1, "E2": 2, "E3": 3, "E4": 4, "E5": 5}


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  {name}.pdf / .png")


# ---------------------------------------------------------------- Figure 1
def fig1():
    """Evidence grade against residual biorisk: the inversion."""
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    for lo, hi, lab in BAND_EDGES:
        if lo >= 9:
            ax.axhspan(lo, min(hi, 21), color=RUST, alpha=0.055, zorder=0, lw=0)
    ax.axhline(9, color=GREY, lw=0.6, ls=(0, (4, 3)), zorder=1)
    ax.text(5.52, 9.45, "Elevated\nand above", fontsize=6.6, color=RUST,
            ha="right", va="bottom", linespacing=1.25)

    # label offsets in points, hand-placed so nothing collides
    place = {"S07": (-7, 0, "right", "center"), "S06": (8, 0, "left", "center"),
             "S05": (8, 0, "left", "center"),   "S03": (0, 9, "center", "bottom"),
             "S02": (2, -10, "left", "top"),  "S01": (8, 0, "left", "center"),
             "S04": (-8, 0, "right", "center")}
    jitter = {"S02": -0.17, "S03": 0.17}
    for sid, r in PRIM.items():
        x = GX[r["evidence_grade"]] + jitter.get(sid, 0.0)
        y = r["RBI_baseline"]
        ax.scatter(x, y, s=55, color=NAVY, zorder=4, edgecolor="white", lw=1.0)
        dx, dy, ha, va = place[sid]
        ax.annotate(FLAT[sid], (x, y), textcoords="offset points", xytext=(dx, dy),
                    ha=ha, va=va, fontsize=6.9, color=INK)
    ax.annotate("", xy=(5.3, 1.5), xytext=(1.3, 1.5),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    ax.text(3.3, 0.55, "weaker evidence", fontsize=6.8, color=GREY, ha="center")
    ax.set_xlim(0.3, 5.9); ax.set_ylim(-0.3, 21.5)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(["E1", "E2", "E3", "E4", "E5"])
    ax.set_xlabel("Evidence grade")
    ax.set_ylabel("Residual Biorisk Index, baseline practice")
    sns.despine(ax=ax)
    save(fig, "fig1_inversion")


# ---------------------------------------------------------------- Figure 2
def fig2():
    """Baseline against recommended control state."""
    order = sorted(PRIM, key=lambda k: PRIM[k]["RBI_baseline"])
    fig, ax = plt.subplots(figsize=(3.4, 3.1))
    for lo, hi, lab in BAND_EDGES:
        if lo > 1:
            ax.axvline(lo, color="#e4e4e4", lw=0.7, zorder=0)
    for i, sid in enumerate(order):
        r = PRIM[sid]
        ax.plot([r["RBI_recommended"], r["RBI_baseline"]], [i, i],
                color=GREY, lw=1.6, zorder=2, solid_capstyle="round", alpha=0.55)
        ax.scatter(r["RBI_baseline"], i, s=42, color=RUST, zorder=4,
                   edgecolor="white", lw=0.9,
                   label="Baseline practice" if i == 0 else None)
        ax.scatter(r["RBI_recommended"], i, s=42, color=NAVY, zorder=4,
                   edgecolor="white", lw=0.9,
                   label="Recommended controls" if i == 0 else None)
        ax.text(r["RBI_baseline"] + 0.55, i, r["evidence_grade"], va="center",
                fontsize=6.6, color=GREY)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([FLAT[s] for s in order], fontsize=7.4)
    ax.set_xlim(0, 22.5)
    ax.set_xlabel("Residual Biorisk Index")
    ax.legend(frameon=False, loc="lower right", handletextpad=0.35,
              borderpad=0.2, labelspacing=0.3)
    ax.grid(axis="x", color="#e8e8e8", lw=0.6, zorder=0)
    sns.despine(ax=ax, left=True)
    ax.tick_params(left=False)
    save(fig, "fig2_control_effect")


# ---------------------------------------------------------------- Figure 3
def fig3():
    """Item-level heat map: where the release actually comes from."""
    a_items = ["A1", "A2", "A3", "A4", "A5"]
    c_items = ["C1", "C2", "C3", "C4"]
    order = sorted(PRIM, key=lambda k: -PRIM[k]["RBI_baseline"])
    A = np.array([[(6 - STEPS[s]["iars"][i]) if i in REV else STEPS[s]["iars"][i]
                   for i in a_items] for s in order], float)
    C = np.array([[STEPS[s]["crs_baseline"][i] for i in c_items] for s in order], float)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.85),
                             gridspec_kw={"width_ratios": [5, 4], "wspace": 0.12})
    labA = ["A1 energy", "A2 loss of containment", "A3 concentration",
            "A4 proximity", "A5 throughput"]
    labC = ["C1 engineering", "C2 operator-independent",
            "C3 verification", "C4 PPE"]

    for k, (ax, M, lab, cmap, title, cbl) in enumerate((
            (axes[0], A, labA, "rocket_r", "(a)  Aerosol release, by item",
             "Release contribution"),
            (axes[1], C, labC, "mako", "(b)  Control reliability, baseline",
             "Control reliability"))):
        hm = sns.heatmap(M, ax=ax, cmap=cmap, vmin=1, vmax=5, annot=True, fmt=".0f",
                         annot_kws={"size": 7.2}, linewidths=1.3, linecolor="white",
                         cbar_kws={"shrink": 0.70, "pad": 0.030, "aspect": 13,
                                   "ticks": [1, 2, 3, 4, 5]})
        ax.set_xticks(np.arange(len(lab)) + 0.5)
        ax.set_xticklabels(lab, fontsize=6.4, rotation=32, ha="right",
                           rotation_mode="anchor")
        ax.set_yticks(np.arange(len(order)) + 0.5)
        if k == 0:
            ax.set_yticklabels([FLAT[s] for s in order], fontsize=7.0, rotation=0)
        else:
            ax.set_yticklabels([])
        ax.set_title(title, fontsize=8.0, loc="left", pad=5)
        ax.tick_params(length=0)
        cb = hm.collections[0].colorbar
        cb.ax.tick_params(labelsize=6.3, length=0)
        cb.set_label(cbl, size=6.5, labelpad=2)
        cb.outline.set_visible(False)
    # the reverse-coding note lives in the LaTeX caption, not on the canvas
    save(fig, "fig3_item_heatmap")


# ---------------------------------------------------------------- Figure 4
def fig4():
    """Sensitivity of each step to the agent profile assumed."""
    pal = {"P1": "#7fb3d5", "P2": "#2874a6", "P3": "#1b2f45"}
    names = {"P1": "P1 bloodborne, not inhalational",
             "P2": "P2 droplet/aerosol, prophylaxis exists",
             "P3": "P3 low-dose inhalational, unsuspected"}
    order = ["S01", "S02", "S03", "S04", "S05", "S06", "S07"]
    by = {(r["step_id"], r["agent_profile"]): float(r["RBI_baseline"]) for r in ROWS}
    fig, ax = plt.subplots(figsize=(7.0, 2.65))
    w, profs = 0.26, ["P1", "P2", "P3"]
    for j, p in enumerate(profs):
        xs, ys = [], []
        for i, sid in enumerate(order):
            if (sid, p) in by:
                xs.append(i + (j - 1) * w); ys.append(by[(sid, p)])
        ax.bar(xs, ys, width=w * 0.92, color=pal[p], label=names[p], zorder=3,
               edgecolor="white", lw=0.7)
    for lo, hi, lab in BAND_EDGES:
        ax.axhline(lo, color=GREY, lw=0.5, ls=(0, (3, 3)), zorder=1, alpha=0.7)
        if lo > 1:
            ax.text(7.32, lo + 0.2, lab, fontsize=6.2, color=GREY, va="bottom", ha="right")
    ax.text(7.32, 1.2, "Low", fontsize=6.2, color=GREY, va="bottom", ha="right")
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([SHORT[s] for s in order], fontsize=6.6, linespacing=1.25)
    ax.set_ylabel("Residual Biorisk Index,\nbaseline practice", fontsize=8)
    ax.set_ylim(0, 25.6); ax.set_xlim(-0.55, 7.38)
    ax.legend(frameon=False, ncol=3, loc="upper left", handlelength=0.9,
              handletextpad=0.35, columnspacing=1.1, labelspacing=0.2,
              borderpad=0.1, bbox_to_anchor=(-0.012, 1.035))
    ax.grid(axis="y", color="#eeeeee", lw=0.6, zorder=0)
    sns.despine(ax=ax)
    save(fig, "fig4_profile_sensitivity")


if __name__ == "__main__":
    print("preprint figures:")
    fig1(); fig2(); fig3(); fig4()
    print(f"written to {OUT}")
