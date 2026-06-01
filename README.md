# Quantum Hardware Telemetry and Noise Analytics Platform

An end-to-end data engineering and interactive visualization platform designed to track, log, and query live environmental noise metrics from quantum hardware.

As a Physics Major, I built this project to bridge the gap between quantum mechanics and modern data engineering. The platform acts as a real-time control room monitor, tracking physical qubit degradation metrics over time, logging automated snapshots to a structured time-series database, and serving an analytical dashboard for hardware health visualization.

---

## Technical and Physical Context

Quantum processors are highly sensitive to environmental interference. Thermal fluctuations, cosmic rays, and electromagnetic waves cause quantum decoherence, introducing calculation errors. This platform monitors two critical hardware physics metrics:
*   **T1 Relaxation Time (Microseconds):** The energy lifespan of a qubit. It measures how long a qubit remains in the high-energy state |1> before decaying back to the ground state |0>.
*   **T2 Decoherence Time (Microseconds):** The phase memory of a qubit. It measures how long a qubit can maintain its quantum superposition phase before losing its quantum properties entirely.

---

## Architecture and Tech Stack

This project is engineered using modern data pipelines and enterprise development tools:
*   **Language:** Python 3.14
*   **Quantum SDK:** Qiskit (Accessing physical device telemetry metadata targets)
*   **Package Management:** uv by Astral (Fast package resolution using isolated virtual environments)
*   **Data Orchestration:** Pandas (Parsing nested telemetry schemas into structured dataframes)
*   **Storage Tier:** SQLite (Time-series data logging using sequential relational tables)
*   **Visualization Engine:** Streamlit and Plotly Express (High-fidelity custom dark-mode interface)
*   **Version Control:** Git and GitHub

---

## Platform Component Breakdown

1. **Automated Telemetry Loop (stream_data.py):** An automated background service that polls the hardware API metrics at scheduled intervals, captures physical environmental noise drifts, and appends live data points into the local database without human intervention.
2. **Relational Database (quantum_noise.db):** An isolated SQLite datastore utilizing an APPEND structural model to construct a clean historical timeline of hardware states, complete with precise data timestamps.
3. **Analytical Filter (query_data.py):** Runs raw SQL queries directly against the data tables to filter and isolate specific hardware components showing unstable phase margins (T2 < 50 us).