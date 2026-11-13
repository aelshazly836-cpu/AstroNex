import pandas as pd
from scipy.stats import ttest_rel

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

participant = df["Sample Name"].str.extract(r"^(C\d+)_")[0]

metrics = {
    "Hemoglobin": "hemoglobin_value_percent",
    "RBC": "red_blood_cell_count_value_million_per_microliter"
}

print("\nNASA Inspiration4 - Paired t-test")
print("=" * 55)

for name, column in metrics.items():

    data = pd.DataFrame({
        "Participant": participant,
        "Phase": df["Phase"],
        "Value": df[column]
    })

    means = data.groupby(
        ["Participant", "Phase"]
    )["Value"].mean().unstack()

    means = means.dropna(
        subset=["Pre-flight", "Post-flight"]
    )

    pre = means["Pre-flight"]
    post = means["Post-flight"]

    result = ttest_rel(post, pre)

    print(f"\n{name}")
    print("Participants:", len(means))
    print("Mean difference:", round((post - pre).mean(), 4))
    print("t-statistic:", round(result.statistic, 4))
    print("p-value:", round(result.pvalue, 4))

    if result.pvalue < 0.05:
        print("Result: Statistically significant")
    else:
        print("Result: Not statistically significant")

print("\nStatistical testing completed!")