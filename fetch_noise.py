import pandas as pd
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

print("Connecting to fake quantum computer backend...")
# Initialize a mock 5-qubit quantum computer backend (IBM Manila)
backend = FakeManilaV2()
properties = backend.target

# Create an empty list to store our rows of data
quantum_data = []

# Loop through all 5 qubits (numbered 0 to 4) to extract noise metrics
for i in range(5):
    qubit_props = properties.qubit_properties[i]
    
    # Convert raw times (seconds) to microseconds (us) for standard industry readability
    # T1 (Relaxation Time): How long a qubit stays in the |1> state before decaying to |0>
    # T2 (Decoherence Time): How long a qubit maintains its quantum superposition phase
    t1_microseconds = qubit_props.t1 * 1e6
    t2_microseconds = qubit_props.t2 * 1e6
    
    # Structure the hardware data into a clean key-value dictionary
    qubit_dict = {
        "qubit_id": i,
        "t1_relaxation_us": round(t1_microseconds, 2),
        "t2_decoherence_us": round(t2_microseconds, 2)
    }
    
    # Append the dictionary to our main data list
    quantum_data.append(qubit_dict)

# Convert the list of dictionaries into a structured Pandas DataFrame
df = pd.DataFrame(quantum_data)

print("\n--- Cleaned Quantum Hardware Data ---")
print(df)