#!/usr/bin/env python3
from pathlib import Path
import csv,json
ART=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step445_route2_stageI_closure_only_no_audit_artifacts')
required=['scope_and_capacity_specification_step445.md','three_component_package_construction_step445.md','axioms_A1_to_A4_verification_step445.md','adequacy_residual_step445.csv','capacity_bound_check_step445.csv','gates_and_absence_checks_step445.csv','falsification_conditions_step445.md','step445_results_summary.md','mode_b_constraint_ledger_step445_snapshot.csv','mode_b_target_lineage_step445_snapshot.csv','mode_b_grammar_manifest_G_closure_only_no_audit_step445.csv','step445_schema.json','nonclaim_boundary_step445.md','run_step445_checks.py']
missing=[p for p in required if not (ART/p).exists()]
if missing: raise SystemExit(f'missing artifacts: {missing}')
schema=json.loads((ART/'step445_schema.json').read_text())
if schema.get('step')!=445 or schema.get('verdict')!='Stage I retract': raise SystemExit('schema mismatch')
with (ART/'adequacy_residual_step445.csv').open(newline='') as f: rows=list(csv.DictReader(f))
eigs=[float(r['value']) for r in rows if r['quantity']=='Xi_eigenvalue']
if len(eigs)!=3 or min(eigs)<=0: raise SystemExit('bad Xi')
err=float([r['value'] for r in rows if r['quantity']=='schur_identity_max_abs_error'][0])
if err>1e-40: raise SystemExit('bad Schur error')
with (ART/'capacity_bound_check_step445.csv').open(newline='') as f: caps=list(csv.DictReader(f))
target=[float(r['value']) for r in caps if r['case']=='target_formal']
control=[float(r['value']) for r in caps if r['case']=='offcritical_control']
if min(target)<=0 or min(control)>=0: raise SystemExit('capacity target/control check failed')
with (ART/'gates_and_absence_checks_step445.csv').open(newline='') as f: grows=list(csv.DictReader(f))
active=[r for r in grows if r['item_type']=='active_constraint_cited']
diagnostic=[r for r in grows if r['item_type']=='diagnostic_constraint_cited']
if len(active)<15: raise SystemExit(f'expected >=15 active constraints cited, got {len(active)}')
if len(diagnostic)<2: raise SystemExit(f'expected 2 diagnostic constraints cited, got {len(diagnostic)}')
def find(item,typ=None):
    xs=[r for r in grows if r['item_id']==item and (typ is None or r['item_type']==typ)]
    if not xs: raise SystemExit(f'missing {item}')
    return xs[0]
if find('G6_no_single_axiom_equivalence','gate')['status']!='FAIL': raise SystemExit('G6 should fail')
if find('C_capacity_bound_semantic_audit_smuggling','new_constraint')['status']!='FAIL': raise SystemExit('new constraint should fail')
for fname,phrases in {'scope_and_capacity_specification_step445.md':['Theta^D','not RH-equivalent'], 'falsification_conditions_step445.md':['external semantic audit','C_capacity_bound_semantic_audit_smuggling'], 'step445_results_summary.md':['Stage I retracts','Xi_Z']}.items():
    text=(ART/fname).read_text()
    for phrase in phrases:
        if phrase not in text: raise SystemExit(f'{fname} missing {phrase}')
print('step445 validation passed')
