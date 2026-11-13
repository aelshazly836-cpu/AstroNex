import pandas as pd

file = "data/processed/NASA_Inspiration4/inspiration4_merged.csv"
df = pd.read_csv(file)

print("Dataset shape:", df.shape)
print("\nMissing values per column:")

missing = df.isnull().sum()
print(missing[missing > 0].to_string())

print("\nData types:")
print(df.dtypes.value_counts())

print("\nFirst 3 rows:")
print(df.iloc[:3, :8].to_string(index=False))
