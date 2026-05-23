
from pathlib import Path
import csv, json
base = Path(__file__).resolve().parent
required = [
    'omega_compatible_burnol_muntz_dictionary_step140.tex',
    'step140_results_summary.md',
    'omega_compatible_dictionary_gate_table_step140.csv',
    'omega_compatible_threshold_sweep_step140.csv',
    'omega_compatible_best_choices_step140.csv',
    'theorem_map_step140.csv',
    'route_status_step140.csv',
    'step140_schema.json'
]
missing = [r for r in required if not (base/r).exists()]
if missing:
    raise SystemExit(f'Missing required artifacts: {missing}')
# lightweight LaTeX balance check
tex = (base/'omega_compatible_burnol_muntz_dictionary_step140.tex').read_text()
checks = {
    'dollar_even': tex.count('$') % 2 == 0,
    'begin_document': '\\begin{document}' in tex,
    'end_document': '\\end{document}' in tex,
    'boxed_count': tex.count('\\boxed')
}
print(json.dumps(checks, indent=2))
