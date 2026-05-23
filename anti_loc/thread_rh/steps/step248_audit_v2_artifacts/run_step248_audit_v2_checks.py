#!/usr/bin/env python3
import csv, json
from pathlib import Path
BASE=Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step248_audit_v2_artifacts")
AUDIT=Path("/home/repos/six-birds-foundations-iii/anti_loc/RH_framework_audit_v2.md")
required=["step248_results_summary.md","step248_schema.json","content_classification_step248.csv","nonclaim_boundary_step248.md","step248_audit_v2_meta.tex","RH_framework_audit_v2.md","run_step248_audit_v2_checks.py","audit_structure_step248.csv","framework_typed_conditions_step248.csv","cross_track_validations_step248.csv","19_carrier_table_step248.csv","literature_audits_step248.csv","corpus_recommendations_step248.csv","open_questions_step248.csv","residual_tree_step248.csv","route_status_step248.csv"]
missing=[r for r in required if not (BASE/r).exists() and r!="RH_framework_audit_v2.md"]
if missing: raise SystemExit(f"missing artifacts: {missing}")
if not AUDIT.exists(): raise SystemExit("main audit missing")
text=AUDIT.read_text().splitlines()
if len(text) < 2000: raise SystemExit(f"audit too short: {len(text)}")
schema=json.loads((BASE/'step248_schema.json').read_text())
assert schema['step']==248
assert schema['final_verdict']=='V_audit_v2_integrated'
assert schema['audit_document_size_lines']==len(text)
for marker in ['Candidate Foundational Typed Conditions','Nineteen-Carrier Dichotomy Survey','Cross-Track Validation Matrix','Independent Codification Table','Strategic Path 1/2/3 Update']:
    if not any(marker in line for line in text): raise SystemExit(f"missing marker {marker}")
with (BASE/'cross_track_validations_step248.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==15
with (BASE/'19_carrier_table_step248.csv').open(newline='') as f:
    carriers=list(csv.DictReader(f))
assert len(carriers)==19
print('step248 validation passed')
