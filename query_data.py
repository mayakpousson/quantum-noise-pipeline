import sqlite3
import pandas as pd

# Connect to our quantum database
conn = sqlite3.connect("quantum_noise.db")

# Pure SQL query to filter out qubits with poor phase memory (T2 < 50 microseconds)
sql_query = """
SELECT timestamp, qubit_id, t2_decoherence_us
FROM qubit_metrics
WHERE t2_decoherence_us < 50.0
ORDER BY t2_decoherence_us ASC;
"""

print("Executing SQL query on quantum_noise.db...")
df_results = pd.read_sql_query(sql_query, conn)
conn.close()

print("\n--- SQL Query Results: Unstable Qubits (T2 < 50us) ---")
print(df_results)