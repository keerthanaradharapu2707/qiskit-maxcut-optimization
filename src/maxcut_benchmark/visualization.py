"""Plot helpers for the Streamlit dashboard and saved benchmark outputs."""
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def graph_figure(graph):
    fig, ax = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(graph, seed=7)
    nx.draw_networkx(graph, pos=pos, ax=ax, node_color="#cfe8ff", edge_color="#667085", node_size=700, font_weight="bold")
    ax.set_title("Max-Cut input graph")
    ax.axis("off")
    fig.tight_layout()
    return fig

def comparison_dataframe(results):
    rows = []
    for result in results:
        cm = result["circuit_metrics"]
        sm = result["solution_metrics"]
        rows.append({
            "Processor": result["processor_label"],
            "Topology status": "Official" if result["processor_is_official"] else "Synthetic",
            "Expected cut": sm["expected_cut"],
            "Best observed cut": sm["best_observed_cut"],
            "Approximation ratio": sm["approximation_ratio"],
            "Circuit depth": cm["transpiled_depth"],
            "Two-qubit gates": cm["two_qubit_gate_count"],
            "Explicit SWAP ops": cm["transpiled_swap_count"],
            "Routing overhead proxy": cm["routing_overhead_proxy_two_qubit_gates"],
            "Transpile time (s)": result["transpilation_seconds"],
        })
    return pd.DataFrame(rows)

def comparison_figure(df, metric, title, ylabel):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["Processor"], df[metric])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", labelrotation=10)
    fig.tight_layout()
    return fig
