#!/usr/bin/env python3
from pathlib import Path
import csv,sys
base=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step434_route2_stageI_quantum_semiclassical_artifacts')
required=['sierra_2011_anchor_step434.md','operator_setup_quantum_semiclassical_step434.md','self_adjoint_extension_audit_step434.md','periodic_orbit_action_step434.md','constraints_and_gates_check_step434.csv','step434_results_summary.md','mode_b_constraint_ledger_step434_snapshot.csv','mode_b_target_lineage_step434_snapshot.csv','mode_b_grammar_manifest_G_quantum_semiclassical_step434.csv','step434_schema.json','nonclaim_boundary_step434.md','run_step434_checks.py']
missing=[p for p in required if not (base/p).exists()]
if missing:
 print('missing artifacts:',missing); sys.exit(1)
rows=list(csv.DictReader((base/'constraints_and_gates_check_step434.csv').open()))
status={r['id']:r['status'] for r in rows}
for key in ['C_self_adjoint_native','C_length_spectrum_arithmetic_mismatch','C_trace_formula_compatibility']:
 if status.get(key)!='FAIL':
  print('expected FAIL for',key,'got',status.get(key)); sys.exit(1)
summary=(base/'step434_results_summary.md').read_text()
if 'C_boundary_phase_arithmetic_smuggling' not in summary or 'Stage I retracts' not in summary:
 print('summary missing retract/new constraint'); sys.exit(1)
print('step434 validation passed')
