import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AstroNex | Health Monitoring",
    page_icon="❤️",
    layout="wide"
)

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "astronex.db"

def connect():
    return sqlite3.connect(DB_PATH)

def initialize():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS health_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                astronaut_id INTEGER NOT NULL,
                heart_rate REAL,
                systolic_bp REAL,
                diastolic_bp REAL,
                spo2 REAL,
                temperature REAL,
                sleep_hours REAL,
                recorded_at TEXT NOT NULL,
                FOREIGN KEY (astronaut_id) REFERENCES astronauts(id)
            )
        """)

initialize()

st.title("❤️ Health Monitoring")
st.caption("ASTRONEX | ASTRONAUT HEALTH RECORDS")
st.divider()

with connect() as conn:
    astronauts = pd.read_sql_query(
        "SELECT id, astronaut_code, full_name FROM astronauts ORDER BY full_name",
        conn
    )

if astronauts.empty:
    st.warning("Register an astronaut first.")
    st.stop()

selected_id = st.selectbox(
    "Select Astronaut",
    astronauts["id"].tolist(),
    format_func=lambda x: (
        astronauts.loc[astronauts["id"] == x, "full_name"].iloc[0]
        + " | "
        + astronauts.loc[astronauts["id"] == x, "astronaut_code"].iloc[0]
    )
)

st.divider()
st.subheader("Record Health Measurements")

st.info(
    "Enter authorized measurements only. "
    "This module stores records and does not diagnose medical conditions."
)

with st.form("health_form"):
    c1, c2 = st.columns(2)

    with c1:
        heart_rate = st.number_input(
            "Heart Rate (bpm)", min_value=0.0, max_value=300.0, value=0.0
        )
        systolic = st.number_input(
            "Systolic Blood Pressure (mmHg)", min_value=0.0, max_value=300.0, value=0.0
        )
        diastolic = st.number_input(
            "Diastolic Blood Pressure (mmHg)", min_value=0.0, max_value=200.0, value=0.0
        )

    with c2:
        spo2 = st.number_input(
            "SpO2 (%)", min_value=0.0, max_value=100.0, value=0.0
        )
        temperature = st.number_input(
            "Body Temperature (°C)", min_value=0.0, max_value=50.0, value=0.0
        )
        sleep_hours = st.number_input(
            "Sleep Duration (hours)", min_value=0.0, max_value=24.0, value=0.0
        )

    submitted = st.form_submit_button(
        "Save Health Record",
        use_container_width=True
    )

    if submitted:
        with connect() as conn:
            conn.execute("""
                INSERT INTO health_readings (
                    astronaut_id, heart_rate, systolic_bp,
                    diastolic_bp, spo2, temperature,
                    sleep_hours, recorded_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                selected_id,
                heart_rate if heart_rate > 0 else None,
                systolic if systolic > 0 else None,
                diastolic if diastolic > 0 else None,
                spo2 if spo2 > 0 else None,
                temperature if temperature > 0 else None,
                sleep_hours if sleep_hours > 0 else None,
                datetime.now().isoformat(timespec="seconds")
            ))

        st.success("Health record saved successfully!")
        st.rerun()

st.divider()
st.subheader("Health History")

with connect() as conn:
    history = pd.read_sql_query("""
        SELECT recorded_at, heart_rate, systolic_bp,
               diastolic_bp, spo2, temperature, sleep_hours
        FROM health_readings
        WHERE astronaut_id = ?
        ORDER BY recorded_at DESC
    """, conn, params=(selected_id,))

if history.empty:
    st.info("No health measurements recorded for this astronaut.")
else:
    st.metric("Total Health Records", len(history))

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "AstroNex stores measurements for monitoring and professional review. "
    "It is not a medical diagnosis system."
)