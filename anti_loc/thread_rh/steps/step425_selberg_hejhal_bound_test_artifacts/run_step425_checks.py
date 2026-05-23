#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
ART=Path(__file__).resolve().parent
REQ=['selberg_hejhal_bound_per_cell_step425.csv','classification_sweep_C_step425.csv','theorem_grade_verdict_step425.md','step425_results_summary.md','step425_schema.json','nonclaim_boundary_step425.md','run_step425_checks.py']
def fail(m): print(f'step425 validation FAILED: {m}'); sys.exit(1)
for name in REQ:
 p=ART/name
 if not p.exists(): fail(f'missing {name}')
 if p.stat().st_size==0: fail(f'empty {name}')
rows=list(csv.DictReader((ART/'selberg_hejhal_bound_per_cell_step425.csv').open()))
if len(rows)!=46: fail(f'expected 46 cells got {len(rows)}')
sweep=list(csv.DictReader((ART/'classification_sweep_C_step425.csv').open()))
if len(sweep)!=5: fail('expected 5 C sweep rows')
if any(r['achieves_46_of_46']=='True' for r in sweep): fail('unexpected theorem-grade pass recorded')
with (ART/'step425_schema.json').open() as f: schema=json.load(f)
if schema.get('step')!=425: fail('schema step mismatch')
print('step425 validation passed')
