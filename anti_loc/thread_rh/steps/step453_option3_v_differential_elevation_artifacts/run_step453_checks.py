#!/usr/bin/env python3
from pathlib import Path
import csv, json
root = Path('/home/repos/six-birds-foundations-iii')
step = root / 'anti_loc/thread/steps/step453_option3_v_differential_elevation_artifacts'
required = json.loads((step / 'step453_schema.json').read_text())['required_artifacts']
missing = [p for p in required if not (step / p).exists()]
if missing:
    raise SystemExit('missing artifacts: ' + ', '.join(missing))
verdict = (step / 'step453_step_verdict.md').read_text()
if 'option3_recognition_under_v_differential_for_RH' not in verdict:
    raise SystemExit('verdict missing')
if 'No theorem-grade derivation' not in verdict:
    raise SystemExit('derivation nonclaim missing')
for name in ['step453_substrate_classification_p_tso.md','step453_derivation_attempt_p_tso_to_B_n.md','step453_classification_verdict.md']:
    text = (step / name).read_text()
    if 'recognition' not in text.lower():
        raise SystemExit('recognition classification missing in ' + name)
with (root / 'anti_loc/thread/mode_b_constraint_ledger.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
xi = [r for r in rows if r.get('constraint_id') == 'Xi_SDTC_domination_records']
if len(xi) != 1:
    raise SystemExit('Xi row not unique')
row = xi[0]
if row.get('status') != 'active' or row.get('last_checked_attempt') != 'step453':
    raise SystemExit('Xi row not updated for step453')
if 'recognition_under_v_differential' not in row.get('satisfaction_history','') + row.get('status_reason',''):
    raise SystemExit('step453 recognition verdict not recorded in ledger')
nb = (step / 'nonclaim_boundary_step453.md').read_text()
if 'does not prove RH' not in nb:
    raise SystemExit('nonclaim boundary missing RH nonclaim')
print('step453 validation passed: artifacts present, V-Differential recognition verdict recorded, ledger updated, nonclaim boundary intact')
