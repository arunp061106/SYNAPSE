import streamlit as st
import pandas as pd
import plotly.express as px

from src.config.experiment_config import ExperimentConfig
from scripts.run_world_simulation import run_simulation

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="SYNAPSE",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
    }
    .metric-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #1c1f26;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- STATE ----------------
if "results" not in st.session_state:
    st.session_state.results = None

# ---------------- TITLE ----------------
st.title("🚀 SYNAPSE") 
st.caption("Synthetic Data Intelligence Platform")
st.caption("Done by Arun karthick P : ) SRMIST")
# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Configuration")

domain = st.sidebar.selectbox("Domain", ["ecommerce", "iot", "fintech"])

dataset_size = st.sidebar.number_input(
    "Dataset Size", 1000, 50000, 1000, step=1000
)

ratio = st.sidebar.slider("Synthetic Ratio", 0.5, 3.0, 1.0)

run_btn = st.sidebar.button("▶ Run Simulation")

# ---------------- RUN ----------------
if run_btn:
    with st.spinner("Running pipeline..."):
        exp = ExperimentConfig(
            dataset_size=int(dataset_size),
            synthetic_ratio=float(ratio),
            domain=domain
        )

        st.session_state.results = run_simulation(exp)

# ---------------- RESULTS ----------------
results = st.session_state.results

if results is None:
    st.warning("Run simulation to generate dataset")
    st.stop()

# ---------------- KPI COLORS ----------------
def score_color(score):
    if score >= 0.85:
        return "🟢"
    elif score >= 0.7:
        return "🟡"
    else:
        return "🔴"

# ---------------- KPI ----------------
st.subheader("📊 Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Distribution", f"{results['distribution']} {score_color(results['distribution'])}")
c2.metric("Correlation", f"{results['correlation']} {score_color(results['correlation'])}")
c3.metric("ML Utility", f"{results['ml_utility']} {score_color(results['ml_utility'])}")
c4.metric("Trust Score", f"{results['trust_score']} {score_color(results['trust_score'])}")

# ---------------- DATA ----------------
df = results.get("synthetic_full")

if df is None or df.empty:
    st.error("Dataset missing")
    st.stop()

st.subheader("📄 Preview")
st.dataframe(results["synthetic_head"], use_container_width=True)

# ---------------- DOWNLOAD ----------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Dataset",
    csv,
    f"{domain}_synthetic_data.csv",
    "text/csv"
)

# ---------------- VISUALS ----------------
st.subheader("📊 Insights")

df_sample = df.sample(min(len(df), 2000))
numeric_cols = df_sample.select_dtypes(include="number").columns

colA, colB = st.columns(2)

# -------- HISTOGRAM --------
with colA:
    st.write("### Distribution")

    if len(numeric_cols) > 0:
        feature = st.selectbox("Feature", numeric_cols)

        fig = px.histogram(
            df_sample,
            x=feature,
            nbins=30,
            title=f"{feature} Distribution"
        )

        fig.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=10, r=10, t=40, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No numeric columns")

# -------- CORRELATION --------
with colB:
    st.write("### Correlation")

    if len(numeric_cols) > 1:
        corr = df_sample[numeric_cols].corr()

        fig2 = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix"
        )

        fig2.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=10, r=10, t=40, b=10)
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("Not enough columns")

# -------- TARGET --------
st.write("### Target Distribution")

target = next(
    (c for c in ["fraud", "is_purchase", "anomaly"] if c in df.columns),
    None
)

if target:
    target_counts = df[target].value_counts().reset_index()
    target_counts.columns = [target, "count"]

    fig3 = px.bar(
        target_counts,
        x=target,
        y="count",
        title="Target Balance"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=300
    )

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("No target column found")