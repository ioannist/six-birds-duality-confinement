#!/usr/bin/env python3
from pathlib import Path
import json, sys
ART = Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step437_modeA_nogo_length_spectrum_artifacts')
required = [
    'mode_a_selection_delta_step437.md','theorem_statement_step437.md','proof_or_diagnosis_step437.md',
    'literature_anchor_step437.md','step437_results_summary.md','step437_schema.json',
    'nonclaim_boundary_step437.md','run_step437_checks.py'
]
missing = [p for p in required if not (ART/p).exists()]
if missing:
    raise SystemExit(f'missing artifacts: {missing}')
schema = json.loads((ART/'step437_schema.json').read_text())
if schema.get('step') != 437 or schema.get('mode') != 'Mode A':
    raise SystemExit('schema mismatch')
checks = {
    'mode_a_selection_delta_step437.md': ['C_length_spectrum_arithmetic_mismatch','Margulis','Lafont-McReynolds','non-clone'],
    'theorem_statement_step437.md': ['arithmetic-independent compact dynamical system','Generic Length-Spectrum No-Go','C_length_spectrum_arithmetic_mismatch'],
    'proof_or_diagnosis_step437.md': ['Margulis','Pollicott-Ruelle','Lafont-McReynolds','Sunada','resists'],
    'literature_anchor_step437.md': ['Margulis','Sarnak','Pollicott-Ruelle','Lafont-McReynolds'],
    'nonclaim_boundary_step437.md': ['No proof of RH','strong universal statement']
}
for fname, phrases in checks.items():
    text = (ART/fname).read_text()
    for phrase in phrases:
        if phrase not in text:
            raise SystemExit(f'{fname} missing phrase: {phrase}')
print('step437 validation passed')
