#!/usr/bin/env python3
from pathlib import Path
import json, csv
base = Path(__file__).resolve().parent
required = [
    'xi_bc_residual_classification_step155.tex',
    'step155_results_summary.md',
    'xi_bc_classification_gate_table_step155.csv',
    'theorem_map_step155.csv',
    'route_status_step155.csv',
    'construction_tasks_step155.csv',
    'nonclaim_boundary_step155.md',
    'step155_schema.json',
]
missing = [f for f in required if not (base/f).exists()]
print(json.dumps({"missing": missing, "ok": not missing}, indent=2))
for csv_name in ['xi_bc_classification_gate_table_step155.csv','theorem_map_step155.csv','route_status_step155.csv']:
    with open(base/csv_name, newline='') as f:
        rows = list(csv.reader(f))
    print(csv_name, 'rows=', len(rows)-1, 'cols=', len(rows[0]))
