#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
ART=Path(__file__).resolve().parent
REQ=['zeros_1_to_1001_step426.csv','exceptional_zeros_n1000_step426.csv','dominance_verification_step426.csv','step426_results_summary.md','step426_schema.json','nonclaim_boundary_step426.md','run_step426_checks.py']
def fail(m): print(f'step426 validation FAILED: {m}'); sys.exit(1)
for name in REQ:
 p=ART/name
 if not p.exists(): fail(f'missing {name}')
 if p.stat().st_size==0: fail(f'empty {name}')
zeros=list(csv.DictReader((ART/'zeros_1_to_1001_step426.csv').open()))
if len(zeros)!=1000: fail(f'expected 1000 zero rows got {len(zeros)}')
ex=list(csv.DictReader((ART/'exceptional_zeros_n1000_step426.csv').open()))
dom=list(csv.DictReader((ART/'dominance_verification_step426.csv').open()))
if len(dom)!=len(ex)+30: fail('dominance row count mismatch')
mis=[r for r in dom if r['condition_matches_actual']!='True']
with (ART/'step426_schema.json').open() as f: schema=json.load(f)
if schema.get('step')!=426: fail('schema step mismatch')
if schema.get('mismatch_count')!=len(mis): fail('schema mismatch count inconsistent')
if len(mis)!=3: fail(f'expected 3 surfaced mismatches, got {len(mis)}')
print('step426 validation passed')
