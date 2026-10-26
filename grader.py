import importlib.util
import json
import math
import random
import sys
from pathlib import Path


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
    return isinstance(actual, float) and math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance)


def expects_error(function, error_types, *args):
    try:
        function(*args)
    except error_types:
        return True
    except Exception:
        return False
    return False


def evaluate(function):
    checks = []

    def record(name, points, passed, detail=""):
        checks.append({"name": name, "points": points, "passed": bool(passed), "detail": detail})

    record("untrimmed mean", 10, close(function([1, 2, 3], 0), 2.0))
    record("symmetric trimming", 10, close(function([1, 2, 3, 4, 100], 0.2), 3.0))
    record("duplicates and negatives", 8, close(function([-8, -2, -2, 4, 20], 0.2), 0.0))
    record("generator input", 7, close(function((x for x in [2, 4, 6, 8]), 0.25), 5.0))

    rng = random.Random(20261026)
    seeded_ok = True
    for _ in range(8):
        values = [rng.uniform(-50, 50) for _ in range(10)]
        expected = sum(sorted(values)[1:-1]) / 8
        seeded_ok = seeded_ok and close(function(values, 0.1), expected)
    record("deterministic seeded cases", 15, seeded_ok)

    record("empty input validation", 5, expects_error(function, ValueError, [], 0.1))
    record("trim fraction validation", 6, expects_error(function, ValueError, [1, 2], 0.5))
    record("non-numeric validation", 5, expects_error(function, TypeError, [1, "2"], 0.1))
    record("boolean rejection", 5, expects_error(function, TypeError, [1, True], 0.1))
    record("non-finite validation", 9, expects_error(function, ValueError, [1, math.inf], 0.1))

    original = [9, 1, 5, 100, 3]
    snapshot = list(original)
    function(original, 0.2)
    record("input immutability", 7, original == snapshot)
    record("float return type", 3, isinstance(function([1, 2, 3], 0), float))

    base = [1, 2, 5, 9, 50]
    shift = 17.25
    base_result = function(base, 0.2)
    shifted_result = function([value + shift for value in base], 0.2)
    record("translation invariance", 10, close(shifted_result, base_result + shift))

    score = sum(check["points"] for check in checks if check["passed"])
    return {
        "benchmark": "robust-trimmed-mean",
        "score": score,
        "maximum_score": 100,
        "passed": score >= 85,
        "checks": checks,
    }


def grade_file(path):
    try:
        function = load_submission(path)
        return evaluate(function)
    except Exception as exc:
        return {
            "benchmark": "robust-trimmed-mean",
            "score": 0,
            "maximum_score": 100,
            "passed": False,
            "checks": [],
            "error": f"{type(exc).__name__}: {exc}",
        }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python grader.py path/to/submission.py")
    submission_path = Path(sys.argv[1]).resolve()
    print(json.dumps(grade_file(submission_path), indent=2, sort_keys=True))

