"""Small CRISP-DM diagrams for the chapter openings: the phases a chapter deals with are coloured,
all others are faded. Same geometry as crisp_dm.py.

Usage: python crisp_you_are_here.py   -> writes crisp-chXX.png for every chapter in CHAPTERS
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.path import Path

plt.rcParams["font.family"] = "DejaVu Sans"
COLOURS = [("#4E79A7", "#DFE7F0"), ("#4E79A7", "#DFE7F0"), ("#F28E2B", "#FDE8D7"),
           ("#F28E2B", "#FDE8D7"), ("#59A14F", "#E0EEDC"), ("#59A14F", "#E0EEDC")]
FADED = ("#C8C8C8", "#F7F7F7")
PHASES = ["1 Engineering\nunderstanding", "2 Data\nunderstanding", "3 Data\npreparation",
          "4 Modelling", "5 Evaluation", "6 Deployment"]

# phases (1-6) treated in each chapter – extend while working through the chapters
CHAPTERS = {
    "02": [2, 3],
}

RX, RY = 4.9, 3.35
W, H = 2.85, 1.35
GAP, ARROW = 0.25, 1.15
angles = np.deg2rad([90, 30, -30, -90, -150, -210])
centres = [(RX * np.cos(a), RY * np.sin(a)) for a in angles]

def inside(p, c, m=GAP):
    return abs(p[0] - c[0]) <= W / 2 + m and abs(p[1] - c[1]) <= H / 2 + m

def arc_points(ta, tb, n=60):
    t = np.linspace(ta, tb, n)
    return np.c_[RX * np.cos(t), RY * np.sin(t)]

def arc_len(ta, tb):
    p = arc_points(ta, tb, 400)
    return np.sum(np.hypot(*np.diff(p, axis=0).T))

def draw(active, fname):
    fig, ax = plt.subplots(figsize=(8.4, 5.9))
    ax.set_aspect("equal"); ax.set_axis_off()
    ax.set_xlim(-6.6, 6.6); ax.set_ylim(-4.4, 4.3)
    for k, ((x, y), text) in enumerate(zip(centres, PHASES)):
        on = (k + 1) in active
        ec, fc = COLOURS[k] if on else FADED
        ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0,rounding_size=0.18",
                                    ec=ec, fc=fc, lw=3.2 if on else 2, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=13, zorder=4, linespacing=1.15,
                color="black" if on else "#AAAAAA", weight="bold" if on else "normal")
    ax.add_patch(Circle((0, 0), 1.3, fc="#F7F7F7", ec="#C8C8C8", lw=2, zorder=2))
    ax.text(0, 0, "Data", ha="center", va="center", fontsize=19, weight="bold", color="#999999", zorder=4)
    for i in range(6):
        a0, a1 = angles[i], (angles[i + 1] if i < 5 else angles[0] - 2 * np.pi)
        t = np.linspace(a0, a1, 4000)
        pts = np.c_[RX * np.cos(t), RY * np.sin(t)]
        ok = np.array([not inside(p, centres[i]) and not inside(p, centres[(i + 1) % 6]) for p in pts])
        ta, tb = t[ok][0], t[ok][-1]
        ts = np.linspace(ta, tb, 2001)[::50]; s = np.array([arc_len(ta, x) for x in ts])
        mid = arc_len(ta, tb) / 2
        p = arc_points(np.interp(mid - ARROW / 2, s, ts), np.interp(mid + ARROW / 2, s, ts))
        ax.add_patch(FancyArrowPatch(path=Path(p), arrowstyle="-|>,head_length=0.45,head_width=0.25",
                                     mutation_scale=22, color="#BBBBBB", lw=2.2, zorder=1))
    fig.savefig(fname, dpi=150, facecolor="white", bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)

if __name__ == "__main__":
    for ch, active in CHAPTERS.items():
        draw(active, f"crisp-ch{ch}.png")
