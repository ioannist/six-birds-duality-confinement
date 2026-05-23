#!/usr/bin/env python3
"""Validate Step 402 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step402_parameter_dictionary_artifacts")
REQUIRED = [
    "parameter_dictionary_candidates_step402.csv",
    "bergman_phi_max_per_p_step402.csv",
    "dictionary_derivation_step402.md",
    "step402_results_summary.md",
    "step402_schema.json",
    "nonclaim_boundary_step402.md",
    "run_step402_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step402_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 402:
        raise SystemExit("schema step is not 402")
    if not schema.get("candidates_tie"):
        raise SystemExit("expected tied candidates")

    candidates = read_csv("parameter_dictionary_candidates_step402.csv")
    if len(candidates) < 5:
        raise SystemExit("candidate table too small")
    if not all(row["inside_log_near_diagonal"] == "TRUE" for row in candidates):
        raise SystemExit("expected all candidates inside log near-diagonal window")

    phi_rows = read_csv("bergman_phi_max_per_p_step402.csv")
    rels = {row["rel_error"] for row in phi_rows}
    if len(rels) != 1:
        raise SystemExit("expected same rel error for p-insensitive half-mass model")

    nonclaim = (ART / "nonclaim_boundary_step402.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 402 checks passed.")
    print("verdict=no_unique_dictionary_half_mass_p_insensitive")


if __name__ == "__main__":
    main()
