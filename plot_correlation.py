import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

hb = "hemoglobin_value_percent"
rbc = "red_blood_cell_count_value_million_per_microliter"

valid = df[[hb, rbc]].dropna()

x = valid[rbc]
y = valid[hb]

# Calculate the linear trendline
slope, intercept = np.polyfit(x, y, 1)
trendline = slope * x + intercept

# Calculate Pearson correlation
correlation = x.corr(y)

plt.figure(figsize=(9, 6))
plt.scatter(x, y, label="Measurements")
plt.plot(x, trendline, label="Linear trendline")

plt.title(f"Hemoglobin vs RBC Count (r = {correlation:.3f})")
plt.xlabel("RBC Count (million/uL)")
plt.ylabel("Hemoglobin (source unit)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "data/processed/NASA_Inspiration4/hemoglobin_rbc_correlation.png",
    dpi=300
)

print("Correlation:", round(correlation, 3))
print("Number of measurements:", len(valid))
print("Scatter plot saved successfully.")
