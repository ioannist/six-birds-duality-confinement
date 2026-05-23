from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step170_zi_cov_attack_artifacts")

REQUIRED = [
    "step170_results_summary.md",
    "step170_schema.json",
    "content_classification_step170.csv",
    "nonclaim_boundary_step170.md",
    "step170_zi_cov_attack.tex",
    "run_step170_zi_cov_checks.py",
    "mellin_projection_definition_step170.csv",
    "target_equivalence_test_step170.csv",
    "zi_cov_attempt_step170.csv",
    "verdict_step170.csv",
    "residual_tree_step170.csv",
    "route_status_step170.csv",
    "construction_tasks_step170.csv",
]


def die(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


for name in REQUIRED:
    path = ART / name
    if not path.exists():
        die(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        die(f"empty artifact: {name}")

schema = json.loads((ART / "step170_schema.json").read_text())
if schema.get("step") != 170:
    die("schema step must be 170")
if schema.get("orientation") != "adequacy":
    die("schema orientation must be adequacy")
if schema.get("active_residual") != "Xi_BC / Xi_cP_shifted_l":
    die("active_residual mismatch")
if schema.get("target_lemma") != "ZI-COV_{l,a}^{CP}":
    die("target_lemma mismatch")
if not schema.get("mellin_projection_definition"):
    die("missing mellin_projection_definition")
if schema.get("target_equivalence_test_result") not in {
    "not_applicable",
    "target_equivalent_to_RH",
    "target_equivalent_to_NotRH",
    "not_target_equivalent",
}:
    die("bad target_equivalence_test_result")
if schema.get("zi_cov_verdict") not in {
    "V_proved",
    "V_refuted",
    "V_target_equivalent",
    "V_subclass_proved",
}:
    die("bad zi_cov_verdict")
if schema.get("final_verdict") != schema.get("zi_cov_verdict"):
    die("final_verdict must equal zi_cov_verdict")
if schema.get("zi_cov_verdict") == "V_subclass_proved" and not schema.get("explicit_A_infty_formula"):
    die("subclass proof requires explicit A_infty formula")

tex = (ART / "step170_zi_cov_attack.tex").read_text()
for needle in [
    "T2a. Direct Operator Computation",
    "T2b. Target-Equivalence Test",
    "T2c. Subclass Proof",
    "V\\_subclass\\_proved",
    "A_\\infty^\\Omega",
]:
    if needle not in tex:
        die(f"tex missing {needle}")

for csv_name in [
    "mellin_projection_definition_step170.csv",
    "target_equivalence_test_step170.csv",
    "zi_cov_attempt_step170.csv",
    "verdict_step170.csv",
    "residual_tree_step170.csv",
    "route_status_step170.csv",
    "construction_tasks_step170.csv",
]:
    with (ART / csv_name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        die(f"{csv_name} has no data rows")

combined = "\n".join(
    (ART / name).read_text(errors="ignore")
    for name in REQUIRED
    if name != "run_step170_zi_cov_checks.py"
)

for phrase in [
    "proves " + "RH",
    "RH " + "proof",
    "essential norm is " + "positive",
    "C_l P_" + "eta is compact",
    "unconditional Xi_BC" + "=0",
]:
    if phrase in combined:
        die(f"forbidden phrase present: {phrase}")

bad_final_values = ["V_" + "stuck", "V_" + "genuinely_" + "stuck"]
for bad in bad_final_values:
    if re.search(r"final_verdict[\"']?\s*[:=]\s*[\"']?" + re.escape(bad), combined):
        die(f"forbidden final verdict: {bad}")

for sentence in re.split(r"(?<=[.!?])\s+", combined):
    lower = sentence.lower().strip()
    if lower == "external operator theory.":
        die("sole obstruction characterized as external operator theory")
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

print("PASS step170 ZI-COV checks")
print(f"artifacts_checked={len(REQUIRED)}")
print(f"zi_cov_verdict={schema['zi_cov_verdict']}")
