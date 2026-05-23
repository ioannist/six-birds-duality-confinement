#!/usr/bin/env python3
"""Validate Step 399 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step399_bergman_to_pswf_transport_artifacts")
REQUIRED = [
    "transport_derivation_step399.md",
    "limit_comparison_step399.csv",
    "step399_results_summary.md",
    "step399_schema.json",
    "nonclaim_boundary_step399.md",
    "run_step399_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step399_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 399:
        raise SystemExit("schema step is not 399")
    if schema.get("identity_status") != "not_found":
        raise SystemExit("unexpected identity status")
    if "off-diagonal" not in schema.get("named_blocker", ""):
        raise SystemExit("named blocker does not mention off-diagonal asymptotic")

    with (ART / "limit_comparison_step399.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 6:
        raise SystemExit("limit comparison table too small")
    if not any(row["match_status"] == "mismatch" for row in rows):
        raise SystemExit("expected at least one mismatch row")
    if not any("off-diagonal" in row["blocker"] for row in rows):
        raise SystemExit("expected off-diagonal blocker row")

    derivation = (ART / "transport_derivation_step399.md").read_text(encoding="utf-8")
    for token in ["K_infty^op", "z = exp(2*pi*i*w)", "P_infty u", "No closed-form transport identity"]:
        if token not in derivation:
            raise SystemExit(f"derivation missing token: {token}")

    nonclaim = (ART / "nonclaim_boundary_step399.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 399 checks passed.")
    print("identity_status=not_found")
    print("named_blocker=off-diagonal log-cusp Bergman-to-PSWF asymptotic")


if __name__ == "__main__":
    main()
