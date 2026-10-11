"""Topology-aware transpilation metrics."""
from __future__ import annotations
from qiskit import transpile
from qiskit.transpiler import CouplingMap

def compile_for_processor(circuit, processor, optimization_level=1, seed=42):
    coupling = processor["coupling_map_object"]
    basis = processor.get("basis_gates") or ["rz", "sx", "x", "cx"]
    compiled = transpile(
        circuit,
        basis_gates=basis,
        coupling_map=coupling,
        optimization_level=int(optimization_level),
        seed_transpiler=int(seed),
        initial_layout=list(range(circuit.num_qubits)),
    )
    # All-to-all compilation provides a baseline for a routing-overhead proxy.
    all_to_all_edges = [(i, j) for i in range(circuit.num_qubits) for j in range(circuit.num_qubits) if i != j]
    all_to_all = transpile(
        circuit,
        basis_gates=basis,
        coupling_map=CouplingMap(couplinglist=all_to_all_edges),
        optimization_level=int(optimization_level),
        seed_transpiler=int(seed),
        initial_layout=list(range(circuit.num_qubits)),
    )
    ops = compiled.count_ops()
    base_ops = all_to_all.count_ops()
    twoq = sum(count for name, count in ops.items() if name in {"cx", "cz", "ecr", "rzz", "iswap", "swap"})
    base_twoq = sum(count for name, count in base_ops.items() if name in {"cx", "cz", "ecr", "rzz", "iswap", "swap"})
    swaps = int(ops.get("swap", 0))
    return compiled, {
        "transpiled_depth": int(compiled.depth() or 0),
        "total_gate_count": int(sum(ops.values())),
        "two_qubit_gate_count": int(twoq),
        "transpiled_swap_count": swaps,
        "all_to_all_two_qubit_gate_count": int(base_twoq),
        "routing_overhead_proxy_two_qubit_gates": int(max(0, twoq - base_twoq)),
        "transpiled_ops": {str(k): int(v) for k, v in ops.items()},
        "note": "SWAP count is the explicit 'swap' operation remaining after transpilation; transpilers may decompose routing SWAPs into native gates. Routing overhead proxy is constrained-topology two-qubit gates minus all-to-all baseline.",
    }
