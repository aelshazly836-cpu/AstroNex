import pandas as pd
import matplotlib.pyplot as plt

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

hb = "hemoglobin_value_percent"
rbc = "red_blood_cell_count_value_million_per_microliter"

order = ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]

metrics = [
    (hb, "Hemoglobin", "hemoglobin_relative_change.png"),
    (rbc, "RBC", "rbc_relative_change.png")
]

participant = df["Sample Name"].str.extract(r"^(C\d+)_")[0]

for column, label, filename in metrics:
    data = pd.DataFrame({
        "Participant": participant,
        "Timepoint": df["Timepoint"],
        "Value": df[column]
    })

    pivot = data.pivot(
        index="Participant",
        columns="Timepoint",
        values="Value"
    ).reindex(columns=order)

    baseline = pivot["L-92"]

    relative_change = (
        pivot.sub(baseline, axis=0)
        .div(baseline, axis=0) * 100
    )

    print("\n" + label + " Relative Change (%)")
    print(relative_change.round(2).to_string())

    plt.figure(figsize=(10, 6))

    for person in relative_change.index:
        plt.plot(
            order,
            relative_change.loc[person],
            marker="o",
            label=person
        )

    plt.axhline(0, linestyle="--")
    plt.title(label + " Relative Change Compared with L-92")
    plt.xlabel("Sampling Timepoint")
    plt.ylabel("Relative Change (%)")
    plt.legend(title="Participant")
    plt.grid(True)
    plt.subplots_adjust(bottom=0.15)

    output = "data/processed/NASA_Inspiration4/" + filename
    plt.savefig(output, dpi=300)
    plt.close()

    print("Saved:", output)

print("\nRelative change analysis completed!")