#!/usr/bin/env python3
"""Route plain-language predictive analytics requests to local skills."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from typing import Dict, Iterable, List, Sequence


PHASE_ORDER: List[str] = [
    "pa-problem-framing",
    "pa-eda",
    "pa-data-prep",
    "pa-modelling",
    "pa-evaluation",
    "pa-report",
]

CROSS_CUTTING: List[str] = ["pa-codebase", "pa-agent-log"]

SKILL_PATTERNS: Dict[str, Sequence[str]] = {
    "pa-problem-framing": [
        "problem statement",
        "define the problem",
        "scope",
        "stakeholder",
        "success criteria",
        "dataset",
        "choose a dataset",
        "frame the prediction task",
    ],
    "pa-eda": [
        "eda",
        "explore the data",
        "visualise",
        "visualize",
        "missingness",
        "outlier",
        "check for leakage",
        "correlation",
    ],
    "pa-data-prep": [
        "preprocess",
        "preprocessing",
        "pipeline",
        "imputation",
        "imputer",
        "encode",
        "encoding",
        "scale",
        "scaling",
        "feature engineering",
        "clean the data",
    ],
    "pa-modelling": [
        "train models",
        "compare models",
        "compare",
        "model",
        "ablation",
        "ablations",
        "hyperparameter",
        "cross-validation",
        "cross validation",
        "select a model",
        "tune",
    ],
    "pa-evaluation": [
        "evaluate",
        "evaluation",
        "evaluation metrics",
        "error analysis",
        "failure mode",
        "shap",
        "interpretability",
        "deployment risk",
    ],
    "pa-report": [
        "write the report",
        "final report",
        "draft the narrative",
        "introduction",
        "discussion",
        "model card",
        "report",
    ],
    "pa-codebase": [
        "repo",
        "repository",
        "structure the code",
        "reproducible",
        "requirements",
        "unit test",
        "tests",
        "docstring",
        "readme",
        "packaging",
    ],
    "pa-agent-log": [
        "agent log",
        "decision register",
        "appendix",
        "agent interactions",
        "agent mistakes",
        "human-agent collaboration",
        "human agent collaboration",
    ],
}

ALIASES: Dict[str, str] = {
    "problem framing": "pa-problem-framing",
    "data prep": "pa-data-prep",
    "modelling": "pa-modelling",
    "modeling": "pa-modelling",
    "evaluation": "pa-evaluation",
    "report": "pa-report",
    "codebase": "pa-codebase",
    "agent log": "pa-agent-log",
}

BROAD_PATTERNS: Sequence[str] = (
    "end-to-end",
    "end to end",
    "full workflow",
    "entire workflow",
    "from start to finish",
)


@dataclass(frozen=True)
class RoutingDecision:
    primary_skills: List[str]
    overlay_skills: List[str]
    assumption: str | None = None


def _contains(haystack: str, needle: str) -> bool:
    if " " in needle or "-" in needle:
        return needle in haystack
    return re.search(rf"\b{re.escape(needle)}\b", haystack) is not None


def _score_skills(query: str) -> Dict[str, int]:
    scores: Dict[str, int] = {skill: 0 for skill in SKILL_PATTERNS}
    for skill, patterns in SKILL_PATTERNS.items():
        for pattern in patterns:
            if _contains(query, pattern):
                scores[skill] += 1
    return scores


def _find_explicit_mentions(query: str) -> List[str]:
    positions: List[tuple[int, str]] = []
    for skill in SKILL_PATTERNS:
        if skill in query:
            positions.append((query.index(skill), skill))
    for alias, skill in ALIASES.items():
        if _contains(query, alias):
            positions.append((query.index(alias), skill))
    positions.sort(key=lambda x: x[0])

    ordered: List[str] = []
    for _, skill in positions:
        if skill not in ordered:
            ordered.append(skill)
    return ordered


def _sort_by_phase_order(skills: Iterable[str]) -> List[str]:
    phase = [s for s in skills if s in PHASE_ORDER]
    cross = [s for s in skills if s in CROSS_CUTTING]
    return sorted(phase, key=PHASE_ORDER.index) + sorted(cross, key=CROSS_CUTTING.index)


def route_request(request: str) -> RoutingDecision:
    query = request.strip().lower()
    if not query:
        return RoutingDecision(
            primary_skills=["pa-problem-framing"],
            overlay_skills=[],
            assumption="Empty request; defaulting to pa-problem-framing as the conservative start.",
        )

    explicit = _find_explicit_mentions(query)
    scores = _score_skills(query)

    broad = any(pattern in query for pattern in BROAD_PATTERNS)
    hit_phases = [s for s in PHASE_ORDER if scores.get(s, 0) > 0]
    hit_cross = [s for s in CROSS_CUTTING if scores.get(s, 0) > 0]

    if explicit:
        selected = _sort_by_phase_order(explicit)
    elif broad:
        selected = PHASE_ORDER.copy()
    elif len(hit_phases) >= 2:
        selected = hit_phases
    elif hit_phases:
        selected = [hit_phases[0]]
    elif hit_cross:
        selected = [hit_cross[0]]
    else:
        return RoutingDecision(
            primary_skills=["pa-problem-framing"],
            overlay_skills=[],
            assumption=(
                "No clear trigger matched; defaulting to pa-problem-framing "
                "as the most conservative route."
            ),
        )

    # Extract overlays only when a primary phase skill is selected.
    primary: List[str] = []
    overlays: List[str] = []
    for skill in selected:
        if skill in CROSS_CUTTING and any(p in selected for p in PHASE_ORDER):
            overlays.append(skill)
        else:
            primary.append(skill)

    # Apply cross-cutting overlays when relevant to the request.
    if "pa-report" in primary and "pa-agent-log" not in overlays:
        overlays.append("pa-agent-log")

    for cross_skill in CROSS_CUTTING:
        if scores.get(cross_skill, 0) > 0 and cross_skill not in primary and cross_skill not in overlays:
            if any(skill in PHASE_ORDER for skill in primary):
                overlays.append(cross_skill)
            else:
                primary.append(cross_skill)

    if not primary and overlays:
        primary = overlays
        overlays = []

    return RoutingDecision(primary_skills=primary, overlay_skills=overlays, assumption=None)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Route requests to predictive analytics skills.")
    parser.add_argument("request", nargs="*", help="Plain-language request to route.")
    parser.add_argument(
        "--show-map",
        action="store_true",
        help="Print the active skill map and exit.",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.show_map:
        payload = {
            "phase_order": PHASE_ORDER,
            "cross_cutting": CROSS_CUTTING,
            "skill_patterns": SKILL_PATTERNS,
        }
        print(json.dumps(payload, indent=2))
        return 0

    request = " ".join(args.request).strip()
    decision = route_request(request)
    print(json.dumps(asdict(decision), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
