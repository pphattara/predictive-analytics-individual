# Predictive Analytics 90+ Checklist

---

## 1. Problem Framing & Dataset Selection

- [ ] Choose a dataset with inherent complexity (real-world, messy data preferred over clean Kaggle benchmarks)
  - [ ] Mixed feature types: numerical, categorical, text, and/or temporal
  - [ ] Some missingness or noise present
  - [ ] Meaningful target variable with real-world implications
  - [ ] Enough rows to support train/validation/test splits without overfitting concerns
- [ ] Frame the problem with precision
  - [ ] Define the exact target variable and describe its distribution
  - [ ] Articulate who would use this prediction and why
  - [ ] Specify quantitative success criteria (e.g., "RMSE below X corresponds to actionable accuracy for stakeholder Y")
  - [ ] State explicit constraints (interpretability, latency, fairness across protected groups)
  - [ ] Declare assumptions and limitations upfront in the report introduction
- [ ] Agent tooling plan documented before coding begins
  - [ ] Write a delegation plan: what the agent will do vs. what you will personally verify
  - [ ] Plan appears in both the report introduction and the repo README

---

## 2. Exploratory Data Analysis — Visualisation (25 marks)

### Target Variable Analysis
- [ ] Plot target variable distribution and explain modelling implications
  - [ ] Skewness → consider log-transform
  - [ ] Heavy tails → consider robust methods
  - [ ] Class imbalance → plan stratified sampling and appropriate metrics

### Feature Analysis
- [ ] Univariate distributions for all features (histograms, KDE)
- [ ] Bivariate relationships between each feature and the target
- [ ] Correlation heatmap produced
- [ ] Non-linear relationships discussed (correlations alone are insufficient)

### Missingness Analysis
- [ ] Missingness matrix created (e.g., using `missingno` library)
- [ ] Each missing feature classified: MCAR, MAR, or MNAR
- [ ] Missingness pattern directly linked to chosen imputation strategy

### Leakage Detection
- [ ] Bar chart of feature–target correlations created
- [ ] "Suspicion threshold" line annotated on the chart
- [ ] Checked for features with suspiciously high correlation (near 1.0) with target
- [ ] Confirmed all features would be available at prediction time in real deployment
- [ ] Temporal ordering checked to rule out information leakage

### Outlier Analysis
- [ ] Visual outlier analysis performed (box plots, scatter plots)
- [ ] Quantitative method applied (e.g., Isolation Forest, DBSCAN cluster assignment)
- [ ] Decision on outlier treatment explicitly justified ("keeping because they represent real edge cases" is valid)

### Class Imbalance (Classification only)
- [ ] Imbalance ratio shown visually
- [ ] Metric choice implications discussed (accuracy misleading; prefer F1, AUC-ROC, PR curves)
- [ ] Resampling strategy previewed

### Visualisation Design Quality
- [ ] Consistent colour palette used throughout
- [ ] All axes clearly labelled with units
- [ ] Titles state the insight, not just the variable (e.g., "Feature X is Right-Skewed — Log Transform Recommended")
- [ ] Appropriate chart types chosen for each purpose
- [ ] Key observations annotated directly on plots
- [ ] Chart junk removed (no 3D pies, no default matplotlib styling, no unnecessary gridlines)
- [ ] Agent-generated plots critically evaluated and corrected where needed
- [ ] At least one instance of correcting an agent visualisation documented

---

## 3. Data Preparation — Methodology (25 marks)

### Splitting
- [ ] Train/validation/test split performed **before** any data-dependent preprocessing
- [ ] Temporal data uses time-based splits (not random splits)
- [ ] Stratified splitting used for imbalanced classification problems

### Pipeline
- [ ] scikit-learn `Pipeline` (or equivalent) used to prevent leakage
- [ ] All transformers fitted on training data only, applied to validation/test

### Feature Engineering
- [ ] Interaction features, polynomial features, or domain-specific transforms considered
- [ ] Every engineered feature justified with a reason it might be predictive
- [ ] No random feature additions without explanation

