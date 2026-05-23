#!/usr/bin/env python3
"""Validate Step 291 artifact contract."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step291_branch_A_burnol_corpus_audit_artifacts")

REQUIRED = [
    "step291_results_summary.md",
    "step291_schema.json",
    "content_classification_step291.csv",
    "nonclaim_boundary_step291.md",
    "step291_branch_A_burnol_corpus.tex",
    "fetch_burnol_corpus_step291.py",
    "burnol_section_tables_step291.md",
    "run_step291_checks.py",
    "burnol_bibliography_step291.csv",
    "candidate_lemma_matches_step291.csv",
    "verbatim_quotes_step291.csv",
    "residual_tree_step291.csv",
    "route_status_step291.csv",
    "construction_tasks_step291.csv",
    "classical_theorems_cited_step291.csv",
]


def count_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        print("MISSING " + ", ".join(missing))
        return 1
    schema = json.loads((ART / "step291_schema.json").read_text(encoding="utf-8"))
    expected = {
        "step": 291,
        "orientation": "adequacy",
        "target": "Branch A exhaustive Burnol corpus audit",
    }
    for key, value in expected.items():
        if schema.get(key) != value:
            print(f"SCHEMA_MISMATCH {key}: {schema.get(key)!r} != {value!r}")
            return 1
    if schema.get("final_verdict") != "V_branch_A_burnol_audit_confirms_no_lemma":
        print("BAD_VERDICT " + repr(schema.get("final_verdict")))
        return 1
    if count_rows(ART / "burnol_bibliography_step291.csv") < 40:
        print("BIBLIOGRAPHY_TOO_SHORT")
        return 1
    if count_rows(ART / "candidate_lemma_matches_step291.csv") == 0:
        print("NO_CANDIDATE_ROWS")
        return 1
    if count_rows(ART / "verbatim_quotes_step291.csv") < 5:
        print("TOO_FEW_QUOTES")
        return 1
    raw = ART / "raw_corpus"
    if not raw.exists() or len(list(raw.glob("*.pdf"))) < 20:
        print("RAW_CORPUS_INCOMPLETE")
        return 1
    print("STEP291_CHECKS_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
