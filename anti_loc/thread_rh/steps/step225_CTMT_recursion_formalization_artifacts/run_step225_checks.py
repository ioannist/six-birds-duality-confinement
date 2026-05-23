#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step225_CTMT_recursion_formalization_artifacts")

required = [
    "step225_results_summary.md",
    "step225_schema.json",
    "content_classification_step225.csv",
    "nonclaim_boundary_step225.md",
    "step225_CTMT_recursion_formalization.tex",
    "run_step225_checks.py",
    "instance_table_step225.csv",
    "terminal_object_adaptation_step225.csv",
    "corpus_inclusion_recommendation_step225.csv",
    "residual_tree_step225.csv",
    "route_status_step225.csv",
    "construction_tasks_step225.csv",
    "classical_theorems_cited_step225.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step225_schema.json").read_text())
assert schema["step"] == 225
assert schema["orientation"] == "synthesis-case-3"
assert schema["target"] == "CTMT recursion formalization as foundational typed condition"
assert schema["final_verdict"] == "V_CTMT_recursion_formalized_5_track"
assert "verified-on-5-track-instances" in schema["theorem_statement"]["status"]
assert len(schema["proof_outline"]) >= 5
assert len(schema["instance_table"]) == 5
assert len(schema["terminal_object_adaptation_sub_finding"]["forms"]) >= 5

with (OUT / "instance_table_step225.csv").open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 6
assert any(row["track"] == "P-vs-NP" for row in rows)
assert any(row["track"] == "Navier-Stokes" for row in rows)
assert any("Branch B" in row["track"] for row in rows)

with (OUT / "terminal_object_adaptation_step225.csv").open() as f:
    adap = list(csv.DictReader(f))
assert len(adap) >= 6
assert any("package-atlas" in row["terminal_object_form"] for row in adap)
assert any("PDE" in row["terminal_object_form"] for row in adap)

with (OUT / "corpus_inclusion_recommendation_step225.csv").open() as f:
    recs = list(csv.DictReader(f))
assert len(recs) >= 4
assert any(row["target_file"] == "adequacy.tex" for row in recs)

print("Step 225 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
