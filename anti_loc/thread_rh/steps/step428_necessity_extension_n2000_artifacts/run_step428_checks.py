#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
ART=Path(__file__).resolve().parent
REQ=['zeros_1001_to_2001_step428.csv','exceptional_j1001_2000_step428.csv','necessity_verification_step428.csv','step428_results_summary.md','step428_schema.json','nonclaim_boundary_step428.md','run_step428_checks.py']
def fail(m): print(f'step428 validation FAILED: {m}'); sys.exit(1)
for name in REQ:
 p=ART/name
 if not p.exists(): fail(f'missing {name}')
 if p.stat().st_size==0: fail(f'empty {name}')
zeros=list(csv.DictReader((ART/'zeros_1001_to_2001_step428.csv').open()))
if len(zeros)!=1001: fail(f'expected 1001 zero rows got {len(zeros)}')
ex=list(csv.DictReader((ART/'exceptional_j1001_2000_step428.csv').open()))
ver=list(csv.DictReader((ART/'necessity_verification_step428.csv').open()))
if len(ex)!=len(ver): fail('exceptional and verification row mismatch')
if any(r['B_gt_0']!='True' for r in ver): fail('necessity counterexample present')
with (ART/'step428_schema.json').open() as f: schema=json.load(f)
if schema.get('step')!=428: fail('schema step mismatch')
print('step428 validation passed')
