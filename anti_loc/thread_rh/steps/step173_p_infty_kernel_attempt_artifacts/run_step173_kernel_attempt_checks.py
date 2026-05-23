from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step173_p_infty_kernel_attempt_artifacts")

REQUIRED = [
    "step173_results_summary.md",
    "step173_schema.json",
    "content_classification_step173.csv",
    "nonclaim_boundary_step173.md",
    "step173_p_infty_kernel_attempt.tex",
    "run_step173_kernel_attempt_checks.py",
    "inherited_records_step173.csv",
    "derivation_chain_step173.csv",
    "kernel_verdict_step173.csv",
    "L_rho_k_evaluation_step173.csv",
    "residual_tree_step173.csv",
    "route_status_step173.csv",
    "construction_tasks_step173.csv",
]

ALLOWED = {
    "V_kernel_explicit",
    "V_operational_identity",
    "V_subkernel_explicit",
    "V_kernel_pswf_only",
    "V_kernel_genuinely_open",
    "V_kernel_target_equivalent",
}


def die(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


for name in REQUIRED:
    path = ART / name
    if not path.exists():
        die(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        die(f"empty artifact: {name}")

schema = json.loads((ART / "step173_schema.json").read_text(encoding="utf-8"))
if schema.get("step") != 173:
    die("schema step must be 173")
if schema.get("orientation") != "adequacy":
    die("orientation must be adequacy")
if schema.get("gap_attacked") != "K_infty(s,s') Mellin kernel of P_infty":
    die("gap_attacked mismatch")
verdict = schema.get("kernel_verdict")
if verdict not in ALLOWED:
    die("bad kernel_verdict")
if schema.get("final_verdict") != verdict:
    die("final_verdict must equal kernel_verdict")

if len(schema.get("inherited_records") or []) < 7:
    die("must cite inherited records R1-R6 plus Step171")
stages = {row.get("stage") for row in schema.get("derivation_chain") or []}
for needed in {"T2a", "T2b", "T2c", "T2d"}:
    if needed not in stages:
        die(f"missing derivation stage {needed}")

if verdict == "V_operational_identity" and not schema.get("operational_identity"):
    die("operational verdict requires operational_identity")
if verdict in {"V_kernel_explicit", "V_subkernel_explicit"} and not schema.get("explicit_kernel_formula"):
    die("explicit/subkernel verdict requires explicit_kernel_formula")
if verdict == "V_kernel_pswf_only" and not schema.get("pswf_external_theorem_needed"):
    die("pswf-only verdict requires pswf_external_theorem_needed")
if verdict == "V_kernel_genuinely_open" and not schema.get("deepest_named_gap"):
    die("open verdict requires deepest_named_gap")
if verdict == "V_kernel_target_equivalent" and not schema.get("target_equivalence_proof_sketch"):
    die("target-equivalent verdict requires proof sketch")
if verdict in {"V_kernel_explicit", "V_operational_identity", "V_subkernel_explicit"}:
    if not schema.get("L_rho_k_test_evaluation"):
        die("positive kernel/identity verdict requires L_rho_k_test_evaluation")

tex = (ART / "step173_p_infty_kernel_attempt.tex").read_text(encoding="utf-8")
for needle in [
    "P_\\lambda(x,y)",
    "\\widehat P_\\lambda(x,y)",
    "S_\\lambda",
    "QPQ",
    "\\phi_n^\\lambda",
    "K_\\infty^{\\mathrm{op}}",
    "L_{\\rho,k}(G)",
    "V\\_operational\\_identity",
]:
    if needle not in tex:
        die(f"tex missing {needle}")

for csv_name in [
    "content_classification_step173.csv",
    "inherited_records_step173.csv",
    "derivation_chain_step173.csv",
    "kernel_verdict_step173.csv",
    "L_rho_k_evaluation_step173.csv",
    "residual_tree_step173.csv",
    "route_status_step173.csv",
    "construction_tasks_step173.csv",
]:
    with (ART / csv_name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        die(f"{csv_name} has no data rows")

combined = "\n".join(
    (ART / name).read_text(errors="ignore", encoding="utf-8")
    for name in REQUIRED
    if name != "run_step173_kernel_attempt_checks.py"
)

for phrase in [
    "split_external_theorem",
    "external work needed",
    "this is an RH proof",
    "RH proof",
    "unconditional Xi_BC=0",
    "auxiliary-grh smuggling is allowed",
    "public-shadow non-promotion is optional",
    "finite-window calkin blindness is optional",
    "incomplete character spectrum is accepted",
    "scalar identity is carrier identity",
]:
    if phrase.lower() in combined.lower():
        die(f"forbidden phrase present: {phrase}")

for sentence in re.split(r"(?<=[.!?])\s+", combined):
    lower = sentence.lower().strip()
    if "prove projected jet-surjectivity" in lower and "does not" not in lower:
        die("positive jet-surjectivity overclaim")
    if "prove full zi-cov" in lower and "does not" not in lower:
        die("positive full ZI-COV overclaim")
    if "zeta-zero spectral projection" in lower and "does not replace" not in lower and "without replacing" not in lower:
        die("projection definition may have been changed")

print("PASS step173 kernel attempt checks")
print(f"artifacts_checked={len(REQUIRED)}")
print(f"kernel_verdict={verdict}")
