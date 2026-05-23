#!/usr/bin/env python3
from pathlib import Path
import json, csv
ART = Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step439_modeA_nogo_spectral_zeta_artifacts')
LEDGER = Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/mode_b_constraint_ledger.csv')
required = [
    'mode_a_selection_delta_step439.md','theorem_statement_step439.md','proof_or_diagnosis_step439.md',
    'literature_anchor_step439.md','step439_results_summary.md','step439_schema.json',
    'nonclaim_boundary_step439.md','run_step439_checks.py'
]
missing = [p for p in required if not (ART/p).exists()]
if missing:
    raise SystemExit(f'missing artifacts: {missing}')
schema = json.loads((ART/'step439_schema.json').read_text())
if schema.get('step') != 439 or schema.get('status') != 'theorem-grade structural no-go':
    raise SystemExit('schema mismatch')
checks = {
    'mode_a_selection_delta_step439.md': ['C_spectral_zeta_not_spectrum','Connes 1999','Connes-Marcolli','non-clone'],
    'theorem_statement_step439.md': ['zeta_D(s)','Spec(D_R)','C_spectral_zeta_not_spectrum'],
    'proof_or_diagnosis_step439.md': ['2 R^s zeta(s)','Spec(D_R)','theorem-grade'],
    'literature_anchor_step439.md': ['Connes 1999','Connes-Marcolli','Step 436 circle counterexample'],
    'nonclaim_boundary_step439.md': ['No proof of RH','pointwise spectral realization']
}
for fname, phrases in checks.items():
    text = (ART/fname).read_text()
    for phrase in phrases:
        if phrase not in text:
            raise SystemExit(f'{fname} missing phrase: {phrase}')
with LEDGER.open(newline='') as f:
    rows = list(csv.DictReader(f))
row = next((r for r in rows if r.get('constraint_id') == 'C_spectral_zeta_not_spectrum'), None)
if row is None:
    raise SystemExit('ledger missing C_spectral_zeta_not_spectrum')
if row.get('last_checked_attempt') != 'step439':
    raise SystemExit('ledger row not updated to step439')
print('step439 validation passed')
