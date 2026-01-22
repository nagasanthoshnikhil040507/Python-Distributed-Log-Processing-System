import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(
    page_title="🔥 Distributed Log Analytics",
    page_icon="🚀",
    layout="wide"
)





# ---------------------------
# Background & Fonts
# ---------------------------
st.markdown("""
<style>

/* App background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2f3, #d9e4f5);
    font-family: 'Segoe UI', sans-serif;
}

/* Header glass card */
.header-card {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    text-align: center;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}

.kpi-card:hover {
    transform: scale(1.05);
}

/* KPI title */
.kpi-title {
    font-size: 1rem;
    opacity: 0.85;
}

/* KPI value */
.kpi-value {
    font-size: 2.2rem;
    font-weight: bold;
}

/* Section headers */
.section-title {
    font-size: 1.8rem;
    margin-top: 40px;
    margin-bottom: 15px;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1f2933, #111827);
    color: white;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 14px;
    margin-top: 50px;
    color: #333;
}

</style>
""", unsafe_allow_html=True)







# ---------------------------
# Dashboard Title
# ---------------------------
st.markdown("""
<div class="header-card">
    <h1>🚀 Distributed Log Analytics Dashboard</h1>
    <p>Visualize logs, monitor system health, and explore trends interactively</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------
# Centered File Uploader
# ---------------------------
uploaded_file = st.file_uploader(
    "📥 Upload your CSV log file",
    type="csv"
)


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=0)
    df.columns = [c.strip() for c in df.columns]
else:
    st.warning("Please upload a CSV file to display the dashboard.")
    st.stop()

# ---------------------------
# Preprocess dataframe
# ---------------------------
df["LogLevel"] = (
    df["LogLevel"].astype(str).str.strip().str.upper()
    if "LogLevel" in df.columns else "UNKNOWN"
)

df["Service"] = (
    df["Service"].astype(str).str.strip().str.upper()
    if "Service" in df.columns else "UNKNOWN"
)

df["TimeTaken"] = (
    pd.to_numeric(df["TimeTaken"], errors="coerce")
    if "TimeTaken" in df.columns else 0
)

df["Timestamp"] = (
    pd.to_datetime(df["Timestamp"], errors="coerce")
    if "Timestamp" in df.columns else pd.NaT
)

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("⚡ Filters")

log_levels = df["LogLevel"].dropna().unique().tolist()
selected_levels = st.sidebar.multiselect(
    "Select Log Levels:", log_levels, default=log_levels
)

services = df["Service"].dropna().unique().tolist()
selected_services = st.sidebar.multiselect(
    "Select Services:", services, default=services
)

# Date range filter
if df["Timestamp"].notna().any():
    min_date = df["Timestamp"].min()
    max_date = df["Timestamp"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    df_filtered = df[
        (df["Timestamp"] >= pd.to_datetime(date_range[0])) &
        (df["Timestamp"] <= pd.to_datetime(date_range[1]))
    ]
else:
    df_filtered = df.copy()

filtered_df = df_filtered[
    (df_filtered["LogLevel"].isin(selected_levels)) &
    (df_filtered["Service"].isin(selected_services))
]

if filtered_df.empty:
    st.warning("No rows match selected filters. Showing all data.")
    filtered_df = df.copy()

# ---------------------------
# Key Metrics Cards
# ---------------------------
st.subheader("📊 Key Metrics")

total_logs = len(filtered_df)
total_errors = len(filtered_df[filtered_df["LogLevel"] == "ERROR"])
error_rate = round((total_errors / total_logs) * 100, 2) if total_logs > 0 else 0

st.markdown('<div class="section-title">📊 Key Metrics</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Logs</div>
        <div class="kpi-value">{total_logs}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card" style="background:linear-gradient(135deg,#ff512f,#dd2476)">
        <div class="kpi-title">ERROR Logs</div>
        <div class="kpi-value">{total_errors}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card" style="background:linear-gradient(135deg,#11998e,#38ef7d)">
        <div class="kpi-title">Error Rate</div>
        <div class="kpi-value">{error_rate}%</div>
    </div>
    """, unsafe_allow_html=True)


ERROR_THRESHOLD = 1000
if total_errors > ERROR_THRESHOLD:
    st.warning(f"⚠️ ALERT: High number of ERROR logs ({total_errors})")
else:
    st.success("✅ System stable. ERROR logs normal.")

# ---------------------------
# Log Counts by Level
# ---------------------------
st.markdown('<div class="section-title">📈 Log Counts by Level</div>', unsafe_allow_html=True)

loglevel_counts = filtered_df.groupby("LogLevel").size().reset_index(name="count")

if not loglevel_counts.empty:
    fig_bar = px.bar(
        loglevel_counts,
        x="LogLevel",
        y="count",
        color="LogLevel",
        text="count",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("No data for selected Log Levels.")

# ---------------------------
# Logs by Service
# ---------------------------
st.subheader("🎯 Logs by Service")

service_counts = filtered_df.groupby("Service").size().reset_index(name="count")

if not service_counts.empty:
    fig_pie = px.pie(
        service_counts,
        names="Service",
        values="count",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("No service data available.")

# ---------------------------
# Log Trend Over Time
# ---------------------------
if filtered_df["Timestamp"].notna().any():
    st.subheader("📆 Log Trend Over Time")

    trend_df = (
        filtered_df
        .groupby(pd.Grouper(key="Timestamp", freq="D"))
        .size()
        .reset_index(name="count")
    )

    fig_line = px.line(
        trend_df,
        x="Timestamp",
        y="count",
        markers=True,
        labels={"count": "Log Count", "Timestamp": "Date"},
        title="Logs Over Time"
    )

    fig_line.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("Trend chart unavailable.")

# ---------------------------
# Detailed logs table
# ---------------------------
st.subheader("📋 Detailed Logs")

if not filtered_df.empty:
    st.dataframe(
        filtered_df.sort_values(by="Timestamp", ascending=False),
        height=400
    )
else:
    st.info("No logs to display.")

# ---------------------------
# Footer
# ---------------------------
st.markdown(
    """
    <div class="footer">
        © 2026 Distributed Log Processing System 🚀
    </div>
    """,
    unsafe_allow_html=True
)
