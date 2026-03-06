# Pre-Submission Checklist (Iteration 5)

## C1. Visualisation
- `[PASS]` Insight-led titles are present across EDA/model-evaluation figures.
- `[PASS]` Missingness mechanism classification figure exists (`missingness_mechanism_classification.png`).
- `[PASS]` Explicit visual correction evidence exists (`agent_visual_correction_example.png`).
- `[PASS]` Learning, evaluation, and failure-mode figures are present and referenced in report.

## C2. Methodology & Analysis
- `[PASS]` Split-first pipeline discipline remains intact (train/val/test before preprocessing).
- `[PASS]` Baseline + multi-model CV + ablations are persisted in metrics artefacts.
- `[PASS]` Hyperparameter tuning summary includes search space and best params.
- `[PASS]` Repeated-CV robustness evidence exists (`repeated_cv_stability.csv`, `tuning_robustness_summary.json`).
- `[PASS]` MLP training dynamics evidence exists (`mlp_training_curve.csv` + figure).

## C3. Argument / Narrative
- `[PASS]` Report includes numbered figure references and Harvard-style references section.
- `[PASS]` Verification-strategy reflection includes accepted/modified/rejected examples.
- `[PASS]` Relative improvement statements are explicit (final vs baseline; tuned vs untuned context).
- `[CHECK]` Final word count must stay within coursework policy interpretation before submission.

## C4. Code / Markup
- `[PASS]` `requirements.txt` present and pinned.
- `[PASS]` README includes environment, run instructions, and attribution policy.
- `[PASS]` Unit tests + smoke test available.
- `[PASS]` Submission checker script added (`scripts/run_submission_checks.sh`).
- `[PASS]` Submission manifest added (`submission_manifest.md`).
- `[PASS]` No `.DS_Store` or Office lock files inside `assignment_final`.
