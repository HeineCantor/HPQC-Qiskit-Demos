from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

import matplotlib.pyplot as plt
import random

def random_linear_balanced_oracle(n):
    """Creates a random linear balanced oracle for Deutsch-Jozsa algorithm."""
    qc = QuantumCircuit(n + 1)

    b = [random.randint(0, 1) for _ in range(n)]
    while all(x == 0 for x in b):
        b = [random.randint(0, 1) for _ in range(n)]
    
    for i in range(n):
        if b[i] == 1:
            qc.cx(i, n)
    return qc

def random_constant_oracle(n):
    """Creates a random constant oracle for Deutsch-Jozsa algorithm."""
    qc = QuantumCircuit(n + 1)
    if random.randint(0, 1) == 1:
        qc.x(n)  # Flip the ancilla qubit to represent constant 1
    return qc

def non_linear_balanced_oracle(n):
    """Creates a non-linear balanced oracle for Deutsch-Jozsa algorithm.
    Implements f(x) = (x0 AND x1) XOR (NOT x0 AND NOT x1) for n=2,
    which gives: f(00)=1, f(01)=0, f(10)=0, f(11)=1 (balanced).
    For n>2, uses pairs of qubits with AND operations XORed together.
    """
    qc = QuantumCircuit(n + 1)
    
    if n >= 2:
        # First term: NOT x0 AND NOT x1
        qc.x(0)
        qc.x(1)
        qc.ccx(0, 1, n)
        qc.x(0)
        qc.x(1)
        
        # Second term: x0 AND x1 (XOR with previous)
        qc.ccx(0, 1, n)
        
        # For n>2, add more balanced terms
        for i in range(2, n, 2):
            if i + 1 < n:
                # Add (xi AND xi+1) to maintain balance
                qc.ccx(i, i + 1, n)
    
    return qc


SHOTS = 1000

PROBLEM_SIZE = 4

quantumCircuit = QuantumCircuit(PROBLEM_SIZE + 1, PROBLEM_SIZE) # +1 for the ancilla

quantumCircuit.x(PROBLEM_SIZE)
quantumCircuit.barrier()

quantumCircuit.h(range(PROBLEM_SIZE + 1))
quantumCircuit.barrier()

oracle = random_linear_balanced_oracle(PROBLEM_SIZE)
# oracle = random_constant_oracle(PROBLEM_SIZE)
# oracle = non_linear_balanced_oracle(PROBLEM_SIZE)

quantumCircuit = quantumCircuit.compose(oracle)

quantumCircuit.barrier()

quantumCircuit.h(range(PROBLEM_SIZE)) # Hadamard just on the input qubits, not the ancilla
quantumCircuit.measure(range(PROBLEM_SIZE), range(PROBLEM_SIZE))

quantumCircuit.draw("mpl")
plt.show()

simulator = AerSimulator(method="statevector")
quantumCircuit_transpiled = transpile(quantumCircuit, simulator)

result = simulator.run(quantumCircuit_transpiled, shots=SHOTS).result()
counts = result.get_counts(quantumCircuit)
print("Measurement results:", counts)

if all(key == '0' * PROBLEM_SIZE for key in counts):
    print("The function is constant.")
else:
    print("The function is balanced.")


