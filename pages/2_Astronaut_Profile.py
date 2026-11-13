import sqlite3
from pathlib import Path

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AstroNex | Astronaut Profile",
    page_icon="🚀",
    layout="wide"
)

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "astronex.db"

st.title("👨‍🚀 Astronaut Profile")
st.caption("ASTRONEX | PERSONAL MISSION RECORD")

if not DB_PATH.exists():
    st.error("Astronaut database was not found.")
    st.stop()

with sqlite3.connect(DB_PATH) as conn:
    astronauts = pd.read_sql_query(
        "SELECT * FROM astronauts ORDER BY full_name",
        conn
    )

if astronauts.empty:
    st.info("No astronauts registered yet.")
    st.write("Register an astronaut first from Astronaut Management.")
    st.stop()

st.subheader("Select Astronaut")

selected_id = st.selectbox(
    "Choose an astronaut",
    astronauts["id"].tolist(),
    format_func=lambda x: (
        astronauts.loc[
            astronauts["id"] == x, "full_name"
        ].iloc[0]
        + " ("
        + astronauts.loc[
            astronauts["id"] == x, "astronaut_code"
        ].iloc[0]
        + ")"
    )
)

with sqlite3.connect(DB_PATH) as conn:
    astronaut = pd.read_sql_query(
        "SELECT * FROM astronauts WHERE id = ?",
        conn,
        params=(selected_id,)
    ).iloc[0]

st.divider()

st.subheader(astronaut["full_name"])

st.caption(f"Astronaut ID: {astronaut['astronaut_code']}")

c1, c2, c3 = st.columns(3)

c1.metric("Mission", astronaut["mission"])
c2.metric("Current Status", astronaut["status"])
c3.metric("Start Date", astronaut["start_date"])

st.divider()

st.subheader("Mission Information")

col1, col2 = st.columns(2)

with col1:
    st.write("Astronaut Name")
    st.write(astronaut["full_name"])

    st.write("Astronaut ID")
    st.write(astronaut["astronaut_code"])

with col2:
    st.write("Mission")
    st.write(astronaut["mission"])

    st.write("Mission Start Date")
    st.write(astronaut["start_date"])

st.divider()

st.subheader("Monitoring Modules")

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("### ❤️ Health")
    st.write("Health readings and vital signs")
    st.caption("Not connected yet")

with m2:
    st.markdown("### ☢️ Radiation")
    st.write("Radiation exposure records")
    st.caption("Not connected yet")

with m3:
    st.markdown("### 🧬 Microgravity")
    st.write("Muscle, bone and cardiovascular changes")
    st.caption("Not connected yet")

st.divider()

st.caption(
    "AstroNex | Astronaut Personal Record"
)