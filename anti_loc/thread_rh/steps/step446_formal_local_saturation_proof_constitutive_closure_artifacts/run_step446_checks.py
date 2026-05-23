#!/usr/bin/env python3
from pathlib import Path
import csv, sys
out = Path(r"/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step446_formal_local_saturation_proof_constitutive_closure_artifacts")
thread = Path(r"/home/repos/six-birds-foundations-iii/anti_loc/thread")
required = ['mode_b_saturation_proof_constitutive_closure_design_space.md', 'constraint_ledger_compression_step446.md', 'reach_delta_accounting_step446.md', 'findings_rh_update_step446.md', 'step446_results_summary.md', 'mode_b_constraint_ledger_step446_snapshot.csv', 'mode_b_target_lineage_step446_snapshot.csv', 'mode_b_grammar_manifest_step446_snapshot.csv', 'mode_b_constraint_ledger_step446_after_compression.csv', 'step446_schema.json', 'nonclaim_boundary_step446.md', 'run_step446_checks.py']
missing = [name for name in required if not (out/name).exists()]
if missing:
    raise SystemExit('missing artifacts: ' + ', '.join(missing))
subsumed_ids = ['C_capacity_bound_semantic_audit_smuggling', 'C_positivity_audit_kernel_positivity_must_derive', 'C_weil_positivity_explicit_formula_smuggling', 'C_zero_height_audit_currency_smuggling']
expected_subsumed_by = 'step446_saturation_proof_constitutive_closure_design_space'
with (out/'mode_b_constraint_ledger_step446_after_compression.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
rows_by_id = {r['constraint_id']: r for r in rows}
for cid in subsumed_ids:
    r = rows_by_id.get(cid)
    if not r:
        raise SystemExit('missing compressed constraint ' + cid)
    if r.get('status') != 'subsumed' or r.get('subsumed_by') != expected_subsumed_by or r.get('last_checked_attempt') != 'step446':
        raise SystemExit('bad compression row ' + cid + ': ' + str(r))
active_count = sum(1 for r in rows if r.get('status') == 'active')
if active_count > 12:
    raise SystemExit(f'active count too high after compression: {active_count}')
with (thread/'mode_b_constraint_ledger.csv').open(newline='') as f:
    live_rows = list(csv.DictReader(f))
live_by_id = {r['constraint_id']: r for r in live_rows}
for cid in subsumed_ids:
    if live_by_id[cid].get('status') != 'subsumed' or live_by_id[cid].get('subsumed_by') != expected_subsumed_by:
        raise SystemExit('live ledger not compressed for ' + cid)
findings = (thread/'findings_rh.md').read_text()
needle = 'Local Mode B saturation of constitutive-closure design space at L-function substrate (step 446)'
if needle not in findings:
    raise SystemExit('findings_rh.md missing step 446 section')
proof = (out/'mode_b_saturation_proof_constitutive_closure_design_space.md').read_text()
for token in ['Design-Class Declaration', 'Step 441', 'Step 445', 'Local Mode B Saturation', 'not global Mode B exhaustion', 'No successor grammar is declared']:
    if token not in proof:
        raise SystemExit('proof artifact missing token: ' + token)
print('step446 validation passed')
print(f'active_count={active_count}')
print('compressed=' + ','.join(subsumed_ids))
