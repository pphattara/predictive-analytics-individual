"""End-to-end smoke checks for the reduced final submission package."""

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "adult_census_income"
METRICS = OUT / "metrics"
FIGS = OUT / "figures"


def tracked_dsstore_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
        text=False,
    )
    return [
        path.decode("utf-8")
        for path in result.stdout.split(b"\x00")
        if path and path.decode("utf-8").endswith(".DS_Store")
    ]


class TestPipelineSmoke(unittest.TestCase):
    def test_required_artifacts_exist(self) -> None:
        required_paths = [
            ROOT / "README.md",
            ROOT / "requirements.txt",
            ROOT / "report_final.pdf",
            ROOT / "submission_manifest.md",
            ROOT / "notebooks" / "adult_census_income_final.ipynb",
            ROOT / "data" / "raw" / "adult_census_income" / "adult.csv",
            METRICS / "preprocessing_validation.json",
            METRICS / "model_comparison_cv.csv",
            METRICS / "ablation_results.csv",
            METRICS / "evaluation_report.json",
            METRICS / "threshold_policy.json",
            METRICS / "final_solution_bundle.json",
            OUT / "agent_log.md",
            OUT / "decision_register.pdf",
            FIGS / "target_distribution.png",
            FIGS / "missingness_summary.png",
            FIGS / "module2" / "confusion_matrix.png",
            FIGS / "module2" / "roc_curve.png",
            FIGS / "module2" / "pr_curve.png",
        ]
        for path in required_paths:
            self.assertTrue(path.exists(), f"Missing artifact: {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty artifact: {path}")

    def test_final_solution_bundle_schema(self) -> None:
        payload = json.loads((METRICS / "final_solution_bundle.json").read_text(encoding="utf-8"))
        for key in [
            "module",
            "dataset",
            "target",
            "positive_class",
            "selection",
            "test_metrics",
            "project_history_summary",
            "module2_artifacts",
            "module3_artifacts",
            "robustness_artifacts",
            "generated_at_note",
        ]:
            self.assertIn(key, payload)

    def test_hygiene(self) -> None:
        self.assertFalse(tracked_dsstore_paths(ROOT), "Found tracked .DS_Store files in repository")
        self.assertFalse(any(OUT.glob("~$*.docx")), "Found Office lock files in outputs folder")


if __name__ == "__main__":
    unittest.main()
