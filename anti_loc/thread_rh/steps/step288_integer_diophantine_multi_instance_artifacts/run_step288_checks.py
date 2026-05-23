#!/usr/bin/env python3
"""Validate Step 288 artifact contract."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step288_integer_diophantine_multi_instance_artifacts")
REQUIRED = [
    "step288_results_summary.md",
    "step288_schema.json",
    "content_classification_step288.csv",
    "nonclaim_boundary_step288.md",
    "step288_integer_diophantine.tex",
    "analyze_instances_step288.py",
    "run_step288_checks.py",
    "hall_pillai_catalan_es_declarations_step288.csv",
    "subtype_refinement_step288.csv",
    "multi_instance_evidence_step288.csv",
    "corpus_inclusion_step288.csv",
    "residual_tree_step288.csv",
    "route_status_step288.csv",
    "construction_tasks_step288.csv",
    "classical_theorems_cited_step288.csv",
]


def fail(msg: str) -> None:
    print(f"Step 288 check failed: {msg}", file=sys.stderr)
    raise SystemExit(1)


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
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

    schema = json.loads((ART / "step288_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 288:
        fail("schema step mismatch")
    if schema.get("final_verdict") != "V_integer_diophantine_multi_instance":
        fail("unexpected verdict")
    if schema.get("status_update", {}).get("cumulative_with_abc") != 5:
        fail("cumulative instance count should be 5")

    declarations = read_csv("hall_pillai_catalan_es_declarations_step288.csv")
    names = {r.get("instance") for r in declarations}
    if names != {"Hall", "Pillai", "Catalan", "Erdos-Straus"}:
        fail(f"unexpected instance set: {sorted(names)}")

    subtypes = read_csv("subtype_refinement_step288.csv")
    subtype_names = {r.get("subtype") for r in subtypes}
    if subtype_names != {"Type A", "Type B", "Type C"}:
        fail(f"unexpected subtype set: {sorted(subtype_names)}")

    sources = read_csv("classical_theorems_cited_step288.csv")
    source_keys = {r.get("key") for r in sources}
    needed = {"Hall_1971", "Pillai_1936", "Mihailescu_2004", "Erdos_Straus_1948", "Salez_2014"}
    if not needed.issubset(source_keys):
        fail(f"missing source keys: {sorted(needed-source_keys)}")

    fw = Path("/home/repos/six-birds-foundations-iii/anti_loc/findings_framework.md").read_text(encoding="utf-8")
    if "Integer-Diophantine Radical-Height Residual Family" not in fw:
        fail("findings_framework.md missing Integer-Diophantine Radical-Height Residual Family entry")
    if "verified-on-5-integer-Diophantine-instances" not in fw:
        fail("findings_framework.md missing cumulative status")

    print("Step 288 checks passed")


if __name__ == "__main__":
    main()
