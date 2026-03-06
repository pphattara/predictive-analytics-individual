import importlib.util
import pathlib
import sys
import unittest

import pandas as pd


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "kaggle_shortlist.py"
SPEC = importlib.util.spec_from_file_location("kaggle_shortlist", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class KaggleShortlistTests(unittest.TestCase):
    def test_infer_task_type_classification_for_low_cardinality(self) -> None:
        s = pd.Series([0, 1, 0, 1, 1, 0] * 3000)
        task = MODULE._infer_task_type(s, len(s))
        self.assertEqual(task, "classification")

    def test_infer_task_type_regression_for_continuous(self) -> None:
        s = pd.Series([float(i) * 0.1 for i in range(20000)])
        task = MODULE._infer_task_type(s, len(s))
        self.assertEqual(task, "regression")

    def test_select_top10_respects_target_mix_when_available(self) -> None:
        rows = []
        for i in range(10):
            rows.append(
                MODULE.Candidate(
                    dataset_slug=f"owner/class_{i}",
                    title=f"class {i}",
                    kaggle_url=f"https://www.kaggle.com/datasets/owner/class_{i}",
                    source_search="test",
                    task_type="classification",
                    verified_rows=20000,
                    target_column="target",
                    feature_overview="12 features",
                    why_proper_for_coursework="why",
                    risks_or_caveats="risk",
                    fit_score=90 - i,
                )
            )
        for i in range(6):
            rows.append(
                MODULE.Candidate(
                    dataset_slug=f"owner/reg_{i}",
                    title=f"reg {i}",
                    kaggle_url=f"https://www.kaggle.com/datasets/owner/reg_{i}",
                    source_search="test",
                    task_type="regression",
                    verified_rows=20000,
                    target_column="target",
                    feature_overview="10 features",
                    why_proper_for_coursework="why",
                    risks_or_caveats="risk",
                    fit_score=89 - i,
                )
            )

        selected = MODULE._select_top10(rows)
        cls = sum(1 for x in selected if x.task_type == "classification")
        reg = sum(1 for x in selected if x.task_type == "regression")
        self.assertEqual(len(selected), 10)
        self.assertEqual(cls, 7)
        self.assertEqual(reg, 3)


if __name__ == "__main__":
    unittest.main()
