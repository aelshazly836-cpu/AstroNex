import pandas as pd

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

df["Participant"] = df["Sample Name"].str.extract(r"^(C\d+)_")[0]

metrics = {
    "Hemoglobin": "hemoglobin_value_percent",
    "RBC": "red_blood_cell_count_value_million_per_microliter"
}

for name, column in metrics.items():

    print("\n" + "=" * 50)
    print(name, "Paired Analysis")
    print("=" * 50)

    participant_means = df.groupby(
        ["Participant", "Phase"]
    )[column].mean().unstack()

    participant_means["Difference"] = (
        participant_means["Post-flight"]
        - participant_means["Pre-flight"]
    )

    participant_means["Change (%)"] = (
        participant_means["Difference"]
        / participant_means["Pre-flight"] * 100
    )

    print(participant_means.round(3).to_string())

    print("\nOverall participant comparison:")
    print("Average difference:",
          round(participant_means["Difference"].mean(), 3))

    print("Average percentage change:",
          round(participant_means["Change (%)"].mean(), 2), "%")

print("\nPaired analysis completed!")