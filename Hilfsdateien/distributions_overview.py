"""Figure for Chapter 3: typical shapes of the five distributions in the table."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, BLUE_F = "#4E79A7", "#DFE7F0"
ORA, GREEN = "#F28E2B", "#59A14F"
DARK, SUB = "#404040", "#666666"

fig, axes = plt.subplots(1, 5, figsize=(12.5, 2.7), gridspec_kw={"wspace": 0.25})

def style(ax, title, note):
    ax.set_title(title, fontsize=11.5, color=DARK, weight="bold", pad=22)
    ax.text(0.5, 1.02, note, transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color=SUB)
    lo, hi = ax.get_ylim()
    ax.set_ylim(0, hi * 1.05)
    ax.set_yticks([])
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8.5, colors=SUB)

# Normal
x = np.linspace(-4, 4, 400)
axes[0].fill_between(x, stats.norm.pdf(x), color=BLUE_F)
axes[0].plot(x, stats.norm.pdf(x), color=BLUE, lw=2)
axes[0].set_xticks([-2, 0, 2], ["$\\mu-2\\sigma$", "$\\mu$", "$\\mu+2\\sigma$"])
style(axes[0], "Normal", "symmetric")

# Lognormal
x = np.linspace(0.001, 4, 400)
f = stats.lognorm.pdf(x, s=0.5)
axes[1].fill_between(x, f, color=BLUE_F)
axes[1].plot(x, f, color=BLUE, lw=2)
axes[1].set_xticks([0], ["0"])
style(axes[1], "Lognormal", "right-skewed, only positive")

# Weibull: three shapes
x = np.linspace(0.001, 2.5, 400)
for b, col in [(0.8, ORA), (1.5, BLUE), (3.5, GREEN)]:
    axes[2].plot(x, stats.weibull_min.pdf(x, b), color=col, lw=2, label=f"$\\beta$ = {b}")
axes[2].set_ylim(0, 1.6)
axes[2].set_xticks([0, 1, 2], ["0", "$\\eta$", "$2\\eta$"])
axes[2].legend(fontsize=8.5, frameon=False, loc="upper right")
style(axes[2], "Weibull", "shape set by $\\beta$")

# Exponential
x = np.linspace(0, 4, 400)
axes[3].fill_between(x, stats.expon.pdf(x), color=BLUE_F)
axes[3].plot(x, stats.expon.pdf(x), color=BLUE, lw=2)
axes[3].set_xticks([0, 1, 2, 3], ["0", "$1/\\lambda$", "$2/\\lambda$", "$3/\\lambda$"])
style(axes[3], "Exponential", "= Weibull with $\\beta$ = 1")

# Poisson (discrete)
k = np.arange(0, 11)
axes[4].bar(k, stats.poisson.pmf(k, 3), color=BLUE, width=0.6)
axes[4].set_xticks([0, 3, 6, 9])
axes[4].text(0.97, 0.95, "$\\lambda$ = 3", transform=axes[4].transAxes, ha="right", va="top", fontsize=9, color=SUB)
style(axes[4], "Poisson", "discrete: counts 0, 1, 2, …")

fig.savefig("distributions.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08)
