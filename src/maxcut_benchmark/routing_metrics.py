def summarize_routing(metrics):
    return {
        "transpiled_swap_count": metrics.get("transpiled_swap_count", 0),
        "routing_overhead_proxy_two_qubit_gates": metrics.get("routing_overhead_proxy_two_qubit_gates", 0),
    }
