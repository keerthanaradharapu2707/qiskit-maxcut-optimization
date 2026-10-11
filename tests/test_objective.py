from maxcut_benchmark.graph_builder import parse_edge_list
from maxcut_benchmark.objective import cut_value, exact_maxcut

def test_cut_value_triangle():
    g = parse_edge_list("0-1,1-2,2-0")
    assert cut_value(g, "010") == 2
    assert cut_value(g, "000") == 0

def test_exact_maxcut_triangle():
    g = parse_edge_list("0-1,1-2,2-0")
    value, bits = exact_maxcut(g)
    assert value == 2
    assert cut_value(g, bits) == 2
