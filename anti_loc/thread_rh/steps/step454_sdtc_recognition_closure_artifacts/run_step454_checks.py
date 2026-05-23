#!/usr/bin/env python3
from pathlib import Path
import csv, json
root = Path('/home/repos/six-birds-foundations-iii')
step = root / 'anti_loc/thread/steps/step454_sdtc_recognition_closure_artifacts'
required = json.loads((step / 'step454_schema.json').read_text())['required_artifacts']
missing = [p for p in required if not (step / p).exists()]
if missing:
    raise SystemExit('missing artifacts: ' + ', '.join(missing))
verdict = (step / 'step454_step_verdict.md').read_text()
if 'rh_recognition_closure_landed_standard_sb_assumption' not in verdict:
    raise SystemExit('verdict missing')
for needle in ['inside Six Birds', 'Outside Six Birds', 'conditional theorem']:
    if needle not in verdict:
        raise SystemExit('claim status missing ' + needle)
gates = (step / 'step454_six_gates_audit.md').read_text()
for g in ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'All seven gates pass']:
    if g not in gates:
        raise SystemExit('gate audit missing ' + g)
nonclaims = (step / 'step454_nonclaim_register.md').read_text()
for i in range(1,13):
    if f'NC-{i}' not in nonclaims:
        raise SystemExit(f'NC-{i} missing')
with (root / 'anti_loc/thread/mode_b_constraint_ledger.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
xi = [r for r in rows if r.get('constraint_id') == 'Xi_SDTC_domination_records']
if len(xi) != 1:
    raise SystemExit('Xi row not unique')
row = xi[0]
if row.get('last_checked_attempt') != 'step454':
    raise SystemExit('Xi row not updated for step454')
if 'recognition-grade closed' not in row.get('status',''):
    raise SystemExit('Xi row not closed recognition-grade')
nb = (step / 'nonclaim_boundary_step454.md').read_text()
if 'does not claim a source-free standard-ZFC proof of RH' not in nb:
    raise SystemExit('standard-ZFC nonclaim missing')
print('step454 validation passed: recognition closure artifacts present, gates/nonclaims complete, Xi closed, conditional boundary intact')
