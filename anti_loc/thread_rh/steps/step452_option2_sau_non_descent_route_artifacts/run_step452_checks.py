#!/usr/bin/env python3
from pathlib import Path
import csv, json
root = Path('/home/repos/six-birds-foundations-iii')
step = root / 'anti_loc/thread/steps/step452_option2_sau_non_descent_route_artifacts'
required = json.loads((step / 'step452_schema.json').read_text())['required_artifacts']
missing = [p for p in required if not (step / p).exists()]
if missing:
    raise SystemExit('missing artifacts: ' + ', '.join(missing))
verdict = (step / 'step452_step_verdict.md').read_text()
if 'option2_sau_non_descent_witness_circular' not in verdict:
    raise SystemExit('verdict missing')
if '4/3' not in verdict:
    raise SystemExit('gate count missing')
w = (step / 'step452_non_descent_witness.md').read_text()
for needle in ['Form A', 'Form B', 'Form C', 'Form D', 'Form E', 'Form F', 'W_C_typed_noncollapse']:
    if needle not in w:
        raise SystemExit('witness audit missing ' + needle)
gates = (step / 'step452_six_gates_plus_gate7.md').read_text()
for needle in ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'Pass: 4', 'Fail: 3']:
    if needle not in gates:
        raise SystemExit('gates artifact missing ' + needle)
with (root / 'anti_loc/thread/mode_b_constraint_ledger.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
xi = [r for r in rows if r.get('constraint_id') == 'Xi_SDTC_domination_records']
if len(xi) != 1:
    raise SystemExit('Xi row not unique')
row = xi[0]
if row.get('status') != 'active' or row.get('last_checked_attempt') != 'step452':
    raise SystemExit('Xi row not updated for step452')
if 'sau_non_descent_witness_circular' not in row.get('satisfaction_history','') + row.get('status_reason',''):
    raise SystemExit('step452 circular verdict not recorded in ledger')
nb = (step / 'nonclaim_boundary_step452.md').read_text()
if 'does not prove RH' not in nb:
    raise SystemExit('nonclaim boundary missing RH nonclaim')
print('step452 validation passed: artifacts present, SAU circular verdict recorded, gates audited, ledger updated')
