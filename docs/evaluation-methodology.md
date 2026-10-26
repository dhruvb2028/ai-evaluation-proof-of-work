# Evaluation methodology checklist

This checklist captures the quality gates used when authoring or reviewing a technical AI benchmark.

## Task validity

- The requested behavior is technically solvable.
- Instructions, constraints and success criteria do not conflict.
- A known-good reference solution satisfies every graded requirement.
- Required files, interfaces and runtime assumptions are explicit.

## Grader validity

- Every scored requirement maps to at least one executable check.
- The rubric totals exactly 100 points and the pass threshold is explicit.
- Critical failures cannot be hidden by unrelated partial credit.
- The grader returns actionable diagnostics.
- Grader regression tests protect calibration from accidental changes.

## Anti-shortcut coverage

- Hidden-style inputs extend beyond examples in the prompt.
- Deterministic randomness broadens coverage reproducibly.
- Metamorphic properties test relationships, not memorized outputs.
- Hard-coded answers and input-specific branches are challenged.
- Candidate code cannot access answer keys or hidden fixtures in production.

## Reproducibility and fairness

- Seeds, runtime versions and dependency constraints are versioned.
- Equivalent valid solutions are accepted.
- Non-essential implementation style is not scored.
- Failures are attributable to requirements visible in the task contract.
- Evaluation changes trigger a fresh reference and adversarial validation run.

## Production safety

- Untrusted code runs in an isolated environment.
- Network access is disabled unless explicitly required.
- CPU, memory, filesystem and wall-clock limits are enforced.
- Secrets, host paths and grader internals are unavailable to submissions.
- Logs retain enough evidence for dispute review without leaking hidden tests.

