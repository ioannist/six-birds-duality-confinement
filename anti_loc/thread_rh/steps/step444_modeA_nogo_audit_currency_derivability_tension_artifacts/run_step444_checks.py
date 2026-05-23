#!/usr/bin/env python3
from pathlib import Path
import json
ART=Path('/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step444_modeA_nogo_audit_currency_derivability_tension_artifacts')
required=['mode_a_selection_delta_step444.md','theorem_statement_step444.md','proof_or_diagnosis_step444.md','literature_anchor_step444.md','three_attempt_cross_step_evidence_step444.md','step444_results_summary.md','step444_schema.json','nonclaim_boundary_step444.md','run_step444_checks.py']
missing=[p for p in required if not (ART/p).exists()]
if missing: raise SystemExit(f'missing artifacts: {missing}')
schema=json.loads((ART/'step444_schema.json').read_text())
if schema.get('step')!=444: raise SystemExit('schema mismatch')
checks={
 'mode_a_selection_delta_step444.md':['C_zero_height_audit_currency_smuggling','C_positivity_audit_kernel_positivity_must_derive','C_weil_positivity_explicit_formula_smuggling','Conrey 2003','Bombieri 2000','Lagarias 2004','non-clone'],
 'theorem_statement_step444.md':['RH-distinguishing','derivable from non-arithmetic primitives','diagnosis-grade'],
 'literature_anchor_step444.md':['Conrey 2003','Bombieri 2000','Lagarias 2004','Weil','Yoshida','[U not_down_q, C(U) down_B a^sharp]'],
 'three_attempt_cross_step_evidence_step444.md':['Step 441','Step 442','Step 443','concrete + RH-distinguishing'],
 'step444_results_summary.md':['theorem-grade for the three dominant classes','diagnosis-grade','local saturation']
}
for fname,phrases in checks.items():
    text=(ART/fname).read_text()
    for phrase in phrases:
        if phrase not in text: raise SystemExit(f'{fname} missing {phrase}')
print('step444 validation passed')
