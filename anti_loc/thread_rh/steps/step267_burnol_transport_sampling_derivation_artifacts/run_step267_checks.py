#!/usr/bin/env python3
"""Validate Step 267 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step267_burnol_transport_sampling_derivation_artifacts"

REQUIRED = [
    "step267_results_summary.md",
    "step267_schema.json",
    "content_classification_step267.csv",
    "nonclaim_boundary_step267.md",
    "step267_burnol_transport_sampling.tex",
    "burnol_paper_extract_step267.md",
    "derive_transport_sampling_step267.py",
    "run_step267_checks.py",
    "burnol_verbatim_step267.csv",
    "derivation_steps_step267.csv",
    "gap_assessment_step267.csv",
    "branch_B_terminus_step267.csv",
    "residual_tree_step267.csv",
    "route_status_step267.csv",
    "construction_tasks_step267.csv",
    "classical_theorems_cited_step267.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fail(message: str) -> int:
    print("FAIL", message)
    return 1


def main() -> int:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        return fail("missing files: " + ", ".join(missing))

    schema = json.loads((ART / "step267_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 267:
        return fail("schema step mismatch")
    if schema.get("orientation") != "attempt_external_derivation":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_burnol_transport_sampling_blocked":
        return fail("unexpected verdict")
    gap = schema.get("gap_assessment", {})
    if gap.get("post_step267_score") != 1:
        return fail("post-step score mismatch")
    if gap.get("found_in_burnol_2002") or gap.get("found_in_burnol_2004"):
        return fail("gap incorrectly marked found")

    formulas = rows("burnol_verbatim_step267.csv")
    names = {row["formula_name"] for row in formulas}
    for expected in ["Sonine projection", "de Branges reproducing kernel", "E_lambda", "Mellin evaluators", "zero evaluator span"]:
        if expected not in names:
            return fail("missing formula " + expected)

    derivation = rows("derivation_steps_step267.csv")
    if not any("finite evaluator expansion" in row["result"] for row in derivation):
        return fail("finite evaluator gap not recorded")

    gaps = rows("gap_assessment_step267.csv")
    if not any(row["gap"] == "finite transported-evaluator expansion" for row in gaps):
        return fail("main gap row missing")

    branch = rows("branch_B_terminus_step267.csv")[0]
    if branch["post_step267_score"] != "1":
        return fail("Branch B post-step score should be 1")
    if branch["verdict"] != "V_burnol_transport_sampling_blocked":
        return fail("Branch B verdict mismatch")

    sources = rows("classical_theorems_cited_step267.csv")
    joined = " ".join(row["source"] for row in sources)
    for token in ["Burnol", "2002", "2004"]:
        if token not in joined:
            return fail("missing source token " + token)

    extract = (ART / "burnol_paper_extract_step267.md").read_text(encoding="utf-8")
    for token in ["Theorem 4", "Theorem 8", "Equation (1)", "Section 6"]:
        if token not in extract:
            return fail("extract missing " + token)

    print("PASS step267 artifact contract")
    print("verdict=V_burnol_transport_sampling_blocked")
    print("post_step267_score=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
