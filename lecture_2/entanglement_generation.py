from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

import matplotlib.pyplot as plt

MPL_DRAW = True
SHOTS = 10000

quantumCircuit = QuantumCircuit(2)

quantumCircuit.h(0)
quantumCircuit.cx(0, 1)
quantumCircuit.measure_all()

if MPL_DRAW:
    quantumCircuit.draw("mpl")
    plt.show()
else:
    print(quantumCircuit.draw())

simulator = AerSimulator(method="statevector")
quantumCircuit_transpiled = transpile(quantumCircuit, simulator)

result = simulator.run(quantumCircuit_transpiled, shots=SHOTS).result()

counts = result.get_counts(quantumCircuit)
print("Risultati della misura:", counts)

