from pathlib import Path
import csv
import json
import re

base = Path(__file__).parent

required = [
    "step165_results_summary.md",
    "step165_schema.json",
    "content_classification_step165.csv",
    "nonclaim_boundary_step165.md",
    "step165_shifted_co_poisson.tex",
    "run_step165_shifted_co_poisson_checks.py",
    "source_audit_step165.csv",
    "bridge_atlas_step165.csv",
    "residual_tree_step165.csv",
    "shifted_co_poisson_obligation_split_step165.csv",
    "route_status_step165.csv",
    "construction_tasks_step165.csv",
]

missing = [name for name in required if not (base / name).exists()]
assert not missing, f"missing required artifacts: {missing}"

schema = json.loads((base / "step165_schema.json").read_text())
allowed = {
    "accepted_exact_route",
    "conditional_exact_route",
    "split_external_theorem",
    "typed_no_go",
}
assert schema["step"] == 165
assert schema["orientation"] == "adequacy"
assert "Xi_BC" in schema["active_residual"]
assert schema["main_operator"] == "C_l P_eta"
assert schema["typed_context"] == "Shifted co-Poisson factorization route on Burnol packets"
assert schema["new_branch_residual"] == "Xi_cP_shifted_l"
assert schema["source_audit_verdict"] in allowed
assert schema["final_verdict"] == schema["source_audit_verdict"]
assert schema["source_audit_verdict"] == "split_external_theorem"
assert "public-shadow non-promotion" in schema["retained_nogos"]
assert "finite-window Calkin blindness" in schema["retained_nogos"]
assert "Calkin-bridge lane G2-G5 (step 163)" in schema["lanes_carried_forward"]
assert "Per-zero finite-carrier lane SL164.1 (step 164)" in schema["lanes_carried_forward"]
assert set(schema["shifted_co_poisson_obligation_split"].keys()) == {
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
}
assert schema["next_step"]["step"] == 166

def read_csv(name):
    with (base / name).open(newline="") as handle:
        return list(csv.DictReader(handle))

source_rows = read_csv("source_audit_step165.csv")
assert len(source_rows) >= 8
assert not any(row["audit_verdict"] == "accepted_exact_route" for row in source_rows)
assert any("unshifted" in row["audit_verdict"] for row in source_rows)

obligations = read_csv("shifted_co_poisson_obligation_split_step165.csv")
assert {row["obligation"] for row in obligations} == {"H1", "H2", "H3", "H4", "H5"}
status = {row["obligation"]: row["status"] for row in obligations}
assert status["H1"] == "framework_defined"
for key in ["H2", "H3", "H4", "H5"]:
    assert status[key] == "open_external_proof"

tree = read_csv("residual_tree_step165.csv")
branches = {row["node_id"] for row in tree}
assert "Xi_BC" in branches
assert "Xi_BC_Calkin_bridge_G2_G5" in branches
assert "Xi_matrix_source_{l,Rho_fin,A_fin,K_fin}" in branches
assert "Xi_cP_shifted_l" in branches

combined_targets = [
    "step165_results_summary.md",
    "step165_shifted_co_poisson.tex",
    "nonclaim_boundary_step165.md",
    "step165_schema.json",
]
combined = "\n".join((base / name).read_text() for name in combined_targets)

literal_forbidden = [
    "proves RH",
    "RH proof",
    "essential norm is positive",
    "C_l P_eta is compact",
    "unconditional Xi_BC=0",
]
hits = [phrase for phrase in literal_forbidden if phrase in combined]
assert not hits, f"forbidden overclaim phrases found: {hits}"

sentences = re.split(r"(?<=[.!?])\s+", combined.replace("\n", " "))

def negated_or_open(sentence):
    lowered = sentence.lower()
    return any(
        token in lowered
        for token in [
            "not",
            "does not",
            "do not",
            "open",
            "carried forward",
            "remain",
            "without",
            "no source",
            "not modified",
        ]
    )

for sentence in sentences:
    lowered = sentence.lower()
    mentions_gates = (
        "g2-g5" in lowered
        or "g2`-`g5" in lowered
        or "g2--g5" in lowered
        or ("g2" in lowered and "g5" in lowered)
    )
    if mentions_gates and re.search(r"\b(closed|closes|proved|settled)\b", lowered):
        assert negated_or_open(sentence), f"Calkin lane closure overclaim: {sentence}"
    if "sl164.1" in lowered and re.search(r"\b(supplied|proved|closed|resolved)\b", lowered):
        assert negated_or_open(sentence), f"SL164.1 overclaim: {sentence}"
    if ("public-shadow" in lowered or "finite-window" in lowered) and re.search(
        r"\b(remove|removed|weaken|weakened|bypass|bypassed|drop|dropped)\b",
        lowered,
    ):
        assert negated_or_open(sentence), f"no-go weakening sentence: {sentence}"

nonclaim = (base / "nonclaim_boundary_step165.md").read_text()
required_nonclaims = [
    "does NOT prove RH",
    "does NOT prove `Xi_BC = 0` unconditionally",
    "does NOT prove the shifted co-Poisson factorization",
    "does NOT close the Calkin-bridge lane",
    "does NOT close the per-zero finite-carrier lane",
    "does NOT remove, weaken, or bypass public-shadow non-promotion",
    "does NOT remove, weaken, or bypass finite-window Calkin blindness",
    "does NOT begin any step 166 lane",
]
missing_nonclaims = [phrase for phrase in required_nonclaims if phrase not in nonclaim]
assert not missing_nonclaims, f"missing mandatory nonclaim phrases: {missing_nonclaims}"

print("Step 165 shifted co-Poisson checks passed.")
