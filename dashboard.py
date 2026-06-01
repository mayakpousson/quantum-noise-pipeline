import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import time

# Page config for high-end styling
st.set_page_config(
    page_title="Quantum Noise Monitor", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimalist, high-end dashboard header
st.markdown(
    """
    <div style="border-bottom: 2px solid #313244; padding-bottom: 15px; margin-bottom: 25px;">
        <div style="font-family: monospace; font-size: 11px; color: #CBA6F7; font-weight: bold; letter-spacing: 2px;">
            TELEMETRY / HARDWARE STATUS
        </div>
        <h1 style="color: #CDD6F4; margin: 5px 0 0 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 32px; font-weight: 700;">
            Quantum Noise Monitor
        </h1>
        <p style="color: #A6ADC8; margin: 4px 0 0 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px;">
            Automated time-series pipeline tracking live qubit coherence degradation curves.
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# 1. DATABASE EXTRACTION
conn = sqlite3.connect("quantum_noise.db")
df = pd.read_sql_query("SELECT * FROM qubit_metrics ORDER BY timestamp ASC", conn)
conn.close()

# Limit the chart data to the last 30 snapshots so it stays clean and readable
if len(df["timestamp"].unique()) > 30:
    recent_timestamps = sorted(df["timestamp"].unique())[-30:]
    df = df[df["timestamp"].isin(recent_timestamps)]

latest_timestamp = df["timestamp"].max()
latest_data = df[df["timestamp"] == latest_timestamp]

# 2. METRICS SNAPSHOT SECTION
st.markdown(f"<p style='color:#89B4FA; font-weight:bold; margin-bottom:5px;'>⏱️ LATEST HARDWARE STATE: {latest_timestamp}</p>", unsafe_allow_html=True)

# Build metrics card layout inside a styled container
with st.container():
    cols = st.columns(5)
    for index, row in latest_data.iterrows():
        q_id = int(row["qubit_id"])
        t2_val = row["t2_decoherence_us"]
        t1_val = row["t1_relaxation_us"]
        
        is_stable = t2_val >= 50.0
        border_color = "#94E2D5" if is_stable else "#F38BA8"
        status_text = "STABLE" if is_stable else "DEGRADED"
        status_color = "#94E2D5" if is_stable else "#F38BA8"
        
        # Injected custom HTML container layout for ultra-clean look
        cols[q_id].markdown(
            f"""
            <div style="background-color:#181825; padding:15px; border-radius:8px; border-left: 5px solid {border_color}; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                <strong style="color:#CDD6F4; font-size:14px;">QUBIT 0{q_id}</strong>
                <div style="color:{status_color}; font-size:11px; font-weight:bold; letter-spacing:1px; margin-top:2px;">{status_text}</div>
                <div style="font-size:22px; font-weight:bold; color:#CDD6F4; margin:8px 0 2px 0;">{t2_val} <span style="font-size:14px; color:#A6ADC8;">μs</span></div>
                <div style="color:#BAC2DE; font-size:11px;">T₁ Phase: {t1_val} μs</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# 3. HIGH-END CHART CONFIGURATION
with st.container():
    # Crisp, tailored custom dark styling for Plotly
    fig = px.line(
        df, 
        x="timestamp", 
        y="t2_decoherence_us", 
        color="qubit_id",
        markers=True,
        line_shape="linear",
        labels={"timestamp": "Timeline", "t2_decoherence_us": "T₂ Coherence Time (μs)", "qubit_id": "Qubit Target"},
    )
    
    # Professional chart typography and background styling
    fig.update_layout(
        template="plotly_dark", 
        hovermode="x unified",
        paper_bgcolor="#11111B",
        plot_bgcolor="#11111B",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="sans-serif", size=12, color="#CDD6F4"),
        xaxis=dict(showgrid=True, gridcolor="#313244", tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor="#313244", title_font=dict(size=13))
    )
    
    # Smooth line configuration
    fig.update_traces(line=dict(width=2.5), marker=dict(size=6))
    
    # Render component
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# 4. BACKGROUND AUTOMATED REFRESH LOOP (5s)
time.sleep(5)
st.rerun()