#!/usr/bin/env python3
from pathlib import Path
import csv,sys
base=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step433_route2_stageI_selberg_analog_artifacts')
required=['M_0_substrate_construction_step433.md','operator_setup_step433.md','length_spectrum_step433.csv','trace_formula_comparison_step433.md','constraints_and_gates_check_step433.csv','step433_results_summary.md','mode_b_constraint_ledger_step433_snapshot.csv','mode_b_target_lineage_step433_snapshot.csv','mode_b_grammar_manifest_G_selberg_analog_step433.csv','step433_schema.json','nonclaim_boundary_step433.md','run_step433_checks.py']
missing=[p for p in required if not (base/p).exists()]
if missing:
 print('missing artifacts:',missing); sys.exit(1)
lengths=list(csv.DictReader((base/'length_spectrum_step433.csv').open()))
if len(lengths)<20:
 print('expected at least 20 length rows'); sys.exit(1)
checks=list(csv.DictReader((base/'constraints_and_gates_check_step433.csv').open()))
status={r['id']:r['status'] for r in checks}
if status.get('C_trace_formula_compatibility')!='FAIL':
 print('expected trace compatibility failure'); sys.exit(1)
summary=(base/'step433_results_summary.md').read_text()
if 'C_length_spectrum_arithmetic_mismatch' not in summary or 'Stage I retracts' not in summary:
 print('summary missing retract/new constraint'); sys.exit(1)
print('step433 validation passed')
