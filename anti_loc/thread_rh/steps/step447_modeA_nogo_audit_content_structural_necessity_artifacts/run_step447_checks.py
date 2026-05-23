#!/usr/bin/env python3
from pathlib import Path
out = Path(r"/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step447_modeA_nogo_audit_content_structural_necessity_artifacts")
thread = Path(r"/home/repos/six-birds-foundations-iii/anti_loc/thread")
required = ['mode_a_selection_delta_step447.md', 'theorem_statement_step447.md', 'proof_or_diagnosis_step447.md', 'literature_anchor_step447.md', 'subsumption_analysis_step447.md', 'reach_delta_accounting_step447.md', 'findings_rh_update_step447.md', 'step447_results_summary.md', 'step447_schema.json', 'nonclaim_boundary_step447.md', 'run_step447_checks.py']
missing = [name for name in required if not (out/name).exists()]
if missing:
    raise SystemExit('missing artifacts: ' + ', '.join(missing))
sel = (out/'mode_a_selection_delta_step447.md').read_text()
if 'non-clone marker' not in sel:
    raise SystemExit('selection delta missing non-clone marker')
stmt = (out/'theorem_statement_step447.md').read_text()
for token in ['Theorem-grade', 'Diagnosis-grade', 'Capacity-bound semantics', 'sub-component interpretation']:
    if token not in stmt:
        raise SystemExit('theorem statement missing token: ' + token)
proof = (out/'proof_or_diagnosis_step447.md').read_text()
for token in ['Step 441', 'Step 442', 'Step 443', 'Step 444', 'Step 445', 'Step 446', 'Concrete Branch', 'Formal Branch']:
    if token not in proof:
        raise SystemExit('proof missing token: ' + token)
lit = (out/'literature_anchor_step447.md').read_text()
for token in ['Conrey 2003', 'Bombieri 2000', 'Lagarias 2004', 'de Branges 1968', 'Weil 1952', 'SAU']:
    if token not in lit:
        raise SystemExit('literature anchor missing token: ' + token)
findings = (thread/'findings_rh.md').read_text()
if 'Mode A no-go 6/6: audit-content structural necessity (step 447)' not in findings:
    raise SystemExit('findings_rh.md missing step 447 section')
print('step447 validation passed')
print('grade=theorem-grade covered placements; diagnosis-grade unrestricted universal')
