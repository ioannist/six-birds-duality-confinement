#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
ART = Path(__file__).resolve().parent
REQ = [
    'saddle_positions_step421.csv',
    'zeta_at_saddle_step421.csv',
    'M_G_star_at_saddle_step421.csv',
    'product_bound_step421.csv',
    'foreclosure_consistency_step421.md',
    'step421_results_summary.md',
    'step421_schema.json',
    'nonclaim_boundary_step421.md',
    'run_step421_checks.py',
]
def fail(msg):
    print(f'step421 validation FAILED: {msg}')
    sys.exit(1)
for name in REQ:
    p = ART/name
    if not p.exists():
        fail(f'missing {name}')
    if p.stat().st_size == 0:
        fail(f'empty {name}')
for name in ['saddle_positions_step421.csv','zeta_at_saddle_step421.csv','M_G_star_at_saddle_step421.csv','product_bound_step421.csv']:
    with (ART/name).open(newline='') as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 15:
        fail(f'{name} does not have 15 rows')
with (ART/'step421_schema.json').open() as f:
    schema = json.load(f)
if schema.get('step') != 421:
    fail('schema step mismatch')
if schema.get('products_ge_threshold') != 0:
    fail('unexpected product threshold count')
print('step421 validation passed')
