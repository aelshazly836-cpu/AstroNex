import pandas as pd

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

hb = "hemoglobin_value_percent"
rbc = "red_blood_cell_count_value_million_per_microliter"

valid = df[[hb, rbc]].dropna()

correlation = valid[hb].corr(valid[rbc])

print("Valid paired measurements:", len(valid))
print("Hemoglobin-RBC correlation:", round(correlation, 3))

