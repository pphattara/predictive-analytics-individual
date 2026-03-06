import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class BlueprintContractTests(unittest.TestCase):
    def test_dataset_blueprint_contains_five_candidates(self) -> None:
        path = ROOT / "configs" / "dataset_blueprints.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        datasets = payload["datasets"]
        self.assertEqual(len(datasets), 5)

    def test_required_dataset_ids_exist(self) -> None:
        path = ROOT / "configs" / "dataset_blueprints.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        ids = {item["id"] for item in payload["datasets"]}
        expected = {
            "adult_census_income",
            "bank_marketing",
            "loan_approval_classification",
            "ecommerce_customer_behavior",
            "california_housing_prices",
        }
        self.assertEqual(ids, expected)

    def test_metrics_contract_has_classification_and_regression(self) -> None:
        path = ROOT / "configs" / "metrics_contract.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("classification", payload)
        self.assertIn("regression", payload)
        self.assertIn("f1_weighted", payload["classification"])
        self.assertIn("rmse", payload["regression"])


if __name__ == "__main__":
    unittest.main()
