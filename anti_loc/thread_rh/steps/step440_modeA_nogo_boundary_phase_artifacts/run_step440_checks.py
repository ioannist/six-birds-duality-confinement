#!/usr/bin/env python3
from pathlib import Path
import json, csv
ART = Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step440_modeA_nogo_boundary_phase_artifacts')
LEDGER = Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/mode_b_constraint_ledger.csv')
required = [
    'mode_a_selection_delta_step440.md','theorem_statement_step440.md','deficiency_index_computation_step440.md',
    'literature_anchor_step440.md','step440_results_summary.md','step440_schema.json',
    'nonclaim_boundary_step440.md','run_step440_checks.py'
]
missing = [p for p in required if not (ART/p).exists()]
if missing:
    raise SystemExit(f'missing artifacts: {missing}')
schema = json.loads((ART/'step440_schema.json').read_text())
if schema.get('step') != 440 or 'theorem-grade' not in schema.get('status',''):
    raise SystemExit('schema mismatch')
checks = {
    'mode_a_selection_delta_step440.md': ['C_boundary_phase_arithmetic_smuggling','Berry-Keating 1999','Sierra-Rodriguez-Laguna 2011','Bender-Brody-Müller 2017','Bellissard 2017','von Neumann','non-clone'],
    'deficiency_index_computation_step440.md': ['(n_+, n_-) = (0, 0)','U H_sym U^{-1} = -i d/du','von Neumann'],
    'theorem_statement_step440.md': ['theta_zeta','C_arithmetic_independence','C_self_adjoint_native','(0,0)'],
    'literature_anchor_step440.md': ['Berry','Sierra','Bender','Bellissard','Von Neumann'],
    'step440_results_summary.md': ['4-dispatch Mode A coordinator cluster','Step 437','Step 438','Step 439','Step 440'],
    'nonclaim_boundary_step440.md': ['No proof of RH','does not declare Route 2 globally exhausted']
}
for fname, phrases in checks.items():
    text = (ART/fname).read_text()
    for phrase in phrases:
        if phrase not in text:
            raise SystemExit(f'{fname} missing phrase: {phrase}')
with LEDGER.open(newline='') as f:
    rows = list(csv.DictReader(f))
row = next((r for r in rows if r.get('constraint_id') == 'C_boundary_phase_arithmetic_smuggling'), None)
if row is None:
    raise SystemExit('ledger missing C_boundary_phase_arithmetic_smuggling')
if row.get('last_checked_attempt') != 'step440':
    raise SystemExit('ledger row not updated to step440')
print('step440 validation passed')
