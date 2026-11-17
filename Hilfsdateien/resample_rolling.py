"""Figure for Chapter 2: resample() vs. rolling() on the same small time series."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, BLUE_F = "#4E79A7", "#DFE7F0"
ORA, ORA_F = "#F28E2B", "#FDE8D7"
DARK, SUB, LIGHT = "#404040", "#666666", "#B8B8B8"

# small example: 3 days, one value every 3 hours (8 values per day)
t = pd.date_range("2025-01-01", periods=24, freq="3h")
hours = np.arange(24) * 3
rng = np.random.default_rng(4)
y = 20 + 6 * np.sin((hours % 24 - 9) / 24 * 2 * np.pi) + hours / 12 + rng.normal(0, 1.2, 24)
y[13] += 9                                                     # a short peak on day 2
s = pd.Series(y, index=t)
daily = s.resample("D").mean()                                 # 3 values
smooth = s.rolling("1D").mean()                                # 24 values

fig, axes = plt.subplots(3, 1, figsize=(8.6, 7.0), sharex=True, sharey=True,
                         gridspec_kw={"hspace": 0.38})
for ax in axes:
    for d in range(3):                                         # light day bands
        ax.axvspan(d * 24, (d + 1) * 24, color="#F4F4F4" if d % 2 == 0 else "white", zorder=0)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    ax.set_ylim(8, 46)
    ax.tick_params(axis="x", length=0)
    ax.set_yticks([])

# colours: blue = raw data (grey in the lower panels), dark grey = intervals / windows,
# orange = results

# (1) raw data
ax = axes[0]
ax.plot(hours, y, color=BLUE, lw=1, zorder=2)
ax.plot(hours, y, "o", color=BLUE, ms=5, zorder=3)
ax.set_title("Raw data: one value every 3 hours (24 values)", loc="left", fontsize=11.5, color=DARK)

# (2) resample
ax = axes[1]
ax.plot(hours, y, "o", color=LIGHT, ms=4, zorder=2)
for d, v in enumerate(daily.values):
    ax.plot([d * 24 + 0.6, (d + 1) * 24 - 0.6], [v, v], color=ORA, lw=3, zorder=3, solid_capstyle="butt")
    ax.plot(d * 24 + 12, v, "o", color=ORA, ms=8, zorder=4, mec="white")
    ax.axvline(d * 24, color=DARK, lw=1.4, ls=(0, (4, 3)), zorder=1)
ax.set_title('resample("D").mean(): fixed intervals → one value per day (3 values)',
             loc="left", fontsize=11.5, color=DARK)

# (3) rolling
ax = axes[2]
ax.plot(hours, y, "o", color=LIGHT, ms=4, zorder=2)
ax.plot(hours, smooth.values, color=ORA, lw=2.5, zorder=3)
ax.plot(hours, smooth.values, "o", color=ORA, ms=5, mec="white", mew=0.8, zorder=4)
for k, (end, yb) in enumerate([(33, 10.0), (45, 12.6)]):      # two positions of the 24 h window
    ax.add_patch(Rectangle((end - 21 - 1.4, yb), 24 - 0.2, 28.0, fill=False, ec=DARK, lw=1.6,
                           ls="-" if k == 1 else (0, (4, 2)), zorder=5))
    i = end // 3
    ax.plot(hours[i], smooth.values[i], "o", color=ORA, ms=10, mec=DARK, mew=1.6, zorder=6)
ax.annotate("", xy=(47.5, 43.0), xytext=(36.5, 43.0),
            arrowprops=dict(arrowstyle="->", color=DARK, lw=1.6))
ax.text(42, 43.6, "window slides", ha="center", va="bottom", fontsize=10, color=DARK)
ax.annotate("mean of the values\nin the window", xy=(hours[15] + 0.8, smooth.values[15] - 0.8),
            xytext=(58, 13.5), ha="center", va="center", fontsize=10, color=SUB,
            arrowprops=dict(arrowstyle="->", color=SUB, lw=1))
ax.set_title('rolling("1D").mean(): sliding 24 h window → one value per time stamp (24 values)',
             loc="left", fontsize=11.5, color=DARK)

axes[2].set_xticks([12, 36, 60], ["Day 1", "Day 2", "Day 3"])
axes[2].tick_params(axis="x", length=0, labelsize=11)
axes[2].set_xlim(-2, 73)

fig.savefig("resample-rolling.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08)
print(daily.round(1).tolist())
