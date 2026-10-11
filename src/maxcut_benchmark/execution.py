"""Local Aer execution. No hardware calls are made by this prototype."""
from qiskit_aer import AerSimulator

def run_local_simulator(measured_circuit, shots=1024, seed=42):
    simulator = AerSimulator()
    result = simulator.run(measured_circuit, shots=int(shots), seed_simulator=int(seed)).result()
    return result.get_counts()