### Preprocessing Decisions Justified
- [ ] Scaling method chosen with justification (StandardScaler vs. RobustScaler vs. quantile transform)
- [ ] Imputation strategy justified based on missingness type (MCAR/MAR/MNAR)
- [ ] Encoding strategy for categorical features explained

### Data Validation After Preprocessing
- [ ] Confirmed no NaN values remain (or documented why acceptable)
- [ ] Feature distributions in train and validation sets compared for distribution shift
- [ ] Verified no target leakage introduced during preprocessing
- [ ] dtypes and categorical encodings verified as correct
- [ ] Explicit assertions or tests written in code for the above checks
- [ ] Agent preprocessing suggestions critically evaluated (e.g., scaler appropriateness verified)

---

## 4. Modelling — Methodology & Analysis (25 marks)

### Baseline
- [ ] Simple baseline model established (mean prediction for regression, majority class or logistic regression for classification)
- [ ] Baseline performance documented as the floor all models must beat

### Model Comparison
- [ ] At least one simple/linear model included (logistic regression, Ridge, Lasso)
- [ ] At least one tree-based ensemble included (Random Forest, XGBoost, LightGBM)
- [ ] At least one modern approach included (MLP, CNN, LSTM, Transformer — justified by data structure)
- [ ] Each architecture choice explicitly justified

### Ablation Studies
- [ ] Ablation table created with columns: Experiment, Change Made, Metric Result, Conclusion
- [ ] Effect of removing feature engineering tested
- [ ] Effect of different imputation strategy tested
- [ ] Effect of class weighting tested (if applicable)
- [ ] At least 3 ablation experiments documented

### Hyperparameter Tuning
- [ ] Principled tuning strategy used (grid search, randomised search, or Bayesian optimisation e.g. Optuna)
- [ ] Tuning performed using cross-validation on training set only (test set never touched)
- [ ] Search space documented
- [ ] Best parameters recorded
- [ ] Visualisation of performance across hyperparameter space included (optional but strong)

### Cross-Validation
- [ ] Stratified k-fold used for classification; regular k-fold or time-series split for regression/temporal
- [ ] Mean **and** standard deviation of metrics reported across folds
- [ ] High variance across folds discussed if present

### Agent Mistake — Documented
- [ ] At least one clear agent mistake caught, documented, and corrected
  - [ ] Examples: wrong metric for imbalanced data, leakage introduced, buggy training loop, overly complex architecture
  - [ ] Explanation of what would have gone wrong included
  - [ ] Correction and verification shown

---

## 5. Evaluation & Error Analysis

### Classification Metrics
- [ ] Confusion matrix produced (normalised)
- [ ] Precision-recall curves produced (especially for imbalanced data)
- [ ] ROC curve with AUC score produced
- [ ] Calibration plot produced (are predicted probabilities meaningful?)
- [ ] Per-class performance breakdown included

### Regression Metrics
- [ ] Residuals vs. predicted values plotted (check heteroscedasticity)
- [ ] Residuals vs. each feature plotted (check non-linear patterns)
- [ ] Q-Q plot of residuals produced (check normality assumptions)
- [ ] Worst predictions identified and analysed

### Failure Mode Analysis
- [ ] Worst-performing subset of data identified
- [ ] Characteristics of failure cases described (demographic group, value range, data quality issue)
- [ ] Deployment risk implications discussed

### Learning & Training Curves
- [ ] Learning curves (performance vs. training set size) plotted
- [ ] Training curves (loss/metric vs. epoch) plotted for neural net models
- [ ] Overfitting/underfitting behaviour interpreted

### Model Interpretability
- [ ] Feature importance or SHAP values computed
- [ ] Permutation importance or partial dependence plots included
- [ ] Model's learned relationships verified for domain plausibility

---

## 6. Final Narrative — Argument (25 marks)

