from pathlib import Path
import json
import pandas as pd

base = Path(__file__).parent

required = [
    "boundary_symbol_theorem_step161.tex",
    "step161_results_summary.md",
    "boundary_symbol_gate_table_step161.csv",
    "bridge_source_ledger_step161.csv",
    "route_status_step161.csv",
    "theorem_map_step161.csv",
    "content_classification_step161.csv",
    "construction_tasks_step161.csv",
    "nonclaim_boundary_step161.md",
    "step161_schema.json",
    "run_step161_boundary_symbol_checks.py",
]

missing = [f for f in required if not (base / f).exists()]
assert not missing, f"missing required artifacts: {missing}"

schema = json.loads((base / "step161_schema.json").read_text())
assert schema["step"] == 161
assert schema["orientation"] == "adequacy"
assert "Xi_BC" in schema["active_residual"]
assert schema["main_operator"] == "C_l P_eta"
assert "open_external_proof" in schema["main_verdict"]

route = pd.read_csv(base / "route_status_step161.csv")
route_pairs = set(zip(route["route"], route["status"]))
assert ("Hard-support obstruction", "public_shadow") in route_pairs
assert ("Finite singular value evidence", "moving_window_support_only") in route_pairs
assert ("Positive source-frame squeeze", "blocked") in route_pairs
assert ("Scoped Xi_BC residual", "active") in route_pairs

gate = pd.read_csv(base / "boundary_symbol_gate_table_step161.csv")
gate_status = dict(zip(gate["gate"], gate["status"]))
assert gate_status["bridge_factorization"] == "open_external_proof"
assert gate_status["public_shadow_no_go"] == "proved_framework_no_go"
assert gate_status["finite_window_no_go"] == "proved_framework_no_go"
assert gate_status["residual_status"] == "active"

source = pd.read_csv(base / "bridge_source_ledger_step161.csv")
assert "accepted_bridge" not in set(source["status"])
assert "public_shadow" in set(source["status"])
assert "moving_window_support_only" in set(source["status"])

theorems = pd.read_csv(base / "theorem_map_step161.csv")
accepted_bridge = theorems[
    theorems["name"].str.contains("Boundary-symbol theorem", case=False, regex=False)
    & theorems["proof_status"].str.contains("proved", case=False, regex=False)
]
assert accepted_bridge.empty, "bridge theorem must not be marked proved locally"

combined = "\n".join((base / f).read_text() for f in required if f.endswith((".md", ".tex", ".csv", ".json")))
forbidden = [
    "proves " + "RH",
    "accepted bridge " + "extracted",
    "C_l P_eta " + "is compact",
    "essential norm " + "is positive",
]
hits = [phrase for phrase in forbidden if phrase in combined]
assert not hits, f"forbidden overclaim phrases found: {hits}"

print("Step 161 checks passed.")
