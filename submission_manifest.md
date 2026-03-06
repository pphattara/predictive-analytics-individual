# Submission Manifest — Adult Census Income (Final)

## Canonical Items

- Final report (submission): `report_final.pdf`
- Canonical notebook: `notebooks/adult_census_income_final.ipynb`
- Final outputs folder: `outputs/adult_census_income/`
- Dataset path: `data/raw/adult_census_income/adult.csv`

## Reproduction Commands

```bash
python3 -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/adult_census_income_final.ipynb --inplace --ExecutePreprocessor.timeout=5400
python3 -u -m unittest tests/test_preprocessing.py tests/test_models.py tests/test_evaluation.py tests/test_pipeline_smoke.py -v
./scripts/run_submission_checks.sh
```

## Key Output Artefacts

- `outputs/adult_census_income/metrics/evaluation_report.json`
- `outputs/adult_census_income/metrics/threshold_policy.json`
- `outputs/adult_census_income/metrics/final_solution_bundle.json`
- `outputs/adult_census_income/metrics/model_comparison_cv.csv`
- `outputs/adult_census_income/metrics/ablation_results.csv`
- `report_final.pdf`
- `outputs/adult_census_income/models/best_model_module2.pkl`

## Agent Evidence

- `outputs/adult_census_income/agent_log.md`
- `outputs/adult_census_income/decision_register.pdf`
- `outputs/adult_census_income/evidence/`

## Verification Logs

- `outputs/adult_census_income/evidence/notebook_execution_log_final.txt`
- `outputs/adult_census_income/evidence/tests_log_final.txt`
- `outputs/adult_census_income/evidence/submission_checks_log_final.txt`

## Final Verification Date

- `2026-03-06`
