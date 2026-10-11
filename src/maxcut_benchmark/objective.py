"""Classical Max-Cut objective utilities."""
from __future__ import annotations
import networkx as nx

def cut_value(graph: nx.Graph, bitstring: str) -> float:
    """Return cut weight; bitstring is indexed by vertex 0 first (left to right)."""
    if len(bitstring) != graph.number_of_nodes() or any(c not in "01" for c in bitstring):
        raise ValueError("Bitstring must contain one 0/1 character per graph vertex.")
    total = 0.0
    for u, v, data in graph.edges(data=True):
        if bitstring[u] != bitstring[v]:
            total += float(data.get("weight", 1.0))
    return total

def exact_maxcut(graph: nx.Graph, max_vertices: int = 20) -> tuple[float, str]:
    """Exhaustive reference optimum for small graphs; fixes first bit to 0 by symmetry."""
    n = graph.number_of_nodes()
    if n > max_vertices:
        raise ValueError(f"Exact enumeration limited to {max_vertices} vertices; graph has {n}.")
    best_value, best_bits = -1.0, ""
    for mask in range(1 << max(0, n - 1)):
        bits = "0" + format(mask, f"0{n-1}b")
        value = cut_value(graph, bits)
        if value > best_value:
            best_value, best_bits = value, bits
    return best_value, best_bits
