"""Graph input parsing and validation."""
from __future__ import annotations
import networkx as nx

def parse_edge_list(text: str) -> nx.Graph:
    """Parse '0-1, 1-2' into a simple unweighted graph."""
    graph = nx.Graph()
    text = text.strip()
    if not text:
        raise ValueError("Enter at least one edge, e.g. 0-1, 1-2, 2-0.")
    for token in text.split(","):
        token = token.strip()
        if not token:
            continue
        parts = token.split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid edge {token!r}; expected u-v.")
        try:
            u, v = (int(part.strip()) for part in parts)
        except ValueError as exc:
            raise ValueError(f"Invalid vertex in edge {token!r}; use integer labels.") from exc
        if u < 0 or v < 0:
            raise ValueError("Vertex labels must be non-negative integers.")
        if u == v:
            raise ValueError(f"Self-loop {token!r} is not supported in this prototype.")
        graph.add_edge(u, v, weight=1.0)
    if graph.number_of_edges() == 0:
        raise ValueError("The graph contains no edges.")
    # QAOA qubits are indexed 0..n-1. Remap sparse labels to contiguous indices.
    graph = nx.convert_node_labels_to_integers(graph, ordering="sorted", label_attribute="original_label")
    return graph

def validate_graph(graph: nx.Graph) -> None:
    if graph.number_of_nodes() < 2:
        raise ValueError("Graph must contain at least two vertices.")
    if graph.number_of_edges() < 1:
        raise ValueError("Graph must contain at least one edge.")
    for u, v, data in graph.edges(data=True):
        weight = float(data.get("weight", 1.0))
        if weight < 0:
            raise ValueError("This prototype expects non-negative edge weights.")
        if u == v:
            raise ValueError("Self-loops are not supported.")
