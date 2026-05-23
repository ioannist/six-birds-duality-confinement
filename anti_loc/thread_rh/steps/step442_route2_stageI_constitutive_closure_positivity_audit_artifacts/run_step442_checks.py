#!/usr/bin/env python3
from pathlib import Path
import csv,json
ART=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step442_route2_stageI_constitutive_closure_positivity_audit_artifacts')
required=['positivity_form_choice_step442.md','audit_currency_redesign_step442.md','smuggling_check_step442.md','package_rebuild_and_axioms_step442.md','adequacy_residual_step442.csv','gates_and_constraints_check_step442.csv','step442_results_summary.md','mode_b_constraint_ledger_step442_snapshot.csv','mode_b_target_lineage_step442_snapshot.csv','mode_b_grammar_manifest_G_constitutive_closure_step442.csv','step442_schema.json','nonclaim_boundary_step442.md','run_step442_checks.py']
missing=[p for p in required if not (ART/p).exists()]
if missing: raise SystemExit(f'missing artifacts: {missing}')
schema=json.loads((ART/'step442_schema.json').read_text())
if schema.get('step')!=442 or schema.get('verdict')!='Stage I retract': raise SystemExit('schema mismatch')
with (ART/'adequacy_residual_step442.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
eigs=[float(r['value']) for r in rows if r['quantity']=='Xi_eigenvalue']
if len(eigs)!=3 or min(eigs)<=0: raise SystemExit('bad Xi spectrum')
err=[float(r['value']) for r in rows if r['quantity']=='schur_identity_max_abs_error'][0]
if err>1e-40: raise SystemExit('Schur identity error too large')
with (ART/'gates_and_constraints_check_step442.csv').open(newline='') as f:
    grows=list(csv.DictReader(f))
active=[r for r in grows if r['item_type']=='active_constraint_cited']
if len(active)<15: raise SystemExit(f'expected >=15 active constraints cited, got {len(active)}')
def find(item,typ=None):
    xs=[r for r in grows if r['item_id']==item and (typ is None or r['item_type']==typ)]
    if not xs: raise SystemExit(f'missing {item}')
    return xs[0]
if find('C_zero_height_audit_currency_smuggling','constraint_check')['status']!='PASS': raise SystemExit('zero-height check should pass')
if find('C_positivity_audit_kernel_positivity_must_derive','new_constraint')['status']!='FAIL': raise SystemExit('new constraint should fail')
for fname, phrases in {'positivity_form_choice_step442.md':['de Branges','1968'], 'smuggling_check_step442.md':['C_zero_height_audit_currency_smuggling','C_native_membrane_no_L_side_smuggling'], 'step442_results_summary.md':['Stage I retracts','Xi_Z']}.items():
    text=(ART/fname).read_text()
    for phrase in phrases:
        if phrase not in text: raise SystemExit(f'{fname} missing {phrase}')
print('step442 validation passed')
