from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Return a quantum circuit on 3 qubits and 3 classical bits
# 1. Create a GHZ state \ket{000}+\ket{111} starting from \ket{000}
# 2. Apply X gate on the 0th qubit to get \ket{100}+\ket{011}
# 3. Measure everything
# Note: the result will be either "100" or "011" due to Qiskit's bit order
def ghz_x_meas():
	qc = QuantumCircuit(3, 3)
	qc.h(0)
	qc.cx(0, 1)
	qc.cx(0, 2)
	qc.x(0)
	qc.measure([0, 1, 2], [0, 1, 2])
	return qc


# Return a quantum circuit on 1 qubit
# Apply an X gate if input x is True
# Similarly for Z gate
def superdense_alice(x, z):
	qc = QuantumCircuit(1)
	if x:
		qc.x(0)
	if z:
		qc.z(0)
	return qc

# Return a quantum circuit on 2 qubits and 2 classical bits
def superdense_bob():
	qc = QuantumCircuit(2, 2)
	qc.cx(0, 1)
	qc.h(0)
	qc.measure([0, 1], [0, 1])
	return qc

# Return Alice's quantum circuit
# qreg: register of 2 qubits
# creg: register of 2 bits
def teleport_alice(qreg: QuantumRegister, creg: ClassicalRegister):
	assert len(qreg) == 2
	assert len(creg) == 2

	qc = QuantumCircuit(qreg, creg)
	qc.cx(qreg[0], qreg[1])
	qc.h(qreg[0])
	qc.measure(qreg[0], creg[0])
	qc.measure(qreg[1], creg[1])
	return qc

# Return Charlie's quantum circuit
# qreg: register of 2 qubits
# creg: register of 2 bits
# Assume the 0th qubit is above the 1st qubit.
# Match the indices when measuring. (That is, qreg[0] goes into creg[0].)
def swap_charlie(qreg: QuantumRegister, creg: ClassicalRegister):
	assert len(qreg) == 2
	assert len(creg) == 2

	qc = QuantumCircuit(qreg, creg)
	qc.cx(qreg[0], qreg[1])
	qc.h(qreg[0])
	qc.measure(qreg[0], creg[0])
	qc.measure(qreg[1], creg[1])
	return qc

# Return Alice's quantum circuit
# qreg: register of 1 qubit
# creg: register of 2 bits
def swap_alice(qreg: QuantumRegister, creg: ClassicalRegister):
	assert len(qreg) == 1
	assert len(creg) == 2

	qc = QuantumCircuit(qreg, creg)

	with qc.if_test((creg[0], 1)):
		qc.z(qreg[0])

	with qc.if_test((creg[1], 1)):
		qc.x(qreg[0])

	return qc


# Output a classical syndrome string based on the error Pauli
# Pauli: One of "X", "XZ", or "Z".
# Wire: A number between 1 and 5.
# Example mappings:
# error_to_syndrome("X", 1) -> "00011"
# error_to_syndrome("X", 3) -> "11000"
# error_to_syndrome("XZ", 3) -> "11101"
def error_to_syndrome(pauli, wire):
	stabilizers = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ", "ZZXIX"]

	assert pauli in ["X", "XZ", "Z"]
	assert 1 <= wire <= 5

	idx = wire - 1
	syndrome = ""

	for stabilizer in stabilizers:
		s = stabilizer[idx]
		anticommutes = 0

		if "X" in pauli and s == "Z":
			anticommutes ^= 1

		if "Z" in pauli and s == "X":
			anticommutes ^= 1

		syndrome += str(anticommutes)

	return syndrome

# Output a quantum circuit that measures with respect to a Pauli operator
# data: register of 5 qubits
# ancilla: register of 1 qubit
# creg: classical register of 1 bit
# synd: A string representing a 5-qubit Pauli operator; e.g. "XZZXI".
# You can assume there will be no "Y" operator in any qubit.
def measure_one_syndrome(data, ancilla, creg, synd):
	assert len(data) == 5
	assert len(ancilla) == 1
	assert len(creg) == 1
	assert len(synd) == 5

	qc = QuantumCircuit(data, ancilla, creg)

	for i, p in enumerate(synd):
		if p == "X":
			qc.h(data[i])
			qc.cx(data[i], ancilla[0])
			qc.h(data[i])
		elif p == "Z":
			qc.cx(data[i], ancilla[0])
		else:
			assert p == "I"

	qc.measure(ancilla[0], creg[0])
	return qc
