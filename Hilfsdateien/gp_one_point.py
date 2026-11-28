"""Figure for Chapter 6: a Gaussian process with a single measurement.
Left: Bayes at the measured point (prior x likelihood -> posterior).
Right: the correction carries over to other inputs according to the kernel correlation."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, ORA, GREY = "#4E79A7", "#F28E2B", "#8C8C8C"
DARK, SUB = "#404040", "#666666"

m, sf = 455.0, 17.0           # prior: mean and standard deviation of the output (MW)
x1, y1, sn = 20.0, 440.0, 10.0  # one measurement at 20 °C: 440 MW, measurement scatter 10 MW
ell = 5.0                     # length scale (°C)

w = sf**2 / (sf**2 + sn**2)                  # weight of the measurement
mu1, sd1 = m + w * (y1 - m), sf * np.sqrt(1 - w)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.2), gridspec_kw={"wspace": 0.25})

f = np.linspace(395, 515, 600)
ax1.plot(f, stats.norm.pdf(f, m, sf), color=GREY, ls="--", lw=1.6, label=f"prior: {m:.0f} ± {sf:.0f} MW")
ax1.plot(f, stats.norm.pdf(f, y1, sn), color=ORA, lw=1.6, label=f"measurement: {y1:.0f} ± {sn:.0f} MW")
ax1.plot(f, stats.norm.pdf(f, mu1, sd1), color=BLUE, lw=2.6, label=f"posterior: {mu1:.1f} ± {sd1:.1f} MW")
ax1.set_title("Step 1 – Bayes at the measured point (20 °C)", fontsize=11, color=DARK, weight="bold")
ax1.set_xlabel("output at 20 °C (MW)", fontsize=9.5, color=SUB)
ax1.set_ylabel("density", fontsize=9.5, color=SUB)
ax1.set_yticks([])
ax1.legend(fontsize=8.5, loc="upper right", frameon=False)

T = np.linspace(0, 40, 400)
rho = np.exp(-(T - x1)**2 / (2 * ell**2))     # kernel: correlation with the value at 20 °C
mu = m + rho * w * (y1 - m)
sd = sf * np.sqrt(1 - rho**2 * w)
ax2.axhline(m, color=GREY, ls="--", lw=1.2, label="prior mean")
ax2.fill_between(T, mu - 2 * sd, mu + 2 * sd, color=BLUE, alpha=0.22, lw=0, label="posterior mean ± 2 standard deviations")
ax2.plot(T, mu, color=BLUE, lw=2, label="posterior mean")
ax2.errorbar(x1, y1, yerr=2 * sn, fmt="o", color=ORA, capsize=3, label="measurement ± 2 σ$_n$")
for t, dy in [(22, -14), (30, 12)]:
    r = np.exp(-(t - x1)**2 / (2 * ell**2))
    mt = m + r * w * (y1 - m)
    ax2.plot(t, mt, "o", color=DARK, ms=4)
    ax2.annotate(f"{t} °C: ρ = {r:.2f}\n{mt:.1f} MW", (t, mt), xytext=(6, dy), textcoords="offset points",
                 fontsize=8.5, color=DARK)
ax2.set_title("Step 2 – transfer to other temperatures (ℓ = 5 °C)", fontsize=11, color=DARK, weight="bold")
ax2.set_xlabel("ambient temperature (°C)", fontsize=9.5, color=SUB)
ax2.set_ylabel("output (MW)", fontsize=9.5, color=SUB)
ax2.set_ylim(412, 498)
ax2.legend(fontsize=8.5, loc="lower left", frameon=False)

fig.savefig("gp-one-point.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08)
