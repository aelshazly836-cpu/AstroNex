import pandas as pd

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

column = "red_blood_cells_value"

print("Available RBC columns:")
print([c for c in df.columns if "red" in c.lower() or "rbc" in c.lower()])
