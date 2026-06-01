import streamlit as pd
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Set up the webpage layout
st.set_page_config(page_title="Quantum Noise Monitor", layout="wide")

st.title("Live Quantum Hardware Noise Analytics Platform")
st.markdown("This dashboard queries a local SQLite database tracking historical quantum hardware coherence metrics.")

# 1. CONNECT TO DATABASE & FETCH DATA
conn = sqlite3.connect("quantum_noise.db")
# Fetch all records sorted by time
df = pd.read_sql_query("SELECT * FROM qubit_metrics ORDER BY timestamp ASC", conn)
conn.close()

# 2. RENDER THE METRIC CARDS (Latest Snapshot)
latest_timestamp = df["timestamp"].max()
latest_data = df[df["timestamp"] == latest_timestamp]

st.subheader(f"Latest Hardware Snapshot: {latest_timestamp}")

# Create 5 columns across the screen for the 5 qubits
cols = st.columns(5)
for index, row in latest_data.iterrows():
    q_id = int(row["qubit_id"])
    t2_val = row["t2_decoherence_us"]
    
    # Simple alert threshold logic
    if t2_val < 50.0:
        status = "UNSTABLE"
    else:
        status = "STABLE"
        
    cols[q_id].metric(
        label=f"Qubit {q_id} Status", 
        value=f"{t2_val} μs", 
        delta=status, 
        delta_color="normal" if t2_val >= 50.0 else "inverse"
    )

st.markdown("---")

# 3. RENDER THE TIME-SERIES GRAPH
st.subheader("Qubit Coherence Degradation Over Time ($T_2$ Phase Memory)")

# Create an interactive line chart using Plotly
fig = px.line(
    df, 
    x="timestamp", 
    y="t2_decoherence_us", 
    color="qubit_id",
    markers=True,
    labels={"timestamp": "Reading Timestamp", "t2_decoherence_us": "T2 Decoherence Time (μs)", "qubit_id": "Qubit ID"},
    title="Historical Phase Stability Timeline"
)

# Style the chart cleanly
fig.update_layout(template="plotly_dark", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)