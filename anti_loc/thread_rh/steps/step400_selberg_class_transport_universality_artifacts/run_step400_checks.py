#!/usr/bin/env python3
"""Validate Step 400 artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step400_selberg_class_transport_universality_artifacts")
REQUIRED = [
    "selberg_class_blocker_analysis_step400.md",
    "step400_results_summary.md",
    "step400_schema.json",
    "nonclaim_boundary_step400.md",
    "run_step400_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step400_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 400:
        raise SystemExit("schema step is not 400")
    if schema.get("transport_blocker_status") != "shared_core_blocker":
        raise SystemExit("unexpected blocker status")
    if schema.get("cusp_width_gamma0_3_infinity") != 1:
        raise SystemExit("unexpected cusp width")

    analysis = (ART / "selberg_class_blocker_analysis_step400.md").read_text(encoding="utf-8")
    for token in ["P_infty^chi", "Gamma_0(3)", "shared", "conductor/parity"]:
        if token not in analysis:
            raise SystemExit(f"analysis missing token: {token}")

    nonclaim = (ART / "nonclaim_boundary_step400.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 400 checks passed.")
    print("verdict=shared blocker with chi-specific normalization layer")


if __name__ == "__main__":
    main()
