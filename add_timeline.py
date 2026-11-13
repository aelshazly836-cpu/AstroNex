import pandas as pd

file = "data/processed/NASA_Inspiration4/inspiration4_merged.csv"
out = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"

df = pd.read_csv(file)

df["Timepoint"] = df["Sample Name"].str.extract(r'_(L-\d+|R\+\d+)_')

df["Phase"] = df["Timepoint"].apply(
    lambda x: "Pre-flight" if x.startswith("L-") else "Post-flight"
)

df.to_csv(out, index=False)

print(df[["Timepoint", "Phase"]].drop_duplicates().sort_values("Timepoint").to_string(index=False))
print("\nSaved:", out)
