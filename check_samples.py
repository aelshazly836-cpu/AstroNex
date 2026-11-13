import pandas as pd

base = "data/raw/NASA_Inspiration4/"

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

sets = [
    set(cbc["sample_key"]),
    set(cmp["sample_key"]),
    set(cv["sample_key"])
]

print("CBC vs CMP:", sets[0] == sets[1])
print("CMP vs Cardiovascular:", sets[1] == sets[2])
print("Common samples:", len(sets[0] & sets[1] & sets[2]))
