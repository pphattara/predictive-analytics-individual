# Skill Routing Contract

## Summary
This workspace uses the local predictive-analytics skills (`*.skill`) as an active routing system.
Requests are routed to the minimum relevant skill set, with lifecycle ordering for multi-phase asks.

## Input Interface
- Input format: plain-language task request.
- Router entrypoint: `python3 skill_router.py "<request>"`.

## Routing Interface
- Primary output: `primary_skills` list in execution order.
- Optional output: `overlay_skills` list for cross-cutting support.
- Optional `assumption`: populated when request ambiguity forces a conservative default.

## Active Skill Map
- `pa-problem-framing`: dataset choice, scope, stakeholder/problem statement.
- `pa-eda`: EDA, visual diagnostics, missingness/outlier/leakage checks.
- `pa-data-prep`: preprocessing pipelines, leakage-safe transforms, feature prep.
- `pa-modelling`: model training, comparison, ablations, hyperparameter tuning.
- `pa-evaluation`: metrics, error analysis, interpretability, deployment risk checks.
- `pa-report`: 2000-word report drafting/structuring/editing.
- `pa-codebase`: repo structure, reproducibility, tests, packaging/docs.
- `pa-agent-log`: decision register and agent-usage appendix.

## Multi-Skill Execution Rule
- Use the minimum skill set required by the request.
- If the request spans phases and does not specify explicit non-lifecycle order:
  - Apply lifecycle order: `framing -> eda -> prep -> modelling -> evaluation -> report`.
- Apply `pa-codebase` and `pa-agent-log` as cross-cutting overlays when relevant.

## Assumptions And Defaults
- Default behavior is automatic skill routing based on request intent.
- If request spans phases, lifecycle order is used unless explicitly overridden.
- If request is ambiguous, the router defaults to `pa-problem-framing` and states the assumption.
- Skill adoption is session-operational and remains active unless changed.

## Quick Checks
- `python3 skill_router.py "Help me pick a dataset and define success metrics."`
- `python3 skill_router.py "Run EDA and decide preprocessing choices."`
- `python3 skill_router.py "Compare 3 models and run ablations."`
- `python3 skill_router.py "Write the final coursework report."`
- `python3 skill_router.py "Make this repo reproducible and testable."`
