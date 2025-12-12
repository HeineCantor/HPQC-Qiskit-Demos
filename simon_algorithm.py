from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

import matplotlib.pyplot as plt

import numpy as np
import random

PROBLEM_SIZE = 2
SHOTS = PROBLEM_SIZE * 10

quantumCircuit = QuantumCircuit(2 * PROBLEM_SIZE, PROBLEM_SIZE)

quantumCircuit.h(range(PROBLEM_SIZE))
quantumCircuit.barrier()

# f(00) = 00, f(01) = 00, f(10) = 11, f(11) = 11 => s = 01
# quantumCircuit.cx(0, PROBLEM_SIZE)
# quantumCircuit.cx(1, PROBLEM_SIZE + 1)

# f(00) = 01, f(01) = 11, f(10) = 01, f(11) = 11 => s = 10
# quantumCircuit.cx(1, PROBLEM_SIZE)
# quantumCircuit.x(PROBLEM_SIZE+1)

# f(00) = 10, f(01) = 01, f(10) = 01, f(11) = 10 => s = 11
# quantumCircuit.x(PROBLEM_SIZE)
# quantumCircuit.cx(0, PROBLEM_SIZE)
# quantumCircuit.cx(0, PROBLEM_SIZE + 1)
# quantumCircuit.cx(1, PROBLEM_SIZE)
# quantumCircuit.cx(1, PROBLEM_SIZE + 1)

# f(00) = 11, f(01) = 10, f(10) = 01, f(11) = 00 => s = 00
# quantumCircuit.cx(0, PROBLEM_SIZE)
# quantumCircuit.cx(1, PROBLEM_SIZE + 1)

quantumCircuit.barrier()

quantumCircuit.h(range(PROBLEM_SIZE))
quantumCircuit.measure(range(PROBLEM_SIZE), range(PROBLEM_SIZE))

quantumCircuit.draw("mpl")
plt.show()

simulator = AerSimulator()
compiled_circuit = transpile(quantumCircuit, simulator)

result = simulator.run(compiled_circuit, shots=SHOTS).result()
counts = result.get_counts()
print("Measurement results:", counts)
print("Note: The measurement results should satisfy s · y = 0 (mod 2) for the secret string s.")