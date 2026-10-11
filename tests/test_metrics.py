from maxcut_benchmark.graph_builder import parse_edge_list
from maxcut_benchmark.metrics import metrics_from_counts

def test_metrics():
    g = parse_edge_list("0-1")
    # Qiskit count strings are displayed with qubit 0 on the right.
    result = metrics_from_counts(g, {"01": 7, "00": 3}, optimum=1)
    assert result["shots"] == 10
    assert result["expected_cut"] == 0.7
    assert result["approximation_ratio"] == 0.7
