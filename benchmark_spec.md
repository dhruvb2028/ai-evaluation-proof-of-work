# Benchmark specification: Robust trimmed mean

## Objective

Implement `robust_mean(values, trim_fraction=0.1)` in the submitted Python file.

The function must return the arithmetic mean after removing the same number of observations from the low and high ends of the sorted data. The number removed from each end is `floor(len(values) * trim_fraction)`.

## Contract

- `values` must be a non-empty iterable of finite `int` or `float` values.
- Boolean values are invalid even though `bool` is a subclass of `int` in Python.
- `trim_fraction` must be numeric, finite, and satisfy `0 <= trim_fraction < 0.5`.
- If trimming would remove every value, raise `ValueError`.
- Invalid inputs must raise `TypeError` or `ValueError` as appropriate.
- The input collection must not be mutated.
- The result must be deterministic and returned as a `float`.
- Use only the Python standard library.

## Evaluation dimensions

1. Core correctness on representative inputs.
2. Robustness on generators, duplicates, negatives, and extreme values.
3. Validation of malformed or non-finite inputs.
4. Behavioral compliance, including input immutability and determinism.
5. Metamorphic properties, such as translation invariance.

## Anti-shortcut design

The grader combines fixed cases with deterministic seeded cases. Metamorphic checks verify relationships between inputs and outputs, making lookup-table and hard-coded solutions less effective.

