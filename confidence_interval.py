import pandas as pd
from scipy.stats import t

file = "data/processed/NASA_Inspiration4/inspiration4_timeline.csv"
df = pd.read_csv(file)

participant = df["Sample Name"].str.extract(r"^(C\d+)_")[0]

metrics = {
    "Hemoglobin": "hemoglobin_value_percent",
    "RBC": "red_blood_cell_count_value_million_per_microliter"
}

print("\nNASA Inspiration4 - 95% Confidence Intervals")
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

    differences = (
        means["Post-flight"] - means["Pre-flight"]
    )

    n = len(differences)
    mean_diff = differences.mean()
    sd = differences.std(ddof=1)
    standard_error = sd / (n ** 0.5)

    critical_value = t.ppf(0.975, df=n - 1)

    margin = critical_value * standard_error

    lower = mean_diff - margin
    upper = mean_diff + margin

    print(f"\n{name}")
    print("Participants:", n)
    print("Mean difference:", round(mean_diff, 4))
    print("95% CI:", round(lower, 4), "to", round(upper, 4))

print("\nConfidence interval analysis completed!")