import pandas as pd
import matplotlib.pyplot as plt

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

column = "hemoglobin_value_percent"

summary = df.groupby("Timepoint")[column].agg(
    ["mean", "min", "max", "count"]
)

order = ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]
summary = summary.reindex(order)

print("Hemoglobin descriptive statistics:")
print(summary.round(2).to_string())

summary["mean"].plot(marker="o")
plt.title("Hemoglobin Across Inspiration4 Sampling Timepoints")
plt.xlabel("Sampling Timepoint")
plt.ylabel("Mean Hemoglobin (source unit)")
plt.grid(True)
plt.tight_layout()
plt.savefig(
    "data/processed/NASA_Inspiration4/hemoglobin_timeline.png"
)
print("\nChart saved successfully.")
