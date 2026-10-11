# Phase 1 Benchmark Report (Template)

## Status
Prototype implementation. Processor A and Processor B are synthetic topology fixtures; all runs use a local Aer simulator. No official hardware experiment has been performed.

## Research question
How do connectivity and transpilation affect QAOA Max-Cut circuit resources and observed solution quality?

## Method
- Graph: record graph edge list and weight convention.
- Algorithm: QAOA with depth p = [record].
- Optimizer: COBYLA; max iterations = [record].
- Execution: local Aer simulator; shots = [record].
- Processor A/B configurations: [replace with official source and revision].
- Seeds and transpiler settings: [record].

## Results
Populate this section from `results/raw/` and `results/tables/`. Do not enter fabricated values.

## Interpretation
Discuss circuit depth, two-qubit gate count, routing overhead proxy, expected cut, approximation ratio, and trial-to-trial variability. Separate compilation resource changes from solution-quality changes.

## Limitations
The supplied example topologies are synthetic. Local simulator results do not represent physical device noise or hardware performance. Validate official metrics and experiment constraints against the Challenge Kit.
