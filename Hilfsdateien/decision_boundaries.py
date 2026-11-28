"""Figures for Chapter 7: decision boundaries of three classifiers, and a decision tree built level by level."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, ORA = "#4E79A7", "#F28E2B"
LIGHT_BLUE, LIGHT_ORA = "#DCE6F0", "#FBE2CC"
DARK, SUB = "#404040", "#666666"

X, y = make_moons(n_samples=300, noise=0.3, random_state=0)        # two interleaving half-moons
x_lo, x_hi = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5                # plot range covers all points
y_lo, y_hi = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.linspace(x_lo, x_hi, 500), np.linspace(y_lo, y_hi, 500))
grid = np.c_[xx.ravel(), yy.ravel()]

def panel(ax, model, title):
    """Shade the predicted class, draw the boundary and the data."""
    cls = model.predict(grid).reshape(xx.shape)
    ax.contourf(xx, yy, cls, levels=[-0.5, 0.5, 1.5], colors=[LIGHT_BLUE, LIGHT_ORA])
    ax.contour(xx, yy, cls, levels=[0.5], colors="k", linewidths=1.6)
    ax.scatter(X[:, 0], X[:, 1], c=np.where(y == 1, ORA, BLUE), s=9, edgecolors="none")
    ax.set_xlim(x_lo, x_hi); ax.set_ylim(y_lo, y_hi); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=12, color=DARK)

# --- Figure 1: three classifiers ---------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(13, 3.9))
models = [("logistic regression", LogisticRegression()),
          ("kNN (k = 15)", KNeighborsClassifier(15)),
          ("decision tree (depth 4)", DecisionTreeClassifier(max_depth=4, random_state=0))]
for ax, (title, m) in zip(axes, models):
    panel(ax, m.fit(X, y), title)
fig.savefig("decision-boundaries.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08)

# --- Figure 2: the tree of depth 4, level by level --------------------------------
tree = DecisionTreeClassifier(max_depth=4, random_state=0).fit(X, y).tree_

def split_lines(node, box, depth, max_depth, out):
    """Collect the split lines down to max_depth as (xs, ys, depth); each line spans only its box."""
    if depth >= max_depth or tree.children_left[node] == -1:          # leaf or deep enough
        return
    feature, t = tree.feature[node], tree.threshold[node]
    xa, xb, ya, yb = box
    if feature == 0:                                                   # split on x1: vertical line
        out.append(([t, t], [ya, yb], depth)); left, right = (xa, t, ya, yb), (t, xb, ya, yb)
    else:                                                              # split on x2: horizontal line
        out.append(([xa, xb], [t, t], depth)); left, right = (xa, xb, ya, t), (xa, xb, t, yb)
    split_lines(tree.children_left[node], left, depth + 1, max_depth, out)
    split_lines(tree.children_right[node], right, depth + 1, max_depth, out)

fig, axes = plt.subplots(1, 4, figsize=(16, 4.2))
for d, ax in zip(range(1, 5), axes):
    panel(ax, DecisionTreeClassifier(max_depth=d, random_state=0).fit(X, y), "")
    for coll in ax.collections[1:2]:                                   # hide the class boundary,
        coll.remove()                                                  # the split lines show it
    lines = []
    split_lines(0, (x_lo, x_hi, y_lo, y_hi), 0, d, lines)
    for xs, ys, k in lines:
        new = (k == d - 1)
        ax.plot(xs, ys, color="k" if new else "0.45", lw=2.2 if new else 0.9)
    n_new = sum(k == d - 1 for *_, k in lines)
    ax.set_title(f"depth {d}: {n_new} new split{'s' if n_new > 1 else ''}", fontsize=12, color=DARK)
    ax.set_xlabel("$x_1$", color=SUB); ax.set_ylabel("$x_2$", color=SUB)
fig.savefig("tree-steps.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08)
