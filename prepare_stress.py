from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).parent
SOURCE = BASE / "wearable-device-dataset-1.0.1" / "Wearable_Dataset" / "STRESS" / "f14_b"
OUTPUT = BASE / "data" / "processed" / "PhysioNet_STRESS" / "f14_b_stress_features.csv"


def load_signal(filename, columns):
    path = SOURCE / filename
    lines = path.read_text().splitlines()

    # ACC has three timestamps; use the first axis timestamp.
    start_time = pd.to_datetime(lines[0].split(",")[0])
    rate = float(lines[1].split(",")[0])

    values = pd.read_csv(path, skiprows=2, header=None)
    values = values.iloc[:, :columns].apply(pd.to_numeric, errors="coerce")

    timestamps = start_time + pd.to_timedelta(
        np.arange(len(values)) / rate, unit="s"
    )

    values.index = timestamps
    return values


hr = load_signal("HR.csv", 1)
eda = load_signal("EDA.csv", 1)
temp = load_signal("TEMP.csv", 1)
acc = load_signal("ACC.csv", 3)

acc["movement"] = np.sqrt(
    np.sqrt(acc.iloc[:, 0]**2 + acc.iloc[:, 1]**2 + acc.iloc[:, 2]**2)
)

signals = {
    "heart_rate": hr.iloc[:, 0],
    "eda": eda.iloc[:, 0],
    "skin_temperature": temp.iloc[:, 0],
    "movement": acc["movement"],
}

features = pd.concat(
    [signal.resample("1s").mean().rename(name)
     for name, signal in signals.items()],
    axis=1
)

print("Available records per sensor:")
for name, signal in signals.items():
    print(f"{name}: {signal.index.min()} -> {signal.index.max()}")

features = features.dropna()

features.insert(0, "participant", "f14")
features.index.name = "timestamp"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
features.to_csv(OUTPUT)

print("\nPreparation completed.")
print("Prepared records:", len(features))
print("Output:", OUTPUT)
print(features.head())