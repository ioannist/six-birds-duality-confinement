#!/usr/bin/env python3
from pathlib import Path
import csv, json
out=Path(__file__).resolve().parent
required=[
 'xi_bc_schatten_tail_audit_step156.tex',
 'step156_results_summary.md',
 'xi_bc_schatten_tail_gate_table_step156.csv',
 'theorem_map_step156.csv',
 'route_status_step156.csv',
 'construction_tasks_step156.csv',
 'nonclaim_boundary_step156.md',
 'step156_schema.json',
 'xi_bc_schatten_singular_profiles_step156.png',
 'xi_bc_tail_payability_step156.png',
 'xi_bc_schatten_proxy_step156.csv',
]
missing=[p for p in required if not (out/p).exists()]
assert not missing, f"Missing files: {missing}"
with open(out/'step156_schema.json') as f:
    data=json.load(f)
assert data['step']==156
with open(out/'xi_bc_schatten_tail_gate_table_step156.csv') as f:
    rows=list(csv.DictReader(f))
assert any(r['status']=='N_scoped_residual' and r['current_verdict']=='active' for r in rows)
print({'status':'ok','checked':len(required),'missing':missing})
