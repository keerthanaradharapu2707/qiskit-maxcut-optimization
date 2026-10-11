"""Convenience wrapper; use scripts/run_benchmark.py for a paired A/B run."""
from pathlib import Path
from maxcut_benchmark.graph_builder import parse_edge_list
from maxcut_benchmark.benchmark import run_one, save_result
ROOT = Path(__file__).resolve().parents[1]
if __name__ == "__main__":
    graph = parse_edge_list("0-1,1-2,2-3,3-0,0-2")
    result = run_one(graph, ROOT / "configs" / "processor_B.json")
    print(save_result(result, ROOT / "results" / "raw"))
