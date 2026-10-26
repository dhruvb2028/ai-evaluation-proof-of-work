import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grader import grade_file


def write_report(candidate_name, source_name, output_name):
    report = grade_file(ROOT / source_name)
    report["candidate"] = candidate_name
    output_path = ROOT / "results" / output_name
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


def main():
    reference = write_report(
        "Reference implementation", "reference_solution.py", "reference_report.json"
    )
    flawed = write_report(
        "Intentionally flawed implementation",
        "sample_buggy_solution.py",
        "flawed_report.json",
    )
    print(
        f"Generated reports: reference={reference['score']}/100, "
        f"flawed={flawed['score']}/100"
    )


if __name__ == "__main__":
    main()

