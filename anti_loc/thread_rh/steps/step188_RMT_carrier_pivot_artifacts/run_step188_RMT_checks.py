#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step188_RMT_carrier_pivot_artifacts")

REQUIRED = [
    "step188_results_summary.md",
    "step188_schema.json",
    "content_classification_step188.csv",
    "nonclaim_boundary_step188.md",
    "step188_RMT_carrier_pivot.tex",
    "run_step188_RMT_checks.py",
    "RMT_declaration_step188.csv",
    "CRE_status_audit_step188.csv",
    "dichotomy_applicability_step188.csv",
    "RMT_verdict_step188.csv",
    "residual_tree_step188.csv",
    "route_status_step188.csv",
    "construction_tasks_step188.csv",
    "classical_theorems_cited_step188.csv",
]

EXPECTED_VERDICT = "V_RMT_outside_dichotomy_scope"


def fail(msg: str) -> None:
    print(f"FAIL step188 RMT checks: {msg}", file=sys.stderr)
    sys.exit(1)


def text(name: str) -> str:
    try:
        return (ROOT / name).read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"could not read {name}: {exc}")


def rows(name: str):
    try:
        with (ROOT / name).open(newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    except Exception as exc:
        fail(f"could not parse {name}: {exc}")


def main() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        fail("missing artifacts: " + ", ".join(missing))

    try:
        schema = json.loads(text("step188_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"invalid schema JSON: {exc}")

    if schema.get("step") != 188:
        fail("schema step must be 188")
    if schema.get("orientation") != "adequacy":
        fail("orientation must be adequacy")
    if schema.get("primary_carrier") != "Random Matrix Theory (RMT) for ζ-zero statistics":
        fail("primary_carrier mismatch")
    if schema.get("RMT_verdict") != EXPECTED_VERDICT:
        fail("RMT_verdict mismatch")
    if schema.get("final_verdict") != EXPECTED_VERDICT:
        fail("final_verdict mismatch")
    if schema.get("dichotomy_coverage_conjecture_status") != "unchanged_domain_refined":
        fail("coverage status must be unchanged_domain_refined")

    cre = schema.get("CRE_status_audit", {})
    if not cre.get("T3a_equivalence_to_RH", "").startswith("no"):
        fail("CRE audit must say not equivalent to RH")
    if "RH" not in cre.get("RH_dependency", ""):
        fail("CRE audit must record RH dependency")
    if cre.get("CRE_status") != "not_CRE_but_not_non_CRE_closure_carrier":
        fail("CRE_status audit mismatch")

    app = schema.get("Dichotomy_applicability_audit", {})
    if app.get("is_RH_analogous_closure_carrier") is not False:
        fail("dichotomy applicability must mark not closure carrier")
    if app.get("coverage_effect") != "outside_scope_not_refutation":
        fail("coverage effect mismatch")

    cited = " ".join(row.get("source", "") for row in schema.get("classical_theorems_cited", []))
    for expected in ["Montgomery 1973", "Odlyzko", "Keating-Snaith", "Diaconis-Shahshahani", "Step 187"]:
        if expected not in cited:
            fail(f"citation missing {expected}")

    if len(schema.get("retained_nogos", [])) < 10:
        fail("retained_nogos must preserve 10 no-gos")

    for csv_name in [
        "RMT_declaration_step188.csv",
        "CRE_status_audit_step188.csv",
        "dichotomy_applicability_step188.csv",
        "RMT_verdict_step188.csv",
        "residual_tree_step188.csv",
        "route_status_step188.csv",
        "construction_tasks_step188.csv",
        "classical_theorems_cited_step188.csv",
    ]:
        if not rows(csv_name):
            fail(f"{csv_name} has no data rows")

    cre_rows = {row.get("audit_item"): row for row in rows("CRE_status_audit_step188.csv")}
    if cre_rows.get("requires_RH_to_state_cleanly", {}).get("result") != "yes":
        fail("CRE status CSV must record RH dependency")
    if cre_rows.get("closure_equivalent_to_RH", {}).get("result") != "no":
        fail("CRE status CSV must record no equivalence")

    app_rows = {row.get("audit_item"): row for row in rows("dichotomy_applicability_step188.csv")}
    if app_rows.get("is_RH_analogous_closure_carrier", {}).get("result") != "no":
        fail("dichotomy applicability CSV must record no closure carrier")
    if app_rows.get("coverage_conjecture_effect", {}).get("result") != "unchanged":
        fail("dichotomy applicability CSV must record unchanged coverage")

    tex = text("step188_RMT_carrier_pivot.tex")
    snippets = [
        "V_{\\mathrm{RMT\\_outside\\_dichotomy\\_scope}}",
        "C_{\\mathrm{RMT}}",
        "\\XiRMT",
        "statistical agreement",
        "outside the dichotomy scope",
        "not a refutation",
        "Montgomery",
        "Keating",
        "Odlyzko",
    ]
    for snippet in snippets:
        if snippet not in tex:
            fail(f"TeX missing snippet: {snippet}")

    combined = "\n".join(
        text(name)
        for name in [
            "step188_results_summary.md",
            "nonclaim_boundary_step188.md",
            "step188_RMT_carrier_pivot.tex",
        ]
    )
    forbidden = [
        r"\bRMT proves RH\b",
        r"\bRMT disproves RH\b",
        r"\bMontgomery.*unconditionally proves RH\b",
        r"\bpair correlation is an unconditional proof\b",
        r"\brefutes the Framework RH-Carrier Dichotomy\b",
        r"\btherefore exact GUE.*implies RH\b",
        r"\bweakens retained no-go\b",
    ]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")

    print("PASS step188 RMT checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"RMT_verdict={schema.get('RMT_verdict')}")
    print(f"dichotomy_coverage_conjecture_status={schema.get('dichotomy_coverage_conjecture_status')}")


if __name__ == "__main__":
    main()
