"""Metrics computed from observed measurement counts."""
from __future__ import annotations
from .objective import cut_value

def metrics_from_counts(graph, counts, optimum=None):
    shots = sum(int(c) for c in counts.values())
    if shots <= 0:
        raise ValueError("Counts contain no shots.")
    weighted_sum = 0.0
    best_value = -1.0
    best_bits = None
    optimal_count = 0
    for qiskit_bits, count in counts.items():
        # Qiskit count strings display classical bit c[n-1] on the left.
        bits = qiskit_bits.replace(" ", "")[::-1]
        value = cut_value(graph, bits)
        weighted_sum += value * int(count)
        if value > best_value:
            best_value, best_bits = value, bits
        if optimum is not None and abs(value - optimum) < 1e-9:
            optimal_count += int(count)
    expected = weighted_sum / shots
    return {
        "shots": int(shots),
        "best_observed_cut": float(best_value),
        "best_bitstring_vertex0_first": best_bits,
        "expected_cut": float(expected),
        "optimal_success_probability": (optimal_count / shots) if optimum is not None else None,
        "approximation_ratio": (expected / optimum) if optimum is not None and optimum > 0 else None,
    }
