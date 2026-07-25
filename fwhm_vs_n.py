import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def sqrt_model(n, a):
    return a * np.sqrt(n)

def get_arrays_with_prob(d_target):
    filename = f"fwhm_{d_target}dp.txt"
    ns, fwhms, prob_rows = [], [], []
    with open(filename) as f:
        next(f)
        for line in f:
            parts = line.strip().split("\t")
            i, w, fwhm_val, prob_str = parts
            ns.append(float(i))
            fwhms.append(float(fwhm_val))
            prob_rows.append(np.array([float(v) for v in prob_str.split(",")]))
    return np.array(ns), np.array(fwhms), prob_rows

colors = {1: "tab:blue", 2: "tab:orange", 3: "tab:green"}
all_data = {}
prob_data = {}

for d in (1, 2, 3):
    ns, fwhms, prob_rows = get_arrays_with_prob(d)
    plt.figure()
    plt.scatter(ns, fwhms, s=10, label="data", alpha=0.6)
    plt.xlabel("n")
    plt.ylabel("FWHM")
    plt.title(f"{d}D random walk: FWHM vs n (normal scale)")
    plt.legend()

    # --- log(n) vs log(prob at x=0) ---
    prob_at_zero = np.array([p[len(p) // 2] for p in prob_rows])
    prob_data[d] = (ns, prob_at_zero)

    log_n = np.log(ns)
    log_p0 = np.log(prob_at_zero)
    slope, intercept = np.polyfit(log_n, log_p0, 1)

    print(f"d={d}: log-log slope = {slope:.4f} (expect ~-{d/2:.1f} for diffusive scaling)")

    all_data[d] = (log_n, log_p0, slope, intercept)
plt.figure(figsize=(8, 6))
for d in (1, 2, 3):
    ns, prob_at_zero = prob_data[d]
    plt.scatter(ns, prob_at_zero, s=10, color=colors[d], alpha=0.75,
                edgecolor="black", linewidth=0.4, label=f"{d}D data")

plt.xlabel("n", fontsize=12)
plt.ylabel("prob at x=0", fontsize=12)
plt.title("Random walk: prob at x=0 vs n — 1D/2D/3D comparison", fontsize=13)
plt.legend(frameon=True, fontsize=9)
plt.grid(True, alpha=0.3, linestyle=":")
plt.tight_layout()
# --- combined log n-log plot: all three dimensions, color-coded ---
plt.figure(figsize=(8, 6))
for d in (1, 2, 3):


    log_n, log_p0, slope, intercept = all_data[d]

    plt.scatter(log_n, log_p0, s=10, color=colors[d], alpha=0.75,
                edgecolor="black", linewidth=0.4, label=f"{d}D data")
    plt.plot(log_n, slope * log_n + intercept, color=colors[d],
             linestyle="--", linewidth=1.5, label=f"{d}D fit (slope={slope:.2f})")

plt.xlabel("log(n)", fontsize=12)
plt.ylabel("log(prob at x=0)", fontsize=12)
plt.title("Random walk: log(n) vs log(prob at x=0) — 1D/2D/3D comparison", fontsize=13)
plt.legend(frameon=True, fontsize=9)
plt.grid(True, alpha=0.3, linestyle=":")
plt.tight_layout()

plt.show()