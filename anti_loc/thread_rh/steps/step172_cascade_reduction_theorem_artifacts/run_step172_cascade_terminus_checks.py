from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step172_cascade_reduction_theorem_artifacts")

REQUIRED = [
    "step172_results_summary.md",
    "step172_schema.json",
    "content_classification_step172.csv",
    "nonclaim_boundary_step172.md",
    "step172_cascade_reduction_theorem.tex",
    "run_step172_cascade_terminus_checks.py",
    "reduction_chain_step172.csv",
    "external_content_interface_step172.csv",
    "foundational_typed_condition_candidate_step172.csv",
    "residual_tree_step172.csv",
    "route_status_step172.csv",
    "next_external_attack_lanes_step172.csv",
]


def die(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


for name in REQUIRED:
    path = ART / name
    if not path.exists():
        die(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        die(f"empty artifact: {name}")

schema = json.loads((ART / "step172_schema.json").read_text(encoding="utf-8"))

if schema.get("step") != 172:
    die("schema step must be 172")
if schema.get("orientation") != "adequacy":
    die("schema orientation must be adequacy")
if schema.get("active_residual") != "Xi_BC":
    die("active_residual must be Xi_BC")
expected_theorem = "Shifted Co-Poisson Cascade Reduction for Xi_BC on the Burnol/Sonine Carrier"
if schema.get("main_theorem") != expected_theorem:
    die("main_theorem mismatch")
if schema.get("final_verdict") != "cascade_reduction_theorem_terminus":
    die("final_verdict mismatch")
if schema.get("track_terminus_state") is not True:
    die("track_terminus_state must be true")

chain = schema.get("reduction_chain") or []
if [item.get("stage") for item in chain] != ["a", "b", "c", "d", "e"]:
    die("reduction_chain must contain stages a-e")
for stage, source in [("a", 169), ("b", 169), ("c", 170), ("d", 171), ("e", 172)]:
    item = next((x for x in chain if x.get("stage") == stage), None)
    if item is None:
        die(f"missing stage {stage}")
    if stage != "e" and source not in item.get("source_steps", []):
        die(f"stage {stage} missing source step {source}")
    if stage == "e" and not all(s in item.get("source_steps", []) for s in [169, 170, 171]):
        die("stage e must cite 169, 170, 171")

iface = schema.get("external_content_interface") or []
ids = {item.get("obligation_id") for item in iface}
for required_id in {
    "BC_C_L_rho_k_per_label",
    "BC_C_full_ZI_COV_CP",
    "BC_C_direct_jet_surjectivity_or_annihilation",
    "Branch_A_G2_G5",
    "Branch_B_SL164_1",
    "Hecke_H1_H5",
    "Hecke_H6_V_NC_bridge",
}:
    if required_id not in ids:
        die(f"missing external interface id: {required_id}")

terminal = next(item for item in iface if item.get("obligation_id") == "BC_C_L_rho_k_per_label")
terminal_text = " ".join(str(terminal.get(key, "")) for key in terminal)
for needle in ["rho", "k", "L_{rho,k}", "legal G", "K_infty"]:
    if needle not in terminal_text:
        die(f"terminal interface missing {needle}")

condition = schema.get("candidate_foundational_typed_condition")
if not condition or condition.get("name") != "Carrier-Typed Matrix-Element Terminality":
    die("missing foundational typed-condition candidate")

nogos = set(schema.get("retained_nogos") or [])
for nogo in {
    "public-shadow non-promotion",
    "finite-window Calkin blindness",
    "auxiliary-GRH smuggling",
    "incomplete character spectrum support-only",
    "scalar identity not carrier identity",
    "ledger-relative Hecke non-comparability",
    "H6 V-NC non-comparability",
}:
    if nogo not in nogos:
        die(f"missing retained no-go: {nogo}")

tex = (ART / "step172_cascade_reduction_theorem.tex").read_text(encoding="utf-8")
for needle in [
    "Shifted Co-Poisson Cascade Reduction",
    "\\textbf{Step 169.}",
    "\\textbf{Steps 169 and 170.}",
    "\\textbf{Step 170.}",
    "\\textbf{Step 171.}",
    "L_{\\rho,k}(G)",
    "Carrier-Typed Matrix-Element Terminality",
    "does not prove RH",
]:
    if needle not in tex:
        die(f"tex missing {needle}")

for csv_name in [
    "content_classification_step172.csv",
    "reduction_chain_step172.csv",
    "external_content_interface_step172.csv",
    "foundational_typed_condition_candidate_step172.csv",
    "residual_tree_step172.csv",
    "route_status_step172.csv",
    "next_external_attack_lanes_step172.csv",
]:
    with (ART / csv_name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        die(f"{csv_name} has no data rows")

combined = "\n".join(
    (ART / name).read_text(errors="ignore", encoding="utf-8")
    for name in REQUIRED
    if name != "run_step172_cascade_terminus_checks.py"
)

standard_bad_phrases = [
    "RH proof",
    "unconditional Xi_BC=0",
    "auxiliary-grh smuggling is allowed",
    "public-shadow non-promotion is optional",
    "finite-window calkin blindness is optional",
    "incomplete character spectrum is accepted",
    "scalar identity is carrier identity",
]
for phrase in standard_bad_phrases:
    if phrase.lower() in combined.lower():
        die(f"forbidden phrase present: {phrase}")

for sentence in re.split(r"(?<=[.!?])\s+", combined):
    lower = sentence.lower().strip()
    if not lower:
        continue
    if "xi_bc" in lower and ("= 0" in lower or "=0" in lower):
        if "does not" not in lower and "not prove" not in lower:
            die("positive Xi_BC=0 claim")
    if "close branch c" in lower or "closes branch c" in lower:
        if "does not" not in lower and "not close" not in lower:
            die("positive Branch C closure claim")
    if "decide l_{rho,k}" in lower or "decides l_{rho,k}" in lower:
        if "does not" not in lower and "external" not in lower and "obligation" not in lower:
            die("positive L_{rho,k} decision claim")
    if "prove jet-surjectivity" in lower or "proves jet-surjectivity" in lower:
        if "does not" not in lower and "external" not in lower:
            die("positive jet-surjectivity claim")
    if "xi_bc" in lower and "xi_bc_hecke" in lower:
        merging_words = ["equal", "same residual", "identified", "merged", "flattened"]
        safe_words = ["distinct", "sibling", "separate", "non-comparable", "not merged"]
        if any(word in lower for word in merging_words) and not any(word in lower for word in safe_words):
            die("sentence may merge Xi_BC and Xi_BC_Hecke after V-NC")

print("PASS step172 cascade terminus checks")
print(f"artifacts_checked={len(REQUIRED)}")
print(f"final_verdict={schema['final_verdict']}")
print(f"track_terminus_state={schema['track_terminus_state']}")
