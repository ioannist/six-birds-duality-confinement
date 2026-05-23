#!/usr/bin/env python3
from pathlib import Path
import json, re, csv
base = Path(__file__).resolve().parent
required = [
    'trace_class_residual_ledger_step146.tex',
    'step146_results_summary.md',
    'trace_class_gate_table_step146.csv',
    'theorem_map_step146.csv',
    'arithmetic_input_table_step146.csv',
    'route_status_step146.csv',
    'nonclaim_boundary_step146.md',
    'step146_schema.json'
]
missing = [f for f in required if not (base/f).exists()]
assert not missing, f"Missing files: {missing}"
tex = (base/'trace_class_residual_ledger_step146.tex').read_text()
for token in ['Trace-class residual ledger criterion','Weighted separation','Tail promotion','Unweighted ledger warning']:
    assert token in tex, f"Missing token {token}"
# crude brace balance
assert tex.count('{') == tex.count('}'), 'Unbalanced braces in TeX'
with open(base/'step146_schema.json') as f:
    schema=json.load(f)
assert schema['step']==146
print('Step 146 artifact check passed.')
