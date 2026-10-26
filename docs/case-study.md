# Case study: designing a benchmark that rewards behavior, not appearances

## The evaluation problem

A coding-agent benchmark can look rigorous while still producing a weak signal. A few visible examples often reward solutions that imitate the examples, omit validation or accidentally exploit gaps in the grader. The goal of this package is to make those shortcuts fail while keeping the task contract unambiguous and the final score explainable.

## Design decisions

### 1. Specify the behavioral contract first

The task defines accepted types, error semantics, mutation rules, output type and dependency constraints. These requirements are independently testable; the grader does not rely on subjective code-style judgments.

### 2. Separate capability dimensions

The rubric allocates 45 points to core correctness, 30 to validation and robustness, and 25 to behavioral compliance. A candidate cannot pass by solving only the happy path.

### 3. Combine fixed, seeded and metamorphic checks

- **Fixed checks** make critical edge cases explicit and reviewable.
- **Seeded checks** broaden coverage without sacrificing reproducibility.
- **Metamorphic checks** validate relationships between executions. Translation invariance, for example, is more resistant to hard-coded outputs than another isolated example.

### 4. Return diagnostic evidence

The grader emits section scores, check-level pass/fail data and failed-check names. This supports benchmark debugging, candidate comparison and failure-pattern analysis.

### 5. Regression-test the evaluator

The test suite confirms that the reference candidate receives full credit, the deliberately flawed candidate fails at a stable score, rubric totals match the grader and malformed submissions return structured failures.

## Observed failure pattern

The flawed implementation looks reasonable on common examples and still earns 68 points. It fails because it:

- ignores the requested trim fraction;
- mutates list inputs;
- accepts booleans as numeric data;
- accepts non-finite values;
- does not enforce the task's validation contract.

This is the intended benchmark signal: plausible code is not treated as complete code.

## Why the sample task is compact

The benchmark is intentionally small enough for a recruiter or evaluator to inspect end to end. The proof is in the evaluation package—specification quality, rubric coverage, deterministic grading, anti-shortcut strategy, diagnostics and calibration—not in maximizing task size.

## Limitations

- The demo imports trusted local candidates in-process; it is not a security sandbox.
- One reference and one flawed candidate demonstrate calibration, but a production benchmark would be calibrated across many model families and repeated runs.
- The task measures a narrow capability slice and should be one item in a diverse benchmark suite.

## Production extension path

For a production program I would add container isolation, resource limits, network denial, hidden-test separation, repeated-agent trials, pass-rate and discrimination analysis, versioned datasets and grader observability.

