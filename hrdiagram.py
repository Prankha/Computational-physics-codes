import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



file = "converted_uploaded_file2.csv"

data = pd.read_csv(file)



g = data["gmag_tab1"]
r = data["rmag_tab1"]
i = data["imag_tab1"]

color = g - r
abs_mag = i-2.5*np.log10(1000)


plt.figure(figsize=(8, 6))

plt.scatter(
    color,
    r,
    s=15,
    color="black",
    alpha=0.7
)

# Astronomical magnitude:
# smaller magnitude = brighter
plt.gca().invert_yaxis()

plt.xlabel("Color (g - r)")
plt.ylabel("Apparent Magnitude (r)")
plt.title("Color-Magnitude Diagram of M44")

plt.grid(True)
plt.tight_layout()

plt.show()