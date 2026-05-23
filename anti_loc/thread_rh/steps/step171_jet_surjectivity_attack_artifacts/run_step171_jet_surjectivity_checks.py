from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step171_jet_surjectivity_attack_artifacts")

REQUIRED = [
    "step171_results_summary.md",
    "step171_schema.json",
    "content_classification_step171.csv",
    "nonclaim_boundary_step171.md",
    "step171_jet_surjectivity_attack.tex",
    "run_step171_jet_surjectivity_checks.py",
    "p_infty_definition_step171.csv",
    "jet_operator_step171.csv",
    "attempt_paths_step171.csv",
    "verdict_step171.csv",
    "residual_tree_step171.csv",
    "route_status_step171.csv",
    "construction_tasks_step171.csv",
]


def die(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


for name in REQUIRED:
    path = ART / name
    if not path.exists():
        die(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        die(f"empty artifact: {name}")

schema = json.loads((ART / "step171_schema.json").read_text(encoding="utf-8"))
if schema.get("step") != 171:
    die("schema step must be 171")
if schema.get("orientation") != "adequacy":
    die("schema orientation must be adequacy")
if schema.get("gap_attacked") != "projected zero-jet surjectivity of P_infty":
    die("gap_attacked mismatch")
if not schema.get("inherited_P_infty_definition"):
    die("missing inherited_P_infty_definition")
if not schema.get("inherited_jet_definition"):
    die("missing inherited_jet_definition")
if not schema.get("attempt_paths"):
    die("missing attempt_paths")

allowed_verdicts = {
    "V_surj_proved_structural",
    "V_surj_refuted_structural",
    "V_surj_partial_structural",
    "V_surj_genuinely_kernel_required",
}
verdict = schema.get("jet_surjectivity_verdict")
if verdict not in allowed_verdicts:
    die("bad jet_surjectivity_verdict")
if schema.get("final_verdict") != verdict:
    die("final_verdict must equal jet_surjectivity_verdict")
if schema.get("factorization", {}).get("jet_surjectivity_verdict") != verdict:
    die("factorization.jet_surjectivity_verdict must equal jet_surjectivity_verdict")

allowed_consequences = {
    "target_equivalent_to_RH",
    "sharper_than_RH",
    "partial",
    "kernel_required_not_decided",
}
if schema.get("target_equivalence_consequence") not in allowed_consequences:
    die("bad target_equivalence_consequence")

if verdict == "V_surj_proved_structural":
    if not schema.get("explicit_G_construction"):
        die("proved verdict requires explicit_G_construction")
    if schema.get("target_equivalence_consequence") != "target_equivalent_to_RH":
        die("proved verdict requires target_equivalent_to_RH")
if verdict == "V_surj_refuted_structural":
    if not schema.get("explicit_obstruction"):
        die("refuted verdict requires explicit_obstruction")
    if schema.get("target_equivalence_consequence") != "sharper_than_RH":
        die("refuted verdict requires sharper_than_RH")
if verdict == "V_surj_partial_structural":
    if schema.get("target_equivalence_consequence") != "partial":
        die("partial verdict requires partial consequence")
if verdict == "V_surj_genuinely_kernel_required":
    missing = schema.get("specific_missing_record") or ""
    if not missing:
        die("kernel-required verdict requires specific_missing_record")
    if "K_infty" not in missing and "range-evaluator" not in missing:
        die("specific_missing_record must name K_infty or range-evaluator record")
    demonstration = schema.get("kernel_required_demonstration") or []
    if len(demonstration) < 5:
        die("kernel-required verdict requires all structural attempts")

tex = (ART / "step171_jet_surjectivity_attack.tex").read_text(encoding="utf-8")
for needle in [
    "T1. Inherited definitions",
    "T2. Surjectivity attack",
    "T2a. Constructive direction",
    "T2b. Refutation direction: structural audit",
    "U1a. Pairing and duality",
    "U1b. Zero-evaluator structure",
    "U1c. Algebraic idempotency",
    "U1d. Specific zero test",
    "U2. Non-kernel constructive direction",
    "V\\_surj\\_genuinely\\_kernel\\_required",
    "(\\Psym F)(s)",
    "L_{\\rho,k}(G)",
]:
    if needle not in tex:
        die(f"tex missing {needle}")

for csv_name in [
    "content_classification_step171.csv",
    "p_infty_definition_step171.csv",
    "jet_operator_step171.csv",
    "attempt_paths_step171.csv",
    "verdict_step171.csv",
    "residual_tree_step171.csv",
    "route_status_step171.csv",
    "construction_tasks_step171.csv",
]:
    with (ART / csv_name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        die(f"{csv_name} has no data rows")

combined = "\n".join(
    (ART / name).read_text(errors="ignore", encoding="utf-8")
    for name in REQUIRED
    if name != "run_step171_jet_surjectivity_checks.py"
)

for phrase in [
    "proves " + "RH",
    "RH " + "proof",
    "unconditional Xi_BC" + "=0",
    "essential norm is " + "positive",
    "C_l P_" + "eta is compact",
]:
    if phrase in combined:
        die(f"forbidden phrase present: {phrase}")

bad_final_values = ["V_" + "stuck", "V_" + "genuinely_" + "stuck"]
for bad in bad_final_values:
    if re.search(r"final_verdict[\"']?\s*[:=]\s*[\"']?" + re.escape(bad), combined):
        die(f"forbidden final verdict: {bad}")

for sentence in re.split(r"(?<=[.!?])\s+", combined):
    lower = sentence.lower().strip()
    if "v_surj_proved" in lower and "not_target_equivalent" in lower:
        die("contradictory sentence: V_surj_proved and not_target_equivalent")
    if "auxiliary-grh smuggling is allowed" in lower:
        die("weakens auxiliary-GRH smuggling no-go")
    if "public-shadow non-promotion is optional" in lower:
        die("weakens public-shadow no-go")
    if "finite-window calkin blindness is optional" in lower:
        die("weakens finite-window no-go")
    if "incomplete character spectrum is accepted" in lower:
        die("weakens incomplete-spectrum no-go")
    if "scalar identity is carrier identity" in lower:
        die("weakens scalar-identity no-go")

print("PASS step171 jet-surjectivity checks")
print(f"artifacts_checked={len(REQUIRED)}")
print(f"jet_surjectivity_verdict={verdict}")
