# Quantum Noise Analytics Pipeline

An end-to-end data engineering and analysis pipeline designed to track, store, and query environmental noise metrics from quantum hardware. 

As a **Physics Major**, I built this project to simulate how real-world environmental interference impacts quantum computing systems. The pipeline tracks qubit degradation metrics over time, logs snapshots to a structured database, and uses data analytics techniques to identify unstable hardware components.

---

## The Physics Context

Quantum computers are highly sensitive to their environments. Thermal fluctuations, cosmic rays, and magnetic fields cause **quantum decoherence**, introducing severe errors into quantum calculations. This pipeline monitors two core hardware metrics:
*   **$T_1$ Relaxation Time (Microseconds):** The lifespan of a qubit. It measures how long a qubit can remain in the high-energy state $|1\rangle$ before decaying back down to the ground state $|0\rangle$.
*   **$T_2$ Decoherence Time (Microseconds):** The phase memory of a qubit. It measures how long a qubit can maintain its quantum superposition phase before losing its quantum properties entirely.

---

## Architecture & Tech Stack

This project is built using professional software engineering and data analysis standards:
*   **Language:** Python 3.14
*   **Quantum SDK:** Qiskit (Accessing simulated IBM Quantum system configurations)
*   **Package Management:** `uv` & isolated virtual environments (`venv`)
*   **Data Manipulation:** Pandas (Structuring nested JSON hardware configurations into dataframes)
*   **Storage Layer:** SQLite (A local relational SQL database tracking historical hardware snapshots)
*   **Query Engine:** Raw SQL (Filtering and isolating faulty hardware components)
*   **Version Control:** Git & GitHub

---

## How It Works

1. **Extraction (`fetch_noise.py`):** Connects to the hardware target, fetches nested device properties, and calculates $T_1$ and $T_2$ times in microseconds.
2. **Database Logging:** Appends a precise, localized `timestamp` to the reading and saves it directly to a local SQL database table named `qubit_metrics`.
3. **Targeted Analytics (`query_data.py`):** Runs pure SQL queries to instantly filter out and isolate qubits currently experiencing a dangerous drop in phase stability ($T_2 < 50 \mu s$).