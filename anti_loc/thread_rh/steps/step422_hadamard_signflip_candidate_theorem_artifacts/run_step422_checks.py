#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
ART=Path(__file__).resolve().parent
REQ=['dominance_condition_step422.md','A_B_per_zero_step422.csv','dominance_match_count_step422.csv','candidate_theorem_statement_step422.md','step422_results_summary.md','step422_schema.json','nonclaim_boundary_step422.md','run_step422_checks.py']
def fail(msg):
    print(f'step422 validation FAILED: {msg}')
    sys.exit(1)
for name in REQ:
    p=ART/name
    if not p.exists(): fail(f'missing {name}')
    if p.stat().st_size==0: fail(f'empty {name}')
with (ART/'A_B_per_zero_step422.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
if len(rows)!=46: fail(f'expected 46 A/B rows, got {len(rows)}')
exc=[r for r in rows if r['group']=='exceptional']
base=[r for r in rows if r['group']=='non_exceptional_baseline']
if len(exc)!=26 or len(base)!=20: fail(f'bad group counts {len(exc)} exceptional {len(base)} baseline')
if any(r['condition_matches_actual_sign']!='True' for r in rows):
    fail('not all rows match dominance condition')
with (ART/'step422_schema.json').open() as f:
    schema=json.load(f)
if schema.get('step')!=422: fail('schema step mismatch')
print('step422 validation passed')
