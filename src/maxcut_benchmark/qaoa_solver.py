"""Small, transparent QAOA Max-Cut implementation using Qiskit and SciPy."""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from .objective import cut_value

def build_qaoa_circuit(graph, gammas, betas, measure=False):
    n = graph.number_of_nodes()
    if len(gammas) != len(betas):
        raise ValueError("gammas and betas must have the same length.")
    qc = QuantumCircuit(n, n if measure else 0)
    qc.h(range(n))
    for gamma, beta in zip(gammas, betas):
        # exp(-i gamma C), where C = sum_edges (1 - Z_u Z_v)/2.
        # Global phase is irrelevant, so RZZ(-gamma) implements the required ZZ phase.
        for u, v, data in graph.edges(data=True):
            weight = float(data.get("weight", 1.0))
            qc.rzz(-gamma * weight, int(u), int(v))
        for qubit in range(n):
            qc.rx(2.0 * beta, qubit)
    if measure:
        qc.measure(range(n), range(n))
    return qc

def _expected_cut_statevector(graph, gammas, betas):
    qc = build_qaoa_circuit(graph, gammas, betas, measure=False)
    probs = Statevector.from_instruction(qc).probabilities()
    expected = 0.0
    n = graph.number_of_nodes()
    for index, probability in enumerate(probs):
        # Statevector index uses qubit 0 as the least-significant bit.
        bits = format(index, f"0{n}b")[::-1]
        expected += float(probability) * cut_value(graph, bits)
    return expected

def optimize_qaoa(graph, p=1, maxiter=80, seed=42):
    if p < 1:
        raise ValueError("QAOA depth p must be >= 1.")
    rng = np.random.default_rng(seed)
    initial = np.concatenate([rng.uniform(0, np.pi, p), rng.uniform(0, np.pi/2, p)])
    def objective(params):
        gammas, betas = params[:p], params[p:]
        return -_expected_cut_statevector(graph, gammas, betas)
    result = minimize(objective, initial, method="COBYLA", options={"maxiter": int(maxiter), "rhobeg": 0.5})
    gammas, betas = result.x[:p], result.x[p:]
    return {
        "gammas": gammas.tolist(),
        "betas": betas.tolist(),
        "optimizer_success": bool(result.success),
        "optimizer_message": str(result.message),
        "optimizer_evaluations": int(getattr(result, "nfev", 0)),
        "optimized_expected_cut": float(-result.fun),
        "circuit": build_qaoa_circuit(graph, gammas, betas, measure=True),
    }
