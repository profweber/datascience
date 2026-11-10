import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, BLUE_F = "#4E79A7", "#DFE7F0"
ORA, ORA_F = "#F28E2B", "#FDE8D7"
GREY, GREY_F = "#999999", "#F0F0F0"
DARK, SUB = "#404040", "#666666"

def box(ax, x, y, w, h, ec, fc, ls="-"):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0,rounding_size=0.18",
                                ec=ec, fc=fc, lw=2.5, ls=ls, zorder=2))

def line(ax, x0, y0, x1, y1, ls="-"):
    ax.plot([x0, x1], [y0, y1], color=DARK, lw=1.8, ls=ls, zorder=1)

def elbow(ax, x0, y0, x1, y1, ls="-"):
    ym = (y0 + y1) / 2
    ax.plot([x0, x0, x1, x1], [y0, ym, ym, y1], color=DARK, lw=1.8, ls=ls, zorder=1, solid_joinstyle="round")

fig = plt.figure(figsize=(7.6, 5.3))
axa = fig.add_axes([0.0, 0.0, 1.0, 1.0])
axa.set_axis_off()
axa.set_xlim(-0.1, 10.1); axa.set_ylim(0.15, 7.05)

# ---- (a) hierarchy
box(axa, 5, 6.55, 2.4, 0.75, GREY, GREY_F)
axa.text(5, 6.55, "Variable", ha="center", va="center", fontsize=14, weight="bold", zorder=3)

groups = [(2.5, "Categorical", "(qualitative)", "values are labels", ORA, ORA_F),
          (7.5, "Numeric", "(quantitative)", "values are amounts", BLUE, BLUE_F)]
for x, t, t2, s, ec, fc in groups:
    elbow(axa, 5, 6.17, x, 5.42)
    box(axa, x, 4.85, 4.2, 1.1, ec, fc)
    axa.text(x, 5.08, f"{t} {t2}", ha="center", va="center", fontsize=13, weight="bold", zorder=3)
    axa.text(x, 4.62, s, ha="center", va="center", fontsize=11.5, color=SUB, zorder=3)

leaves = [(1.25, "Nominal", "unordered", "fault type,\nsupplier", ORA, ORA_F, 2.5),
          (3.75, "Ordinal", "ordered", "quality class\nL/M/H", ORA, ORA_F, 2.5),
          (6.25, "Discrete", "countable", "defects per part,\nfailures per year", BLUE, BLUE_F, 7.5),
          (8.75, "Continuous", "any value in a range", "temperature,\ntorque", BLUE, BLUE_F, 7.5)]
for x, t, s, ex, ec, fc, xp in leaves:
    elbow(axa, xp, 4.30, x, 3.62)
    box(axa, x, 2.85, 2.3, 1.5, ec, fc)
    axa.text(x, 3.33, t, ha="center", va="center", fontsize=12.5, weight="bold", zorder=3)
    axa.text(x, 2.98, s, ha="center", va="center", fontsize=10.5, color=SUB, zorder=3)
    axa.text(x, 2.45, ex, ha="center", va="center", fontsize=10.5, style="italic", color=DARK, zorder=3,
             linespacing=1.15)

# binary as special case of nominal
line(axa, 1.25, 2.10, 1.25, 1.42, ls=(0, (3, 2)))
box(axa, 1.25, 0.85, 2.3, 1.1, ORA, "white", ls=(0, (4, 2)))
axa.text(1.25, 1.12, "Binary", ha="center", va="center", fontsize=12, weight="bold", zorder=3)
axa.text(1.25, 0.70, "two categories:\nfailure yes/no", ha="center", va="center", fontsize=10, color=SUB,
         zorder=3, linespacing=1.15)
axa.text(2.55, 0.85, "special case of nominal", ha="left", va="center", fontsize=10.5, color=SUB)

fig.savefig("variable-types.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08)
