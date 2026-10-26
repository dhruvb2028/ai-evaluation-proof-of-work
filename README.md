# AI Evaluation Proof of Work

This compact, sanitized project demonstrates how I design coding-agent evaluations that are difficult, fair, reproducible, and resistant to shortcuts.

The sample task asks an agent to implement a robust statistical mean. The task is intentionally small enough to inspect, but the evaluation structure mirrors production benchmark work:

- a precise task contract;
- a reference implementation;
- deterministic public and hidden-style checks;
- behavior, robustness, and compliance scoring;
- metamorphic tests that discourage hard-coded answers;
- machine-readable score output for repeatable evaluation.

## What this demonstrates

| Evaluation capability | Evidence in this repository |
| --- | --- |
| Benchmark design | `benchmark_spec.md` defines the interface, constraints, and success criteria. |
| Grader design | `grader.py` evaluates correctness, edge cases, invariants, and implementation behavior. |
| Rubric design | `rubric.json` separates core correctness, robustness, and compliance. |
| Failure analysis | The grader returns check-level diagnostics instead of a single opaque score. |
| Anti-shortcut design | Seeded randomized and metamorphic tests detect brittle or hard-coded solutions. |
| Reproducibility | The harness uses the Python standard library and deterministic seeds. |

## Run it

```bash
python grader.py reference_solution.py
python grader.py sample_buggy_solution.py
python -m unittest discover -s tests -v
```

The reference solution should score 100. The intentionally flawed solution should fail several checks and receive a substantially lower score.

## Repository structure

```text
benchmark_spec.md        Human-readable task specification
rubric.json              Machine-readable scoring rubric
grader.py                Deterministic evaluation harness
reference_solution.py    Known-good implementation
sample_buggy_solution.py Intentionally flawed implementation
tests/test_grader.py     Regression tests for the grader itself
```

## Evaluation philosophy

A difficult task is not automatically a good benchmark. A useful benchmark must distinguish capability levels while remaining fair, reproducible, verifiably solvable, and resistant to leakage or grader exploitation.

This sample contains no proprietary task material, datasets, hidden tests, or confidential information from client work.

