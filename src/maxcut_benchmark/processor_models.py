"""Load processor topology fixtures. Example configurations are synthetic only."""
from __future__ import annotations
import json
from pathlib import Path
from qiskit.transpiler import CouplingMap

def load_processor(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if "num_qubits" not in data or "coupling_edges" not in data:
        raise ValueError(f"{path}: expected num_qubits and coupling_edges.")
    n = int(data["num_qubits"])
    edges = [(int(u), int(v)) for u, v in data["coupling_edges"]]
    for u, v in edges:
        if u < 0 or v < 0 or u >= n or v >= n or u == v:
            raise ValueError(f"{path}: invalid coupling edge {(u, v)} for {n} qubits.")
    data["coupling_map_object"] = CouplingMap(couplinglist=edges)
    data["is_synthetic"] = not bool(data.get("is_official", False))
    return data
