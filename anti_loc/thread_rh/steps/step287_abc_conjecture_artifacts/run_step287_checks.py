#!/usr/bin/env python3
"""Validate Step 287 artifact contract."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step287_abc_conjecture_artifacts")

REQUIRED = [
    "step287_results_summary.md",
    "step287_schema.json",
    "content_classification_step287.csv",
    "nonclaim_boundary_step287.md",
    "step287_abc_conjecture.tex",
    "analyze_abc_step287.py",
    "run_step287_checks.py",
    "abc_declaration_step287.csv",
    "classification_step287.csv",
    "eleventh_finding_audit_step287.csv",
    "residual_tree_step287.csv",
    "route_status_step287.csv",
    "construction_tasks_step287.csv",
    "classical_theorems_cited_step287.csv",
]


def fail(msg: str) -> None:
    print(f"Step 287 check failed: {msg}", file=sys.stderr)
    raise SystemExit(1)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    if not ART.is_dir():
        fail(f"artifact directory missing: {ART}")
    for name in REQUIRED:
        path = ART / name
        if not path.exists():
            fail(f"missing {name}")
        if path.stat().st_size == 0:
            fail(f"empty {name}")

    schema = json.loads((ART / "step287_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 287:
        fail("schema step mismatch")
    if schema.get("final_verdict") != "V_abc_11th_finding":
        fail("unexpected final verdict")
    if "abc_carrier_definition" not in schema:
        fail("schema missing abc carrier definition")
    if "Integer-Diophantine" not in schema.get("framework_finding_target", ""):
        fail("schema missing 11th finding target")

    classification = read_csv(ART / "classification_step287.csv")
    if not any(r.get("finding") == "new candidate 11th" and r.get("fit") == "yes" for r in classification):
        fail("classification does not mark 11th candidate")
    if not any(r.get("finding") == "SCDG" and r.get("fit") == "no" for r in classification):
        fail("classification missing SCDG no-fit")

    sources = read_csv(ART / "classical_theorems_cited_step287.csv")
    keys = {r.get("key") for r in sources}
    needed = {"Oesterle_1987_1988", "Masser_1985", "Vojta_1987", "Granville_Tucker_2002", "Robert_Stewart_Tenenbaum_2014", "Mochizuki_2021_IV"}
    missing = needed - keys
    if missing:
        fail(f"missing cited source keys: {sorted(missing)}")

    nonclaim = (ART / "nonclaim_boundary_step287.md").read_text(encoding="utf-8")
    for needle in ["does not prove abc", "does not accept Mochizuki", "11th finding is a corpus-pending"]:
        if needle not in nonclaim:
            fail(f"nonclaim boundary missing {needle!r}")

    print("Step 287 checks passed")


if __name__ == "__main__":
    main()
