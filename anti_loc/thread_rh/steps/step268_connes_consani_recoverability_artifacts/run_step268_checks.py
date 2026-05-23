#!/usr/bin/env python3
"""Validate Step 268 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step268_connes_consani_recoverability_artifacts"

REQUIRED = [
    "step268_results_summary.md",
    "step268_schema.json",
    "content_classification_step268.csv",
    "nonclaim_boundary_step268.md",
    "step268_connes_consani_recoverability.tex",
    "connes_consani_paper_extract_step268.md",
    "derive_recoverability_step268.py",
    "run_step268_checks.py",
    "connes_consani_verbatim_step268.csv",
    "derivation_steps_step268.csv",
    "gap_assessment_step268.csv",
    "branch_A_terminus_step268.csv",
    "residual_tree_step268.csv",
    "route_status_step268.csv",
    "construction_tasks_step268.csv",
    "classical_theorems_cited_step268.csv",
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

    schema = json.loads((ART / "step268_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 268:
        return fail("schema step mismatch")
    if schema.get("orientation") != "attempt_external_derivation":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_connes_consani_recoverability_blocked":
        return fail("unexpected verdict")
    gap = schema.get("gap_assessment", {})
    if gap.get("post_step268_score") != 1:
        return fail("post-step score mismatch")
    if gap.get("found_in_connes_consani_2014") or gap.get("found_in_connes_consani_2018"):
        return fail("gap incorrectly marked found")

    constructions = rows("connes_consani_verbatim_step268.csv")
    names = {row["construction"] for row in constructions}
    for expected in ["arithmetic site", "adele-class quotient", "distributional trace formula", "complete zeta as zeta_N", "summation map E", "scaling site", "RH quadratic form criterion", "complex lift C(G)"]:
        if expected not in names:
            return fail("missing construction " + expected)

    derivation = rows("derivation_steps_step268.csv")
    if not any("no such embedding" in row["result"] for row in derivation):
        return fail("Sonine embedding gap not recorded")
    if not any("no Hochschild trace" in row["result"] for row in derivation):
        return fail("Hochschild trace gap not recorded")

    gaps = rows("gap_assessment_step268.csv")
    for expected in ["Sonine-to-scaling-site carrier functor", "commutator recoverability", "essential-norm/Hochschild trace identity"]:
        if expected not in {row["gap"] for row in gaps}:
            return fail("missing gap " + expected)

    branch = rows("branch_A_terminus_step268.csv")[0]
    if branch["post_step268_score"] != "1":
        return fail("Branch A post-step score should be 1")
    if branch["verdict"] != "V_connes_consani_recoverability_blocked":
        return fail("Branch A verdict mismatch")

    sources = rows("classical_theorems_cited_step268.csv")
    joined = " ".join(row["source"] for row in sources)
    for token in ["Connes", "Consani", "2014", "2018"]:
        if token not in joined:
            return fail("missing source token " + token)

    extract = (ART / "connes_consani_paper_extract_step268.md").read_text(encoding="utf-8")
    for token in ["Arithmetic Site", "Scaling Site", "Riemann-Roch", "Complex Lift"]:
        if token not in extract:
            return fail("extract missing " + token)

    print("PASS step268 artifact contract")
    print("verdict=V_connes_consani_recoverability_blocked")
    print("post_step268_score=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
