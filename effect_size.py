import pandas as pd

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

participant = df["Sample Name"].str.extract(r"^(C\d+)_")[0]

metrics = {
    "Hemoglobin": "hemoglobin_value_percent",
    "RBC": "red_blood_cell_count_value_million_per_microliter"
}

print("\nNASA Inspiration4 - Effect Size Analysis")
print("=" * 55)

for name, column in metrics.items():

    data = pd.DataFrame({
        "Participant": participant,
        "Phase": df["Phase"],
        "Value": df[column]
    })

    means = data.groupby(
        ["Participant", "Phase"]
    )["Value"].mean().unstack()

    means = means.dropna(
        subset=["Pre-flight", "Post-flight"]
    )

    differences = (
        means["Post-flight"] - means["Pre-flight"]
    )

    mean_difference = differences.mean()
    sd_difference = differences.std(ddof=1)

    if sd_difference == 0:
        print(f"\n{name}: Cannot calculate Cohen's dz")
        continue

    cohen_dz = mean_difference / sd_difference

    print(f"\n{name}")
    print("Participants:", len(differences))
    print("Mean difference:", round(mean_difference, 4))
    print("SD of differences:", round(sd_difference, 4))
    print("Cohen's dz:", round(cohen_dz, 4))

print("\nEffect size analysis completed!")