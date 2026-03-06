import unittest

from skill_router import route_request


class SkillRouterTests(unittest.TestCase):
    def test_problem_framing_route(self) -> None:
        decision = route_request("Help me pick a dataset and define success metrics.")
        self.assertEqual(decision.primary_skills, ["pa-problem-framing"])
        self.assertEqual(decision.overlay_skills, [])
        self.assertIsNone(decision.assumption)

    def test_eda_then_data_prep_route(self) -> None:
        decision = route_request("Run EDA and decide preprocessing choices.")
        self.assertEqual(decision.primary_skills, ["pa-eda", "pa-data-prep"])
        self.assertEqual(decision.overlay_skills, [])
        self.assertIsNone(decision.assumption)

    def test_modelling_route(self) -> None:
        decision = route_request("Compare 3 models and run ablations.")
        self.assertEqual(decision.primary_skills, ["pa-modelling"])
        self.assertEqual(decision.overlay_skills, [])
        self.assertIsNone(decision.assumption)

    def test_report_plus_agent_log_overlay_route(self) -> None:
        decision = route_request("Write the final coursework report.")
        self.assertEqual(decision.primary_skills, ["pa-report"])
        self.assertEqual(decision.overlay_skills, ["pa-agent-log"])
        self.assertIsNone(decision.assumption)

    def test_codebase_route(self) -> None:
        decision = route_request("Make this repo reproducible and testable.")
        self.assertEqual(decision.primary_skills, ["pa-codebase"])
        self.assertEqual(decision.overlay_skills, [])
        self.assertIsNone(decision.assumption)

    def test_ambiguous_defaults_to_problem_framing(self) -> None:
        decision = route_request("Help me with this project.")
        self.assertEqual(decision.primary_skills, ["pa-problem-framing"])
        self.assertEqual(decision.overlay_skills, [])
        self.assertIsNotNone(decision.assumption)


if __name__ == "__main__":
    unittest.main()
