import sqlite3
from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AstroNex | Astronaut Management",
    page_icon="👨‍🚀",
    layout="wide"
)

# Database
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "astronex.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS astronauts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                astronaut_code TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                mission TEXT NOT NULL,
                start_date TEXT,
                status TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def add_astronaut(code, name, mission, start_date, status):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO astronauts
            (astronaut_code, full_name, mission, start_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (code, name, mission, str(start_date), status))

def load_astronauts():
    with get_connection() as conn:
        return pd.read_sql_query(
            "SELECT * FROM astronauts ORDER BY id DESC",
            conn
        )

initialize_database()

# Interface
st.title("👨‍🚀 Astronaut Management")
st.caption("ASTRONEX | ASTRONAUT REGISTRY")

st.divider()

st.subheader("Register New Astronaut")

with st.form("astronaut_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        code = st.text_input("Astronaut ID", placeholder="AST-001")
        name = st.text_input("Full Name")
        mission = st.text_input("Mission Name")

    with col2:
        start_date = st.date_input(
            "Mission Start Date",
            value=date.today()
        )
        status = st.selectbox(
            "Current Status",
            ["Active", "Training", "Inactive", "Under Review"]
        )

    submitted = st.form_submit_button(
        "Register Astronaut",
        use_container_width=True
    )

    if submitted:
        if not code.strip() or not name.strip() or not mission.strip():
            st.error("Please complete all required fields.")
        else:
            try:
                add_astronaut(
                    code.strip().upper(),
                    name.strip(),
                    mission.strip(),
                    start_date,
                    status
                )
                st.success("Astronaut registered successfully.")
            except sqlite3.IntegrityError:
                st.error("This Astronaut ID already exists.")

st.divider()

st.subheader("Astronaut Registry")

df = load_astronauts()

if not df.empty:
    search = st.text_input("Search by name or ID")

    if search:
        df = df[
            df["full_name"].str.contains(search, case=False, na=False)
            | df["astronaut_code"].str.contains(search, case=False, na=False)
        ]

    st.metric("Registered Astronauts", len(load_astronauts()))

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No astronauts registered yet. Add the first astronaut above.")
