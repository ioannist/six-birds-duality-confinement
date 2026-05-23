#!/usr/bin/env python3
from pathlib import Path
import json
ART = Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step438_modeA_nogo_ensemble_pointwise_artifacts')
required = [
    'mode_a_selection_delta_step438.md','theorem_statement_step438.md','proof_or_diagnosis_step438.md',
    'literature_anchor_step438.md','step438_results_summary.md','step438_schema.json',
    'nonclaim_boundary_step438.md','run_step438_checks.py'
]
missing = [p for p in required if not (ART/p).exists()]
if missing:
    raise SystemExit(f'missing artifacts: {missing}')
schema = json.loads((ART/'step438_schema.json').read_text())
if schema.get('step') != 438 or schema.get('status') != 'theorem-grade structural no-go':
    raise SystemExit('schema mismatch')
checks = {
    'mode_a_selection_delta_step438.md': ['C_ensemble_distributional_not_pointwise','Erdős-Schlein-Yau','Tao-Vu','Montgomery','Odlyzko','non-clone'],
    'theorem_statement_step438.md': ['vague','Spec(H)','sine-kernel','C_ensemble_distributional_not_pointwise'],
    'proof_or_diagnosis_step438.md': ['Vague convergence','gamma_n+1','probability zero','theorem-grade'],
    'literature_anchor_step438.md': ['Erdős-Schlein-Yau','Tao','Wigner-Dyson-Mehta','Montgomery 1973','Odlyzko 1987/2001'],
    'nonclaim_boundary_step438.md': ['No proof of RH','distributional local statistics']
}
for fname, phrases in checks.items():
    text = (ART/fname).read_text()
    for phrase in phrases:
        if phrase not in text:
            raise SystemExit(f'{fname} missing phrase: {phrase}')
print('step438 validation passed')
