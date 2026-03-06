"""
Rebuild iteration4 notebook:
  1. Fix attribution tags (3 distinct types: Agent-generated / Modified-from-agent / Scratch-written)
  2. Remove noise cells (Iteration Label, empty heading, Figure-Numbered Summary, Output Summary)
  3. Simplify verbose markdown - strip "What this does / How to use" boilerplate
  4. Add numbered sub-headings (1.1, 1.2, 2.1 ...)
  5. Add Table of Contents as first cell
  6. Keep Column Meanings table under step 2 EDA (rename to numbered heading)
  7. Keep Agent Mistake narrative cell (C3 marks)
"""
import json, copy, re
from pathlib import Path

NB_PATH = Path(__file__).parent.parent / "notebooks/adult_census_income_iteration4_six_steps.ipynb"
BACKUP  = NB_PATH.with_suffix(".ipynb.bak")

nb = json.loads(NB_PATH.read_text(encoding="utf-8"))
cells = nb["cells"]

# ── 1. ATTRIBUTION MAP  (by code-cell index within code cells list) ───────────
# Cell numbering = order in code_cells (0-based)
ATTRIBUTION = {
    0:  "[Modified-from-agent]",   # setup/paths — agent scaffold, modified for project
    1:  "[Scratch-written]",        # problem framing — stakeholder/criteria written by student
    2:  "[Modified-from-agent]",   # load + normalize data
    3:  "[Modified-from-agent]",   # EDA target distribution
    4:  "[Modified-from-agent]",   # EDA numeric distributions
    5:  "[Modified-from-agent]",   # EDA categorical cardinality
    6:  "[Modified-from-agent]",   # EDA missingness summary
    7:  "[Modified-from-agent]",   # EDA feature-target signal
    8:  "[Modified-from-agent]",   # EDA leakage / correlation / bivariate / outlier
    9:  "[Modified-from-agent]",   # preprocessing pipeline + split
    10: "[Scratch-written]",        # preprocessing validation — assertions written from scratch
    11: "[Agent-generated]",        # modeling setup/helpers — template accepted as-is
    12: "[Modified-from-agent]",   # CV protocol — agent suggested, modified scoring
    13: "[Agent-generated]",        # baseline models — dummy+logistic template
    14: "[Modified-from-agent]",   # candidate model comparison — constrained to sklearn
    15: "[Modified-from-agent]",   # ablation studies
    16: "[Modified-from-agent]",   # hyperparameter tuning (RandomizedSearchCV)
    17: "[Modified-from-agent]",   # model selection + threshold tuning
    18: "[Modified-from-agent]",   # final test evaluation
    19: "[Modified-from-agent]",   # learning curve diagnostic
    20: "[Agent-generated]",        # module 3 setup — template accepted
    21: "[Modified-from-agent]",   # failure-slice analysis
    22: "[Modified-from-agent]",   # interpretability (SHAP→permutation importance)
    23: "[Scratch-written]",        # threshold stress test — written after agent rejection
    24: "[Scratch-written]",        # deployment risk statement — written after agent rejection
    25: "[Modified-from-agent]",   # module 3 summary artefact
    26: "[Modified-from-agent]",   # decision log + artifact checks
}

def apply_attribution(code_cells):
    for ci, c in enumerate(code_cells):
        tag = ATTRIBUTION.get(ci, "[Modified-from-agent]")
        src = "".join(c["source"])
        # replace existing attribution line
        new_src = re.sub(
            r"# Attribution: \[.*?\]",
            f"# Attribution: {tag}",
            src,
            count=1,
        )
        c["source"] = [new_src]

# ── 2. SECTION → SUB-SECTION NUMBERING MAP ───────────────────────────────────
# Original heading text → new numbered heading
HEADING_MAP = {
    # Step 1
    "Code Chunk 1: Environment and path setup":            "### 1.1 Environment and path setup",
    "Code Chunk 2: Problem framing metadata":              "### 1.2 Problem framing metadata",
    # Step 2
    "Code Chunk 3: Load and normalize raw data":           "### 2.1 Load and normalize raw data",
    "Code Chunk 4: EDA: target distribution":              "### 2.2 EDA: target distribution",
    "Code Chunk 5: EDA: numeric distributions":            "### 2.3 EDA: numeric distributions",
    "Code Chunk 6: EDA: categorical cardinality":          "### 2.4 EDA: categorical cardinality",
    "Code Chunk 7: EDA: missingness summary":              "### 2.5 EDA: missingness summary",
    "Code Chunk 8: EDA: feature-target signal check":      "### 2.6 EDA: feature-target signal check",
    "Code Chunk 8B: EDA leakage, correlation, bivariate, and outlier diagnostics":
                                                           "### 2.7 EDA: leakage, correlation, bivariate and outlier diagnostics",
    "Ambiguous Column Meanings":                           "### 2.8 Column meanings reference",
    # Step 3
    "Code Chunk 9: Preprocessing pipeline + data split":   "### 3.1 Preprocessing pipeline and data split",
    "Code Chunk 10: Preprocessing validation + log":        "### 3.2 Preprocessing validation",
    # Step 4
    "Code Chunk 11: Modeling setup and helpers":            "### 4.1 Modeling setup and helpers",
    "Code Chunk 12: CV protocol definition":                "### 4.2 CV protocol",
    "Code Chunk 13: Baseline models":                       "### 4.3 Baseline models",
    "Code Chunk 14: Candidate model comparison":            "### 4.4 Candidate model comparison",
    "Code Chunk 15: Ablation studies":                      "### 4.5 Ablation studies",
    "Code Chunk 15B: Principled Hyperparameter Tuning (HistGradientBoosting)":
                                                            "### 4.6 Hyperparameter tuning",
    # Step 5
    "Code Chunk 16: Model selection + threshold tuning":    "### 5.1 Model selection and threshold tuning",
    "Code Chunk 17: Final test evaluation":                  "### 5.2 Final test evaluation",
    "Code Chunk 17B: Learning Curve Diagnostic":             "### 5.3 Learning curve diagnostic",
    "Code Chunk 18: Module 3 setup":                         "### 5.4 Deep-evaluation setup",
    "Code Chunk 19: Failure-slice analysis":                 "### 5.5 Failure-slice analysis",
    "Code Chunk 20: Interpretability":                       "### 5.6 Interpretability",
    "Code Chunk 21: Threshold stress testing":               "### 5.7 Threshold stress testing",
    # Step 6
    "Code Chunk 22: Deployment risk statement":              "### 6.1 Deployment risk statement",
    "Code Chunk 23: Module 3 summary artefact":              "### 6.2 Summary artefact",
    "Agent Mistake Caught and Corrected (Explicit Narrative)": "### 6.3 Agent mistake caught and corrected",
    "Code Chunk 24: Decision log + artifact checks":         "### 6.4 Decision log and artefact checks",
}

