import pandas as pd

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

metrics = {
    "Hemoglobin": "hemoglobin_value_percent",
    "RBC": "red_blood_cell_count_value_million_per_microliter"
}

print("\nNASA Inspiration4 - Phase Comparison")
print("=" * 55)

for name, column in metrics.items():
    summary = df.groupby("Phase")[column].agg(
        ["count", "mean", "std", "min", "max"]
    )

    print(f"\n{name}")
    print(summary.round(3).to_string())

    pre = df.loc[df["Phase"] == "Pre-flight", column].mean()
    post = df.loc[df["Phase"] == "Post-flight", column].mean()

    difference = post - pre
    percent = (difference / pre) * 100

    print(f"\nPre-flight mean: {pre:.3f}")
    print(f"Post-flight mean: {post:.3f}")
    print(f"Difference: {difference:.3f}")
    print(f"Percentage difference: {percent:.2f}%")

print("\nPhase comparison completed!")