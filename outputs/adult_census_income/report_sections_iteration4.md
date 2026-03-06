# Adult Census Income Project Report (Iteration 4 Draft)

## 1. Introduction
This project addresses a policy-relevant classification problem: predicting whether an individual's annual income exceeds $50K using the Adult Census Income dataset. The intended decision context is workforce and social-policy analytics, where analysts need a ranked risk signal to prioritize interventions, triage review effort, or simulate policy impact under limited operational capacity. In this context, a model is only useful if its probabilities are calibrated enough to support threshold policy, and if performance remains acceptable for subgroups that could be disproportionately affected by errors.

The dataset contains 32,561 records with 14 predictors and one binary target (`income`). Predictors include six numeric variables (`age`, `fnlwgt`, `education.num`, `capital.gain`, `capital.loss`, `hours.per.week`) and eight categorical variables (`workclass`, `education`, `marital.status`, `occupation`, `relationship`, `race`, `sex`, `native.country`). The target distribution is imbalanced: 24,720 instances of `<=50K` (75.92%) and 7,841 instances of `>50K` (24.08%), as shown in **Figure 1**.

Success criteria were fixed before modelling to prevent post-hoc metric selection. The primary criterion is weighted F1 >= 0.82. Two operational constraints are coupled to that objective: positive-class recall >= 0.75 and low calibration error to support policy thresholding. This choice reflects stakeholder needs: missing truly high-income cases reduces intervention quality, while poorly calibrated probabilities make threshold-based deployment brittle.

The final selected model is a tuned HistGradientBoosting pipeline with a validated operating threshold of 0.36. On the held-out test split it achieves weighted F1 = 0.8622, PR-AUC = 0.8282, ROC-AUC = 0.9259, recall-positive = 0.7840, and calibration error = 0.0139. This exceeds all predefined success criteria while preserving a transparent risk-governance discussion in the final section.

## 2. Methodology
The methodology is organized around decisions supported by evidence, not chronology. The pipeline enforces split-first discipline, leakage protection, reproducibility, and controlled comparison so that improvements can be trusted as causal consequences of design changes rather than accidental data contamination.

### 2.1 EDA findings that directly changed pipeline choices
**Class imbalance and split strategy.** **Figure 1** confirms a 3:1 class ratio, which makes raw accuracy an unsuitable primary objective. This directly motivated three choices: stratified splitting, weighted F1 as the main model-selection metric, and recall-positive as a hard secondary constraint.

**Missingness mechanism and imputation policy.** **Figure 2** and `missingness_mechanism_notes.csv` show that missingness is concentrated in `occupation` (5.66%), `workclass` (5.64%), and `native.country` (1.79%). These are likely MAR/MNAR patterns rather than pure MCAR. Consequently, row deletion was rejected because it would amplify representation distortion in already under-represented subgroups. The selected policy uses most-frequent imputation for categorical variables and median imputation for numeric variables.

**Leakage and redundancy diagnostics.** **Figure 3** (target-correlation leakage suspicion chart) shows no numeric feature crossing the 0.9 suspicion threshold. This allowed retention of all numeric features while still documenting leakage checks explicitly. **Figure 4** (numeric correlation heatmap) informed interpretation of co-movement between numeric fields and reduced risk of over-interpreting a single correlated variable.

**Distribution tails and scaling choice.** **Figure 5** and **Figure 6** (IQR outlier rates and isolation-based outlier diagnostic) show highly skewed and heavy-tailed patterns in `capital.gain` and `capital.loss`. This evidence justified robust scaling in the reference preprocessing pipeline. Standard scaling was kept only as a controlled ablation, not as default.

### 2.2 Data preparation and leakage control
Data preparation follows a strict train/validation/test split of 70/15/15 with `random_state=42` and stratification by target. The resulting split sizes are 22,792 (train), 4,884 (validation), and 4,885 (test). All transformers are fit on training data only and then applied to validation/test. This preserves test integrity and prevents target leakage through preprocessing statistics.

The preprocessing pipeline is:
- Numeric branch: median imputation plus robust scaling.
- Categorical branch: most-frequent imputation plus one-hot encoding with unknown-category safety.

Post-transform assertions are treated as hard gates before modelling: no NaN in transformed arrays, equal transformed dimensionality across splits, and class-balance preservation after split. These checks are persisted in `preprocessing_validation.json` and were rerun during Iteration 4 execution.

### 2.3 Model families, experimental design, and selection logic
A floor baseline and a meaningful linear baseline were established first:
- DummyClassifier (`most_frequent`) as non-informative floor.
- Logistic Regression as interpretable linear baseline.

Four non-trivial model families were then compared with a consistent protocol:
- Logistic Regression
- Random Forest
- HistGradientBoosting
- MLPClassifier

Cross-validation uses `StratifiedKFold` (5 folds, shuffle, fixed seed) on the training split. Mean and standard deviation are reported for weighted F1, alongside PR-AUC, ROC-AUC, and recall-positive. Runtime is also recorded to keep deployment feasibility visible.

