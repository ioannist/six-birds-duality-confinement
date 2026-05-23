#!/usr/bin/env python3
"""Validate Step 327 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step327_hecke_H4_paper_audit_artifacts")
REQUIRED = [
    "fetched_sources_step327.csv",
    "paper_extracts_step327.md",
    "H4_subclaim_match_step327.csv",
    "step327_results_summary.md",
    "step327_schema.json",
    "nonclaim_boundary_step327.md",
    "run_step327_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [p for p in REQUIRED if not (ART / p).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    sources = rows("fetched_sources_step327.csv")
    if len(sources) < 4:
        raise SystemExit("expected at least 4 sources")
    matches = rows("H4_subclaim_match_step327.csv")
    if not any(r["match_level"] == "partial" for r in matches):
        raise SystemExit("expected partial H4 matches")
    if not any(r["match_level"] == "missing" for r in matches):
        raise SystemExit("expected missing H4 finite residual")
    schema = json.loads((ART / "step327_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 327:
        raise SystemExit("schema step incorrect")
    if "GRH" not in (ART / "nonclaim_boundary_step327.md").read_text(encoding="utf-8"):
        raise SystemExit("nonclaim boundary missing GRH")
    print("STEP327_CHECKS_PASS")


if __name__ == "__main__":
    main()
