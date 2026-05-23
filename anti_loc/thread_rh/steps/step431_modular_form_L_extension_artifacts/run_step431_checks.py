#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
base=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step431_modular_form_L_extension_artifacts')
required=['L_Delta_zeros_step431.csv','exceptional_modular_form_step431.csv','necessity_verification_modular_step431.csv','cross_class_comparison_step431.md','step431_results_summary.md','step431_schema.json','nonclaim_boundary_step431.md','run_step431_checks.py']
missing=[p for p in required if not (base/p).exists()]
if missing:
    print('missing artifacts:', missing); sys.exit(1)
zeros=list(csv.DictReader((base/'L_Delta_zeros_step431.csv').open()))
if len(zeros)!=30:
    print('expected 30 zeros, found', len(zeros)); sys.exit(1)
ver=list(csv.DictReader((base/'necessity_verification_modular_step431.csv').open()))
if any(r['necessity_pass']!='True' for r in ver):
    print('necessity counterexample in modular sample'); sys.exit(1)
print('step431 validation passed')
