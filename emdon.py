import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Lane Emden eq
def emdon(z, u, n):
    theta, y = u
    return [y, -2*y/z - theta**n]

indices = [0, 1, 2, 3, 4]
zmax_values = [3, 4, 5, 8, 16]
z0 = 1e-5
results = []
plt.figure(figsize=(9, 6))

for n, zmax in zip(indices, zmax_values):
    # Taylor series expansion
    theta0 = 1 - z0**2/6 + n*z0**4/120
    y0 = -z0/3 + n*z0**3/30
    # Numerical integration
    sol = solve_ivp(
        emdon,
        (z0, zmax),
        [theta0, y0],
        args=(n,),
        dense_output=True,
        rtol=1e-10,
        atol=1e-12,
        max_step=0.05
    )
    crossing = np.where(sol.y[0] <= 0)[0]
    if len(crossing) == 0:
        print(f"First zero not found for n = {n}")
        continue
    i = crossing[0]
    a, b = sol.t[i-1], sol.t[i]
    theta_a, theta_b = sol.y[0, i-1], sol.y[0, i]
    # Initial root estimate by linear interpolation
    root = a - theta_a*(b-a)/(theta_b-theta_a)
    # NewtonRaphson iterations
    for k in range(20):
        theta_r, y_r = sol.sol(root)
        root_new = root - theta_r/y_r
        if abs(root_new-root) < 1e-11:
            root = root_new
            break
        root = root_new
    # Surface derivative
    theta_R, y_R = sol.sol(root)
    results.append((n, root, y_R))
    Z = np.linspace(0, root, 1000)
    T = np.empty_like(Z)
    T[0] = 1.0
    T[1:] = sol.sol(Z[1:])[0]
    plt.plot(Z, T, label=f"n = {n}")
# Print numerical results
print("\nNumerical Results")
print("-" * 55)
print(f"{'n':>3} {'zeta_R':>15} {'dtheta/dzeta':>18}")
for n, radius, derivative in results:
    print(f"{n:3d} {radius:15.8f} {derivative:18.8f}")
# Analytical comparisons
analytical = {
    0: (np.sqrt(6), -np.sqrt(6)/3),
    1: (np.pi, -1/np.pi)
}

print("\nAnalytical Comparison")

for n, radius, derivative in results:
    if n in analytical:
        exact_radius, exact_derivative = analytical[n]
        print(f"\nn = {n}")
        print(f"Numerical radius    = {radius:.8f}")
        print(f"Analytical radius   = {exact_radius:.8f}")
        print(f"Numerical derivative = {derivative:.8f}")
        print(f"Analytical derivative= {exact_derivative:.8f}")

plt.axhline(0, color="black", linewidth=0.8)
plt.xlabel(r"$\zeta$")
plt.ylabel(r"$\theta(\zeta)$")
plt.title("Numerical Solutions of the Lane-Emden Equation")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
