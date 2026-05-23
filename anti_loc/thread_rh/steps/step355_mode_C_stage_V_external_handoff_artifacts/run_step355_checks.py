#!/usr/bin/env python3
"""Validator for Step 355 Mode C Stage-V external handoff artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step355_mode_C_stage_V_external_handoff_artifacts")

REQUIRED = [
    "fetched_sources_stage_V_step355.csv",
    "paper_extracts_stage_V_step355.md",
    "residual_translation_outcome_step355.csv",
    "Mode_C_Stage_V_verdict_step355.md",
    "step355_schema.json",
    "nonclaim_boundary_step355.md",
    "run_step355_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step355_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 355
    assert schema["sources_fetched"] == 4
    assert schema["sources_with_verbatim_extracts"] == 4
    assert schema["refined_residual"] == ["lambda_mag", "lambda_phase", "lambda_operator"]
    assert schema["closure_available"] is False
    assert schema["no_go_found"] is False
    assert schema["outcome"] == "partial_with_named_gap"
    assert "kernel-preserving" in schema["named_gap"]
    assert schema["mode_C_completed"] is True
    assert schema["final_verdict"] == "V_mode_C_stage_V_partial_with_named_gap"

    sources = read_csv("fetched_sources_stage_V_step355.csv")
    assert len(sources) >= 5
    assert sum(row["accessible"] == "Y" for row in sources) >= 4

    extracts = (BASE / "paper_extracts_stage_V_step355.md").read_text(encoding="utf-8")
    for needle in ["Arthur", "Sakellaridis", "Watson", "Langlands"]:
        assert needle in extracts
    assert "transfer operators" in extracts

    outcomes = read_csv("residual_translation_outcome_step355.csv")
    assert any(row["source"] == "Step355_overall" and row["overall_outcome"] == "partial_with_named_gap" for row in outcomes)
    assert any(row["lambda_operator_match"] == "missing" for row in outcomes)

    verdict = (BASE / "Mode_C_Stage_V_verdict_step355.md").read_text(encoding="utf-8")
    assert "partial with named gap" in verdict
    assert "No fetched source provides the H6 closure theorem" in verdict

    boundary = (BASE / "nonclaim_boundary_step355.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge theorem" in boundary

    print("Step 355 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
