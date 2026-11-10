import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.path import Path

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, BLUE_F = "#4E79A7", "#DFE7F0"
ORA, ORA_F = "#F28E2B", "#FDE8D7"
GREEN, GREEN_F = "#59A14F", "#E0EEDC"
DARK = "#404040"

RX, RY = 4.9, 3.35  # box centres lie on an ellipse (chosen so that all gaps between boxes are equal)
W, H = 2.85, 1.35    # box size
GAP = 0.25           # clearance between arrows and boxes
ARROW = 1.15         # visible length of every arrow (all arrows identical)
phases = ["1 Engineering\nunderstanding", "2 Data\nunderstanding", "3 Data\npreparation",
          "4 Modelling", "5 Evaluation", "6 Deployment"]
colours = [(BLUE, BLUE_F), (BLUE, BLUE_F), (ORA, ORA_F), (ORA, ORA_F), (GREEN, GREEN_F), (GREEN, GREEN_F)]
angles = np.deg2rad([90, 30, -30, -90, -150, -210])   # clockwise, starting at the top
centres = [(RX * np.cos(a), RY * np.sin(a)) for a in angles]

def inside(p, c, m=GAP):
    return abs(p[0] - c[0]) <= W / 2 + m and abs(p[1] - c[1]) <= H / 2 + m

def free_arc(i):
    """Angles of the part of the ellipse between box i and box i+1 that keeps the clearance."""
    a0, a1 = angles[i], (angles[i + 1] if i < 5 else angles[0] - 2 * np.pi)
    t = np.linspace(a0, a1, 4000)
    pts = np.c_[RX * np.cos(t), RY * np.sin(t)]
    ok = [not inside(p, centres[i]) and not inside(p, centres[(i + 1) % 6]) for p in pts]
    t = t[np.array(ok)]
    return t[0], t[-1]

def arc_points(ta, tb, n=60):
    t = np.linspace(ta, tb, n)
    return np.c_[RX * np.cos(t), RY * np.sin(t)]

def arc_len(ta, tb):
    p = arc_points(ta, tb, 400)
    return np.sum(np.hypot(*np.diff(p, axis=0).T))

fig, ax = plt.subplots(figsize=(8.4, 6.6))
ax.set_aspect("equal"); ax.set_axis_off()
ax.set_xlim(-6.6, 6.6); ax.set_ylim(-5.3, 4.3)

for (x, y), text, (ec, fc) in zip(centres, phases, colours):
    ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0,rounding_size=0.18",
                                ec=ec, fc=fc, lw=2.5, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=13, zorder=4, linespacing=1.15)

ax.add_patch(Circle((0, 0), 1.3, fc="#F0F0F0", ec="#999999", lw=2, zorder=2))
ax.text(0, 0, "Data", ha="center", va="center", fontsize=19, weight="bold", zorder=4)

gaps = []
for i in range(6):
    ta, tb = free_arc(i)
    gaps.append(arc_len(ta, tb))
    # centre an arrow of fixed length in the free part of the arc
    t = np.linspace(ta, tb, 2001)
    s = np.array([arc_len(ta, x) for x in t[::50]]); ts = t[::50]
    mid = arc_len(ta, tb) / 2
    t_start = np.interp(mid - ARROW / 2, s, ts); t_end = np.interp(mid + ARROW / 2, s, ts)
    p = arc_points(t_start, t_end)
    ax.add_patch(FancyArrowPatch(path=Path(p), arrowstyle="-|>,head_length=0.45,head_width=0.25",
                                 mutation_scale=22, color=DARK, lw=2.2, zorder=1, shrinkA=0, shrinkB=0))
print("free arc lengths:", np.round(gaps, 2))

ax.text(0, -4.85, "in practice, phases are revisited: e.g. modelling reveals data problems,\n"
        "evaluation leads back to a sharper engineering question",
        ha="center", va="center", fontsize=10.5, color="#888888", linespacing=1.3)
fig.savefig("crisp-dm.png", dpi=150, facecolor="white", bbox_inches="tight", pad_inches=0.15)
