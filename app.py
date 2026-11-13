import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from modules.ai_engine import run_tool


# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="AstroNex | Inspiration4",
    page_icon="🚀",
    layout="wide"
)

DATA_PATH = Path(
    "data/processed/NASA_Inspiration4/inspiration4_merged.csv"
)

TIME_ORDER = [
    "L-92", "L-44", "L-3",
    "R+1", "R+45", "R+82", "R+194"
]

# ---------------- STYLE ----------------

st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #e5e7eb;
}
[data-testid="stSidebar"] {
    background-color: #111827;
}
.metric-card {
    background: #172238;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #293750;
}
h1, h2, h3 {
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------

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


if not DATA_PATH.exists():
    st.error(f"Data file not found: {DATA_PATH}")
    st.stop()

df = load_data()

# ---------------- HEADER ----------------

st.title("🚀 AstroNex")
st.caption(
    "NASA Inspiration4 | Biomedical Research Dashboard"
)

st.divider()

# ---------------- SIDEBAR ----------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose Section",
    ["Overview", "Biomarker Explorer", "Raw Data", "AI Assistant"]
)

st.sidebar.divider()
st.sidebar.caption("MISSION: INSPIRATION4")
st.sidebar.caption("DATA SOURCE: NASA OSDR")

# ---------------- OVERVIEW ----------------

if page == "Overview":

    st.subheader("Mission Data Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Participants", df["Participant"].nunique())

    with c2:
        st.metric("Samples", len(df))

    with c3:
        st.metric(
            "Biomarker Variables",
            len([
                col for col in df.columns
                if "value" in col
            ])
        )

    st.divider()

    st.subheader("Participants")

    participant_counts = (
        df.groupby("Participant", observed=True)
        .size()
        .reset_index(name="Samples")
    )

    st.dataframe(
        participant_counts,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "L = Before launch | R = After return. "
        "These are scheduled sampling timepoints, "
        "not continuous in-flight measurements."
    )

    st.subheader("Available Biomarkers")

    biomarkers = [
        col for col in df.columns
        if "value" in col
    ]

    st.write(f"Total available value columns: {len(biomarkers)}")

    st.dataframe(
        pd.DataFrame({"Biomarker columns": biomarkers}),
        use_container_width=True,
        hide_index=True
    )


# ---------------- BIOMARKER EXPLORER ----------------

elif page == "Biomarker Explorer":

    st.subheader("Biomarker Explorer")

    value_columns = [
        col for col in df.columns
        if "value" in col
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    metric_labels = {
        col: col.replace("value", " | ").replace("_", " ").title()
        for col in value_columns
    }

    selected_metric = st.selectbox(
        "Select Biomarker",
        value_columns,
        format_func=lambda x: metric_labels[x],
        index=(
            value_columns.index("hemoglobin_value_percent")
            if "hemoglobin_value_percent" in value_columns
            else 0
        )
    )

    participants = ["All Participants"] + sorted(
        df["Participant"].dropna().unique().tolist()
    )

    selected_participant = st.selectbox(
        "Select Participant",
        participants
    )

    if selected_participant == "All Participants":
        filtered = (
            df.groupby("Timepoint", observed=True)[selected_metric]
            .mean()
            .reset_index()
        )

        filtered["Participant"] = "Group Mean"

        st.caption(
            "Showing the mean across available participants "
            "at each timepoint."
        )

    else:
        filtered = df[
            df["Participant"] == selected_participant
        ][["Timepoint", selected_metric, "Participant"]].copy()

    filtered = filtered.dropna(subset=[selected_metric])
    filtered = filtered.sort_values("Timepoint")

    if filtered.empty:
        st.warning("No available measurements for this selection.")

    else:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=filtered["Timepoint"].astype(str),
            y=filtered[selected_metric],
            mode="lines+markers",
            name=selected_participant,
            line=dict(width=3),
            marker=dict(size=10),
            hovertemplate=(
                "Timepoint: %{x}<br>"
                "Value: %{y:.3f}<extra></extra>"
            )
        ))

        # Reference range columns
        min_col = selected_metric.replace(
            "value", "range_min"
        )
        max_col = selected_metric.replace(
            "value", "range_max"
        )

        # Special column naming in source dataset
        if selected_metric == "alt_value_units_per_liter":
            max_col = "alt_max_units_per_liter"

        elif selected_metric == "ast_value_units_per_liter":
            max_col = "ast_max_units_per_liter"

        if min_col in df.columns and max_col in df.columns:

            if selected_participant == "All Participants":
                reference = (
                    df.groupby("Timepoint", observed=True)
                    .agg({
                        min_col: "mean",
                        max_col: "mean"
                    })
                    .reset_index()
                )
            else:
                reference = df[
                    df["Participant"] == selected_participant
                ].sort_values("Timepoint")

            reference = reference.dropna(
                subset=[min_col, max_col]
            )

            if not reference.empty:
                fig.add_trace(go.Scatter(
                    x=reference["Timepoint"].astype(str),
                    y=reference[max_col],
                    mode="lines",
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo="skip"
                ))

                fig.add_trace(go.Scatter(
                    x=reference["Timepoint"].astype(str),
                    y=reference[min_col],
                    mode="lines",
                    line=dict(width=0),
                    fill="tonexty",
                    fillcolor="rgba(34, 197, 94, 0.12)",
                    name="Reference Range",
                    hovertemplate="Minimum: %{y:.3f}<extra></extra>"
                ))

        fig.update_layout(
            template="plotly_dark",
            title=metric_labels[selected_metric],
            xaxis_title="Mission Timepoint",
            yaxis_title="Measured Value",
            height=500,
            hovermode="x unified",
            legend=dict(orientation="h")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Measurement Statistics")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Mean",
                f"{filtered[selected_metric].mean():.3f}"
            )

        with c2:
            st.metric(
                "Minimum",
                f"{filtered[selected_metric].min():.3f}"
            )

        with c3:
            st.metric(
                "Maximum",
                f"{filtered[selected_metric].max():.3f}"
            )

        st.subheader("Measurements Table")

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )


# ---------------- RAW DATA ----------------

elif page == "Raw Data":

    st.subheader("Raw Dataset Explorer")

    selected_participant = st.selectbox(
        "Filter Participant",
        ["All"] + sorted(
            df["Participant"].dropna().unique().tolist()
        )
    )

    if selected_participant != "All":
        display_df = df[
            df["Participant"] == selected_participant
        ]
    else:
        display_df = df

    st.write(f"Showing {len(display_df)} samples")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    csv = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Filtered Data",
        data=csv,
        file_name="astronex_filtered_data.csv",
        mime="text/csv"
    )
# ---------------- AI ASSISTANT ----------------

elif page == "AI Assistant":

    st.subheader("AstroNex AI Assistant")

    st.caption(
        "AI tools for experimental biomedical data analysis."
    )


    if st.button("Run Stress Analysis", type="primary"):

        stress_file = (
            Path("data/processed/PhysioNet_STRESS/")
            / "f14_b_stress_features.csv"
        )

        result = run_tool(
            "stress_analyzer",
            file_path=stress_file
        )

        # ---------------- FOOTER ----------------

st.divider()

st.caption(
    "AstroNex | Inspiration4 Biomedical Data Analysis | "
    "Research visualization, not medical diagnosis."
)