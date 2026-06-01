import pandas as pd
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
import sqlite3
from datetime import datetime

print("Connecting to fake quantum computer backend...")
backend = FakeManilaV2()
properties = backend.target

# Capture the exact date and time of this reading
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

quantum_data = []

for i in range(5):
    qubit_props = properties.qubit_properties[i]
    
    t1_microseconds = qubit_props.t1 * 1e6
    t2_microseconds = qubit_props.t2 * 1e6
    
    qubit_dict = {
        "timestamp": current_time, 
        "qubit_id": i,
        "t1_relaxation_us": round(t1_microseconds, 2),
        "t2_decoherence_us": round(t2_microseconds, 2)
    }
    quantum_data.append(qubit_dict)

df = pd.DataFrame(quantum_data)

print("Connecting to local SQLite database...")
conn = sqlite3.connect("quantum_noise.db")

# Save to the 'qubit_metrics' table
df.to_sql("qubit_metrics", conn, if_exists="append", index=False)
conn.close()

print("Success! Data successfully saved to local SQL database (quantum_noise.db).")