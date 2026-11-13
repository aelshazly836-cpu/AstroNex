import pandas as pd
import matplotlib.pyplot as plt

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

hb = "hemoglobin_value_percent"
rbc = "red_blood_cell_count_value_million_per_microliter"

order = ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]

df["Participant"] = df["Sample Name"].str.extract(r"^(C\d+)_")

for column, label, unit, filename in [
    (hb, "Hemoglobin", "Source unit", "hemoglobin"),
    (rbc, "RBC Count", "million/uL", "rbc")
]:
    plt.figure(figsize=(10, 6))

    for participant, group in df.groupby("Participant"):
        group = group.set_index("Timepoint").reindex(order)
        plt.plot(
            order,
            group[column],
            marker="o",
            label=participant
        )

    plt.title(f"{label} Individual Timeline")
    plt.xlabel("Sampling Timepoint")
    plt.ylabel(f"{label} ({unit})")
    plt.legend(title="Participant")
    plt.grid(True)
    plt.tight_layout()

    output = (
        f"data/processed/NASA_Inspiration4/"
        f"{filename}_individual_timeline.png"
    )
    plt.savefig(output, dpi=300)
    plt.close()

    print("Saved:", output)

print("\nIndividual timeline analysis completed!")
