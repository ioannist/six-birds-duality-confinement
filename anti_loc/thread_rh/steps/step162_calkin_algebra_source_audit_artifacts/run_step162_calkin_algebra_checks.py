from pathlib import Path
import json
import pandas as pd

base = Path(__file__).parent

required = [
    "calkin_algebra_source_audit_step162.tex",
    "step162_results_summary.md",
    "calkin_algebra_gate_table_step162.csv",
    "operator_generator_ledger_step162.csv",
    "source_theorem_extraction_step162.csv",
    "bridge_normal_form_step162.csv",
    "route_status_step162.csv",
    "theorem_map_step162.csv",
    "content_classification_step162.csv",
    "construction_tasks_step162.csv",
    "nonclaim_boundary_step162.md",
    "step162_schema.json",
    "run_step162_calkin_algebra_checks.py",
]

missing = [f for f in required if not (base / f).exists()]
assert not missing, f"missing required artifacts: {missing}"

schema = json.loads((base / "step162_schema.json").read_text())
assert schema["step"] == 162
assert schema["orientation"] == "adequacy"
assert "Xi_BC" in schema["active_residual"]
assert schema["main_operator"] == "C_l P_eta"
assert schema["final_status"] == "split_external_theorem"
assert schema["algebra"]["A_eta"] == "C*(P_infty, M_m, P_eta, I)"
assert schema["algebra"]["quotient_object"] == "q_eta(C_l P_eta)"

gates = pd.read_csv(base / "calkin_algebra_gate_table_step162.csv")
gate_status = dict(zip(gates["gate"], gates["status"]))
assert gate_status["algebra_declaration"] == "framework_defined"
assert gate_status["compact_ideal"] == "framework_defined"
assert gate_status["quotient_object"] == "framework_defined"
assert gate_status["faithful_symbol"] == "open_external_proof"
assert gate_status["normal_form"] == "open_external_proof"
assert gate_status["final_verdict"] == "split_external_theorem"

ops = pd.read_csv(base / "operator_generator_ledger_step162.csv")
for op in ["P_infty", "M_m", "P_eta", "C_l", "C_l P_eta"]:
    assert op in set(ops["operator"]), f"missing operator ledger row: {op}"

sources = pd.read_csv(base / "source_theorem_extraction_step162.csv")
accepted = sources[sources["verdict"] == "accepted_bridge_source"]
gate_cols = ["exact_carrier", "calkin_quotient", "h_eta_bridge", "lower_faithfulness", "compact_remainder"]
if not accepted.empty:
    assert (accepted[gate_cols] == "pass").all(axis=None), "accepted bridge source without all gates passed"
assert accepted.empty, "Step 162 should not accept a local bridge source"
assert "public_shadow" in set(sources["verdict"])
assert "diagnostic_only" in set(sources["verdict"])

normal = pd.read_csv(base / "bridge_normal_form_step162.csv")
assert "Semilocal prolate repair normal form" in set(normal["candidate"])
assert "Co-Poisson exact factorization normal form" in set(normal["candidate"])

route = pd.read_csv(base / "route_status_step162.csv")
route_pairs = set(zip(route["route"], route["status"]))
assert ("Typed Calkin algebra declaration", "framework_defined") in route_pairs
assert ("Burnol/Sonine boundary-symbol theorem", "split_external_theorem") in route_pairs
assert ("Accepted bridge source", "not_found") in route_pairs
assert ("Hard-support obstruction", "public_shadow") in route_pairs
assert ("Finite singular value evidence", "moving_window_support_only") in route_pairs

combined = "\n".join((base / f).read_text() for f in required if f.endswith((".md", ".tex", ".csv", ".json")))
forbidden = [
    "proves " + "RH",
    "RH " + "proof",
    "unconditional " + "Xi_BC=0",
    "C_l P_eta " + "is compact",
    "essential norm " + "is positive",
    "accepted_bridge_source," + "pass,pass,pass,pass,pass",
]
hits = [phrase for phrase in forbidden if phrase in combined]
assert not hits, f"forbidden overclaim phrases found: {hits}"

print("Step 162 checks passed.")
