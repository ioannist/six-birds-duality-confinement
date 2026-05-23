#!/usr/bin/env python3
from pathlib import Path
import csv, json
root = Path('/home/repos/six-birds-foundations-iii')
step = root / 'anti_loc/thread/steps/step451_option1_framework_primitive_derivation_artifacts'
required = json.loads((step / 'step451_schema.json').read_text())['required_artifacts']
missing = [p for p in required if not (step / p).exists()]
if missing:
    raise SystemExit('missing artifacts: ' + ', '.join(missing))
verdict = (step / 'step451_step_verdict.md').read_text()
if 'option1_partial_with_named_substrate_input_gap' not in verdict:
    raise SystemExit('verdict string missing')
for name in ['step451_schur_complement_route.md','step451_exhaustive_moving_ledger_route.md','step451_obstruction_budget_route.md','step451_construction_synthesis.md']:
    text = (step / name).read_text()
    if 'Xi_SDTC_trace_decay_input' not in text:
        raise SystemExit(f'named gap missing in {name}')
smuggle = (step / 'step451_smuggle_audit.md').read_text()
for needle in ['Test 1', 'Test 2', 'Test 3', 'Test 4', 'No smuggle is detected']:
    if needle not in smuggle:
        raise SystemExit('smuggle audit missing ' + needle)
with (root / 'anti_loc/thread/mode_b_constraint_ledger.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
xi = [r for r in rows if r.get('constraint_id') == 'Xi_SDTC_domination_records']
if len(xi) != 1:
    raise SystemExit('Xi_SDTC_domination_records row not unique')
row = xi[0]
if row.get('status') != 'active' or row.get('last_checked_attempt') != 'step451':
    raise SystemExit('Xi_SDTC_domination_records not updated as active/step451')
if 'Xi_SDTC_trace_decay_input' not in row.get('status_reason','') + row.get('failure_shape','') + row.get('satisfaction_history',''):
    raise SystemExit('named gap not recorded in ledger row')
nb = (step / 'nonclaim_boundary_step451.md').read_text()
if 'does not prove RH' not in nb:
    raise SystemExit('nonclaim boundary missing RH nonclaim')
print('step451 validation passed: artifacts present, verdict recorded, ledger updated, nonclaim boundary intact')
