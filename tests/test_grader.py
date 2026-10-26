import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grader import grade_file


class GraderRegressionTests(unittest.TestCase):
    def test_reference_solution_passes_with_full_score(self):
        result = grade_file(ROOT / "reference_solution.py")
        self.assertTrue(result["passed"])
        self.assertEqual(result["score"], 100)

    def test_buggy_solution_is_rejected(self):
        result = grade_file(ROOT / "sample_buggy_solution.py")
        self.assertFalse(result["passed"])
        self.assertLess(result["score"], 85)


if __name__ == "__main__":
    unittest.main()