The shortlist and final pick use a two-stage rule:
1. Rank by CV mean weighted F1 while checking fold stability (`cv_std`).
2. Enforce recall-positive and calibration constraints during threshold selection.

### 2.4 Ablation design and tuning
Ablations were designed as single-change interventions to isolate causal impact:
- Remove class weighting
- Replace robust scaler with standard scaler
- Drop `fnlwgt`
- Drop `education` or `education.num` separately
- Drop `capital.gain` and `capital.loss`

The ablation suite confirms that capital features are structurally important: removing them drops CV weighted F1 from 0.8688 to 0.8381 (absolute -0.0308). By contrast, dropping either `education` text or `education.num` causes only marginal change, indicating controlled redundancy in that feature pair.

Hyperparameter tuning was conducted with `RandomizedSearchCV` over HistGradientBoosting settings (`learning_rate`, `max_leaf_nodes`, `min_samples_leaf`, `l2_regularization`, `max_iter`) using CV scoring on weighted F1. Best parameters were:
- `learning_rate`: 0.08
- `max_leaf_nodes`: 31
- `min_samples_leaf`: 10
- `l2_regularization`: 0.1
- `max_iter`: 300

These settings yield a tuned candidate (`tree_hgb_tuned`) that modestly improves CV weighted F1 from 0.8688 to 0.8695 while preserving low fold variance.

## 3. Results
### 3.1 Model comparison
**Table 1** summarises the model shortlist under consistent 5-fold CV.

| Table 1. Model comparison (5-fold CV on train split) | Val weighted F1 (mean ± std) | Val AUC-PR | Val ROC-AUC | Val recall-positive | Notes |
|---|---:|---:|---:|---:|---|
| Logistic Regression | 0.8211 ± 0.0051 | 0.7661 | 0.9071 | 0.8506 | Strong linear baseline, high recall |
| Random Forest | 0.8511 ± 0.0076 | 0.7660 | 0.9044 | 0.6181 | Higher F1 than logistic but less recall |
| MLPClassifier | 0.8511 ± 0.0025 | 0.7780 | 0.9107 | 0.6291 | Stable but not best |
| HistGradientBoosting (untuned) | 0.8688 ± 0.0028 | 0.8274 | 0.9273 | 0.6566 | Best untuned model |
| HistGradientBoosting (tuned) | 0.8695 ± 0.0027 | 0.8304 | 0.9286 | 0.6606 | Best overall shortlist candidate |

Compared with logistic baseline, tuned HistGradientBoosting improves CV weighted F1 by +0.0483 absolute (+5.89% relative). Compared with untuned HistGradientBoosting, tuning adds +0.0006 absolute (+0.07% relative), which is small but directionally consistent and achieved with transparent search-space documentation.

### 3.2 Baseline and threshold-policy evidence
Validation baselines in `evaluation_report.json` show why a floor baseline is necessary:
- Dummy validation weighted F1 = 0.6553, recall-positive = 0.0000.
- Logistic baseline validation weighted F1 = 0.8180, recall-positive = 0.8469.

Dummy performance confirms that majority prediction alone is unusable for the positive class. Logistic establishes a realistic linear benchmark and highlights the precision-recall trade-off under imbalance.

Threshold stress testing (see **Figure 15**) reveals the expected trade-off: lower thresholds increase recall but sharply raise positive-rate and false positives; higher thresholds improve precision at the cost of recall-positive. The selected threshold (0.36) was chosen because it satisfies recall constraints on validation while preserving strong weighted F1. This is a deployment-policy choice, not just a metric-optimization artifact.

### 3.3 Held-out test performance and model behaviour
After model and threshold freeze, evaluation was run once on the untouched test split.
- Weighted F1: 0.8622
- PR-AUC: 0.8282
- ROC-AUC: 0.9259
- Recall-positive: 0.7840
- Calibration error: 0.0139
- Brier score: 0.0890

All predefined success criteria are met:
- Weighted F1 >= 0.82: achieved (0.8622)
- Recall-positive >= 0.75: achieved (0.7840)
- Calibration readiness: achieved (0.0139 calibration error)

**Figure 9** and **Figure 10** show strong ranking quality (PR and ROC behavior). **Figure 11** shows good probability calibration around operating ranges relevant to thresholding. **Figure 12** quantifies confusion-matrix trade-offs at the selected threshold and confirms that performance is not achieved by collapsing minority detection.

### 3.4 Ablation findings
**Table 2** reports key ablation outcomes.

| Table 2. Selected ablation outcomes (HistGradientBoosting family) | CV weighted F1 | Delta vs reference | Interpretation |
|---|---:|---:|---|
| Reference pipeline | 0.8688 | 0.0000 | Baseline for all ablations |
| Drop `education` text | 0.8693 | +0.0005 | `education.num` captures most signal |
| Drop `education.num` | 0.8681 | -0.0008 | Small drop, redundancy manageable |
| Drop `fnlwgt` | 0.8681 | -0.0008 | Limited but non-zero signal |
| No capital features | 0.8381 | -0.0308 | Largest degradation; capital fields are critical |

