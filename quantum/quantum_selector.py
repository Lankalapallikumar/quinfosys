from qiskit import transpile
from qiskit_aer import Aer
from .quantum_circuit import create_circuit
from .error_mitigation import mitigate_noise

def run_quantum(n_qubits=3):
    qc = create_circuit(n_qubits)

    simulator = Aer.get_backend('aer_simulator')
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=4096).result()

    counts = result.get_counts()

    return mitigate_noise(counts)