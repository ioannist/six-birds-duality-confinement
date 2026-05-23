#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

ART = Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step436_route2_stageI_spectral_geometric_artifacts')
required = [
    'ncg_substrate_choice_step436.md',
    'spectral_zeta_function_step436.md',
    'arithmetic_independence_audit_step436.md',
    'constraints_and_gates_check_step436.csv',
    'step436_results_summary.md',
    'mode_b_constraint_ledger_step436_snapshot.csv',
    'mode_b_target_lineage_step436_snapshot.csv',
    'mode_b_grammar_manifest_G_spectral_geometric_step436.csv',
    'step436_schema.json',
    'nonclaim_boundary_step436.md',
    'run_step436_checks.py',
]
missing = [name for name in required if not (ART/name).exists()]
if missing:
    raise SystemExit(f'missing required artifacts: {missing}')

schema = json.loads((ART/'step436_schema.json').read_text())
if schema.get('step') != 436 or schema.get('verdict') != 'retract':
    raise SystemExit('schema step/verdict mismatch')
if schema.get('new_constraint') != 'C_spectral_zeta_not_spectrum':
    raise SystemExit('new constraint missing from schema')

with (ART/'constraints_and_gates_check_step436.csv').open() as f:
    rows = list(csv.DictReader(f))
by_id = {r['item_id']: r for r in rows}
for needed in [
    'C_arithmetic_independence','C_self_adjoint_native','C_no_adelic_substrate',
    'C_explicit_formula_natural','C_GUE_natural','C_trace_formula_compatibility',
    'C_spectral_zeta_not_spectrum','Gate_5_small_spectrum_match','Gate_6_no_single_axiom_equivalence'
]:
    if needed not in by_id:
        raise SystemExit(f'missing constraint/gate row: {needed}')
if by_id['C_spectral_zeta_not_spectrum']['status'] != 'FAIL':
    raise SystemExit('new constraint row must be FAIL')
if by_id['C_self_adjoint_native']['status'] != 'PASS':
    raise SystemExit('self-adjoint native should pass for circle Dirac')
if by_id['C_explicit_formula_natural']['status'] != 'FAIL':
    raise SystemExit('explicit formula natural should fail')

summary = (ART/'step436_results_summary.md').read_text()
for phrase in ['zeta_D(s) = Tr |D_R|^{-s} = 2 R^s zeta(s)', 'Stage I retracts', 'does not by itself declare Route 2 globally exhausted']:
    if phrase not in summary:
        raise SystemExit(f'summary missing phrase: {phrase}')

print('step436 validation passed')
