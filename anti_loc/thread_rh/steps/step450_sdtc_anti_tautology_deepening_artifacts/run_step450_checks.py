#!/usr/bin/env python3
from pathlib import Path
import csv
out=Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step450_sdtc_anti_tautology_deepening_artifacts")
required=['step450_isomorphism_audit_connes.md', 'step450_isomorphism_audit_selberg_maass.md', 'step450_isomorphism_audit_weil_deligne.md', 'step450_isomorphism_audit_beurling_nyman.md', 'step450_isomorphism_joint_observation.md', 'step450_operational_predicate_Pop.md', 'step450_Pop_inaccessibility_to_top_4.md', 'step450_non_conjunctive_verification.md', 'step450_remaining_16_carriers.md', 'step450_anti_tautology_exhibit_update.md', 'step450_mode_b_constraint_ledger.csv', 'step450_mode_b_target_lineage.csv', 'step450_mode_b_grammar_manifest.csv', 'step450_source_notes.md', 'step450_reach_delta.md', 'step450_step_verdict.md', 'step450_schema.json', 'nonclaim_boundary_step450.md', 'run_step450_checks.py']
missing=[x for x in required if not (out/x).exists()]
if missing:
    raise SystemExit('missing artifacts: '+', '.join(missing))
for name in ['connes','selberg_maass','weil_deligne','beurling_nyman']:
    text=(out/f'step450_isomorphism_audit_{name}.md').read_text()
    if 'fails' not in text.lower() or 'Typed-isomorphism failure' not in text:
        raise SystemExit('weak isomorphism audit for '+name)
pop=(out/'step450_operational_predicate_Pop.md').read_text()
if 'Pop_SDTC_DominationCandidateAudit' not in pop or 'Inputs:' not in pop or 'Outputs:' not in pop:
    raise SystemExit('Pop artifact incomplete')
nonconj=(out/'step450_non_conjunctive_verification.md').read_text()
if 'mutual coupling' not in nonconj.lower():
    raise SystemExit('non-conjunctive proof missing mutual coupling')
rem=(out/'step450_remaining_16_carriers.md').read_text()
if rem.count('|') < 50:
    raise SystemExit('remaining carrier table too small')
ex=(out/'step450_anti_tautology_exhibit_update.md').read_text()
if 'T_SDTC_DTC_SourceReady_Pop' not in ex:
    raise SystemExit('exhibit not upgraded')
with (out/'step450_mode_b_constraint_ledger.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
r=next((x for x in rows if x['constraint_id']=='Xi_anti_tautology_strict_isomorphism'), None)
if not r or r['last_checked_attempt']!='step450':
    raise SystemExit('ledger not updated for strict isomorphism')
verdict=(out/'step450_step_verdict.md').read_text()
if 'sdtc_anti_tautology_deepened_at_pvnp_bar' not in verdict:
    raise SystemExit('wrong verdict')
print('step450 validation passed')
print('verdict=sdtc_anti_tautology_deepened_at_pvnp_bar')
print('operational_predicate=Pop_SDTC_DominationCandidateAudit')
