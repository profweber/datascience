"""Figure for Chapter 3: idealised Q-Q plots for typical deviations from the model."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, ORA = "#4E79A7", "#F28E2B"
DARK, SUB = "#404040", "#666666"

n = 40
p = (np.arange(1, n + 1) - 0.5) / n          # share below the i-th smallest value

def normal_model_q(dist):
    """Quantiles of a normal model that matches dist in the middle (same median and IQR)."""
    q1, med, q3 = dist.ppf([0.25, 0.5, 0.75])
    return stats.norm.ppf(p, med, (q3 - q1) / 1.349)

cases = [
    ("Model fits", "points on the diagonal",
     stats.norm(0, 1), stats.norm(0, 1)),
    ("Heavier tails than the model", "low end below, high end above:\nmore extreme values on both sides",
     stats.t(3), None),
    ("Data skewed to the right", "both ends above:\nshort left tail, long right tail",
     stats.lognorm(0.6), None),
    ("Model with too small spread", "straight, but steeper:\ndata scatter more than assumed",
     stats.norm(0, 1.5), stats.norm(0, 1)),
]

fig, axes = plt.subplots(1, 4, figsize=(13.5, 4.0), gridspec_kw={"wspace": 0.3})
for ax, (title, note, data, model) in zip(axes, cases):
    data_q = data.ppf(p)                                     # idealised data: exact quantiles
    model_q = model.ppf(p) if model is not None else normal_model_q(data)
    lo = min(data_q.min(), model_q.min()); hi = max(data_q.max(), model_q.max())
    pad = 0.08 * (hi - lo)
    ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color=DARK, lw=1)   # diagonal y = x
    ax.scatter(model_q, data_q, s=14, color=BLUE, zorder=3)
    ax.set_xlim(lo - pad, hi + pad); ax.set_ylim(lo - pad, hi + pad)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=11, color=DARK, weight="bold", pad=34)
    ax.text(0.5, 1.03, note, transform=ax.transAxes, ha="center", va="bottom", fontsize=8.8, color=SUB)
    ax.set_xlabel("model quantile", fontsize=9.5, color=SUB)
    ax.set_ylabel("data quantile", fontsize=9.5, color=SUB)

fig.savefig("qq-patterns.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08)
