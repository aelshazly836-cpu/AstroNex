import pandas as pd
import matplotlib.pyplot as plt

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

participant = df["Sample Name"].str.extract(r"^(C\d+)_")[0]
df["Participant"] = participant

metrics = [
    ("hemoglobin_value_percent", "Hemoglobin",
     "paired_hemoglobin.png"),
    ("red_blood_cell_count_value_million_per_microliter",
     "RBC", "paired_rbc.png")
]

for column, label, filename in metrics:

    summary = df.groupby(
        ["Participant", "Phase"]
    )[column].mean().unstack()

    summary = summary[["Pre-flight", "Post-flight"]]

    plt.figure(figsize=(9, 6))

    for person in summary.index:
        plt.plot(
            ["Pre-flight", "Post-flight"],
            summary.loc[person],
            marker="o",
            linewidth=2,
            label=person
        )

    plt.title(f"{label}: Pre-flight vs Post-flight")
    plt.xlabel("Flight Phase")
    plt.ylabel(label)
    plt.legend(title="Participant")
    plt.grid(True, alpha=0.3)

    output = "data/processed/NASA_Inspiration4/" + filename

    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()

    print("Saved:", output)

print("\nPaired visualization completed!")