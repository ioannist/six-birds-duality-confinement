#!/usr/bin/env python3
"""Validate Step 253 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step253_de_bruijn_newman_pivot_artifacts")

REQUIRED = [
    "step253_results_summary.md",
    "step253_schema.json",
    "content_classification_step253.csv",
    "nonclaim_boundary_step253.md",
    "step253_de_bruijn_newman_pivot.tex",
    "derive_dbn_residual_step253.py",
    "run_step253_checks.py",
    "dbn_declaration_step253.csv",
    "CRE_audit_step253.csv",
    "CRCFT_mode_audit_step253.csv",
    "bounds_history_step253.csv",
    "residual_tree_step253.csv",
    "route_status_step253.csv",
    "construction_tasks_step253.csv",
    "classical_theorems_cited_step253.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fail(msg: str) -> int:
    print("FAIL", msg)
    return 1


def main() -> int:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        return fail("missing files: " + ", ".join(missing))

    schema = json.loads((ART / "step253_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 253:
        return fail("schema step mismatch")
    if schema.get("orientation") != "adequacy":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_de_Bruijn_Newman_CRCFT_TE":
        return fail("unexpected verdict")
    if schema.get("CRE_status") != "CRE" or schema.get("CRCFT_mode") != "TE":
        return fail("CRE/mode mismatch")

    bounds = rows("bounds_history_step253.csv")
    if not any("Lambda>=0" in r["bound_or_result"] for r in bounds):
        return fail("missing Rodgers-Tao lower bound")
    if not any("0.22" in r["bound_or_result"] for r in bounds):
        return fail("missing Polymath upper bound")

    mode = rows("CRCFT_mode_audit_step253.csv")
    if not any(r["mode"] == "TE" and r["status"] == "selected" for r in mode):
        return fail("TE mode not selected")

    nonclaim = (ART / "nonclaim_boundary_step253.md").read_text(encoding="utf-8")
    if "does not prove RH" not in nonclaim:
        return fail("nonclaim boundary missing RH disclaimer")

    print("PASS step253 artifact contract")
    print("verdict=V_de_Bruijn_Newman_CRCFT_TE")
    print("CRE_status=CRE CRCFT_mode=TE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
