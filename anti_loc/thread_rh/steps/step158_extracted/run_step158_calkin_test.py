#!/usr/bin/env python3
import csv, json, pathlib
base=pathlib.Path(__file__).resolve().parent
required=[
 'pulled_evaluator_weyl_symbol_step158.tex',
 'step158_results_summary.md',
 'calkin_weyl_gate_table_step158.csv',
 'calkin_classification_step158.csv',
 'theorem_map_step158.csv',
 'route_status_step158.csv',
 'step158_schema.json'
]
missing=[p for p in required if not (base/p).exists()]
assert not missing, f'missing files: {missing}'
with open(base/'step158_schema.json') as f:
    schema=json.load(f)
assert schema['orientation']=='adequacy'
assert 'Xi_BC' in schema['active_residual']
print(json.dumps({'ok':True,'checked':required,'step':schema['step']},indent=2))
