import pandas as pd
import glob
import os

files = glob.glob("data/raw/NASA_Inspiration4/*.csv")

for file in files:
    df = pd.read_csv(file)

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    print("\n==============================")
    print(os.path.basename(file))
    print("Missing columns:")

    if missing.empty:
        print("No missing values")
    else:
        print(missing.to_string())