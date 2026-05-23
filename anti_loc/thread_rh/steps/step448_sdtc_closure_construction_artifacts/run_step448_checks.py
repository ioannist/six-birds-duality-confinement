#!/usr/bin/env python3
from pathlib import Path
import csv
out=Path(r"/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step448_sdtc_closure_construction_artifacts")
required=['step448_audited_shell_definition.md', 'step448_history_carrier_definition.md', 'step448_trace_instrument_definition.md', 'step448_observable_saturation_trace.md', 'step448_predictive_zero_family.md', 'step448_involution_and_fixed_locus.md', 'step448_zero_ledger_and_anti_invariant_ledger.md', 'step448_quotients_and_comparison_map.md', 'step448_lawfulness_theoremlet.md', 'step448_translation_theorem.md', 'step448_recognition_source_naming.md', 'step448_admissibility_audit.md', 'step448_anti_tautology_check.md', 'step448_negative_controls_audit.md', 'step448_status_of_gamma_sdtc.md', 'step448_mode_b_constraint_ledger.csv', 'step448_mode_b_target_lineage.csv', 'step448_mode_b_grammar_manifest.csv', 'step448_source_notes.md', 'step448_reach_delta.md', 'step448_step_verdict.md', 'step448_schema.json', 'nonclaim_boundary_step448.md', 'run_step448_checks.py']
missing=[x for x in required if not (out/x).exists()]
if missing:
    raise SystemExit('missing artifacts: '+', '.join(missing))
trans=(out/'step448_translation_theorem.md').read_text()
for token in ['A_Z(L)=0', 'RH(L)', 'theorem-grade by construction']:
    if token not in trans:
        raise SystemExit('translation theorem missing '+token)
rec=(out/'step448_recognition_source_naming.md').read_text()
for token in ['Gamma_SDTC-Selberg', 'named, not accepted', 'Readout_SDTC', 'source record is not the readout']:
    if token not in rec:
        raise SystemExit('recognition naming missing '+token)
audit=(out/'step448_admissibility_audit.md').read_text()
if audit.count('| pass |') < 7:
    raise SystemExit('seven-schema audit does not show 7 pass rows')
verdict=(out/'step448_step_verdict.md').read_text()
if 'sdtc_closure_constructed_translation_landed' not in verdict:
    raise SystemExit('wrong verdict')
notes=(out/'step448_source_notes.md').read_text()
for token in ['def:main:involutive-ledger', 'thm:main:duality-confinement-master', 'C_arithmetic_independence', 'Step 447']:
    if token not in notes:
        raise SystemExit('source notes missing '+token)
with (out/'step448_mode_b_grammar_manifest.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
if not any(r['grammar_id']=='G_SDTC_selberg_trace_closure' for r in rows):
    raise SystemExit('grammar manifest missing G_SDTC')
print('step448 validation passed')
print('verdict=sdtc_closure_constructed_translation_landed')
print('gamma_sdtc_status=named_not_accepted')
