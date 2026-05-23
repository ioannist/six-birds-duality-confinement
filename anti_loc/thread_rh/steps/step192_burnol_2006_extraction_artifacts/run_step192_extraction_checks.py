#!/usr/bin/env python3
import csv
import json
import subprocess
import sys
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step192_burnol_2006_extraction_artifacts")

REQUIRED = [
    "step192_results_summary.md",
    "step192_schema.json",
    "content_classification_step192.csv",
    "nonclaim_boundary_step192.md",
    "step192_burnol_2006_extraction.tex",
    "compute_kappa_step192.py",
    "run_step192_extraction_checks.py",
    "burnol_2006_content_step192.csv",
    "specialization_chain_step192.csv",
    "kappa_formula_step192.csv",
    "c_11_attempt_step192.csv",
    "path_1_status_step192.csv",
    "residual_tree_step192.csv",
    "route_status_step192.csv",
    "construction_tasks_step192.csv",
]

VALID = {
    "V_burnol_2006_specializes_to_kappa",
    "V_burnol_2006_partial_specialization",
    "V_burnol_2006_specialization_fails",
    "V_burnol_2006_extraction_partial",
}

def fail(msg: str) -> None:
    print(f"FAIL step192 extraction checks: {msg}", file=sys.stderr)
    sys.exit(1)

def rows(name: str):
    with (BASE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).is_file()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step192_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "burnol_2006_content_summary",
        "specialization_attempt",
        "kappa_formula_if_derived",
        "c_11_log_2_if_computed",
        "extraction_verdict",
        "path_1_status_after",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 192:
        fail("schema step must be 192")
    if schema["orientation"] != "adequacy":
        fail("orientation must be adequacy")
    verdict = schema["extraction_verdict"]
    if verdict not in VALID:
        fail(f"invalid verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal extraction_verdict")
    if verdict == "V_burnol_2006_specializes_to_kappa":
        if not schema["kappa_formula_if_derived"]:
            fail("successful specialization must include kappa formula")
    if verdict == "V_burnol_2006_specialization_fails":
        if schema["kappa_formula_if_derived"] is not None:
            fail("failed specialization must not include derived kappa formula")
        if schema["path_1_status_after"] != "still_blocked_refined":
            fail("failed specialization must mark path still_blocked_refined")

    tex = (BASE / "step192_burnol_2006_extraction.tex").read_text(encoding="utf-8")
    for snippet in [
        "V\\_burnol\\_2006\\_specialization\\_fails",
        "J_0(2\\sqrt{xy})",
        "\\Gamma(1-s)",
        "\\pi^{-s/2}\\Gamma(s/2)",
        "Resolvent versus projection",
        "path\\_1\\_status\\_after = still\\_blocked\\_refined",
    ]:
        if snippet not in tex:
            fail(f"TeX missing required snippet: {snippet}")

    chain = rows("specialization_chain_step192.csv")
    statuses = {row.get("status") for row in chain}
    for status in ["analog_identified", "fails_at_carrier_identification", "fails_at_projection_parameter", "fails_at_normalization_match", "kappa_not_derived"]:
        if status not in statuses:
            fail(f"specialization chain missing status {status}")

    kappa_rows = rows("kappa_formula_step192.csv")
    if not any(row.get("status") == "not_derived" for row in kappa_rows):
        fail("kappa formula CSV must record not_derived")
    c_rows = rows("c_11_attempt_step192.csv")
    if not any(row.get("status") == "not_computed" for row in c_rows):
        fail("c_11 CSV must record not_computed")

    subprocess.run(["python3", str(BASE / "compute_kappa_step192.py")], check=True, cwd=str(BASE), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    status_path = BASE / "compute_kappa_status_step192.json"
    if not status_path.is_file():
        fail("compute status JSON missing")
    status = json.loads(status_path.read_text(encoding="utf-8"))
    if status.get("formula_derived") is not False:
        fail("compute status must mark formula_derived false")

    combined = "\n".join(
        (BASE / name).read_text(encoding="utf-8", errors="ignore")
        for name in REQUIRED
        if name != "run_step192_extraction_checks.py"
        and (BASE / name).suffix in {".md", ".tex", ".json", ".csv", ".py"}
    )
    forbidden = [
        "Path 1 unlocks",
        "explicit kappa formula derived",
        "we derived kappa",
        "c_11(log 2) computed",
        "J0 Hankel resolvent equals P_{L_a^Gamma}",
        "weaken any retained no-go",
    ]
    for phrase in forbidden:
        if phrase.lower() in combined.lower():
            fail(f"forbidden phrase found: {phrase}")

    print("PASS step192_extraction_checks: Burnol 2006 specialization attempt validated")
    print(f"extraction_verdict={verdict}")
    print(f"path_1_status_after={schema['path_1_status_after']}")

if __name__ == "__main__":
    main()