The most consequential ablation is removing `capital.gain` and `capital.loss`, which causes a substantial performance loss. This confirms that the model depends on economically meaningful predictors and supports retaining those variables with careful fairness interpretation.

### 3.5 Failure modes and interpretability
Subgroup slicing (see **Figure 14**) reveals uneven performance despite strong aggregate metrics. Recall-positive is notably lower in slices such as `relationship=Own-child` and younger age bands, which indicates that decision quality is not uniform across cohorts. This is operationally important: without slice monitoring, global metrics can hide localized failure.

Permutation importance (**Figure 16**) identifies top drivers: `marital.status`, `capital.gain`, `education.num`, `age`, and `occupation`. These are plausible and align with domain intuition, but they also reinforce the need for policy caution because some high-signal predictors correlate with sensitive socio-economic patterns.

Learning-curve diagnostics (**Figure 13**) show validation weighted F1 rising from ~0.852 at small sample size to ~0.869 at larger sample size, while training F1 declines from near-perfect overfit toward a narrower generalization gap. This pattern suggests the model is not underfitting and that additional data could still yield incremental gains.

## 4. Discussion
The final model is strong enough for decision support under controlled conditions, but it should not be treated as an autonomous decision-maker. Three risk categories matter most for deployment readiness.

**Distribution shift risk.** Adult Census-style tabular relationships can drift over time due to labor-market changes, reporting behavior changes, or policy interventions. Because the selected threshold is tuned to current class prevalence and score distributions, drift can silently degrade recall-positive or calibration. Operationally, threshold and calibration must be revalidated on a cadence tied to incoming data refresh.

**Fairness and subgroup risk.** Slice analysis shows uneven positive-class recall across groups, even when aggregate metrics are good. This means a single global threshold may produce asymmetric error burdens. The model should therefore be coupled to subgroup monitoring dashboards and escalation rules. At minimum, production governance should track recall-positive and error-rate by key demographic and structural slices, and trigger review when drift exceeds tolerance.

**Interpretability and accountability.** Permutation importance provides global explanations, but local decision accountability is still limited compared with rule-based systems. If this model informs high-impact human decisions, users need decision-support interfaces that expose confidence, top contributing factors, and fallback guidance when confidence is low.

### Critical reflection on agent tooling
Delegation worked well for scaffolding repetitive but high-risk tasks: consistent CV setup, artifact serialization, and figure-generation plumbing were produced quickly and then hardened by local checks. Delegation worked less well where context-sensitive statistical judgment was required. The clearest mistake was an early accuracy-first ranking suggestion on imbalanced data. If accepted, this would have rewarded majority-class performance while violating project objectives for positive-class detection.

The most effective verification strategy was layered, not single-step. First, each agent suggestion was translated into a falsifiable check (for example: does this change improve weighted F1 without violating recall constraints?). Second, changes were validated under fixed-seed CV and isolated ablations. Third, high-level claims were cross-checked against raw artifact files (`model_comparison_cv.csv`, `ablation_results.csv`, `threshold_stress.csv`) rather than trusting notebook prose. This reduced narrative drift and made corrections auditable.

If repeated, one change would improve efficiency: enforce a pre-commit checklist that blocks any recommendation lacking a corresponding artifact check and metric delta statement. This would have caught low-value suggestions earlier and reduced revision overhead in late iterations.

### Next steps
1. Add subgroup-aware threshold policy: evaluate whether one threshold per operational segment improves fairness without excessive complexity.
2. Expand interpretability from global permutation importance to local explanation traces for high-confidence errors.
3. Implement periodic drift tests (feature distribution drift, calibration drift, subgroup recall drift) and trigger threshold recalibration when thresholds are breached.

## 5. Model Card Summary
**Model name:** HistGradientBoosting Classifier v1.0 (tuned, thresholded)  
**Intended use:** Decision support for workforce/policy analytics where analysts prioritize review effort using calibrated income-risk probabilities.  
**Out-of-scope uses:** Fully automated high-stakes decisions, legal adjudication, or any context requiring deterministic justification without human oversight.  
**Training data:** Adult Census Income dataset, 32,561 rows, 14 predictors; class distribution 75.92% (`<=50K`) and 24.08% (`>50K`); known limitations include historical and socio-economic bias risks.  
**Evaluation:** Held-out test weighted F1 = 0.8622, PR-AUC = 0.8282, ROC-AUC = 0.9259, recall-positive = 0.7840, calibration error = 0.0139. Performance varies across slices (for example, lower recall in younger and `Own-child` relationship groups).  
**Ethical considerations:** Sensitive attributes (`sex`, `race`) and proxy variables can induce uneven error burden. Results must be monitored by subgroup and used only with human review.  
**Caveats:** Threshold and calibration are prevalence-sensitive; performance may degrade under distribution shift. Revalidation is required before policy transfer to new populations or time periods.
