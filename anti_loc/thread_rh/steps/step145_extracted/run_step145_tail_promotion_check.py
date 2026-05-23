
import json
from pathlib import Path
p=Path('/mnt/data/rh_membrane_step145_burnol_residual_carrier')
required=[
 'burnol_residual_carrier_step145.tex',
 'step145_results_summary.md',
 'burnol_residual_carrier_gate_table_step145.csv',
 'theorem_map_step145.csv',
 'route_status_step145.csv',
 'arithmetic_input_table_step145.csv',
 'construction_tasks_step145.csv',
 'nonclaim_boundary_step145.md',
 'step145_schema.json'
]
missing=[x for x in required if not (p/x).exists()]
print(json.dumps({'missing':missing,'ok':not missing},indent=2))
