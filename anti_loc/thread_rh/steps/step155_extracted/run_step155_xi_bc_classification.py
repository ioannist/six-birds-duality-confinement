from pathlib import Path
import json

base = Path('/mnt/data/rh_membrane_step155_xi_bc_classification')
required = [
    'xi_bc_residual_classification_step155.tex',
    'step155_results_summary.md',
    'xi_bc_classification_gate_table_step155.csv',
    'xi_bc_classification_table_step155.csv',
    'route_status_step155.csv',
    'construction_tasks_step155.csv',
    'nonclaim_boundary_step155.md',
    'theorem_map_step155.csv',
    'step155_schema.json',
]
results = {'missing': [], 'present': [], 'latex_balance': {}}
for name in required:
    p = base / name
    if p.exists() and p.stat().st_size > 0:
        results['present'].append(name)
    else:
        results['missing'].append(name)
tex = (base / 'xi_bc_residual_classification_step155.tex').read_text()
for sym in ['\\begin{theorem}', '\\end{theorem}', '\\XiBC', '\\Cell']:
    results['latex_balance'][sym] = tex.count(sym)
results['ok'] = not results['missing'] and results['latex_balance']['\\begin{theorem}'] == results['latex_balance']['\\end{theorem}']
(base / 'step155_check_results.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
