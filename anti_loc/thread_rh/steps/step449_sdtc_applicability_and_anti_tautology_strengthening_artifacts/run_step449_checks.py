#!/usr/bin/env python3
from pathlib import Path
import csv
out=Path(r"/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step449_sdtc_applicability_and_anti_tautology_strengthening_artifacts")
required=['step449_master_theorem_applicability_audit.md', 'step449_applicability_smuggle_audit.md', 'step449_xi_sdtc_domination_records_residual.md', 'step449_carrier_inventory.md', 'step449_pairwise_isomorphism_audit.md', 'step449_joint_packaging_audit.md', 'step449_strengthened_exhibit.md', 'step449_structural_state_pre_derivation_sweep.md', 'step449_anti_tautology_meta.md', 'step449_mode_b_constraint_ledger.csv', 'step449_mode_b_target_lineage.csv', 'step449_mode_b_grammar_manifest.csv', 'step449_source_notes.md', 'step449_reach_delta.md', 'step449_step_verdict.md', 'step449_schema.json', 'nonclaim_boundary_step449.md', 'run_step449_checks.py']
missing=[x for x in required if not (out/x).exists()]
if missing:
    raise SystemExit('missing artifacts: '+', '.join(missing))
app=(out/'step449_master_theorem_applicability_audit.md').read_text()
for token in ['Hypothesis 1', 'PASS', 'Hypothesis 3', 'NOT ESTABLISHED']:
    if token not in app:
        raise SystemExit('applicability audit missing '+token)
smuggle=(out/'step449_applicability_smuggle_audit.md').read_text()
if 'no smuggle detected' not in smuggle.lower():
    raise SystemExit('smuggle audit did not pass')
res=(out/'step449_xi_sdtc_domination_records_residual.md').read_text()
if 'Xi_SDTC_domination_records' not in res:
    raise SystemExit('residual not named')
iso=(out/'step449_pairwise_isomorphism_audit.md').read_text()
if iso.count('| no |') < 20:
    raise SystemExit('pairwise audit missing 20 no-isomorphism rows')
ex=(out/'step449_strengthened_exhibit.md').read_text()
if 'T_SDTC_DTC_SourceReady' not in ex:
    raise SystemExit('strengthened exhibit missing')
with (out/'step449_mode_b_constraint_ledger.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
if not any(r['constraint_id']=='Xi_SDTC_domination_records' and r['status']=='active' for r in rows):
    raise SystemExit('ledger missing active Xi_SDTC residual')
if not any(r['constraint_id']=='Xi_anti_tautology_strict_isomorphism' for r in rows):
    raise SystemExit('ledger missing strict isomorphism row')
verdict=(out/'step449_step_verdict.md').read_text()
if 'sdtc_applicability_audited_anti_tautology_strict_pass' not in verdict:
    raise SystemExit('wrong verdict')
print('step449 validation passed')
print('verdict=sdtc_applicability_audited_anti_tautology_strict_pass')
print('named_residual=Xi_SDTC_domination_records')
