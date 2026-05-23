#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
base=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step432_extended_modular_sample_artifacts')
required=['L_Delta_zeros_31_to_100_step432.csv','exceptional_modular_extended_step432.csv','necessity_verification_extended_step432.csv','step432_results_summary.md','step432_schema.json','nonclaim_boundary_step432.md','run_step432_checks.py']
missing=[p for p in required if not (base/p).exists()]
if missing:
 print('missing artifacts:',missing); sys.exit(1)
rows=list(csv.DictReader((base/'L_Delta_zeros_31_to_100_step432.csv').open()))
if len(rows)<10:
 print('too few stable rows:',len(rows)); sys.exit(1)
ver=list(csv.DictReader((base/'necessity_verification_extended_step432.csv').open()))
if any(r['necessity_pass']!='True' for r in ver):
 print('necessity counterexample found'); sys.exit(1)
print('step432 validation passed')
