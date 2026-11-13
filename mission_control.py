import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AstroNex | Mission Control",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #08111f;
    color: #e8f0ff;
}
[data-testid="stMetric"] {
    background: #111f33;
    padding: 18px;
    border: 1px solid #263b59;
    border-radius: 12px;
}
section[data-testid="stSidebar"] {
    background-color: #0d1929;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AstroNex")
st.caption("MISSION CONTROL CENTER | SPACE HUMAN MONITORING")

st.divider()

st.subheader("Mission Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Astronauts", "04", "Demo data")
c2.metric("Active Missions", "01", "Demo data")
c3.metric("Active Alerts", "02", "Demo data")
c4.metric("System Status", "ONLINE")

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("👨‍🚀 Astronaut Monitoring")

    astronauts = pd.DataFrame({
        "Astronaut": ["Astronaut 01", "Astronaut 02",
                      "Astronaut 03", "Astronaut 04"],
        "Mission": ["Mission Alpha"] * 4,
        "Status": ["Monitoring", "Monitoring",
                   "Review Required", "Monitoring"]
    })

    st.dataframe(
        astronauts,
        use_container_width=True,
        hide_index=True
    )

with right:
    st.subheader("⚠️ Mission Alerts")

    st.warning("Demo alert: Health data requires review.")
    st.info("Demo alert: Radiation data awaiting sensor connection.")

st.divider()

st.subheader("🛰️ Monitoring Modules")

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("### ❤️ Health")
    st.write("Vital signs and health records.")
    st.caption("Awaiting real data connection.")

with m2:
    st.markdown("### ☢️ Radiation")
    st.write("Individual exposure and radiation events.")
    st.caption("Awaiting detector connection.")

with m3:
    st.markdown("### 🧬 Microgravity")
    st.write("Muscle, bone, balance and fluid changes.")
    st.caption("Awaiting medical data connection.")

st.divider()

st.caption(
    "AstroNex Research Platform | "
    "All displayed astronaut records and alerts are demonstration data."
)