#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
ART=Path(__file__).resolve().parent
REQ=['A_bound_derivation_step423.md','arch_bound_step423.csv','g_rest_bound_step423.csv','A_total_bound_step423.csv','classification_verdict_step423.csv','step423_results_summary.md','step423_schema.json','nonclaim_boundary_step423.md','run_step423_checks.py']
def fail(m):
 print(f'step423 validation FAILED: {m}'); sys.exit(1)
for name in REQ:
 p=ART/name
 if not p.exists(): fail(f'missing {name}')
 if p.stat().st_size==0: fail(f'empty {name}')
for name in ['arch_bound_step423.csv','g_rest_bound_step423.csv','A_total_bound_step423.csv','classification_verdict_step423.csv']:
 rows=list(csv.DictReader((ART/name).open()))
 if len(rows)!=46: fail(f'{name} expected 46 rows got {len(rows)}')
with (ART/'step423_schema.json').open() as f: schema=json.load(f)
if schema.get('step')!=423: fail('schema step mismatch')
if schema.get('bound_classifier_matches')>=46: fail('unexpected theorem-grade closure claimed')
print('step423 validation passed')
