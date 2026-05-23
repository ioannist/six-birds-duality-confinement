#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step169_shifted_factorization_attempt_artifacts")

REQUIRED = [
    "step169_results_summary.md",
    "step169_schema.json",
    "content_classification_step169.csv",
    "nonclaim_boundary_step169.md",
    "step169_shifted_factorization_derivation.tex",
    "run_step169_factorization_checks.py",
    "inherited_records_step169.csv",
    "derivation_steps_step169.csv",
    "verdict_step169.csv",
    "subclass_attempt_step169.csv",
    "residual_tree_step169.csv",
    "route_status_step169.csv",
    "construction_tasks_step169.csv",
]

ALLOWED = {
    "V_success_subclass",
    "V_failure_subclass",
    "V_conditional_subclass",
    "V_genuinely_stuck",
}

def die(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

for name in REQUIRED:
    p = ART / name
    if not p.exists():
        die(f"missing artifact {p}")
    if p.stat().st_size == 0:
        die(f"empty artifact {p}")

schema = json.loads(read(ART / "step169_schema.json"))
if schema.get("step") != 169:
    die("schema step must be 169")
if schema.get("orientation") != "adequacy":
    die("schema orientation must be adequacy")
verdict = schema.get("factorization_verdict")
if verdict not in ALLOWED:
    die(f"factorization_verdict not allowed: {verdict!r}")
if schema.get("final_verdict") != verdict:
    die("final_verdict must match factorization_verdict")
blocked_verdict = "split" + "_external" + "_theorem"
if schema.get("final_verdict") == blocked_verdict:
    die("attempt-mode final verdict cannot be " + blocked_verdict)

steps = schema.get("derivation_steps")
if not isinstance(steps, list) or len(steps) < 3:
    die("derivation_steps must have at least 3 entries")
for i, step in enumerate(steps):
    if not step.get("intermediate_expression"):
        die(f"derivation step {i} missing intermediate_expression")

subclass = schema.get("subclass_attempt")
if not isinstance(subclass, dict):
    die("schema requires subclass_attempt object")
if subclass.get("subclass") != "u = Cg":
    die("subclass_attempt must target u = Cg")
if subclass.get("verdict_upgrade") != verdict:
    die("subclass verdict_upgrade must match factorization_verdict")
if not subclass.get("explicit_formula"):
    die("subclass_attempt requires explicit_formula")
if not subclass.get("obstruction_or_named_deeper_lemma"):
    die("subclass_attempt requires obstruction_or_named_deeper_lemma")
if verdict == "V_conditional_subclass" and "ZI-COV" not in subclass["obstruction_or_named_deeper_lemma"]:
    die("conditional subclass verdict must name ZI-COV deeper lemma")

for csv_name in [
    "content_classification_step169.csv",
    "inherited_records_step169.csv",
    "derivation_steps_step169.csv",
    "verdict_step169.csv",
    "subclass_attempt_step169.csv",
    "residual_tree_step169.csv",
    "route_status_step169.csv",
    "construction_tasks_step169.csv",
]:
    with (ART / csv_name).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        die(f"{csv_name} has no data rows")

with (ART / "derivation_steps_step169.csv").open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
if len(rows) < 3:
    die("derivation_steps_step169.csv must have at least 3 rows")
for row in rows:
    if not row.get("intermediate_expression"):
        die("derivation_steps_step169.csv row missing intermediate_expression")

combined = "\n".join(
    read(ART / name)
    for name in REQUIRED
    if name != "run_step169_factorization_checks.py"
)

for phrase in [
    "proves " + "RH",
    "RH " + "proof",
    "essential norm " + "is positive",
    "C_l P_eta " + "is compact",
    "unconditional " + "Xi_BC=0",
]:
    if phrase in combined:
        die(f"forbidden phrase present: {phrase}")

if blocked_verdict in combined:
    die(blocked_verdict + " appears in artifacts")

sentences = re.split(r"(?<=[.!?])\s+", combined)
for sentence in sentences:
    lower = sentence.lower().strip()
    if lower in {"external work.", "external operator theory."}:
        die("stuck point characterized only as external work/operator theory")
    if "auxiliary-grh smuggling is allowed" in lower:
        die("weakens auxiliary-GRH smuggling no-go")
    if "public-shadow non-promotion is optional" in lower:
        die("weakens public-shadow no-go")
    if "finite-window calkin blindness is optional" in lower:
        die("weakens finite-window no-go")
    if "incomplete character spectrum is accepted" in lower:
        die("weakens incomplete-spectrum no-go")
    if "scalar l-function identity is carrier identity" in lower:
        die("weakens scalar-identity no-go")

print("PASS step169 factorization checks")
print(f"artifacts_checked={len(REQUIRED)}")
print(f"factorization_verdict={verdict}")
