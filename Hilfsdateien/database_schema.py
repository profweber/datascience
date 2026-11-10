"""Schema of the example production database (appendix 'Data from Databases')."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, BLUE_F = "#4E79A7", "#DFE7F0"
GREY, GREY_F = "#999999", "#F4F4F4"
DARK = "#404040"

fig, ax = plt.subplots(figsize=(10, 4.6))
ax.set_xlim(0, 20); ax.set_ylim(0, 9.2); ax.set_aspect("equal"); ax.set_axis_off()
ROW = 0.62

def table(x, y_top, name, cols, ec=BLUE, fc=BLUE_F, w=4.6):
    """Draw a table box; cols = list of (name, tag) with tag in {"PK", "FK", ""}. Returns row y-positions."""
    h = ROW * (len(cols) + 1) + 0.2
    ax.add_patch(FancyBboxPatch((x, y_top - h), w, h, boxstyle="round,pad=0,rounding_size=0.15",
                                fc="white", ec=ec, lw=2.2, zorder=2))
    ax.add_patch(FancyBboxPatch((x, y_top - ROW - 0.1), w, ROW + 0.1, boxstyle="round,pad=0,rounding_size=0.15",
                                fc=fc, ec=ec, lw=2.2, zorder=3))
    ax.text(x + w / 2, y_top - ROW / 2 - 0.05, name, ha="center", va="center", fontsize=12.5, weight="bold",
            family="DejaVu Sans Mono", zorder=4)
    ys = {}
    for k, (c, tag) in enumerate(cols):
        yy = y_top - ROW * (k + 1.5) - 0.1
        ax.text(x + 0.3, yy, c, ha="left", va="center", fontsize=11, family="DejaVu Sans Mono",
                weight="bold" if tag == "PK" else "normal", zorder=4)
        if tag:
            ax.text(x + w - 0.3, yy, tag, ha="right", va="center", fontsize=9.5, zorder=4,
                    color=BLUE if tag == "PK" else "#B25E0B", weight="bold")
        ys[c] = yy
    return ys

ins = table(0.4, 8.6, "inspections", [("part_id", "PK"), ("order_id", "FK"), ("diameter_mm", ""), ("result", "")])
ords = table(7.7, 8.6, "orders", [("order_id", "PK"), ("machine_id", "FK"), ("start_time", ""), ("shift", ""),
                                   ("material", ""), ("quantity", "")])
mach = table(15.0, 8.6, "machines", [("machine_id", "PK"), ("line", ""), ("year_built", "")])
mnt = table(15.0, 4.0, "maintenance", [("machine_id", "FK"), ("date", ""), ("kind", "")], ec=GREY, fc=GREY_F)

def link(x0, y0, x1, y1, rad=0.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>,head_length=0.5,head_width=0.25",
                                 mutation_scale=20, color=DARK, lw=1.8, zorder=1,
                                 connectionstyle=f"arc3,rad={rad}"))

link(5.0, ins["order_id"], 7.7, ords["order_id"])                 # inspections.order_id -> orders.order_id
link(12.3, ords["machine_id"], 15.0, mach["machine_id"])          # orders.machine_id -> machines.machine_id
link(15.0, mnt["machine_id"], 15.0, mach["machine_id"] - 0.05, rad=-0.6)  # maintenance -> machines
ax.text(9.9, 0.45, "PK = primary key,  FK = foreign key;  arrows point from a foreign key to the key it refers to",
        ha="center", va="center", fontsize=10, color="#666666")
fig.savefig("database-schema.png", dpi=180, facecolor="white", bbox_inches="tight", pad_inches=0.1)
