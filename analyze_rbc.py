import pandas as pd
import matplotlib.pyplot as plt

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

column = "red_blood_cell_count_value_million_per_microliter"

order = ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]

summary = df.groupby("Timepoint")[column].agg(
    ["mean", "min", "max", "count"]
).reindex(order)

print("RBC descriptive statistics:")
print(summary.round(3).to_string())

summary["mean"].plot(marker="o")
plt.title("RBC Count Across Inspiration4 Sampling Timepoints")
plt.xlabel("Sampling Timepoint")
plt.ylabel("RBC Count (million/uL)")
plt.grid(True)
plt.tight_layout()
plt.savefig(
    "data/processed/NASA_Inspiration4/rbc_timeline.png"
)

print("\nChart saved successfully.")
