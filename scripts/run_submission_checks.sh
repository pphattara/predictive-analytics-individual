#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

NOTEBOOK_PATH="notebooks/adult_census_income_final.ipynb"

echo "[1/3] Notebook execution-state check: ${NOTEBOOK_PATH}"
python3 -u - <<'PY'
import json
from pathlib import Path

nb_path = Path('notebooks/adult_census_income_final.ipynb')
nb = json.loads(nb_path.read_text(encoding='utf-8'))
code_cells = [c for c in nb.get('cells', []) if c.get('cell_type') == 'code']
none_exec = [
    i for i, c in enumerate(nb.get('cells', []))
    if c.get('cell_type') == 'code' and c.get('execution_count') is None
]
if not code_cells:
    raise SystemExit('No code cells found in canonical notebook.')
if none_exec:
    raise SystemExit(f'Notebook has unexecuted code cells at indices: {none_exec}')
print(f'Notebook execution state OK: {len(code_cells)} code cells, all executed.')
PY

echo "[2/3] Running tests"
python3 -u -m unittest \
  tests/test_preprocessing.py \
  tests/test_models.py \
  tests/test_evaluation.py \
  tests/test_pipeline_smoke.py \
  -v

echo "[3/3] Running final package assertions"
python3 -u - <<'PY'
from pathlib import Path
import json
import subprocess

root = Path('.').resolve()
out = root / 'outputs' / 'adult_census_income'
metrics = out / 'metrics'
figs = out / 'figures'

required = [
    root / 'README.md',
    root / 'requirements.txt',
    root / 'report_final.pdf',
    root / 'submission_manifest.md',
    root / 'notebooks' / 'adult_census_income_final.ipynb',
    root / 'data' / 'raw' / 'adult_census_income' / 'adult.csv',
    metrics / 'preprocessing_validation.json',
    metrics / 'model_comparison_cv.csv',
    metrics / 'ablation_results.csv',
    metrics / 'evaluation_report.json',
    metrics / 'threshold_policy.json',
    metrics / 'final_solution_bundle.json',
    out / 'agent_log.md',
    out / 'decision_register.pdf',
    figs / 'target_distribution.png',
    figs / 'missingness_summary.png',
    figs / 'module2' / 'confusion_matrix.png',
    figs / 'module2' / 'roc_curve.png',
    figs / 'module2' / 'pr_curve.png',
]
missing = [str(p) for p in required if not p.exists() or p.stat().st_size == 0]
if missing:
    raise SystemExit(f'Missing/empty required artifacts: {missing}')

tracked_files = subprocess.run(
    ['git', 'ls-files', '-z'],
    cwd=root,
    check=True,
    capture_output=True,
    text=False,
).stdout.split(b'\x00')
tracked_dsstore = [path.decode('utf-8') for path in tracked_files if path and path.decode('utf-8').endswith('.DS_Store')]
if tracked_dsstore:
    raise SystemExit(f'Found tracked .DS_Store files in repository: {tracked_dsstore}')
if any(out.glob('~$*.docx')):
    raise SystemExit('Found temporary Office lock files in outputs/adult_census_income')

payload = json.loads((metrics / 'evaluation_report.json').read_text(encoding='utf-8'))
for k in ['module', 'dataset', 'selection', 'test_metrics']:
    if k not in payload:
        raise SystemExit(f'evaluation_report.json missing key: {k}')

print('Artifact assertions passed.')
PY

echo "Submission checks completed successfully"
