#!/usr/bin/env python3
"""Validate Step 385 P_infty asymptotic attempt artifacts."""

from __future__ import annotations

import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step385_P_infty_spectral_asymptotic_attempt_artifacts")


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"STEP385_CHECK_FAIL: {msg}")


def main() -> None:
    required = [
        "cascade_records_audit_step385.md",
        "P_infty_kernel_form_step385.md",
        "large_k_asymptotic_step385.md",
        "step385_results_summary.md",
        "step385_schema.json",
        "nonclaim_boundary_step385.md",
        "run_step385_checks.py",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    audit = (BASE / "cascade_records_audit_step385.md").read_text()
    require("Step 102" in audit and "Step 153" in audit and "Step 173" in audit, "audit missing key records")
    require("K_infty^op" in audit, "audit missing K_infty identity")

    kernel = (BASE / "P_infty_kernel_form_step385.md").read_text()
    require("K_infty^op" in kernel and "c_{n,k}(rho)" in kernel, "kernel attempt missing operational coefficient")

    asymp = (BASE / "large_k_asymptotic_step385.md").read_text()
    require("c_{n,k}(rho) ~ ?" in asymp, "missing named stalled identity")
    require("gamma_zeta=pi/(T log(T/(2pi)))" in asymp, "missing gamma comparison")

    schema = json.loads((BASE / "step385_schema.json").read_text())
    require(schema["large_k_closed"] is False, "schema should not claim closure")
    require(schema["verdict"] == "partial_named_missing_identity", "schema verdict mismatch")

    boundary = (BASE / "nonclaim_boundary_step385.md").read_text().lower()
    require("does not prove rh" in boundary, "missing RH nonclaim")
    require("ambient hardy kernel cannot replace" in boundary, "missing Hardy-shadow caveat")

    print("STEP385_CHECK_PASS")
    print(f"verdict={schema['verdict']}")
    print(f"missing_identity={schema['missing_identity']}")


if __name__ == "__main__":
    main()
