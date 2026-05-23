from pathlib import Path
import csv
import json
import re
import sys

base = Path(__file__).parent

required = [
    "step164_results_summary.md",
    "step164_schema.json",
    "content_classification_step164.csv",
    "nonclaim_boundary_step164.md",
    "step164_per_zero_decomposition.tex",
    "run_step164_per_zero_checks.py",
    "per_zero_declarations_step164.csv",
    "finite_carrier_step164.csv",
    "matrix_elements_step164.csv",
    "per_zero_gate_status_step164.csv",
    "sub_residual_tree_step164.csv",
    "route_status_step164.csv",
    "construction_tasks_step164.csv",
    "source_ledger_step164.csv",
]

missing = [name for name in required if not (base / name).exists()]
if missing:
    raise AssertionError(f"missing required artifacts: {missing}")

schema = json.loads((base / "step164_schema.json").read_text())
assert schema["step"] == 164
assert schema["orientation"] == "adequacy"
assert "Xi_BC" in schema["active_residual"]
assert schema["main_operator"] == "C_l P_eta"
assert schema["diagonal_structure"] in {
    "diagonal",
    "off-diagonal-structured",
    "off-diagonal-unstructured",
    "indeterminate-on-fin",
}
assert schema["final_verdict"] in {
    "finite_carrier_diagnostic_diagonal",
    "finite_carrier_diagnostic_coupled",
    "finite_carrier_diagnostic_indeterminate",
}
assert "public-shadow non-promotion" in schema["retained_nogos"]
assert "finite-window Calkin blindness" in schema["retained_nogos"]
assert schema["final_verdict"] == "finite_carrier_diagnostic_indeterminate"
assert schema["diagonal_structure"] == "indeterminate-on-fin"
assert schema["next_step"]["step"] == 165

def read_csv(name):
    with (base / name).open(newline="") as handle:
        return list(csv.DictReader(handle))

decls = read_csv("per_zero_declarations_step164.csv")
assert {row["id"] for row in decls} == {"D1", "D2", "D3", "D4"}

finite = read_csv("finite_carrier_step164.csv")
finite_items = {row["item"] for row in finite}
assert {"Rho_fin", "N", "A_fin", "K_fin", "H_eta_fin"}.issubset(finite_items)

matrix = read_csv("matrix_elements_step164.csv")
assert len(matrix) == 9
assert {row["source_ledger_ref"] for row in matrix} == {"SL164.1"}
assert all("conditional" in row["status"] for row in matrix)

gates = read_csv("per_zero_gate_status_step164.csv")
gate_status = {row["gate"]: row["status"] for row in gates}
assert gate_status["G1_rho"] == "framework_defined"
for gate in ["G2_rho", "G3_rho", "G4_rho", "G5_rho"]:
    assert gate_status[gate] == "open_external_proof"

routes = read_csv("route_status_step164.csv")
route_names = {row["route"] for row in routes}
for expected in [
    "Per-rho diagonal lane",
    "Per-rho coupling lane",
    "Shifted co-Poisson lane",
    "Global G2-G5 lanes",
]:
    assert expected in route_names

combined_targets = [
    "step164_results_summary.md",
    "step164_per_zero_decomposition.tex",
    "nonclaim_boundary_step164.md",
    "step164_schema.json",
]
combined = "\n".join((base / name).read_text() for name in combined_targets)

literal_forbidden = [
    "proves RH",
    "RH proof",
    "essential norm is positive",
    "C_l P_eta is compact",
    "unconditional Xi_BC=0",
    "C_l on the completed H_eta is compact",
]
hits = [phrase for phrase in literal_forbidden if phrase in combined]
if hits:
    raise AssertionError(f"forbidden overclaim phrases found: {hits}")

sentences = re.split(r"(?<=[.!?])\s+", combined.replace("\n", " "))

def is_negated(sentence):
    lowered = sentence.lower()
    negators = [
        "not",
        "does not",
        "do not",
        "no ",
        "without",
        "open_external_proof",
        "open",
        "not certify",
        "not close",
        "not proved",
    ]
    return any(negator in lowered for negator in negators)

for sentence in sentences:
    lowered = sentence.lower()
    mentions_global_gates = (
        "g2-g5" in lowered
        or "g2`-`g5" in lowered
        or "g2--g5" in lowered
        or ("g2" in lowered and "g5" in lowered)
    )
    if mentions_global_gates and re.search(r"\b(proved|closed|settled)\b", lowered):
        if not is_negated(sentence):
            raise AssertionError(f"global G2-G5 overclaim sentence: {sentence}")
    if "completed-carrier theorem" in lowered and "promote" in lowered:
        if not is_negated(sentence):
            raise AssertionError(f"diagnostic promotion overclaim sentence: {sentence}")
    if ("public-shadow" in lowered or "finite-window" in lowered) and re.search(
        r"\b(remove|removed|weaken|weakened|drop|dropped)\b", lowered
    ):
        raise AssertionError(f"no-go removal sentence: {sentence}")

nonclaim = (base / "nonclaim_boundary_step164.md").read_text()
required_nonclaims = [
    "does NOT prove RH",
    "does NOT prove `Xi^BC = 0`",
    "does NOT promote this finite-carrier diagnostic",
    "does NOT prove `G2`-`G5`",
    "does NOT promote `public_shadow`",
    "does NOT subsume the global `Xi_BC`",
    "does NOT pivot to a different carrier",
    "does NOT begin any step 165 lane",
]
missing_nonclaims = [phrase for phrase in required_nonclaims if phrase not in nonclaim]
if missing_nonclaims:
    raise AssertionError(f"missing mandatory nonclaim phrases: {missing_nonclaims}")

print("Step 164 per-zero checks passed.")
