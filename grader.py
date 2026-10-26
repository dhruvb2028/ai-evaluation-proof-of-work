import ast
import importlib.util
import json
import math
import random
import sys
from pathlib import Path


BENCHMARK_ID = "robust-trimmed-mean"
GRADER_VERSION = "2.0"
SEED = 20261026
PASSING_SCORE = 85


def load_submission(path):
    spec = importlib.util.spec_from_file_location("candidate_submission", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load submission")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    function = getattr(module, "robust_mean", None)
    if not callable(function):
        raise AttributeError("Submission must define callable robust_mean")
    return function


def close(actual, expected, tolerance=1e-9):
    return isinstance(actual, float) and math.isclose(
        actual, expected, rel_tol=tolerance, abs_tol=tolerance
    )


def expects_error(function, error_types, *args):
    try:
        function(*args)
    except error_types:
        return True
    except Exception:
        return False
    return False


def uses_only_standard_library(path):
    source = Path(path).read_text(encoding="utf-8")
    tree = ast.parse(source)
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level or not node.module:
                return False
            roots.add(node.module.split(".")[0])
    return roots.issubset(sys.stdlib_module_names)


def evaluate(function, submission_path):
    checks = []

    def record(section, name, points, check):
        detail = ""
        try:
            passed = bool(check())
        except Exception as exc:
            passed = False
            detail = f"{type(exc).__name__}: {exc}"
        checks.append(
            {
                "section": section,
                "name": name,
                "points": points,
                "passed": passed,
                "detail": detail,
            }
        )

    core = "Core correctness"
    robustness = "Robustness and validation"
    behavior = "Behavioral compliance"

    record(core, "untrimmed mean", 10, lambda: close(function([1, 2, 3], 0), 2.0))
    record(
        core,
        "symmetric trimming",
        10,
        lambda: close(function([1, 2, 3, 4, 100], 0.2), 3.0),
    )
    record(
        core,
        "duplicates and negatives",
        8,
        lambda: close(function([-8, -2, -2, 4, 20], 0.2), 0.0),
    )
    record(
        core,
        "generator input",
        7,
        lambda: close(function((x for x in [2, 4, 6, 8]), 0.25), 5.0),
    )

    def seeded_cases_pass():
        rng = random.Random(SEED)
        for _ in range(8):
            values = [rng.uniform(-50, 50) for _ in range(10)]
            expected = sum(sorted(values)[1:-1]) / 8
            if not close(function(values, 0.1), expected):
                return False
        return True

    record(core, "deterministic seeded cases", 10, seeded_cases_pass)
    record(
        robustness,
        "empty input validation",
        5,
        lambda: expects_error(function, ValueError, [], 0.1),
    )
    record(
        robustness,
        "trim fraction validation",
        6,
        lambda: expects_error(function, ValueError, [1, 2], 0.5),
    )
    record(
        robustness,
        "non-numeric validation",
        5,
        lambda: expects_error(function, TypeError, [1, "2"], 0.1),
    )
    record(
        robustness,
        "boolean rejection",
        5,
        lambda: expects_error(function, TypeError, [1, True], 0.1),
    )
    record(
        robustness,
        "non-finite validation",
        9,
        lambda: expects_error(function, ValueError, [1, math.inf], 0.1),
    )

    def preserves_input():
        original = [9, 1, 5, 100, 3]
        snapshot = list(original)
        function(original, 0.2)
        return original == snapshot

    def is_translation_invariant():
        base = [1, 2, 5, 9, 50]
        shift = 17.25
        base_result = function(base, 0.2)
        shifted_result = function([value + shift for value in base], 0.2)
        return close(shifted_result, base_result + shift)

    record(behavior, "input immutability", 7, preserves_input)
    record(
        behavior,
        "float return type",
        3,
        lambda: isinstance(function([1, 2, 3], 0), float),
    )
    record(behavior, "translation invariance", 10, is_translation_invariant)
    record(
        behavior,
        "standard-library-only implementation",
        5,
        lambda: uses_only_standard_library(submission_path),
    )

    score = sum(check["points"] for check in checks if check["passed"])
    section_scores = {}
    for section in (core, robustness, behavior):
        section_checks = [check for check in checks if check["section"] == section]
        section_scores[section] = {
            "score": sum(check["points"] for check in section_checks if check["passed"]),
            "maximum_score": sum(check["points"] for check in section_checks),
        }

    failed_checks = [check["name"] for check in checks if not check["passed"]]
    return {
        "schema_version": "1.0",
        "benchmark": BENCHMARK_ID,
        "grader_version": GRADER_VERSION,
        "seed": SEED,
        "score": score,
        "maximum_score": 100,
        "passing_score": PASSING_SCORE,
        "passed": score >= PASSING_SCORE,
        "checks_passed": sum(check["passed"] for check in checks),
        "checks_total": len(checks),
        "failed_checks": failed_checks,
        "section_scores": section_scores,
        "checks": checks,
    }


def grade_file(path):
    submission_path = Path(path).resolve()
    try:
        function = load_submission(submission_path)
        return evaluate(function, submission_path)
    except Exception as exc:
        return {
            "schema_version": "1.0",
            "benchmark": BENCHMARK_ID,
            "grader_version": GRADER_VERSION,
            "score": 0,
            "maximum_score": 100,
            "passing_score": PASSING_SCORE,
            "passed": False,
            "checks_passed": 0,
            "checks_total": 14,
            "failed_checks": [],
            "section_scores": {},
            "checks": [],
            "error": f"{type(exc).__name__}: {exc}",
        }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python grader.py path/to/submission.py")
    print(json.dumps(grade_file(sys.argv[1]), indent=2, sort_keys=True))

