#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
base=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step430_phase_line_full_verification_artifacts')
required=['phase_residuals_410_step430.csv','residual_statistics_step430.md','step430_results_summary.md','step430_schema.json','nonclaim_boundary_step430.md','run_step430_checks.py']
missing=[p for p in required if not (base/p).exists()]
if missing:
    print('missing artifacts:', missing); sys.exit(1)
rows=list(csv.DictReader((base/'phase_residuals_410_step430.csv').open()))
if len(rows)!=410:
    print('expected 410 audit rows, found', len(rows)); sys.exit(1)
max_res=max(abs(float(r['abs_residual'])) for r in rows)
if max_res >= 1e-30:
    print('residual threshold failed:', max_res); sys.exit(1)
schema=json.loads((base/'step430_schema.json').read_text())
if schema.get('total_audit_rows') != 410 or schema.get('unique_mathematical_cells') != 403:
    print('schema count mismatch'); sys.exit(1)
print('step430 validation passed')
