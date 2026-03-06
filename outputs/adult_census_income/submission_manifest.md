# Submission Manifest — Adult Census Income (Final)

## Package Scope
- Root package: repository root final submission package
- Canonical notebook: `notebooks/adult_census_income_final.ipynb`
- Canonical submission report: `report_final.pdf`

## Repository Metadata
- Repository URL: `https://github.com/pphattara/predictive-analytics-individual`
- Commit hash: tracked in git history for the final submission branch
- Build timestamp (local): `2026-03-06`

## Core Artefacts
- Supporting report markdown export: `outputs/adult_census_income/archive/report_exports/report_supporting_export.md`
- Supporting report DOCX export: `outputs/adult_census_income/archive/report_exports/report_supporting_export.docx`
- Supporting report PDF export: `outputs/adult_census_income/archive/report_exports/report_supporting_export.pdf`
- Canonical submission report: `report_final.pdf`
- Decision log: `outputs/adult_census_income/agent_log.md`

## Model and Metrics Artefacts
- Model comparison: `outputs/adult_census_income/metrics/model_comparison_cv.csv`
- Ablation results: `outputs/adult_census_income/metrics/ablation_results.csv`
- Threshold policy: `outputs/adult_census_income/metrics/threshold_policy.json`
- Evaluation report: `outputs/adult_census_income/metrics/evaluation_report.json`
- Tuning summary: `outputs/adult_census_income/metrics/hyperparameter_tuning_summary.json`
- Repeated-CV stability: `outputs/adult_census_income/metrics/repeated_cv_stability.csv`
- MLP training curve data: `outputs/adult_census_income/metrics/mlp_training_curve.csv`
- Tuning robustness summary: `outputs/adult_census_income/metrics/tuning_robustness_summary.json`
- Deep evaluation summary: `outputs/adult_census_income/metrics/module3_deep_evaluation.json`
- Final solution bundle: `outputs/adult_census_income/metrics/final_solution_bundle.json`

## Figure Artefacts (Robustness Additions)
- `outputs/adult_census_income/figures/missingness_mechanism_classification.png`
- `outputs/adult_census_income/figures/agent_visual_correction_example.png`
- `outputs/adult_census_income/figures/module2/mlp_training_curve.png`
- `outputs/adult_census_income/figures/module2/repeated_cv_stability.png`

## Reproducibility Commands
```bash
python3 -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/adult_census_income_final.ipynb --inplace --ExecutePreprocessor.timeout=5400
python3 -u -m unittest tests/test_preprocessing.py tests/test_models.py tests/test_evaluation.py tests/test_pipeline_smoke.py -v
./scripts/run_submission_checks.sh
```

## Verification Evidence
- Notebook execution log: `outputs/adult_census_income/evidence/notebook_execution_log_final.txt`
- Unit test log: `outputs/adult_census_income/evidence/tests_log_final.txt`
- Submission checks log: `outputs/adult_census_income/evidence/submission_checks_log_final.txt`
- Clean-room install attempt log: `outputs/adult_census_income/evidence/clean_room_install_attempt_final.txt`
- Agent interaction screenshots: `outputs/adult_census_income/interaction_log_images/`

## Section-6 Note
- Section `6.2` in the canonical notebook is the concise technical final bundle summarizing the project evolution and final evidence.
- Section `6.4` remains the detailed iteration narrative and decision rationale.
