from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

import matplotlib.pyplot as plt

MPL_DRAW = True
SHOTS = 10000

# Quantum Circuit initialization
#   - QuantumCircuit(qubit_register_size, bit_register_size)

quantumCircuit = QuantumCircuit(1)

# Quantum operations + final measurement

quantumCircuit.h(0)
quantumCircuit.measure_all()

if MPL_DRAW:
    quantumCircuit.draw("mpl")
    plt.show()
else:
    print(quantumCircuit.draw())

# Simulator: state vector simulation grows as 2^n, with n=#qubits
#   Simulation is the core of quantum algorithm testing since
#   real hardware is kinda noisy.

simulator = AerSimulator(method="statevector")
quantumCircuit_transpiled = transpile(quantumCircuit, simulator)

# Multiple shots of execution
result = simulator.run(quantumCircuit_transpiled, shots=SHOTS).result()

# Results display
counts = result.get_counts(quantumCircuit)
print("Risultati della misura:", counts)

