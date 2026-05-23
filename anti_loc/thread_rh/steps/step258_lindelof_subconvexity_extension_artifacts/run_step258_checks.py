#!/usr/bin/env python3
"""Validate Step 258 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step258_lindelof_subconvexity_extension_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step258_results_summary.md",
    "step258_schema.json",
    "content_classification_step258.csv",
    "nonclaim_boundary_step258.md",
    "step258_lindelof_subconvexity_extension.tex",
    "derive_subconvexity_step258.py",
    "run_step258_checks.py",
    "lindelof_declaration_step258.csv",
    "subconvexity_family_step258.csv",
    "subconvexity_extension_step258.csv",
    "instance_evidence_step258.csv",
    "corpus_inclusion_step258.csv",
    "residual_tree_step258.csv",
    "route_status_step258.csv",
    "construction_tasks_step258.csv",
    "classical_theorems_cited_step258.csv",
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

    schema = json.loads((ART / "step258_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 258:
        return fail("schema step mismatch")
    if schema.get("final_verdict") != "V_lindelof_subconvexity_extension":
        return fail("unexpected verdict")
    if schema.get("bourgain_2017_bound") != "|zeta(1/2+it)| << t^(13/84+epsilon)":
        return fail("Bourgain bound mismatch")

    evidence = rows("instance_evidence_step258.csv")
    if len(evidence) != 3:
        return fail("expected three evidence rows")
    joined_e = " ".join(r["instance"] + " " + r["known_result"] for r in evidence)
    for token in ["Bourgain", "Burgess", "Michel-Venkatesh"]:
        if token not in joined_e:
            return fail("missing evidence token " + token)

    sources = rows("classical_theorems_cited_step258.csv")
    joined_s = " ".join(r["source"] for r in sources)
    for token in ["Lindelof", "Bourgain", "Burgess", "Michel"]:
        if token not in joined_s:
            return fail("missing source token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "Selberg-Class Subconvexity Extension" not in findings:
        return fail("findings_framework.md missing subconvexity extension")
    if "verified-on-3-subconvexity-instances" not in findings:
        return fail("findings_framework.md missing 3-instance status")

    print("PASS step258 artifact contract")
    print("verdict=V_lindelof_subconvexity_extension")
    print("finding=Selberg-Class Subconvexity Extension")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
