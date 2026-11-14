import csv
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB = BASE / "data" / "astronex.db"
CSV_FILE = BASE / "data" / "simulated_wearable_data.csv"

with sqlite3.connect(DB) as conn:
    conn.execute("PRAGMA foreign_keys = ON")

    with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        imported = 0
        skipped = 0

        for row in reader:
            astronaut = conn.execute(
                "SELECT id FROM astronauts WHERE astronaut_code = ?",
                (row["astronaut_code"],)
            ).fetchone()

            if astronaut is None:
                raise ValueError(
                    f"Astronaut not found: {row['astronaut_code']}"
                )

            astronaut_id = astronaut[0]
            timestamp = row["timestamp"]

            exists = conn.execute(
                """SELECT 1 FROM health_readings
                   WHERE astronaut_id = ? AND recorded_at = ?""",
                (astronaut_id, timestamp)
            ).fetchone()

            if exists:
                skipped += 1
                continue
            conn.execute(
                """INSERT INTO health_readings
                   (astronaut_id, heart_rate, systolic_bp, diastolic_bp,
                    spo2, temperature, sleep_hours, recorded_at, is_test)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    astronaut_id,
                    float(row["heart_rate"]),
                    float(row["systolic_bp"]),
                    float(row["diastolic_bp"]),
                    float(row["spo2"]),
                    float(row["temperature"]),
                    float(row["sleep_hours"]),
                    timestamp,
                    1
                )
            )
            imported += 1
print(f"Imported: {imported}")
print(f"Skipped duplicates: {skipped}")
print("Simulation data import completed.")

