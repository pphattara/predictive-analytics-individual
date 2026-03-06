#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

NOTEBOOK_PATH="notebooks/adult_census_income_final.ipynb"
KERNEL_NAME="${KERNEL_NAME:-vscode-env}"
EXECUTE_NOTEBOOK="${EXECUTE_NOTEBOOK:-0}"

echo "[1/4] Notebook execution check: ${NOTEBOOK_PATH}"
if [[ "${EXECUTE_NOTEBOOK}" == "1" ]]; then
  echo "      EXECUTE_NOTEBOOK=1 -> running nbconvert execution pass"
  jupyter nbconvert \
    --to notebook \
    --execute "${NOTEBOOK_PATH}" \
    --inplace \
    --ExecutePreprocessor.timeout=5400 \
    --ExecutePreprocessor.kernel_name="${KERNEL_NAME}"
else
  echo "      EXECUTE_NOTEBOOK=0 -> validating saved execution state (no kernel launch)"
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
fi

echo "[2/4] Running unit + smoke tests"
python3 -u -m unittest \
  tests/test_preprocessing.py \
  tests/test_models.py \
  tests/test_evaluation.py \
  tests/test_pipeline_smoke.py \
  -v

echo "[3/4] Running artifact assertions"
python3 -u - <<'PY'
from pathlib import Path
import json
import re
import subprocess

root = Path('.').resolve()
out = root / 'outputs' / 'adult_census_income'
metrics = out / 'metrics'

tracked_files = subprocess.run(
    ['git', 'ls-files', '-z'],
    cwd=root,
    check=True,
    capture_output=True,
    text=False,
).stdout.split(b'\x00')
tracked_dsstore = [path.decode('utf-8') for path in tracked_files if path and path.decode('utf-8').endswith('.DS_Store')]

required = [
    root / 'report_final.pdf',
    metrics / 'evaluation_report.json',
    metrics / 'final_solution_bundle.json',
    metrics / 'repeated_cv_stability.csv',
    metrics / 'mlp_training_curve.csv',
    metrics / 'tuning_robustness_summary.json',
    out / 'figures' / 'missingness_mechanism_classification.png',
    out / 'figures' / 'agent_visual_correction_example.png',
    out / 'figures' / 'module2' / 'mlp_training_curve.png',
    out / 'figures' / 'module2' / 'repeated_cv_stability.png',
]
missing = [str(p) for p in required if not p.exists() or p.stat().st_size == 0]
if missing:
    raise SystemExit(f'Missing/empty required artifacts: {missing}')

payload = json.loads((metrics / 'evaluation_report.json').read_text(encoding='utf-8'))
for k in ['module', 'dataset', 'selection', 'test_metrics']:
    if k not in payload:
        raise SystemExit(f'evaluation_report.json missing key: {k}')

metric = payload['test_metrics']
for k in ['f1_weighted', 'auc_pr', 'roc_auc', 'recall_positive', 'calibration_error']:
    if k not in metric or metric[k] is None:
        raise SystemExit(f'evaluation_report.json missing metric value: {k}')

bundle = json.loads((metrics / 'final_solution_bundle.json').read_text(encoding='utf-8'))
bundle_required = {
    'module',
    'dataset',
    'target',
    'positive_class',
    'selection',
    'test_metrics',
    'project_history_summary',
    'workflow_evidence_links',
    'module2_artifacts',
    'module3_artifacts',
    'robustness_artifacts',
    'packaging_artifacts',
    'narrative_links',
    'generated_at_note',
}
missing_bundle_keys = sorted(bundle_required - set(bundle.keys()))
if missing_bundle_keys:
    raise SystemExit(f'final_solution_bundle.json missing keys: {missing_bundle_keys}')

timeline_keys = set(bundle.get('project_history_summary', {}).keys())
expected_timeline = {'foundation_build', 'six_step_restructure', 'quality_uplift', 'report_polish', 'final_submission'}
if timeline_keys != expected_timeline:
    raise SystemExit(f'final_solution_bundle.json timeline mismatch: got {sorted(timeline_keys)}')

if tracked_dsstore:
    raise SystemExit(f'Found tracked .DS_Store files in repository: {tracked_dsstore}')
if any((out).glob('~$*.docx')):
    raise SystemExit('Found temporary Office lock files in outputs/adult_census_income')

print('Artifact assertions passed.')
PY

echo "[4/4] Submission checks completed successfully"
