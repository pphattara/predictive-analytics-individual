# Iteration 3 Kickoff: Fit Iteration 1 Into Coursework Step Headings

This document starts **Iteration 3** by consolidating all Iteration 1 work under the exact six headings from the coursework brief.

## 1. Obtain a dataset and frame the predictive problem
### Iteration 1 evidence fitted
- Dataset: `data/raw/adult_census_income/adult.csv`
- Prediction task: binary classification (`income >50K` vs `<=50K`)
- Framing artifact: `outputs/adult_census_income/problem_statement.md`
- Success metrics/constraints: weighted F1, recall-positive, calibration readiness, interpretability/fairness constraints.
- Agent-plan evidence: `outputs/adult_census_income/agent_log.md`.

### Iteration 3 follow-through
- Keep this heading in final report and make all claims explicitly metric-backed.

## 2. Explore the data to gain insights
### Iteration 1 evidence fitted
- Notebook EDA sections with inline plots and saved artefacts in `outputs/adult_census_income/figures/`.
- Coverage: target imbalance, distribution shape, missingness, categorical cardinality, feature-target checks.
- Explicit "insight -> preprocessing action" notes included.

### Iteration 3 follow-through
- In final write-up, reference each EDA figure by number and tie it to one downstream design decision.

## 3. Prepare the data
### Iteration 1 evidence fitted
- Split-first preprocessing pipeline implemented in notebook.
- Outputs: processed splits in `data/processed/adult_census_income/`.
- Validation checks in `outputs/adult_census_income/metrics/preprocessing_validation.json`:
  - no NaN across splits
  - equal transformed feature counts
  - stratified split discipline preserved.

### Iteration 3 follow-through
- Convert validation checks into a concise reproducibility checklist in the final appendix.

## 4. Explore different models and shortlist the best ones
### Iteration 1 evidence fitted
- Baselines + multi-family comparison completed.
- Candidate comparison: `outputs/adult_census_income/metrics/model_comparison_cv.csv`.
- Ablations: `outputs/adult_census_income/metrics/ablation_results.csv`.
- Selected family/variant rationale captured through CV mean/std and ablation results.

### Iteration 3 follow-through
- Present shortlisted models in one compact comparison table in the report.

## 5. Fine-tune and evaluate
### Iteration 1 evidence fitted
- Threshold policy: `outputs/adult_census_income/metrics/threshold_policy.json`.
- Core evaluation: `outputs/adult_census_income/metrics/evaluation_report.json` and module2 figures.
- Deep evaluation: failure slices, worst-case errors, permutation importance, threshold stress tests in module3 metrics/figures.
- Explicit caught agent mistake documented (accuracy-first framing corrected to imbalance-aware protocol).

### Iteration 3 follow-through
- Keep one explicit subsection titled "Agent mistake caught and correction" in report discussion.

## 6. Present the final solution
### Iteration 1 evidence fitted
- Final selected model: `outputs/adult_census_income/models/best_model_module2.pkl`.
- Final rationale and caveats: `evaluation_report.json`, `module3_deployment_risk.md`.
- Model-card style content already drafted in `outputs/adult_census_income/report_sections_draft.md`.

### Iteration 3 follow-through
- Finalize concise model-card paragraph with intended use, non-use, provenance, caveats, monitoring triggers.

## Iteration 3 Status
- Step-heading fit of Iteration 1 outputs: **completed**.
- Next immediate task: convert this structure into final submission prose with figure/table callouts and references.
