#!/usr/bin/env python3
from pathlib import Path
import csv,sys
base=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step435_route2_stageI_universal_forced_GUE_artifacts')
required=['ensemble_specification_step435.md','universality_theorem_anchor_step435.md','distributional_vs_pointwise_audit_step435.md','constraints_and_gates_check_step435.csv','step435_results_summary.md','mode_b_constraint_ledger_step435_snapshot.csv','mode_b_target_lineage_step435_snapshot.csv','mode_b_grammar_manifest_G_universal_forced_GUE_step435.csv','step435_schema.json','nonclaim_boundary_step435.md','run_step435_checks.py']
missing=[p for p in required if not (base/p).exists()]
if missing:
 print('missing artifacts:',missing); sys.exit(1)
rows=list(csv.DictReader((base/'constraints_and_gates_check_step435.csv').open()))
status={r['id']:r['status'] for r in rows}
if status.get('C_ensemble_distributional_not_pointwise')!='PROPOSED_FAIL':
 print('missing proposed distributional failure'); sys.exit(1)
for key in ['C_explicit_formula_natural','C_trace_formula_compatibility']:
 if status.get(key)!='FAIL':
  print('expected fail for',key); sys.exit(1)
summary=(base/'step435_results_summary.md').read_text()
if 'Stage I retracts' not in summary or 'C_ensemble_distributional_not_pointwise' not in summary:
 print('summary missing retract/new constraint'); sys.exit(1)
print('step435 validation passed')
