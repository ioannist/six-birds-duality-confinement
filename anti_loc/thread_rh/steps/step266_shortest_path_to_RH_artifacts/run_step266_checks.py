#!/usr/bin/env python3
"""Validate Step 266 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step266_shortest_path_to_RH_artifacts"

REQUIRED = [
    "step266_results_summary.md",
    "step266_schema.json",
    "content_classification_step266.csv",
    "nonclaim_boundary_step266.md",
    "step266_shortest_path_to_RH.tex",
    "enumerate_cascade_termini_step266.py",
    "run_step266_checks.py",
    "cascade_termini_step266.csv",
    "external_classification_step266.csv",
    "attack_interface_ranking_step266.csv",
    "shortest_path_step266.csv",
    "residual_tree_step266.csv",
    "route_status_step266.csv",
    "construction_tasks_step266.csv",
    "classical_theorems_cited_step266.csv",
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

    schema = json.loads((ART / "step266_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 266:
        return fail("schema step mismatch")
    if schema.get("orientation") != "attack_path":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_RH_attack_path_blocked_by_external_gap":
        return fail("unexpected final verdict")

    classes = rows("external_classification_step266.csv")
    score_by_class = {row["class_id"]: int(row["score"]) for row in classes}
    if score_by_class != {"i": 3, "ii": 2, "iii": 1, "iv": 0}:
        return fail("classification scoring mismatch")

    termini = rows("cascade_termini_step266.csv")
    active = [row for row in termini if row["status"].startswith("active")]
    if any(int(row["score"]) == 3 for row in active):
        return fail("active score-3 path found despite blocked verdict")
    if not any(row["status"] == "resolved support" and int(row["score"]) == 3 for row in termini):
        return fail("resolved score-3 Burnol support missing")
    for branch in ["A", "B", "C"]:
        if branch not in {row["branch"] for row in termini}:
            return fail("missing branch " + branch)

    ranking = rows("attack_interface_ranking_step266.csv")
    if int(ranking[0]["score"]) != 2:
        return fail("top active score should be 2")
    if not any("Connes-Consani" in row["terminus"] for row in ranking):
        return fail("Connes-Consani interface missing")
    if not any("transport-sampling" in row["terminus"] for row in ranking):
        return fail("Burnol transport-sampling interface missing")

    shortest = rows("shortest_path_step266.csv")[0]
    if shortest["path_status"] != "no score-3 active path":
        return fail("shortest path status mismatch")
    if shortest["final_verdict"] != "V_RH_attack_path_blocked_by_external_gap":
        return fail("shortest path verdict mismatch")

    sources = rows("classical_theorems_cited_step266.csv")
    joined = " ".join(row["source"] for row in sources)
    for token in ["Burnol", "Connes", "Consani", "Bombieri", "Huxley"]:
        if token not in joined:
            return fail("missing source token " + token)

    print("PASS step266 artifact contract")
    print("verdict=V_RH_attack_path_blocked_by_external_gap")
    print("top_active_score=2")
    print("active_score3_paths=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
