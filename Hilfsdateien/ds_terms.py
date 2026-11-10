import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, PathPatch
from matplotlib.path import Path

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, ORA, GREEN, RED, PURP = "#4E79A7", "#F28E2B", "#59A14F", "#E15759", "#B07AA1"
DARK, SUB = "#333333", "#555555"

fig = plt.figure(figsize=(13, 6.4))
axa = fig.add_axes([0.0, 0.0, 0.47, 0.88]); axb = fig.add_axes([0.49, 0.0, 0.51, 0.88])
for ax in (axa, axb):
    ax.set_axis_off(); ax.set_aspect("equal")
fig.text(0.02, 0.935, "(a) Competences: what you need to know", fontsize=15.5, weight="bold")
fig.text(0.50, 0.935, "(b) Methods: how the method families relate", fontsize=15.5, weight="bold")
fig.add_artist(plt.Line2D([0.478, 0.478], [0.04, 0.90], color="#CCCCCC", lw=1.2))

# ---------------- (a) Venn diagram of competences
axa.set_xlim(0, 10); axa.set_ylim(0.3, 8.75)
r = 2.5
centres = {"stat": (3.6, 5.75), "cs": (6.4, 5.75), "dom": (5.0, 3.33)}
cols = {"stat": BLUE, "cs": ORA, "dom": GREEN}
for k, (x, y) in centres.items():
    axa.add_patch(Circle((x, y), r, fc=cols[k], alpha=0.18, ec="none"))
for k, (x, y) in centres.items():
    axa.add_patch(Circle((x, y), r, fc="none", ec=cols[k], lw=2.5))
axa.text(2.65, 6.75, "Statistics &\nmathematics", ha="center", va="center", fontsize=13.5, weight="bold",
         color="#2F4F7A", linespacing=1.1)
axa.text(7.35, 6.75, "Computer\nscience &\nprogramming", ha="center", va="center", fontsize=13.5, weight="bold",
         color="#B25E0B", linespacing=1.1)
axa.text(5.0, 1.75, "Domain knowledge\n(engineering)", ha="center", va="center", fontsize=13.5, weight="bold",
         color="#3B7032", linespacing=1.1)
axa.text(5.0, 6.95, "models\nwithout\ncontext", ha="center", va="center", fontsize=11, color=DARK,
         linespacing=1.1)
axa.text(3.5, 3.85, "classical\nengineering\nstatistics", ha="center", va="center", fontsize=10, color=DARK,
         linespacing=1.1)
axa.text(6.5, 3.85, "danger zone:\ntools without\nstatistics", ha="center", va="center", fontsize=10,
         color="#B22222", linespacing=1.1)
axa.text(5.0, 4.95, "Data\nscience", ha="center", va="center", fontsize=14.5, weight="bold", color="black",
         linespacing=1.1)

# ---------------- (b) method families
axb.set_xlim(0, 11); axb.set_ylim(0.0, 8.75)
mc, mr = np.array([6.55, 4.45]), 3.05            # machine learning circle
off = 0.10                                       # AI outline runs just outside the ML arc
t1, t2 = np.deg2rad(115), np.deg2rad(245)
xL = mc[0] + (mr + off) * np.cos(t1)             # x where AI's straight left edges meet the arc
top, bot, right = 8.55, 0.35, 10.85
arc = [(mc[0] + (mr + off) * np.cos(t), mc[1] + (mr + off) * np.sin(t)) for t in np.linspace(t1, t2, 60)]
c = 0.35   # corner radius (quadratic Bezier corners)
verts, codes = [], []
def mv(p): verts.append(p); codes.append(Path.MOVETO)
def ln(p): verts.append(p); codes.append(Path.LINETO)
def cv(ctrl, p): verts.extend([ctrl, p]); codes.extend([Path.CURVE3, Path.CURVE3])
mv((xL + c, top)); ln((right - c, top)); cv((right, top), (right, top - c)); ln((right, bot + c))
cv((right, bot), (right - c, bot)); ln((xL + c, bot)); cv((xL, bot), (xL, bot + c)); ln(arc[-1])
for p in arc[::-1][1:]:
    ln(p)
ln((xL, top - c)); cv((xL, top), (xL + c, top)); codes[-1] = Path.CURVE3
ai = Path(verts, codes)
axb.add_patch(PathPatch(ai, fc=RED, alpha=0.08, ec="none"))
axb.add_patch(PathPatch(ai, fc="none", ec=RED, lw=2.5, joinstyle="round"))
axb.text(xL + 0.35, top - 0.5, "Artificial intelligence", ha="left", va="center", fontsize=14, weight="bold",
         color="#B22222")
axb.text(right - 0.25, bot + 0.75, "AI without ML: rule-based\nexpert systems, search, planning", ha="right",
         va="center", fontsize=11, color=SUB, linespacing=1.15)

# statistics: crosses into AI only through the ML circle
sc = (2.75, 4.45)
axb.add_patch(Ellipse(sc, 5.3, 4.6, fc=BLUE, alpha=0.15, ec="none"))
axb.add_patch(Circle(mc, mr, fc=ORA, alpha=0.16, ec="none"))
axb.add_patch(Ellipse((7.75, 3.85), 2.9, 2.5, fc=PURP, alpha=0.18, ec="none"))
axb.add_patch(Ellipse(sc, 5.3, 4.6, fc="none", ec=BLUE, lw=2.5))
axb.add_patch(Circle(mc, mr, fc="none", ec=ORA, lw=2.5))
axb.add_patch(Ellipse((7.75, 3.85), 2.9, 2.5, fc="none", ec=PURP, lw=2.5))

axb.text(1.95, 5.25, "Statistics", ha="center", va="center", fontsize=14, weight="bold", color="#2F4F7A")
axb.text(1.95, 4.05, "hypothesis tests,\nconfidence\nintervals, DoE,\ndistributions,\nsampling",
         ha="center", va="center", fontsize=10.5, color=SUB, linespacing=1.15)
axb.text(4.45, 4.45, "statistical\nlearning:\nregression,\nlogistic reg.,\nPCA, Gaussian\nprocesses",
         ha="center", va="center", fontsize=10, color=DARK, linespacing=1.15)
axb.text(7.05, 6.85, "Machine learning", ha="center", va="center", fontsize=14, weight="bold", color="#B25E0B")
axb.text(7.05, 6.1, "random forests, gradient\nboosting, k-means,\nisolation forest", ha="center", va="center",
         fontsize=10.5, color=SUB, linespacing=1.15)
axb.text(7.75, 4.3, "Deep learning", ha="center", va="center", fontsize=12.5, weight="bold", color="#7B4B6E")
axb.text(7.75, 3.55, "neural networks:\nMLP, CNN, LSTM,\nLLMs", ha="center", va="center", fontsize=10,
         color=SUB, linespacing=1.15)

fig.savefig("ds-terms.png", dpi=160, facecolor="white")
