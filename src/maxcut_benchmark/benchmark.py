"""Run one controlled synthetic Processor A/B benchmark."""
from __future__ import annotations
from pathlib import Path
import json, time
from .qaoa_solver import optimize_qaoa
from .processor_models import load_processor
from .transpilation import compile_for_processor
from .execution import run_local_simulator
from .metrics import metrics_from_counts
from .objective import exact_maxcut

def run_one(graph, processor_path, p=1, shots=1024, maxiter=80, seed=42, optimization_level=1, exact_max_vertices=20):
    processor = load_processor(processor_path)
    if graph.number_of_nodes() > int(processor["num_qubits"]):
        raise ValueError(f"Graph uses {graph.number_of_nodes()} qubits, but {processor['label']} defines {processor['num_qubits']}.")
    t0 = time.perf_counter()
    optimized = optimize_qaoa(graph, p=p, maxiter=maxiter, seed=seed)
    optimization_seconds = time.perf_counter() - t0
    logical = optimized["circuit"]
    t1 = time.perf_counter()
    compiled, circuit_metrics = compile_for_processor(logical, processor, optimization_level, seed)
    transpile_seconds = time.perf_counter() - t1
    t2 = time.perf_counter()
    counts = run_local_simulator(compiled, shots=shots, seed=seed)
    execution_seconds = time.perf_counter() - t2
    optimum = None
    if graph.number_of_nodes() <= exact_max_vertices:
        optimum, optimum_bits = exact_maxcut(graph, max_vertices=exact_max_vertices)
    else:
        optimum_bits = None
    measured_metrics = metrics_from_counts(graph, counts, optimum)
    return {
        "processor_id": processor["processor_id"],
        "processor_label": processor["label"],
        "processor_is_official": bool(processor.get("is_official", False)),
        "data_status": "SYNTHETIC TOPOLOGY + LOCAL SIMULATOR; NOT OFFICIAL HARDWARE DATA",
        "processor_source": processor.get("source", "Not specified"),
        "execution_mode": "local_aer_simulator",
        "num_qubits_in_graph": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "qaoa_depth_p": int(p),
        "logical_depth": int(logical.depth() or 0),
        "logical_gate_count": int(sum(logical.count_ops().values())),
        "optimization_seconds": float(optimization_seconds),
        "transpilation_seconds": float(transpile_seconds),
        "execution_seconds": float(execution_seconds),
        "optimizer_success": optimized["optimizer_success"],
        "optimizer_message": optimized["optimizer_message"],
        "optimizer_evaluations": optimized["optimizer_evaluations"],
        "optimized_expected_cut_statevector": optimized["optimized_expected_cut"],
        "classical_optimum": optimum,
        "classical_optimum_bitstring": optimum_bits,
        "circuit_metrics": circuit_metrics,
        "solution_metrics": measured_metrics,
        "raw_counts": {str(k): int(v) for k, v in counts.items()},
        "settings": {"p": int(p), "shots": int(shots), "maxiter": int(maxiter), "seed": int(seed), "optimization_level": int(optimization_level)},
    }

def save_result(result, output_dir="results/raw"):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{result['processor_id'].lower()}_result.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return path
