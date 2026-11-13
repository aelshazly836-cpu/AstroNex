import pandas as pd

file = "data/processed/NASA_Inspiration4/inspiration4_merged.csv"
df = pd.read_csv(file)

columns = [
    "Sample Name",
    "egfr_african_american_value_milliliter_per_minute_per_1.73_meter_squared",
    "egfr_non_african_american_value_milliliter_per_minute_per_1.73_meter_squared",
    "egfr_african_american_range_max_milliliter_per_minute_per_1.73_meter_squared",
    "egfr_non_african_american_range_max_milliliter_per_minute_per_1.73_meter_squared",
    "urea_nitrogen_bun_value_milligram_per_deciliter",
    "creatinine_value_milligram_per_deciliter",
    "bun_to_creatinine_ratio_value"
]

print(df[columns].to_string(index=False))
