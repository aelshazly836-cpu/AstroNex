import pandas as pd

base = "data/raw/NASA_Inspiration4/"
out = "data/processed/NASA_Inspiration4/"

cbc = pd.read_csv(base + "LSDS-7_Complete_Blood_Count_CBC_TRANSFORMED.csv")
cmp = pd.read_csv(base + "LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv")
cv = pd.read_csv(base + "LSDS-8_Multiplex_serum_cardiovascular_EvePanel_TRANSFORMED.csv")

cbc["sample_key"] = (
    cbc["Sample Name"]
    .str.replace("_whole-blood_", "_serum_", regex=False)
    .str.replace("_cbc", "", regex=False)
)

cmp["sample_key"] = cmp["Sample Name"]
cv["sample_key"] = cv["Sample Name"]

merged = cbc.merge(
    cmp.drop(columns=["Sample Name"]),
    on="sample_key",
    validate="one_to_one"
)

merged = merged.merge(
    cv.drop(columns=["Sample Name"]),
    on="sample_key",
    validate="one_to_one"
)

merged = merged.drop(columns=["sample_key"])

merged.to_csv(out + "inspiration4_merged.csv", index=False)

print("Merge completed!")
print("Rows:", merged.shape[0])
print("Columns:", merged.shape[1])
print("Missing values:", merged.isna().sum().sum())
print("Saved to:", out + "inspiration4_merged.csv")
