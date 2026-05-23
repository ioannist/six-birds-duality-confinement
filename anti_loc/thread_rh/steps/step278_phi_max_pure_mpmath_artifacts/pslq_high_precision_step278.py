#!/usr/bin/env python3
"""Step 278 PSLQ retry using the pure-mpmath convergence result."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


mp.mp.dps = 100
ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step278_phi_max_pure_mpmath_artifacts")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def constants() -> list[tuple[str, mp.mpf]]:
    return [
        ("1", mp.mpf(1)),
        ("pi", mp.pi),
        ("log2", mp.log(2)),
        ("log3", mp.log(3)),
        ("logpi", mp.log(mp.pi)),
        ("EulerGamma", mp.euler),
        ("zeta3", mp.zeta(3)),
        ("Catalan", mp.catalan),
        ("Khinchin", mp.khinchin),
        ("Gamma_1_4", mp.gamma(mp.mpf(1) / 4)),
        ("zeta_1_2", mp.zeta(mp.mpf(1) / 2)),
        ("abs_zeta_prime_0", abs(mp.diff(lambda z: mp.zeta(z), mp.mpf(0)))),
        ("J0_first_zero", mp.besseljzero(0, 1)),
    ]


def main() -> None:
    rows = list(csv.DictReader((ART / "phi_max_high_precision_step278.csv").open(encoding="utf-8")))
    selected = rows[0]
    phi = mp.mpf(selected["Phi"])
    stable = selected["stability_status"] == "stable_50_digits"

    consts = constants()
    pslq_rows = []
    if stable:
        for name, value in consts:
            if name == "1":
                continue
            rel = mp.pslq([phi, mp.mpf(1), value], tol=mp.mpf("1e-60"), maxcoeff=10**8, maxsteps=1000)
            status = "no_relation" if rel is None else ("candidate_relation" if int(rel[0]) != 0 else "trivial_basis_relation")
            pslq_rows.append(
                {
                    "target": "pure_mpmath_phi",
                    "basis": f"Phi;1;{name}",
                    "relation": "" if rel is None else ";".join(str(int(x)) for x in rel),
                    "status": status,
                    "notes": "stable input",
                }
            )
    else:
        # Diagnostic retry: record that PSLQ is intentionally not trusted.
        for name, _ in consts:
            pslq_rows.append(
                {
                    "target": "pure_mpmath_phi",
                    "basis": f"Phi;1;{name}",
                    "relation": "",
                    "status": "not_run_unstable_input",
                    "notes": "pure mpmath convergence did not produce stable digits",
                }
            )

    write_csv(ART / "pslq_retry_step278.csv", pslq_rows)

    persistence_rows = [
        {
            "check": "basis_size_doubling",
            "input": "N=80 vs N=160 at dps80",
            "result": "failed",
            "notes": "values differ far beyond PSLQ tolerance; no trusted high precision digits",
        },
        {
            "check": "dps_doubling",
            "input": "N=80 dps80 vs N=80 dps120",
            "result": "same discretization but not reference-converged",
            "notes": "dps increase does not fix quadrature/projection convergence",
        },
        {
            "check": "pslq_persistence",
            "input": "candidate relations",
            "result": "not_applicable",
            "notes": "no trusted high-precision candidate relation was generated",
        },
    ]
    write_csv(ART / "persistence_step278.csv", persistence_rows)

    payload = {
        "stable_input": stable,
        "pslq_status": "skipped_as_untrusted" if not stable else "run",
        "final_verdict": "V_branch_A_high_precision_partial" if not stable else "V_branch_A_high_precision_no_closed_form",
    }
    (ART / "pslq_high_precision_output_step278.txt").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
