from __future__ import annotations
import argparse, json
from pathlib import Path
from maxcut_benchmark.graph_builder import parse_edge_list
from maxcut_benchmark.benchmark import run_one, save_result
from maxcut_benchmark.visualization import comparison_dataframe

ROOT = Path(__file__).resolve().parents[1]
def main():
    parser = argparse.ArgumentParser(description="Run synthetic Processor A/B Max-Cut benchmark.")
    parser.add_argument("--graph", default="0-1,1-2,2-3,3-0,0-2")
    parser.add_argument("--p", type=int, default=1)
    parser.add_argument("--shots", type=int, default=1024)
    parser.add_argument("--maxiter", type=int, default=60)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    graph = parse_edge_list(args.graph)
    results = []
    for name in ("processor_A.json", "processor_B.json"):
        result = run_one(graph, ROOT / "configs" / name, p=args.p, shots=args.shots, maxiter=args.maxiter, seed=args.seed)
        path = save_result(result, ROOT / "results" / "raw")
        print(f"Saved {path}")
        results.append(result)
    df = comparison_dataframe(results)
    out = ROOT / "results" / "tables"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "processor_ab_comparison.csv", index=False)
    print(df.to_string(index=False))
    print("\nNOTICE: synthetic topology + local simulator results; not official hardware results.")
if __name__ == "__main__":
    main()
