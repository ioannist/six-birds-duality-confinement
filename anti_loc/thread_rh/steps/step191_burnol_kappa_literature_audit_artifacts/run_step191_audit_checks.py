#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step191_burnol_kappa_literature_audit_artifacts")

REQUIRED = [
    "step191_results_summary.md",
    "step191_schema.json",
    "content_classification_step191.csv",
    "nonclaim_boundary_step191.md",
    "step191_burnol_kappa_literature_audit.tex",
    "run_step191_audit_checks.py",
    "surveyed_burnol_papers_step191.csv",
    "surveyed_adjacent_step191.csv",
    "specific_findings_step191.csv",
    "path_1_status_step191.csv",
    "residual_tree_step191.csv",
    "route_status_step191.csv",
    "construction_tasks_step191.csv",
]

VALID_VERDICTS = {
    "V_kappa_classical_source_identified",
    "V_kappa_partial_source_found",
    "V_kappa_genuinely_open_in_classical_literature",
    "V_kappa_audit_partial",
}

def fail(msg: str) -> None:
    print(f"FAIL step191 audit checks: {msg}", file=sys.stderr)
    sys.exit(1)

def rows(name: str):
    with (BASE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).is_file()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step191_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "inherited_records",
        "surveyed_burnol_papers",
        "surveyed_adjacent_classical",
        "specific_findings",
        "kappa_audit_verdict",
        "path_1_status",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 191:
        fail("step must be 191")
    if schema["orientation"] != "adequacy":
        fail("orientation must be adequacy")
    verdict = schema["kappa_audit_verdict"]
    if verdict not in VALID_VERDICTS:
        fail(f"invalid verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal kappa_audit_verdict")
    if verdict == "V_kappa_classical_source_identified" and schema["path_1_status"] != "unlocked":
        fail("identified source must unlock Path 1")
    if verdict == "V_kappa_partial_source_found" and schema["path_1_status"] != "partially_clarified":
        fail("partial source verdict must mark Path 1 partially_clarified")
    if len(schema["surveyed_burnol_papers"]) < 5:
        fail("must survey at least five Burnol papers")
    if len(schema["surveyed_adjacent_classical"]) < 4:
        fail("must survey adjacent classical sources")

    tex = (BASE / "step191_burnol_kappa_literature_audit.tex").read_text(encoding="utf-8")
    for snippet in [
        "V\\_kappa\\_partial\\_source\\_found",
        "P_{\\mathcal L_a^\\Gamma}",
        "K_a^{\\Gamma,\\mathrm{amb}}",
        "Scattering, determinants, hyperfunctions",
        "path\\_1\\_status = partially\\_clarified",
    ]:
        if snippet not in tex:
            fail(f"TeX missing snippet: {snippet}")

    burnol = rows("surveyed_burnol_papers_step191.csv")
    if len(burnol) < 5:
        fail("surveyed_burnol_papers CSV too short")
    if not any("Scattering" in row.get("title", "") and "closest_candidate" in row.get("relevance", "") for row in burnol):
        fail("Burnol CSV must mark Scattering as closest candidate")
    findings = rows("specific_findings_step191.csv")
    if not any(row.get("status") == "not_found_as_exact_source" for row in findings):
        fail("specific findings must record exact source not found")
    path_rows = rows("path_1_status_step191.csv")
    if not any(row.get("path_1_status") == schema["path_1_status"] for row in path_rows):
        fail("path_1_status CSV mismatch")

    combined = "\n".join((BASE / name).read_text(encoding="utf-8", errors="ignore") for name in REQUIRED if (BASE / name).suffix in {".md", ".tex", ".json", ".csv"})
    forbidden = [
        "Path 1 is unlocked",
        "Branch A is closed",
        "Branch B is closed",
        "the theorem is proved",
        "we derive kappa",
        "we identify the ambient Hardy kernel as the projected Burnol",
        "ambient Hardy kernel equals the projected Burnol",
        "weakens any retained no-go",
    ]
    for phrase in forbidden:
        if phrase.lower() in combined.lower():
            fail(f"forbidden phrase found: {phrase}")

    print("PASS step191_audit_checks: literature audit artifacts validated")
    print(f"kappa_audit_verdict={verdict}")
    print(f"path_1_status={schema['path_1_status']}")

if __name__ == "__main__":
    main()