### Report Structure (~2000 words)
- [ ] **Introduction** (~200 words): problem motivation, dataset summary, success criteria, one-sentence result preview
- [ ] **Methodology** (~600 words): EDA insights that drove decisions, preprocessing rationale, model selection logic, experimental design
- [ ] **Results** (~600 words): model comparison table, best model deep-dive with error analysis, ablation/sensitivity findings
- [ ] **Discussion** (~400 words): limitations and deployment risks, critical reflection on agent tooling, next steps
- [ ] **Model Card Summary** (~200 words): intended use, out-of-scope uses, data provenance, evaluation metrics and caveats, ethical considerations

### Writing Quality
- [ ] Every sentence presents evidence or advances an argument (no filler)
- [ ] Active voice used throughout
- [ ] All claims quantified (e.g., "F1 improved from 0.72 to 0.81, a 12.5% relative gain")
- [ ] All figures and tables referenced by number in the text
- [ ] Concise — no padding or repetition

### Critical Reflection on Agent Tooling
- [ ] Analysis of where delegation worked well
- [ ] Analysis of where time was wasted fixing agent outputs
- [ ] Verification strategies assessed for effectiveness
- [ ] Metacognitive layer present (not just listing what the agent did)

---

## 7. Code & Repository — Code/Markup (25 marks)

### Repository Structure
- [ ] `README.md` with clear run instructions and environment setup
- [ ] `requirements.txt` or `environment.yml` with **pinned** package versions
- [ ] `data/README.md` with data access instructions and license info
- [ ] `notebooks/analysis.ipynb` — clean, well-documented notebook
- [ ] `src/` directory with modular Python files (preprocessing, models, evaluation)
- [ ] `tests/` directory with at least a few unit tests
- [ ] `outputs/` directory for saved models, figures, and metrics

### Code Quality
- [ ] Functions used (no copy-pasted blocks)
- [ ] Docstrings written for all functions
- [ ] Type hints added where helpful
- [ ] Consistent naming conventions throughout
- [ ] No dead code or commented-out experiments left in
- [ ] Markdown cells in notebooks explain the "why" between code blocks

### Reproducibility
- [ ] Random seeds set everywhere (numpy, torch, sklearn, etc.)
- [ ] Environment file with pinned package versions present
- [ ] Data loading works from the repo root without modification
- [ ] All outputs (figures, metrics, models) saved to files so they can be regenerated

### Tests / Validation
- [ ] Explicit assertions written in code (e.g., `assert X_train.shape[0] == expected_rows`)
- [ ] Unit tests written for at least core preprocessing functions
- [ ] Pipeline tested for correct handling of missing values

### Attribution
- [ ] Agent-generated code clearly marked with comments
- [ ] Modified-from-agent code clearly marked
- [ ] Scratch-written code clearly marked
- [ ] Attribution approach documented in README

---

## 8. Agent Usage Log & Decision Register (Appendix)

- [ ] Meaningful interaction logs included (not trivial ones)
- [ ] Prompts shown alongside agent outputs and your decisions
- [ ] Screenshots or exports are readable and annotated with commentary
- [ ] Decision register table completed with columns:
  - `#` | `Agent Task` | `Agent Output Summary` | `Your Decision` | `Rationale`
- [ ] At least one **acceptance** entry (agent output accepted after verification)
- [ ] At least one **partial rejection** entry (agent output partially modified)
- [ ] At least one clear **rejection/correction** entry (agent output rejected and corrected)

---

## Final Self-Check — Distinguishing 90+ from 70–80

- [ ] Every visualisation informs a specific modelling decision
- [ ] Experimental methodology is systematic with ablations and controlled comparisons
- [ ] Error analysis goes deep into failure modes and deployment risks
- [ ] Code is professional and immediately reproducible by a stranger
- [ ] Narrative is concise, evidence-driven, and quantified throughout
- [ ] Agent tooling is used strategically with documented verification — including catching at least one mistake
- [ ] **Intellectual ownership is demonstrated throughout** — every decision is yours, justified, and documented
