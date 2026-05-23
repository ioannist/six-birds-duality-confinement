#!/usr/bin/env python3
"""Validator for Step 348 KL-divergence Mode A calibration artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step348_mode_A_KL_calibration_artifacts")

REQUIRED = [
    "compute_KL_divergence_step348.py",
    "KL_pairs_step348.csv",
    "pinsker_check_step348.csv",
    "ablation_KL_axiom_step348.csv",
    "step348_results_summary.md",
    "step348_schema.json",
    "nonclaim_boundary_step348.md",
    "run_step348_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step348_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 348
    assert int(schema["dps"]) >= 80
    assert int(schema["KL_pair_count"]) == 21
    assert int(schema["pinsker_pass_count"]) == 21
    assert schema["ablation_numeric_output_changed"] is False
    assert int(schema["mode_A_retract_count_update"]) == 2
    assert schema["final_verdict"] == "V_mode_A_KL_nominal_pinsker_passes_but_ablation_inert_cyclic_retract"

    pairs = read_csv("KL_pairs_step348.csv")
    assert len(pairs) == 21
    assert all(row["KL_nonnegative"] == "yes" for row in pairs)
    assert all(float(row["Pinsker_margin"]) > 0.0 for row in pairs)

    pinsker = read_csv("pinsker_check_step348.csv")
    assert len(pinsker) == 21
    assert all(row["pinsker_holds"] == "yes" for row in pinsker)

    ablations = read_csv("ablation_KL_axiom_step348.csv")
    detail_rows = [row for row in ablations if row["character"] != "SUMMARY"]
    assert len(detail_rows) == 42
    assert all(row["numeric_output_changed"] == "no" for row in detail_rows)
    assert all(row["pinsker_numeric_holds_after_ablation"] == "yes" for row in detail_rows)

    summary_rows = {row["ablation"]: row for row in ablations if row["character"] == "SUMMARY"}
    assert summary_rows["drop_nonnegativity_axiom"]["numeric_output_changed"] == "changed_pairs=0/21"
    assert summary_rows["drop_nonnegativity_axiom"]["pinsker_numeric_holds_after_ablation"] == "numeric_failures=0/21"
    assert summary_rows["drop_nonnegativity_axiom"]["proof_certificate_status"] == "certificate_failures=21/21"
    assert summary_rows["drop_chain_rule_axiom"]["numeric_output_changed"] == "changed_pairs=0/21"
    assert summary_rows["drop_chain_rule_axiom"]["pinsker_numeric_holds_after_ablation"] == "numeric_failures=0/21"
    assert summary_rows["drop_chain_rule_axiom"]["proof_certificate_status"] == "certificate_failures=0/21"

    boundary = (BASE / "nonclaim_boundary_step348.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary

    print("Step 348 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
