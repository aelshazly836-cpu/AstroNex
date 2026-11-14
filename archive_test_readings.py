import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / "data" / "astronex.db"

with sqlite3.connect(db_path) as conn:
    conn.execute("BEGIN")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS health_readings_archive
        AS SELECT * FROM health_readings WHERE 0
    """)

    conn.execute("""
        INSERT OR IGNORE INTO health_readings_archive
        SELECT * FROM health_readings
        WHERE is_test = 1
    """)

    archived = conn.execute(
        "SELECT COUNT(*) FROM health_readings_archive"
    ).fetchone()[0]

    remaining = conn.execute(
        "SELECT COUNT(*) FROM health_readings WHERE is_test = 1"
    ).fetchone()[0]

    if archived < remaining:
        raise RuntimeError("Archive verification failed.")

    conn.execute("DELETE FROM health_readings WHERE is_test = 1")

print(f"Archived readings: {archived}")
