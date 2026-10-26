import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grader import grade_file, uses_only_standard_library


class GraderRegressionTests(unittest.TestCase):
    def test_reference_solution_passes_with_full_score(self):
        result = grade_file(ROOT / "reference_solution.py")
        self.assertTrue(result["passed"])
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["checks_passed"], result["checks_total"])
        self.assertEqual(result["failed_checks"], [])

    def test_buggy_solution_is_rejected_at_expected_score(self):
        result = grade_file(ROOT / "sample_buggy_solution.py")
        self.assertFalse(result["passed"])
        self.assertEqual(result["score"], 68)
        self.assertIn("input immutability", result["failed_checks"])
        self.assertIn("boolean rejection", result["failed_checks"])

    def test_rubric_totals_match_grader(self):
        rubric = json.loads((ROOT / "rubric.json").read_text(encoding="utf-8"))
        result = grade_file(ROOT / "reference_solution.py")
        self.assertEqual(rubric["maximum_score"], result["maximum_score"])
        self.assertEqual(rubric["passing_score"], result["passing_score"])
        self.assertEqual(
            sum(section["points"] for section in rubric["sections"]),
            result["maximum_score"],
        )

    def test_non_standard_library_import_is_detected(self):
        source = (
            "import definitely_not_stdlib\n\n"
            "def robust_mean(values, trim_fraction=0.1):\n"
            "    return 0.0\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.py"
            path.write_text(source, encoding="utf-8")
            self.assertFalse(uses_only_standard_library(path))

    def test_missing_function_returns_structured_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.py"
            path.write_text("VALUE = 1\n", encoding="utf-8")
            result = grade_file(path)
        self.assertEqual(result["score"], 0)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()

