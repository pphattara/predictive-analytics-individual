# Agent Usage Log: adult_census_income

## Iteration 1 Module 1 Entries

| # | Agent Task | Agent Output Summary | Your Decision | Rationale |
|---|---|---|---|---|
| 1 | Framing target/stakeholder | Proposed `income` and HR stakeholder | Accepted (verified) | Aligned with dataset structure and project scope. |
| 2 | Missingness handling | Suggested dropping missing rows | Modified | Switched to imputation to preserve data and class distribution. |
| 3 | Scaling recommendation | Suggested standard scaling everywhere | Rejected/Corrected | Robust scaling chosen due outlier-heavy gain/loss distributions. |

## Iteration 1 Module 2 Entries

| # | Agent Task | Agent Output Summary | Your Decision | Rationale |
|---|---|---|---|---|
| 4 | CV protocol recommendation | Suggested 5-fold stratified CV and fixed seed | Accepted (verified) | Matches class imbalance profile and reproducibility requirements. |
| 5 | Candidate model shortlist | Suggested broad family list including boosting libraries not installed | Modified | Constrained to sklearn-only stack (Logistic/RF/HGB/MLP) for environment compatibility. |
| 6 | Metric focus suggestion | Suggested emphasizing raw accuracy for model ranking | Rejected/Corrected | Retained weighted F1 as primary metric with PR-AUC/ROC-AUC/recall+calibration support for imbalance-aware selection. |

## Iteration 1 Module 3 Entries

| # | Agent Task | Agent Output Summary | Your Decision | Rationale |
|---|---|---|---|---|
| 7 | Failure-slice template | Suggested subgroup diagnostics for sex/race and behavior bands | Accepted (verified) | Directly supports fairness and operational risk analysis requirements. |
| 8 | Interpretability method | Proposed SHAP by default | Modified | Used permutation importance due dependency/lightweight constraints while retaining model-agnostic interpretability. |
| 9 | Deployment recommendation | Suggested static threshold without stress test | Rejected/Corrected | Added threshold stress testing and explicit do-not-use conditions for safer deployment guidance. |

## Iteration 2 Entries

| # | Agent Task | Agent Output Summary | Your Decision | Rationale |
|---|---|---|---|---|
| 10 | Coursework-step structure alignment | Suggested direct mapping of all analysis to six brief headings | Accepted (verified) | Improved report traceability and ensured full coverage of required sections. |
| 11 | Notebook sectioning strategy | Suggested moving code into clearly labelled chunked sections | Modified | Kept sectioned structure but added concise explanatory markdown per chunk for clarity. |
| 12 | Export strategy | Suggested keeping auxiliary markdown artefacts mandatory | Rejected/Corrected | Prioritized notebook-first evidence and kept markdown as support, not dependency. |

## Iteration 3 Entries

| # | Agent Task | Agent Output Summary | Your Decision | Rationale |
|---|---|---|---|---|
| 13 | Visual rubric uplift | Suggested adding leakage, heatmap, bivariate and outlier diagnostics | Accepted (verified) | Closed known marking gaps and linked visuals to preprocessing/model decisions. |
| 14 | Model improvement path | Suggested principled hyperparameter tuning and learning curve checks | Accepted (verified) | Added RandomizedSearchCV and learning diagnostics with persisted tuning summary. |
| 15 | Marking-compliance shortcuts | Suggested relying on metric improvements without execution evidence | Rejected/Corrected | Enforced saved notebook outputs/execution counts for reproducibility and marking proof. |

## Iteration 4 Entries

| # | Agent Task | Agent Output Summary | Your Decision | Rationale |
|---|---|---|---|---|
| 16 | Final narrative polish | Suggested figure-numbered argument-led rewrite with quantified gains | Accepted (verified) | Strengthened report coherence and criterion-3 evidence quality. |
| 17 | Reflection depth | Suggested expanding agent reflection with verification strategy detail | Modified | Kept concise but added explicit verification layers and consequence-focused discussion. |
| 18 | Packaging scope | Suggested broad repo-wide cleanup before submission | Rejected/Corrected | Scoped changes to `assignment_final` only to protect stable workspace history. |

## Final Submission Entries

| # | Agent Task | Agent Output Summary | Your Decision | Rationale |
|---|---|---|---|---|
| 19 | Final package assembly | Suggested consolidating Adult artefacts into a single submission folder | Accepted (verified) | Produced `assignment_final` with notebooks, data, outputs, scripts, configs and dependencies. |
| 20 | Final evidence checks | Suggested explicit section-level log completeness validation | Accepted (verified) | Added ordered heading checks to prevent ambiguity about iteration coverage. |
