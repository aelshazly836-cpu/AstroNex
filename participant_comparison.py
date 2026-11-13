import pandas as pd

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

hb = "hemoglobin_value_percent"
rbc = "red_blood_cell_count_value_million_per_microliter"

df["Participant"] = df["Sample Name"].str.extract(r"^(C\d+)_")

selected = df[df["Timepoint"].isin(["L-3", "R+1"])]

for column, label in [(hb, "Hemoglobin"), (rbc, "RBC")]:
    pivot = selected.pivot(
        index="Participant",
        columns="Timepoint",
        values=column
    )

    pivot["Change"] = pivot["R+1"] - pivot["L-3"]
    pivot["Change_Percent"] = (
        pivot["Change"] / pivot["L-3"] * 100
    )

    print("\n", label)
    print(pivot.round(3).to_string())

