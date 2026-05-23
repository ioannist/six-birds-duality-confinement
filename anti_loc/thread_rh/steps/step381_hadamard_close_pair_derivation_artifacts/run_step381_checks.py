#!/usr/bin/env python3
"""Validate Step 381 Hadamard close-pair derivation artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step381_hadamard_close_pair_derivation_artifacts")


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"STEP381_CHECK_FAIL: {msg}")


def main() -> None:
    required = [
        "hadamard_derivation_step381.md",
        "g_prime_evaluation_step381.csv",
        "re_zeta2_sign_prediction_step381.csv",
        "R_j_prediction_step381.csv",
        "step381_results_summary.md",
        "step381_schema.json",
        "nonclaim_boundary_step381.md",
        "run_step381_checks.py",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    g_rows = rows("g_prime_evaluation_step381.csv")
    sign_rows = rows("re_zeta2_sign_prediction_step381.csv")
    r_rows = rows("R_j_prediction_step381.csv")
    require(len(g_rows) == 22, f"expected 22 g' rows, got {len(g_rows)}")
    require(len(sign_rows) == 22, f"expected 22 sign rows, got {len(sign_rows)}")
    require(len(r_rows) == 22, f"expected 22 R rows, got {len(r_rows)}")

    identity_matches = sum(1 for r in sign_rows if r["identity_match"] == "True")
    close_matches = sum(1 for r in sign_rows if r["close_pair_match"] == "True")
    exc_close = sum(1 for r in sign_rows if r["group"] == "exceptional" and r["close_pair_match"] == "True")
    base_close = sum(1 for r in sign_rows if r["group"] == "baseline" and r["close_pair_match"] == "True")
    require(identity_matches == 22, f"identity matches {identity_matches}/22")
    require(close_matches == 8, f"close pair matches {close_matches}/22")
    require(exc_close == 7 and base_close == 1, f"unexpected close pair split exc={exc_close}, base={base_close}")

    corr = float(r_rows[0]["pearson_R_vs_inv_s_min"])
    require(corr > 0.7, f"R vs 1/s_min correlation below threshold: {corr}")

    schema = json.loads((BASE / "step381_schema.json").read_text())
    require(schema["dps"] >= 80, "dps below hard constraint")
    require(schema["identity_sign_matches"] == 22, "schema identity mismatch")
    require(schema["close_pair_exception_sign_matches"] == 7, "schema exception close-pair mismatch")
    require(schema["pearson_R_vs_inv_s_min"] > 0.7, "schema R correlation below threshold")

    deriv = (BASE / "hadamard_derivation_step381.md").read_text()
    require("zeta''(rho_j) = 2 zeta'(rho_j) g'_j(rho_j)" in deriv, "missing key formula")
    boundary = (BASE / "nonclaim_boundary_step381.md").read_text().lower()
    require("does not prove rh" in boundary, "missing RH nonclaim")
    require("regular hadamard remainder" in boundary, "missing regular remainder caveat")

    print("STEP381_CHECK_PASS")
    print(f"identity_matches={identity_matches}/22")
    print(f"close_pair_matches={close_matches}/22 exceptions={exc_close}/7 baseline={base_close}/15")
    print(f"corr_R_inv_s={corr:.12g}")


if __name__ == "__main__":
    main()
