#!/usr/bin/env python3
from pathlib import Path
import csv, json
ART=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step441_route2_stageI_constitutive_closure_artifacts')
required=[
 'scope_declaration_step441.md','package_construction_step441.md','axioms_A1_to_A4_verification_step441.md',
 'adequacy_residual_budget_step441.csv','gates_and_grammar_local_check_step441.csv','step441_results_summary.md',
 'mode_b_constraint_ledger_step441_snapshot.csv','mode_b_target_lineage_step441_snapshot.csv','mode_b_grammar_manifest_G_constitutive_closure_step441.csv',
 'step441_schema.json','nonclaim_boundary_step441.md','run_step441_checks.py'
]
missing=[p for p in required if not (ART/p).exists()]
if missing:
    raise SystemExit(f'missing artifacts: {missing}')
schema=json.loads((ART/'step441_schema.json').read_text())
if schema.get('step')!=441 or schema.get('verdict')!='Stage I retract':
    raise SystemExit('schema mismatch')
with (ART/'adequacy_residual_budget_step441.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
vals=[float(r['value']) for r in rows if r['quantity']=='Xi_eigenvalue']
if len(vals)!=3 or min(vals) <= 0:
    raise SystemExit('Xi eigenvalues not strictly positive as expected')
with (ART/'gates_and_grammar_local_check_step441.csv').open(newline='') as f:
    grows=list(csv.DictReader(f))
ids={}
for r in grows:
    ids.setdefault(r['item_id'], []).append(r)
for needed in ['G1_primitive_exclusion','G4_negative_controls','G6_no_single_axiom_equivalence','C_zero_height_audit_currency_smuggling','C_adequacy_residual_must_derive','C_native_membrane_no_L_side_smuggling']:
    if needed not in ids:
        raise SystemExit(f'missing gate row {needed}')
new_rows=[r for r in ids['C_zero_height_audit_currency_smuggling'] if r['item_type']=='new_constraint']
if not new_rows or new_rows[0]['status']!='FAIL':
    raise SystemExit('new constraint row must fail')
active_cited=[r for r in grows if r['item_type']=='active_constraint_cited']
if len(active_cited) < 14:
    raise SystemExit(f'expected at least 14 active constraints cited, got {len(active_cited)}')
summary=(ART/'step441_results_summary.md').read_text()
for phrase in ['Stage I retracts','Xi_Z','C_zero_height_audit_currency_smuggling']:
    if phrase not in summary:
        raise SystemExit(f'summary missing {phrase}')
print('step441 validation passed')
