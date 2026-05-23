#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step232_dirichlet_L_selberg_test_artifacts")

required = [
    "step232_results_summary.md",
    "step232_schema.json",
    "content_classification_step232.csv",
    "nonclaim_boundary_step232.md",
    "step232_dirichlet_L_selberg_test.tex",
    "derive_dirichlet_L_residual_step232.py",
    "run_step232_checks.py",
    "dirichlet_L_declaration_step232.csv",
    "classification_step232.csv",
    "selberg_generalization_step232.csv",
    "other_selberg_examples_step232.csv",
    "residual_tree_step232.csv",
    "route_status_step232.csv",
    "construction_tasks_step232.csv",
    "classical_theorems_cited_step232.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step232_schema.json").read_text())
assert schema["step"] == 232
assert schema["final_verdict"] == "V_dirichlet_L_outside_dichotomy_selberg_generalization"
assert schema["carrier_definition"]["critical_line"] == "Re(s)=1/2"
assert "outside_Riemann_Dichotomy" in schema["classification_under_Riemann_dichotomy"]
assert "generalized_CRCFT_TE" in schema["selberg_generalization_classification"]

with (OUT / "classification_step232.csv").open() as f:
    rows = list(csv.DictReader(f))
assert any(row["classification_option"] == "outside Riemann Dichotomy" and row["status"] == "accepted" for row in rows)
assert any("generalized CRCFT-TE" in row["classification_option"] and "accepted" in row["status"] for row in rows)

with (OUT / "other_selberg_examples_step232.csv").open() as f:
    examples = list(csv.DictReader(f))
assert len(examples) >= 4
assert any("GL_n" in row["example"] for row in examples)

print("Step 232 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
