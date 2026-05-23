from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step172_track_closeout_artifacts")

REQUIRED = [
    "step172_results_summary.md",
    "step172_schema.json",
    "content_classification_step172.csv",
    "nonclaim_boundary_step172.md",
    "step172_track_closeout.tex",
    "run_step172_closeout_checks.py",
    "cascade_state_step172.csv",
    "external_content_interface_step172.csv",
    "framework_derived_outputs_step172.csv",
    "retained_nogos_step172.csv",
    "manager_led_arc_retrospective_step172.csv",
    "residual_tree_step172.csv",
    "route_status_step172.csv",
    "construction_tasks_step172.csv",
]

REQUIRED_SCHEMA_FIELDS = {
    "step",
    "orientation",
    "active_residuals",
    "cascade_state",
    "closeout_theorem_name",
    "external_content_interface",
    "framework_derived_outputs",
    "final_verdict",
    "manager_led_arc_summary",
    "next_track_directions",
}

FORBIDDEN_PHRASES = [
    "proves " + "RH",
    "RH " + "proof",
    "essential norm is " + "positive",
    "C_l P_" + "eta is compact",
    "unconditional Xi_BC" + "=0",
    "Xi_BC_Hecke" + "=0",
]

WEAKENING_PATTERNS = [
    r"public-shadow non-promotion (is )?(optional|weakened|bypassed|inactive)",
    r"finite-window Calkin blindness (is )?(optional|weakened|bypassed|inactive)",
    r"auxiliary-GRH smuggling (is )?(allowed|accepted|weakened)",
    r"incomplete character spectrum (is )?(accepted|source-grade|complete)",
    r"scalar .* identity is carrier identity",
    r"Hecke non-comparability (is )?(optional|weakened|inactive)",
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
missing = sorted(REQUIRED_SCHEMA_FIELDS - set(schema))
if missing:
    die(f"schema missing fields: {missing}")
if schema.get("step") != 172:
    die("schema step must be 172")
if schema.get("orientation") != "adequacy":
    die("schema orientation must be adequacy")
if schema.get("active_residuals") != ["Xi_BC", "Xi_BC_Hecke"]:
    die("active_residuals mismatch")
if schema.get("closeout_theorem_name") != "RH membrane packet cascade closeout":
    die("closeout theorem name mismatch")
if schema.get("final_verdict") != "track_closeout_cascade_diagnostic_complete_at_inherited_records_ceiling":
    die("final verdict mismatch")

cascade = schema.get("cascade_state", {})
branches = cascade.get("branches", {})
for branch in [
    "A_Calkin_bridge_G2_G5",
    "B_per_zero_finite_carrier_SL164_1",
    "C_shifted_co_Poisson_H1_H5",
]:
    if branch not in branches:
        die(f"schema missing branch {branch}")
if branches["A_Calkin_bridge_G2_G5"].get("status") != "split_external_theorem":
    die("Branch A status drift")
if branches["B_per_zero_finite_carrier_SL164_1"].get("status") != "finite_carrier_diagnostic_indeterminate":
    die("Branch B status drift")
if "kernel_required" not in branches["C_shifted_co_Poisson_H1_H5"].get("status", ""):
    die("Branch C status must retain kernel-required keystone")

nogos = cascade.get("retained_nogos", [])
if len(nogos) != 6:
    die("schema must carry six retained no-gos")
for required in [
    "public-shadow non-promotion",
    "finite-window Calkin blindness",
    "auxiliary-GRH smuggling",
    "incomplete character spectrum support-only",
    "scalar L-function identity is not carrier identity",
    "ledger-relative Hecke non-comparability",
]:
    if required not in [item.get("name") for item in nogos]:
        die(f"missing retained no-go: {required}")

interface = schema.get("external_content_interface", [])
entries = {item.get("entry") for item in interface}
if entries != {"Branch A", "Branch B", "Branch C", "Entry C-K", "Entry C-II"}:
    die(f"bad external interface entries: {sorted(entries)}")
for needle in ["K_infty", "SL164.1", "G2-G5", "ZI-COV(ii)"]:
    if needle not in json.dumps(interface):
        die(f"external interface missing {needle}")

for csv_name in [
    "content_classification_step172.csv",
    "cascade_state_step172.csv",
    "external_content_interface_step172.csv",
    "framework_derived_outputs_step172.csv",
    "retained_nogos_step172.csv",
    "manager_led_arc_retrospective_step172.csv",
    "residual_tree_step172.csv",
    "route_status_step172.csv",
    "construction_tasks_step172.csv",
]:
    with (ART / csv_name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        die(f"{csv_name} has no data rows")

combined = "\n".join(
    (ART / name).read_text(errors="ignore", encoding="utf-8")
    for name in REQUIRED
    if name != "run_step172_closeout_checks.py"
)

for phrase in FORBIDDEN_PHRASES:
    if phrase in combined:
        die(f"forbidden phrase present: {phrase}")

for sentence in re.split(r"(?:\n+|(?<=[.!?])\s+)", combined):
    clean = sentence.strip()
    lower = clean.lower()
    if re.search(r"\bbranch(es)? [abc](?:/b/c)? (is|are|was|were) closed\b", lower):
        die(f"sentence asserts branch closure: {clean}")
    if re.search(r"\b(branch a|branch b|branch c)\b\s+(closed|is closed|was closed|has been closed|now closed)\b", lower):
        die(f"sentence asserts branch closure: {clean}")
    if re.search(r"\b(external record|named external record|k_infty|sl164\.1|g2-g5|zi-cov\(ii\)).*\b(is|are|was|were) supplied\b", lower):
        if "does not supply" not in lower and "not supplied" not in lower:
            die(f"sentence claims external record supplied: {clean}")
    for pattern in WEAKENING_PATTERNS:
        if re.search(pattern, clean, flags=re.IGNORECASE):
            die(f"sentence weakens retained no-go: {clean}")

nonclaim = (ART / "nonclaim_boundary_step172.md").read_text(encoding="utf-8")
for required_line in [
    "Does NOT prove RH.",
    "Does NOT prove `Xi_BC = 0` or `Xi_BC_Hecke = 0`.",
    "Does NOT close any of Branches A/B/C.",
    "Does NOT supply `K_infty(s,s')` or any other named external record.",
    "Does NOT weaken any retained no-go.",
    "Does NOT claim RH is decidable under inherited records.",
]:
    if required_line not in nonclaim:
        die(f"nonclaim boundary missing: {required_line}")

print("PASS step172 closeout checks")
print(f"artifacts_checked={len(REQUIRED)}")
print(f"final_verdict={schema['final_verdict']}")
