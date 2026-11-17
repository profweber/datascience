"""Figure for Chapter 2: how quartiles divide the data and how a box plot is read."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, BLUE_F = "#4E79A7", "#DFE7F0"
ORA = "#F28E2B"
DARK, SUB = "#404040", "#666666"

rng = np.random.default_rng(9)
x = rng.gamma(shape=3.0, scale=15.0, size=1500)            # right-skewed example data
q1, med, q3 = np.quantile(x, [0.25, 0.5, 0.75])
iqr = q3 - q1
lo_lim, hi_lim = q1 - 1.5 * iqr, q3 + 1.5 * iqr
w_lo, w_hi = x[x >= lo_lim].min(), x[x <= hi_lim].max()      # whisker ends
xmax = x.max() * 1.03

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6, 5.6), sharex=True,
                               gridspec_kw={"height_ratios": [2.3, 1.6], "hspace": 0.05})

# ---- top: histogram, divided into four parts by the quartiles
ax1.hist(x, bins=45, color=BLUE_F, edgecolor=BLUE, lw=0.8)
ytop = ax1.get_ylim()[1] * 1.22
ax1.set_ylim(0, ytop)
edges = [x.min(), q1, med, q3, x.max()]
for a, b in zip(edges[:-1], edges[1:]):
    ax1.text((a + b) / 2, ytop * 0.9, "25 %", ha="center", va="center",
             fontsize=10.5, color=DARK, weight="bold")
ax1.set_ylabel("count", color=SUB)
ax1.text(0.99, 0.62, "each part contains\n25 % of the values", transform=ax1.transAxes,
         ha="right", va="center", fontsize=10.5, color=SUB)
for s in ["top", "right"]:
    ax1.spines[s].set_visible(False)

# ---- bottom: box plot of the same data
ax2.boxplot(x, orientation="horizontal", widths=0.32, positions=[0.0], whis=1.5, patch_artist=True,
            boxprops=dict(facecolor=BLUE_F, edgecolor=BLUE, lw=1.8),
            medianprops=dict(color=ORA, lw=2.5),
            whiskerprops=dict(color=BLUE, lw=1.6), capprops=dict(color=BLUE, lw=1.6),
            flierprops=dict(marker="o", markersize=4, markerfacecolor="white", markeredgecolor=BLUE))
ax2.set_ylim(-1.15, 1.05)
ax2.set_yticks([])
for s in ["top", "right", "left"]:
    ax2.spines[s].set_visible(False)
ax2.set_xlabel("value")

# dashed lines through Q1, median, Q3 in both panels
for v in (q1, med, q3):
    for ax in (ax1, ax2):
        ax.axvline(v, color=DARK, lw=1, ls=(0, (4, 3)), zorder=0)

# labels below the box
for v, t, ha, dx in [(q1, "$Q_1$", "right", -0.8), (med, "median", "center", 0), (q3, "$Q_3$", "left", 0.8)]:
    ax2.text(v + dx, -0.30, t, ha=ha, va="top", fontsize=11, color=DARK,
             bbox=dict(fc="white", ec="none", pad=1))
# IQR bracket above the box
yb = 0.30
ax2.annotate("", xy=(q1, yb), xytext=(q3, yb),
             arrowprops=dict(arrowstyle="<->", color=DARK, lw=1.3, shrinkA=0, shrinkB=0))
ax2.text((q1 + q3) / 2, yb + 0.07, "IQR = $Q_3 - Q_1$\n(middle half)", ha="center", va="bottom",
         fontsize=10.5, color=DARK, bbox=dict(fc="white", ec="none", pad=1))
# whiskers
ax2.annotate("whisker: up to the last value\nwithin 1.5 IQR of the box", xy=(w_hi, -0.05),
             xytext=(w_hi + 4, -0.82), ha="center", va="center", fontsize=10, color=SUB,
             arrowprops=dict(arrowstyle="->", color=SUB, lw=1))
ax2.annotate("whisker", xy=(w_lo, -0.05), xytext=(w_lo + 2, -0.82), ha="center", va="center",
             fontsize=10, color=SUB, arrowprops=dict(arrowstyle="->", color=SUB, lw=1))
# points beyond the whiskers
fl = x[x > hi_lim]
ax2.annotate("values beyond:\ndrawn individually", xy=(np.median(fl), 0.05),
             xytext=(np.median(fl) + 8, 0.62), ha="center", va="center", fontsize=10, color=SUB,
             arrowprops=dict(arrowstyle="->", color=SUB, lw=1))
ax2.set_xlim(0, xmax)

fig.savefig("boxplot-anatomy.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08)
print(f"Q1={q1:.1f} median={med:.1f} Q3={q3:.1f} whiskers {w_lo:.1f}..{w_hi:.1f}, beyond: {len(fl)}")
