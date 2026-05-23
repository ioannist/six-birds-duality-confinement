#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd

base = Path(__file__).resolve().parent
required = [
    'xi_bc_schatten_tail_step156.tex',
    'step156_results_summary.md',
    'xi_bc_schatten_classification_step156.csv',
    'xi_bc_schatten_gate_table_step156.csv',
    'theorem_map_step156.csv',
    'route_status_step156.csv',
    'nonclaim_boundary_step156.md',
    'step156_schema.json'
]
missing = [f for f in required if not (base/f).exists()]
checks = {'missing_required': missing}
tex = (base/'xi_bc_schatten_tail_step156.tex').read_text()
checks['has_main_identity'] = 'mathcal R_\\ell=A_\\ell^*A_\\ell' in tex
checks['has_calkin_gate'] = '[C_\\ell P_\\eta]' in tex
checks['classification_rows'] = len(pd.read_csv(base/'xi_bc_schatten_classification_step156.csv'))
checks['gate_rows'] = len(pd.read_csv(base/'xi_bc_schatten_gate_table_step156.csv'))
checks['passed'] = not missing and checks['has_main_identity'] and checks['has_calkin_gate']
print(json.dumps(checks, indent=2))
