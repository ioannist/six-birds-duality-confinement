#!/usr/bin/env python3
from pathlib import Path
import csv,json
ART=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step443_route2_stageI_constitutive_closure_weil_positivity_artifacts')
required=['weil_positivity_audit_choice_step443.md','audit_currency_construction_step443.md','smuggling_check_step443.md','package_rebuild_and_axioms_step443.md','adequacy_residual_step443.csv','gates_and_constraints_check_step443.csv','cluster_meta_pattern_step443.md','step443_results_summary.md','mode_b_constraint_ledger_step443_snapshot.csv','mode_b_target_lineage_step443_snapshot.csv','mode_b_grammar_manifest_G_constitutive_closure_step443.csv','step443_schema.json','nonclaim_boundary_step443.md','run_step443_checks.py']
missing=[p for p in required if not (ART/p).exists()]
if missing: raise SystemExit(f'missing artifacts: {missing}')
schema=json.loads((ART/'step443_schema.json').read_text())
if schema.get('step')!=443 or schema.get('verdict')!='Stage I retract': raise SystemExit('schema mismatch')
with (ART/'adequacy_residual_step443.csv').open(newline='') as f: rows=list(csv.DictReader(f))
eigs=[float(r['value']) for r in rows if r['quantity']=='Xi_eigenvalue']
if len(eigs)!=3 or min(eigs)<=0: raise SystemExit('bad Xi spectrum')
err=[float(r['value']) for r in rows if r['quantity']=='schur_identity_max_abs_error'][0]
if err>1e-40: raise SystemExit('Schur identity error too large')
with (ART/'gates_and_constraints_check_step443.csv').open(newline='') as f: grows=list(csv.DictReader(f))
active=[r for r in grows if r['item_type']=='active_constraint_cited']
if len(active)<16: raise SystemExit(f'expected >=16 active constraints cited, got {len(active)}')
def find(item,typ=None):
    xs=[r for r in grows if r['item_id']==item and (typ is None or r['item_type']==typ)]
    if not xs: raise SystemExit(f'missing {item}')
    return xs[0]
if find('C_weil_positivity_explicit_formula_smuggling','new_constraint')['status']!='FAIL': raise SystemExit('new constraint should fail')
for fname, phrases in {'weil_positivity_audit_choice_step443.md':['Weil 1952','W[f]'], 'smuggling_check_step443.md':['zero side','prime side','archimedean'], 'cluster_meta_pattern_step443.md':['three structurally distinct attempts','audit-currency derivability tension'], 'step443_results_summary.md':['Stage I retracts','Xi_Z']}.items():
    text=(ART/fname).read_text()
    for phrase in phrases:
        if phrase not in text: raise SystemExit(f'{fname} missing {phrase}')
print('step443 validation passed')
