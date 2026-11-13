import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="AstroNex | NASA Research",
    page_icon="🛰️",
    layout="wide"
)

# Dataset
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    BASE_DIR / "data" / "processed"
    / "NASA_Inspiration4" / "inspiration4_merged.csv"
)

TIME_ORDER = [
    "L-92", "L-44", "L-3",
    "R+1", "R+45", "R+82", "R+194"
]

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    parsed = df["Sample Name"].str.extract(
        r"^(C\d+)_whole-blood_(L-\d+|R\+\d+)_cbc$"
    )

    df["Participant"] = parsed[0]
    df["Timepoint"] = parsed[1]

    df["Timepoint"] = pd.Categorical(
        df["Timepoint"],
        categories=TIME_ORDER,
        ordered=True
    )

    return df


st.title("🛰️ NASA Research Center")
st.caption("ASTRONEX | INSPIRATION4 BIOMEDICAL DATA")

st.divider()

if not DATA_PATH.exists():
    st.error("NASA dataset was not found.")
    st.stop()

df = load_data()

if df["Participant"].notna().sum() == 0:
    st.error("Could not identify participants from sample names.")
    st.stop()

# Overview
c1, c2, c3 = st.columns(3)

c1.metric("Total Samples", len(df))
c2.metric("Participants", df["Participant"].nunique())
c3.metric(
    "Available Biomarkers",
    len([
        col for col in df.columns
        if "_value_" in col.lower()
    ])
)

st.divider()

# Filters
st.subheader("Research Explorer")

participants = ["All Participants"] + sorted(
    df["Participant"].dropna().unique().tolist()
)

selected_participant = st.selectbox(
    "Select Participant",
    participants
)

value_columns = [
    col for col in df.columns
    if "_value_" in col.lower()
    and pd.api.types.is_numeric_dtype(df[col])
    and df[col].notna().any()
]

def readable_name(column):
    name = column.replace("_value_", " ")
    name = name.replace("_", " ")
    return name.title()

selected_metric = st.selectbox(
    "Select Biomarker",
    value_columns,
    format_func=readable_name
)

# Matching reference ranges
prefix = selected_metric.split("_value_")[0]

min_column = prefix + "_range_min_" + selected_metric.split("_value_")[1]
max_column = prefix + "_range_max_" + selected_metric.split("_value_")[1]

has_reference = (
    min_column in df.columns
    and max_column in df.columns
)

filtered = df.copy()

if selected_participant != "All Participants":
    filtered = filtered[
        filtered["Participant"] == selected_participant
    ]

filtered = filtered.dropna(
    subset=["Timepoint", selected_metric]
).sort_values("Timepoint")

st.divider()

# Chart
st.subheader(f"📈 {readable_name(selected_metric)}")

fig = go.Figure()

for participant in filtered["Participant"].dropna().unique():
    person = filtered[
        filtered["Participant"] == participant
    ]

    fig.add_trace(go.Scatter(
        x=person["Timepoint"].astype(str),
        y=person[selected_metric],
        mode="lines+markers",
        name=participant
    ))

if has_reference and not filtered.empty:
    reference_min = filtered[min_column].dropna()
    reference_max = filtered[max_column].dropna()

    if not reference_min.empty and not reference_max.empty:
        fig.add_hline(
            y=reference_min.iloc[0],
            line_dash="dash",
            annotation_text="Reference Minimum"
        )

        fig.add_hline(
            y=reference_max.iloc[0],
            line_dash="dash",
            annotation_text="Reference Maximum"
        )

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Mission Timeline",
    yaxis_title=readable_name(selected_metric),
    hovermode="x unified",
    legend_title="Participant"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Statistics
st.subheader("📊 Research Statistics")

if not filtered.empty:
    values = filtered[selected_metric]

    a, b, c, d = st.columns(4)

    a.metric("Mean", f"{values.mean():.3f}")
    b.metric("Minimum", f"{values.min():.3f}")
    c.metric("Maximum", f"{values.max():.3f}")
    d.metric("Measurements", len(values))

else:
    st.warning("No measurements available for this selection.")

st.divider()

# Raw data
with st.expander("View Raw Research Data"):
    display_columns = [
        "Sample Name",
        "Participant",
        "Timepoint",
        selected_metric
    ]

    if has_reference:
        display_columns.extend([
            min_column,
            max_column
        ])

    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "Historical NASA Inspiration4 research data. "
    "Measurements are not live astronaut monitoring."
)