#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step197_mertens_criterion_pivot_artifacts")

REQUIRED = [
    "step197_results_summary.md",
    "step197_schema.json",
    "content_classification_step197.csv",
    "nonclaim_boundary_step197.md",
    "step197_mertens_criterion_pivot.tex",
    "run_step197_mertens_checks.py",
    "mertens_declaration_step197.csv",
    "CRE_audit_step197.csv",
    "CRCFT_mode_audit_step197.csv",
    "strong_vs_weak_mertens_step197.csv",
    "cascade_initial_branches_step197.csv",
    "residual_tree_step197.csv",
    "route_status_step197.csv",
    "construction_tasks_step197.csv",
    "classical_theorems_cited_step197.csv",
]

VALID_VERDICTS = {
    "V_mertens_CRCFT_TE",
    "V_mertens_CRCFT_CTMT",
    "V_mertens_CRCFT_BF",
    "V_mertens_substantively_new",
    "V_mertens_partial",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def read_csv(name: str):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step197_schema.json").read_text())
    if schema.get("step") != 197:
        fail("schema step must be 197")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("primary_carrier") != "Mertens function M(x) and the weak Mertens criterion":
        fail("primary carrier mismatch")
    if schema.get("mertens_verdict") not in VALID_VERDICTS:
        fail("invalid mertens verdict")
    if schema.get("final_verdict") != schema.get("mertens_verdict"):
        fail("final_verdict must match mertens_verdict")
    if schema.get("CRE_status", {}).get("status") != "CRE":
        fail("Mertens carrier must be classified CRE")
    if schema.get("CRCFT_mode_classification", {}).get("primary_mode") != "CRCFT-TE":
        fail("expected CRCFT-TE primary mode")
    if schema.get("strong_mertens_refuted_status", {}).get("status") != "refuted":
        fail("strong Mertens refuted status missing")
    if "RH-equivalent" not in schema.get("weak_mertens_RH_equivalent_status", {}).get("status", ""):
        fail("weak Mertens RH-equivalent status missing")

    strong_rows = read_csv("strong_vs_weak_mertens_step197.csv")
    if not any("Strong Mertens" in row["claim"] and row["status"] == "refuted" for row in strong_rows):
        fail("strong-vs-weak CSV missing refuted strong Mertens")
    if not any("Weak Mertens" in row["claim"] and "RH" in row["status"] for row in strong_rows):
        fail("strong-vs-weak CSV missing weak RH-equivalent status")

    citations = (BASE / "classical_theorems_cited_step197.csv").read_text()
    for expected in ["Mertens", "Littlewood", "Odlyzko", "te Riele"]:
        if expected not in citations:
            fail(f"missing citation token {expected}")

    tex = (BASE / "step197_mertens_criterion_pivot.tex").read_text()
    for expected in ["V\\_mertens\\_CRCFT\\_TE", "Odlyzko--te Riele", "Littlewood", "CRCFT\\mbox{-}TE"]:
        if expected not in tex:
            fail(f"tex missing {expected}")

    print("PASS step197 Mertens carrier checks")
    print(f"verdict={schema['mertens_verdict']}")


if __name__ == "__main__":
    main()

