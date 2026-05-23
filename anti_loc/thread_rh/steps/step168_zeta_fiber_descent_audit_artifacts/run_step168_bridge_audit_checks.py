#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step168_zeta_fiber_descent_audit_artifacts")

REQUIRED = [
    "step168_results_summary.md",
    "step168_schema.json",
    "content_classification_step168.csv",
    "nonclaim_boundary_step168.md",
    "step168_zeta_fiber_descent.tex",
    "run_step168_bridge_audit_checks.py",
    "bridge_comparison_step168.csv",
    "source_audit_step168.csv",
    "bridge_verdict_step168.csv",
    "residual_tree_step168.csv",
    "route_status_step168.csv",
    "construction_tasks_step168.csv",
]

def die(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

for name in REQUIRED:
    path = ART / name
    if not path.exists():
        die(f"missing artifact {path}")
    if path.stat().st_size == 0:
        die(f"empty artifact {path}")

schema = json.loads(read_text(ART / "step168_schema.json"))

expected_top = {
    "step": 168,
    "orientation": "adequacy",
    "bridge_under_audit": "H6 zeta_fiber_descent_to_Xi_BC",
    "bridge_verdict": "non_comparability",
    "final_verdict": "non_comparability",
}
for key, value in expected_top.items():
    if schema.get(key) != value:
        die(f"schema {key} expected {value!r}, got {schema.get(key)!r}")

if schema.get("parent_residuals") != ["Xi_BC", "Xi_BC_Hecke"]:
    die("schema parent_residuals mismatch")

if "typed_no_go_statement" not in schema:
    die("schema missing typed_no_go_statement for non_comparability verdict")

retained = schema.get("retained_nogos", [])
required_nogos = [
    "public-shadow non-promotion",
    "finite-window Calkin blindness",
    "auxiliary-GRH smuggling",
    "incomplete character spectrum is support-only without tail/exhaustivity",
    "scalar L-function identity is not carrier identity",
]
for item in required_nogos:
    if item not in retained:
        die(f"retained no-go missing: {item}")

tree_update = schema.get("residual_tree_update", {}).get("H6_zeta_fiber_descent_to_Xi_BC", {})
if tree_update.get("updated_status") != "non_comparability":
    die("H6 residual tree update missing non_comparability")

for csv_name in [
    "bridge_comparison_step168.csv",
    "source_audit_step168.csv",
    "bridge_verdict_step168.csv",
    "residual_tree_step168.csv",
    "route_status_step168.csv",
    "construction_tasks_step168.csv",
    "content_classification_step168.csv",
]:
    with (ART / csv_name).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        die(f"{csv_name} has no data rows")

comparison = list(csv.DictReader((ART / "bridge_comparison_step168.csv").open(newline="", encoding="utf-8")))
axes = {row["axis"] for row in comparison}
for axis in ["Hilbert carrier", "Native probes", "Dissolving probes", "Audit energy", "Zero ledger"]:
    if axis not in axes:
        die(f"bridge comparison missing axis {axis}")

verdict_rows = list(csv.DictReader((ART / "bridge_verdict_step168.csv").open(newline="", encoding="utf-8")))
if verdict_rows[0].get("verdict") != "non_comparability":
    die("bridge_verdict_step168.csv verdict mismatch")

tree_rows = list(csv.DictReader((ART / "residual_tree_step168.csv").open(newline="", encoding="utf-8")))
h6 = [row for row in tree_rows if row.get("node_id") == "H6_zeta_fiber_descent_to_Xi_BC"]
if not h6 or h6[0].get("status") != "non_comparability":
    die("residual_tree_step168.csv does not update H6")

combined = "\n".join(
    read_text(ART / name)
    for name in REQUIRED
    if name != "run_step168_bridge_audit_checks.py"
)

forbidden = [
    "proves " + "RH",
    "RH " + "proof",
    "essential norm " + "is positive",
    "C_l P_eta " + "is compact",
    "unconditional " + "Xi_BC=0",
]
for phrase in forbidden:
    if phrase in combined:
        die(f"forbidden phrase present: {phrase}")

sentences = re.split(r"(?<=[.!?])\s+", combined)
for sentence in sentences:
    if "Xi_BC_Hecke|_{K=Q,chi=1} = Xi_BC" in sentence and "does not claim" not in sentence:
        die("unqualified equality assertion found")
    if "bridge_equality" in sentence and "would require" not in sentence and "lacks" not in sentence and "excluded" not in sentence:
        die("bridge_equality mentioned without rejection or conditions")
    if "does not supply closure of Xi_BC" in sentence and "closure of Xi_BC_Hecke" in sentence:
        continue

weakening_markers = [
    "public-shadow non-promotion is optional",
    "finite-window Calkin blindness is optional",
    "auxiliary-GRH smuggling is allowed",
    "incomplete character spectra are accepted",
    "scalar L-function identity is carrier identity",
]
for marker in weakening_markers:
    if marker in combined:
        die(f"weakening retained no-go found: {marker}")

print("PASS step168 bridge audit checks")
print(f"artifacts_checked={len(REQUIRED)}")
print("bridge_verdict=non_comparability")

