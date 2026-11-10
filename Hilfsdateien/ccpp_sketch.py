"""Block diagram of a combined cycle power plant with the variables of the UCI CCPP dataset."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, BLUE_F = "#4E79A7", "#DFE7F0"     # features
ORA, ORA_F = "#F28E2B", "#FDE8D7"       # target
GAS = "#8C8C8C"                         # air and exhaust gas
WATER = "#2A9D8F"                       # steam and water
EL = "#333333"                          # electrical power
COMP_F, COMP_E = "#F4F4F4", "#666666"

fig, ax = plt.subplots(figsize=(13, 5.6))
ax.set_xlim(0, 17.6); ax.set_ylim(0, 7.3); ax.set_aspect("equal"); ax.set_axis_off()

def block(x, y, w, h, title, sub=None):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.15",
                                fc=COMP_F, ec=COMP_E, lw=2.2, zorder=3))
    if sub:
        ax.text(x, y + 0.22, title, ha="center", va="center", fontsize=12, weight="bold", zorder=4,
                linespacing=1.1)
        ax.text(x, y - 0.38, sub, ha="center", va="center", fontsize=10, color="#555555", zorder=4,
                linespacing=1.1)
    else:
        ax.text(x, y, title, ha="center", va="center", fontsize=12, weight="bold", zorder=4, linespacing=1.1)

def arrow(pts, col, label=None, lpos=None, lw=2.6, ha="center", fs=10.5):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=col, lw=lw, zorder=2, solid_capstyle="butt", solid_joinstyle="round")
    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>,head_length=0.5,head_width=0.25",
                                 mutation_scale=20, color=col, lw=0, zorder=2, shrinkA=0, shrinkB=0))
    if label:
        ax.text(*lpos, label, ha=ha, va="center", fontsize=fs, color=col if col != GAS else "#555555",
                linespacing=1.1)

def tag(x, y, text, ec, fc, fs=12.5):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, weight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.35", fc=fc, ec=ec, lw=2))

Y = 3.3                     # main line
GT, HR, ST = 4.6, 9.3, 13.7  # x positions of the blocks

block(GT, Y, 3.4, 1.6, "Gas turbine", "compressor, combustion\nchamber, turbine")
block(HR, Y, 3.0, 1.6, "Heat recovery\nsteam generator")
block(ST, Y, 2.8, 1.6, "Steam turbine")
block(ST, 0.75, 2.8, 1.0, "Condenser")

# air in, fuel in
arrow([(0.5, Y), (GT - 1.7, Y)], GAS, "ambient air", (1.6, Y + 0.35))
tag(1.6, Y - 0.55, "AT, AP, RH", BLUE, BLUE_F, fs=11.5)
arrow([(GT, 0.6), (GT, Y - 0.8)], "#B07AA1", "natural gas", (GT + 0.2, 1.0), ha="left")
# gas path
arrow([(GT + 1.7, Y), (HR - 1.5, Y)], GAS, "hot\nexhaust\ngas", ((GT + 1.7 + HR - 1.5) / 2, Y + 0.65), fs=10)
arrow([(HR, Y + 0.8), (HR, Y + 1.55)], GAS, "to stack", (HR + 0.2, Y + 1.35), ha="left")
# water / steam cycle
arrow([(HR + 1.5, Y), (ST - 1.4, Y)], WATER, "steam", ((HR + 1.5 + ST - 1.4) / 2, Y + 0.35))
arrow([(ST, Y - 0.8), (ST, 1.25)], WATER, "exhaust\nsteam", (ST + 0.2, 1.95), ha="left", fs=10)
arrow([(ST - 1.4, 0.75), (HR, 0.75), (HR, Y - 0.8)], WATER, "water", ((ST - 1.4 + HR) / 2 + 0.3, 0.45))
# cooling
arrow([(17.4, 0.95), (ST + 1.4, 0.95)], "#76B7B2")
arrow([(ST + 1.4, 0.55), (17.4, 0.55)], "#76B7B2")
ax.text(16.2, 1.35, "cooling water\nor air", ha="center", va="center", fontsize=10, color="#3F7F7A",
        linespacing=1.05)
tag(ST - 2.15, 1.75, "V", BLUE, BLUE_F)
ax.plot([ST - 1.88, ST - 1.4], [1.6, 1.15], color=BLUE, lw=1.6, zorder=5)
ax.text(ST - 2.15, 2.35, "condenser\npressure", ha="center", va="center", fontsize=10, color=BLUE,
        linespacing=1.05)

# electrical power
TOP = 6.25
ax.add_patch(FancyBboxPatch((GT - 1.7, TOP - 0.45), ST + 1.4 - (GT - 1.7), 0.9,
                            boxstyle="round,pad=0,rounding_size=0.15", fc=ORA_F, ec=ORA, lw=2.2, zorder=3))
ax.text((GT + ST) / 2, TOP, "PE  net electrical output to the grid", ha="center", va="center", fontsize=12.5,
        weight="bold", zorder=4)
arrow([(GT, Y + 0.8), (GT, TOP - 0.45)], EL, "electrical power\n(about 2/3)", (GT + 0.2, 4.85), ha="left",
      lw=2.2, fs=10)
arrow([(ST, Y + 0.8), (ST, TOP - 0.45)], EL, "electrical power\n(about 1/3)", (ST + 0.2, 4.85), ha="left",
      lw=2.2, fs=10)

fig.savefig("ccpp-sketch.png", dpi=160, facecolor="white", bbox_inches="tight", pad_inches=0.1)
