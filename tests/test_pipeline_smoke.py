"""End-to-end submission smoke checks for the final submission package."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "adult_census_income"
METRICS = OUT / "metrics"
FIGS = OUT / "figures"
ARCHIVE = OUT / "archive" / "report_exports"


class TestPipelineSmoke(unittest.TestCase):
    def test_required_artifacts_exist(self) -> None:
        required_paths = [
            ROOT / "report_final.pdf",
            ARCHIVE / "report_supporting_export.md",
            ARCHIVE / "report_supporting_export.pdf",
            ARCHIVE / "report_supporting_export.docx",
            METRICS / "evaluation_report.json",
            METRICS / "model_comparison_cv.csv",
            METRICS / "ablation_results.csv",
            METRICS / "threshold_policy.json",
            METRICS / "repeated_cv_stability.csv",
            METRICS / "mlp_training_curve.csv",
            METRICS / "tuning_robustness_summary.json",
            METRICS / "module3_deep_evaluation.json",
            METRICS / "final_solution_bundle.json",
            FIGS / "missingness_mechanism_classification.png",
            FIGS / "agent_visual_correction_example.png",
            FIGS / "module2" / "mlp_training_curve.png",
            FIGS / "module2" / "repeated_cv_stability.png",
        ]
        for path in required_paths:
            self.assertTrue(path.exists(), f"Missing artifact: {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty artifact: {path}")

    def test_evaluation_report_schema_and_ranges(self) -> None:
        payload = json.loads((METRICS / "evaluation_report.json").read_text(encoding="utf-8"))

        for key in ["module", "dataset", "target", "positive_class", "split_sizes", "selection", "test_metrics"]:
            self.assertIn(key, payload)

        metrics = payload["test_metrics"]
        for metric in ["f1_weighted", "auc_pr", "roc_auc", "recall_positive", "calibration_error"]:
            self.assertIn(metric, metrics)
            self.assertIsNotNone(metrics[metric], f"Metric missing value: {metric}")

        self.assertGreaterEqual(metrics["f1_weighted"], 0.0)
        self.assertLessEqual(metrics["f1_weighted"], 1.0)
        self.assertGreaterEqual(metrics["auc_pr"], 0.0)
        self.assertLessEqual(metrics["auc_pr"], 1.0)
        self.assertGreaterEqual(metrics["roc_auc"], 0.0)
        self.assertLessEqual(metrics["roc_auc"], 1.0)
        self.assertGreaterEqual(metrics["recall_positive"], 0.0)
        self.assertLessEqual(metrics["recall_positive"], 1.0)
        self.assertGreaterEqual(metrics["calibration_error"], 0.0)

    def test_module3_has_robustness_subsection(self) -> None:
        payload = json.loads((METRICS / "module3_deep_evaluation.json").read_text(encoding="utf-8"))
        self.assertIn("robustness_checks", payload)
        self.assertIsInstance(payload["robustness_checks"], dict)
        self.assertTrue(len(payload["robustness_checks"]) > 0)

    def test_final_solution_bundle_schema(self) -> None:
        payload = json.loads((METRICS / "final_solution_bundle.json").read_text(encoding="utf-8"))

        required_keys = {
            "module",
            "dataset",
            "target",
            "positive_class",
            "selection",
            "test_metrics",
            "project_history_summary",
            "workflow_evidence_links",
            "module2_artifacts",
            "module3_artifacts",
            "robustness_artifacts",
            "packaging_artifacts",
            "narrative_links",
            "generated_at_note",
        }
        self.assertTrue(required_keys.issubset(payload.keys()))

        timeline = payload["project_history_summary"]
        self.assertIsInstance(timeline, dict)
        self.assertEqual(
            set(timeline.keys()),
            {"foundation_build", "six_step_restructure", "quality_uplift", "report_polish", "final_submission"},
        )

    def test_hygiene_no_dsstore_or_temp_docx_locks(self) -> None:
        self.assertFalse(any(ROOT.glob("**/.DS_Store")), "Found .DS_Store files in project root")
        self.assertFalse(any(OUT.glob("~$*.docx")), "Found Office lock files in outputs folder")


if __name__ == "__main__":
    unittest.main()
