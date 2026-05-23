#!/usr/bin/env python3
"""Validator for Step 359 Mode B Stage-IV refinement artifacts."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step359_mode_B_stage_IV_refinement_artifacts")

REQUIRED = [
    "converse_probe_step359.csv",
    "failure_decomposition_step359.csv",
    "earning_at_scale_step359.md",
    "equivalence_audit_modes_B_C_step359.csv",
    "step359_results_summary.md",
    "step359_schema.json",
    "nonclaim_boundary_step359.md",
    "run_step359_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step359_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 359
    assert schema["converse_probe_coherent"] is True
    assert schema["extra_state_f_admissibility_achieved"] is False
    assert schema["lookup_variant_rejected_by_SAU"] is True
    assert schema["failure_decomposition_cells"] == 70
    assert schema["dominant_operator_cells"] == 46
    assert schema["dominant_magnitude_cells"] == 22
    assert schema["dominant_phase_cells"] == 2
    assert schema["mag_phase_only_magnitude_dominant_cells"] == 59
    assert schema["earning_at_scale_content"] is True
    assert schema["mode_B_mode_C_structurally_distinct"] is True
    assert schema["mode_B_retract_count"] == 1
    assert schema["final_verdict"] == "V_mode_B_stage_IV_passes_sharper_underfit_operator_diagnostic"

    converse = read_csv("converse_probe_step359.csv")
    assert len(converse) == 4
    assert any(row["admissibility_achieved"] == "rejected" for row in converse)
    assert all(row["admissibility_achieved"] in {"no", "rejected"} for row in converse)

    decomp = read_csv("failure_decomposition_step359.csv")
    assert len(decomp) == 70
    counts = Counter(row["dominant_component"] for row in decomp)
    assert counts["operator"] == 46
    assert counts["mag"] == 22
    assert counts["phase"] == 2

    earning = (BASE / "earning_at_scale_step359.md").read_text(encoding="utf-8")
    assert "numeric under-fit at R_compare" in earning
    assert "missing certificate at R_operator_audit" in earning

    audit = read_csv("equivalence_audit_modes_B_C_step359.csv")
    assert len(audit) == 5
    assert all(row["structurally_same"] == "no" for row in audit)

    boundary = (BASE / "nonclaim_boundary_step359.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge" in boundary

    print("Step 359 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
