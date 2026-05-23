#!/usr/bin/env python3
"""Validate Step 326 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step326_hecke_H3_paper_audit_artifacts")
REQUIRED = [
    "fetched_sources_step326.csv",
    "paper_extracts_step326.md",
    "H3_subclaim_match_step326.csv",
    "step326_results_summary.md",
    "step326_schema.json",
    "nonclaim_boundary_step326.md",
    "run_step326_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [p for p in REQUIRED if not (ART / p).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    sources = rows("fetched_sources_step326.csv")
    if len(sources) < 4:
        raise SystemExit("expected at least 4 fetched source rows")
    matches = rows("H3_subclaim_match_step326.csv")
    levels = {r["subclaim"]: r["match_level"] for r in matches}
    if not any(v == "missing" for v in levels.values()):
        raise SystemExit("expected at least one missing H3 subclaim")
    schema = json.loads((ART / "step326_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 326:
        raise SystemExit("schema step incorrect")
    if "RH" not in (ART / "nonclaim_boundary_step326.md").read_text(encoding="utf-8"):
        raise SystemExit("nonclaim boundary missing RH")
    print("STEP326_CHECKS_PASS")


if __name__ == "__main__":
    main()
