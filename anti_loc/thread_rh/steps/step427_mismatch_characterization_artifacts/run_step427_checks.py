#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
ART=Path(__file__).resolve().parent
REQ=['mismatch_hadamard_decomposition_step427.csv','common_features_step427.md','mechanism_2_structural_signature_step427.md','step427_results_summary.md','step427_schema.json','nonclaim_boundary_step427.md','run_step427_checks.py']
def fail(m): print(f'step427 validation FAILED: {m}'); sys.exit(1)
for name in REQ:
 p=ART/name
 if not p.exists(): fail(f'missing {name}')
 if p.stat().st_size==0: fail(f'empty {name}')
rows=list(csv.DictReader((ART/'mismatch_hadamard_decomposition_step427.csv').open()))
if len(rows)!=3: fail(f'expected 3 rows got {len(rows)}')
for r in rows:
 if r['mechanism_label']!='regular_residual_driven_positive_signflip': fail('bad mechanism label')
 if abs(float(r['exact_sum_minus_Re_zeta2']))>1e-20: fail('exact decomposition does not close')
with (ART/'step427_schema.json').open() as f: schema=json.load(f)
if schema.get('step')!=427: fail('schema step mismatch')
print('step427 validation passed')
