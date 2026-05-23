#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
base = Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step429_analytical_necessity_derivation_artifacts')
required = [
    'functional_equation_phase_step429.md',
    'L_prime_phase_constraint_step429.md',
    'necessity_derivation_step429.md',
    'numerical_verification_step429.csv',
    'step429_results_summary.md',
    'step429_schema.json',
    'nonclaim_boundary_step429.md',
    'run_step429_checks.py',
]
missing = [p for p in required if not (base/p).exists()]
if missing:
    print('missing artifacts:', missing)
    sys.exit(1)
rows = list(csv.DictReader((base/'numerical_verification_step429.csv').open()))
if len(rows) != 4:
    print('expected 4 numerical verification rows, found', len(rows))
    sys.exit(1)
max_res = max(abs(float(r['phase_residual_mod_pi'])) for r in rows)
if max_res > 1e-20:
    print('phase residual too large:', max_res)
    sys.exit(1)
summary = (base/'step429_results_summary.md').read_text()
for token in ['Partial derivation', 'phase-sensitive bound', '410/410']:
    if token not in summary:
        print('summary missing token:', token)
        sys.exit(1)
print('step429 validation passed')
