#!/usr/bin/env python3
"""Validate Step 259 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step259_zeta_moments_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step259_results_summary.md",
    "step259_schema.json",
    "content_classification_step259.csv",
    "nonclaim_boundary_step259.md",
    "step259_zeta_moments.tex",
    "derive_moments_step259.py",
    "run_step259_checks.py",
    "moments_declaration_step259.csv",
    "keating_snaith_prediction_step259.csv",
    "classification_step259.csv",
    "instance_evidence_step259.csv",
    "corpus_inclusion_step259.csv",
    "residual_tree_step259.csv",
    "route_status_step259.csv",
    "construction_tasks_step259.csv",
    "classical_theorems_cited_step259.csv",
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

    schema = json.loads((ART / "step259_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 259:
        return fail("schema step mismatch")
    if schema.get("final_verdict") != "V_moments_inside_subconvexity_extension":
        return fail("unexpected verdict")
    if schema["keating_snaith_leading_coefficient"]["g_k"] != "prod_{j=0}^{k-1} j!/(j+k)!":
        return fail("g_k formula mismatch")

    evidence = rows("instance_evidence_step259.csv")
    if len(evidence) != 4:
        return fail("expected four evidence rows")
    statuses = {(r["k"], r["status"]) for r in evidence}
    if ("1", "proved") not in statuses or ("2", "proved") not in statuses:
        return fail("proved k=1,2 status missing")
    if not any(r["k"] == "general" and r["status"] == "conjectural" for r in evidence):
        return fail("general conjectural status missing")

    classification = rows("classification_step259.csv")
    if not any(r["verdict"] == "V_moments_inside_subconvexity_extension" for r in classification):
        return fail("classification verdict row missing")

    sources = rows("classical_theorems_cited_step259.csv")
    joined = " ".join(r["source"] for r in sources)
    for token in ["Hardy", "Ingham", "Conrey", "Keating", "Snaith"]:
        if token not in joined:
            return fail("missing source token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "Type beta" not in findings:
        return fail("findings_framework.md missing Type beta")
    if "verified-on-4-growth-rate-instances" not in findings:
        return fail("findings_framework.md missing 4-growth-rate status")

    print("PASS step259 artifact contract")
    print("verdict=V_moments_inside_subconvexity_extension")
    print("subconvexity_extension=Type_beta_moments_added")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