# ── 3. TABLE OF CONTENTS ──────────────────────────────────────────────────────
TOC_SOURCE = """# Adult Census Income — Predictive Analytics Coursework

## Table of Contents

**1. Obtain a dataset and frame the predictive problem**
- 1.1 Environment and path setup
- 1.2 Problem framing metadata

**2. Explore the data to gain insights**
- 2.1 Load and normalize raw data
- 2.2 EDA: target distribution
- 2.3 EDA: numeric distributions
- 2.4 EDA: categorical cardinality
- 2.5 EDA: missingness summary
- 2.6 EDA: feature-target signal check
- 2.7 EDA: leakage, correlation, bivariate and outlier diagnostics
- 2.8 Column meanings reference

**3. Prepare the data**
- 3.1 Preprocessing pipeline and data split
- 3.2 Preprocessing validation

**4. Explore different models and shortlist the best ones**
- 4.1 Modeling setup and helpers
- 4.2 CV protocol
- 4.3 Baseline models
- 4.4 Candidate model comparison
- 4.5 Ablation studies
- 4.6 Hyperparameter tuning

**5. Fine-tune and evaluate**
- 5.1 Model selection and threshold tuning
- 5.2 Final test evaluation
- 5.3 Learning curve diagnostic
- 5.4 Deep-evaluation setup
- 5.5 Failure-slice analysis
- 5.6 Interpretability
- 5.7 Threshold stress testing

**6. Present the final solution**
- 6.1 Deployment risk statement
- 6.2 Summary artefact
- 6.3 Agent mistake caught and corrected
- 6.4 Decision log and artefact checks
"""

def make_toc_cell():
    return {
        "cell_type": "markdown",
        "id": "toc-cell-auto",
        "metadata": {},
        "source": [TOC_SOURCE],
    }

# ── 4. CELLS TO REMOVE (by their original 0-based index in nb['cells']) ───────
# We remove: Iteration Label [1], empty "Column Meaning Notes" header [7],
#            Figure-Numbered Summary [65], Output Summary [66]
REMOVE_INDICES = {1, 7, 65, 66}

# ── 5. SIMPLIFY VERBOSE MARKDOWN CELLS ────────────────────────────────────────
def simplify_markdown(src: str, new_heading: str) -> str:
    """Keep only the new heading and the column meanings table (if present)."""
    # If this is the column meanings cell, keep the table beneath the new heading
    if "fnlwgt" in src or "education.num" in src:
        # Find the table portion
        lines = src.split("\n")
        table_start = next((i for i, l in enumerate(lines) if l.startswith("|")), None)
        if table_start is not None:
            table = "\n".join(lines[table_start:]).strip()
            caveat_line = next(
                (l for l in lines if "Interpretation caveat" in l), ""
            )
            body = table
            if caveat_line:
                body += f"\n\n*{caveat_line.strip()}*"
            return f"{new_heading}\n\n{body}"
    # For all other cells, just return the heading
    return new_heading

# ── MAIN REBUILD ──────────────────────────────────────────────────────────────

# Step A: apply attribution to code cells
code_cells = [c for c in cells if c["cell_type"] == "code"]
apply_attribution(code_cells)

# Step B: rebuild the cell list
new_cells = []

# Insert ToC as very first cell
new_cells.append(make_toc_cell())

for orig_idx, c in enumerate(cells):
    # Skip removed cells
    if orig_idx in REMOVE_INDICES:
        continue

    if c["cell_type"] == "markdown":
        src = "".join(c["source"])
        # Check if this cell needs heading replacement
        replaced = False
        for old_title, new_heading in HEADING_MAP.items():
            if old_title in src:
                new_src = simplify_markdown(src, new_heading)
                c2 = copy.deepcopy(c)
                c2["source"] = [new_src]
                new_cells.append(c2)
                replaced = True
                break
        if not replaced:
            # Keep cell as-is (main section headers, agent narrative, etc.)
            # But update the main title
            if src.startswith("# Adult Census Income"):
                # Skip old title — we already have ToC as first cell
                continue
            new_cells.append(c)
    else:
        new_cells.append(c)

nb["cells"] = new_cells

# Backup original, write new
BACKUP.write_bytes(NB_PATH.read_bytes())
NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")

print(f"Rebuilt notebook: {NB_PATH}")
print(f"Original backed up to: {BACKUP}")
print(f"Total cells before: {len(cells)} → after: {len(new_cells)}")
code_after = sum(1 for c in new_cells if c["cell_type"] == "code")
md_after   = sum(1 for c in new_cells if c["cell_type"] == "markdown")
print(f"Code cells: {code_after} | Markdown cells: {md_after}")
