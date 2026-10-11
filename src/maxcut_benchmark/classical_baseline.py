from .objective import exact_maxcut

def solve_exact(graph, max_vertices=20):
    return exact_maxcut(graph, max_vertices=max_vertices)
