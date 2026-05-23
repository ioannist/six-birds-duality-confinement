#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step199_BN_extension_N2000_artifacts")

REQUIRED = [
    "step199_results_summary.md",
    "step199_schema.json",
    "content_classification_step199.csv",
    "nonclaim_boundary_step199.md",
    "step199_BN_extension_N2000.tex",
    "compute_BN_N2000_step199.py",
    "compute_BN_N2000_output_step199.txt",
    "run_step199_BN_N2000_checks.py",
    "extended_data_step199.csv",
    "updated_decay_fit_step199.csv",
    "residual_tree_step199.csv",
    "route_status_step199.csv",
    "construction_tasks_step199.csv",
]

VALID_VERDICTS = {
    "V_BN_N2000_consistent",
    "V_BN_N2000_drift",
    "V_BN_N2000_conditioning_limit",
    "V_BN_N2000_partial",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def read_csv(name: str):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step199_schema.json").read_text())
    if schema.get("step") != 199:
        fail("schema step must be 199")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("target") != "BN harmonic chain extension to N=2000":
        fail("target mismatch")
    verdict = schema.get("BN_N2000_verdict")
    if verdict not in VALID_VERDICTS:
        fail(f"invalid verdict {verdict}")
    if schema.get("final_verdict") != verdict:
        fail("final verdict mismatch")
    if 1500 not in schema.get("N_values_computed", []):
        fail("N=1500 missing from schema")
    if 2000 not in schema.get("N_values_computed", []):
        fail("N=2000 missing from schema")
    if schema.get("method", {}).get("mpmath_dps", 0) < 80:
        fail("mpmath precision below 80 dps")

    rows = read_csv("extended_data_step199.csv")
    got = {int(row["N"]): row for row in rows}
    for n in (1500, 2000):
        if n not in got:
            fail(f"N={n} missing from extended data")
        if float(got[n]["delta_sq"]) <= 0:
            fail(f"N={n} delta_sq not positive")
        if float(got[n]["delta_sq_logN"]) <= 0:
            fail(f"N={n} delta_sq_logN not positive")

    fit_rows = read_csv("updated_decay_fit_step199.csv")
    if not any(row["model"] == "tail_mean_delta_sq_logN" for row in fit_rows):
        fail("tail mean fit missing")
    tail = next(row for row in fit_rows if row["model"] == "tail_mean_delta_sq_logN")
    C = float(tail["C"])
    if not (0.04 < C < 0.06):
        fail(f"tail mean C out of expected slow-log range: {C}")

    output = (BASE / "compute_BN_N2000_output_step199.txt").read_text()
    for token in ["N=1500", "N=2000", "mpmath_dps=80", "full mpmath 2000x2000 SVD infeasible"]:
        if token not in output:
            fail(f"output missing token {token}")

    tex = (BASE / "step199_BN_extension_N2000.tex").read_text()
    for token in ["V\\_BN\\_N2000\\_consistent", "0.00592901311818050", "Baez--Duarte"]:
        if token not in tex:
            fail(f"tex missing token {token}")

    print("PASS step199 BN N2000 checks")
    print(f"verdict={verdict} tail_mean={C}")


if __name__ == "__main__":
    main()

