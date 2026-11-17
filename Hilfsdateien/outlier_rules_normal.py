"""Figure for Chapter 2: where the IQR rule and the robust z-score set their limits
for normally distributed data (no errors at all)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, BLUE_F = "#4E79A7", "#DFE7F0"
ORA, RED = "#F28E2B", "#C0392B"
DARK, SUB = "#404040", "#666666"

q = stats.norm.ppf(0.75)                 # Q3 = 0.674 sigma
k_iqr = q + 1.5 * 2 * q                  # IQR limit = 2.698 sigma
k_z = 3.5                                # robust z limit (1.4826 MAD = sigma for normal data)
DASH_I, DASH_Z = (0, (5, 3)), (0, (1.5, 2))

fig = plt.figure(figsize=(9.6, 4.6))
gs = fig.add_gridspec(2, 2, width_ratios=[1.75, 1], height_ratios=[2.4, 1], wspace=0.12, hspace=0.05)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
ax3 = fig.add_subplot(gs[:, 1])

# ---- left top: density
x = np.linspace(-4.2, 4.2, 800)
f = stats.norm.pdf(x)
ax1.plot(x, f, color=BLUE, lw=2)
ax1.fill_between(x, f, color=BLUE_F, zorder=0)
for sgn in (-1, 1):
    ax1.plot([sgn * k_iqr] * 2, [0, 0.10], color=ORA, lw=1.8, ls=DASH_I)
    ax1.plot([sgn * k_z] * 2, [0, 0.10], color=RED, lw=1.8, ls=DASH_Z)
ax1.text(k_iqr, 0.115, "IQR\nrule", ha="center", va="bottom", fontsize=9.5, color=ORA, weight="bold")
ax1.text(k_z + 0.05, 0.115, "robust\nz", ha="center", va="bottom", fontsize=9.5, color=RED, weight="bold")
ax1.text(-4.1, 0.40, "Normal distribution –\nevery value is valid", ha="left", va="center", fontsize=10.5,
         color=DARK)
ax1.set_ylim(0, 0.43)
ax1.set_yticks([])
ax1.tick_params(axis="x", length=0, labelbottom=False)
for s in ["top", "right", "left"]:
    ax1.spines[s].set_visible(False)
ax1.add_patch(plt.Rectangle((2.3, 0), 1.9, 0.035, fill=False, ec=SUB, lw=1))   # zoom region

# ---- left bottom: box plot of the same distribution
ax2.add_patch(plt.Rectangle((-q, -0.3), 2 * q, 0.6, fc=BLUE_F, ec=BLUE, lw=1.8))
ax2.plot([0, 0], [-0.3, 0.3], color=ORA, lw=2.5)
for a, b in [(-k_iqr, -q), (q, k_iqr)]:
    ax2.plot([a, b], [0, 0], color=BLUE, lw=1.6)
for c in (-k_iqr, k_iqr):
    ax2.plot([c, c], [-0.15, 0.15], color=BLUE, lw=1.6)
for sgn in (-1, 1):
    ax2.axvline(sgn * k_iqr, color=ORA, lw=1.4, ls=DASH_I, zorder=0)
    ax2.axvline(sgn * k_z, color=RED, lw=1.4, ls=DASH_Z, zorder=0)
for xe, t, xt in [(-q, "$Q_1$ = \u22120.67 \u03c3", -1.75), (q, "$Q_3$ = +0.67 \u03c3", 1.75)]:
    ax2.annotate(t, xy=(xe, -0.31), xytext=(xt, -0.72), ha="center", va="center", fontsize=9.5,
                 color=SUB, arrowprops=dict(arrowstyle="->", color=SUB, lw=1, shrinkA=2, shrinkB=0))
ax2.annotate("median", xy=(0, -0.31), xytext=(0, -0.72), ha="center", va="center", fontsize=9.5,
             color=SUB, arrowprops=dict(arrowstyle="->", color=SUB, lw=1, shrinkA=2, shrinkB=0))
ax2.text(k_iqr - 0.08, 0.42, "whisker end = IQR limit", ha="right", va="bottom", fontsize=9, color=SUB)
ax2.set_ylim(-0.95, 0.75)
ax2.set_yticks([])
for s in ["top", "right", "left"]:
    ax2.spines[s].set_visible(False)
ax2.set_xticks(range(-4, 5), [f"{v} \u03c3" if v else "0" for v in range(-4, 5)])
ax2.set_xlabel("distance from the centre")
ax2.set_xlim(-4.2, 4.2)

# ---- right: tail, enlarged
xt = np.linspace(2.3, 4.2, 300)
ft = stats.norm.pdf(xt)
ax3.plot(xt, ft, color=BLUE, lw=2)
ax3.fill_between(xt[xt >= k_iqr], ft[xt >= k_iqr], color=ORA, alpha=0.85, lw=0)
ax3.fill_between(xt[xt >= k_z], ft[xt >= k_z], color=RED, lw=0)
ax3.axvline(k_iqr, color=ORA, lw=1.8, ls=DASH_I)
ax3.axvline(k_z, color=RED, lw=1.8, ls=DASH_Z)
ax3.set_xlim(2.3, 4.2); ax3.set_ylim(0, 0.035)
ax3.set_xticks([k_iqr, k_z], ["2.7 \u03c3", "3.5 \u03c3"])
ax3.set_yticks([])
for s in ["top", "right", "left"]:
    ax3.spines[s].set_visible(False)
ax3.set_title("right tail, enlarged", fontsize=10.5, color=SUB, loc="left")
ax3.text(2.75, 0.031, f"IQR rule:\n{stats.norm.sf(k_iqr):.2%} per side,\n{2 * stats.norm.sf(k_iqr):.1%} in total",
         ha="left", va="top", fontsize=10, color=ORA, weight="bold", zorder=5,
         bbox=dict(fc="white", ec="none", pad=1.5))
ax3.text(3.55, 0.017, f"robust z:\n{stats.norm.sf(k_z):.3%} per side,\n\u2248 0.05% in total",
         ha="left", va="top", fontsize=10, color=RED, weight="bold", zorder=5,
         bbox=dict(fc="white", ec="none", pad=1.5))

fig.savefig("outlier-rules-normal.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08)
