#!/usr/bin/env python3
"""Validate Step 254 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step254_selberg_orthogonality_pivot_artifacts")

REQUIRED = [
    "step254_results_summary.md",
    "step254_schema.json",
    "content_classification_step254.csv",
    "nonclaim_boundary_step254.md",
    "step254_selberg_orthogonality_pivot.tex",
    "derive_SOC_residual_step254.py",
    "run_step254_checks.py",
    "SOC_declaration_step254.csv",
    "SOC_vs_GRH_step254.csv",
    "classification_step254.csv",
    "residual_tree_step254.csv",
    "route_status_step254.csv",
    "construction_tasks_step254.csv",
    "classical_theorems_cited_step254.csv",
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

    schema = json.loads((ART / "step254_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 254:
        return fail("schema step mismatch")
    if schema.get("final_verdict") != "V_selberg_orthogonality_outside_dichotomy":
        return fail("unexpected verdict")

    declaration = rows("SOC_declaration_step254.csv")
    if not declaration or "limsup" not in declaration[0]["residual"]:
        return fail("SOC declaration missing residual")

    vs = rows("SOC_vs_GRH_step254.csv")
    if not any(r["comparison"] == "SOC_vs_Riemann_RH" and r["status"] == "not_equivalent" for r in vs):
        return fail("SOC vs RH not-equivalence missing")

    classification = rows("classification_step254.csv")
    if not any(r["framework"] == "Selberg_Class_Dichotomy_Generalization" and "outside" in r["classification"] for r in classification):
        return fail("Selberg single-L outside classification missing")

    sources = rows("classical_theorems_cited_step254.csv")
    joined = " ".join(r["source"] for r in sources)
    for token in ["Selberg", "Conrey", "Murty", "Kaczorowski"]:
        if token not in joined:
            return fail("missing source token " + token)

    print("PASS step254 artifact contract")
    print("verdict=V_selberg_orthogonality_outside_dichotomy")
    print("classification=outside_Riemann_and_outside_single_L_Selberg_Dichotomy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
