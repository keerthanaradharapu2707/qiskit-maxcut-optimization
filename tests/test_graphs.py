import pytest
from maxcut_benchmark.graph_builder import parse_edge_list, validate_graph

def test_parse_graph():
    g = parse_edge_list("0-1, 1-2, 2-0")
    assert g.number_of_nodes() == 3
    assert g.number_of_edges() == 3
    validate_graph(g)

def test_reject_self_loop():
    with pytest.raises(ValueError):
        parse_edge_list("0-0,0-1")
