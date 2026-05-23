#!/usr/bin/env python3
"""Step 307: verify M(G_star)(1) and related local values."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step307_delta_Dk_lower_bound_artifacts")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")

MP_DPS = 100
RHO1 = mp.mpc(mp.mpf("0.5"), mp.mpf("14.134725141734693790457251983562470270784257115699"))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def cstr(z: mp.mpc, digits: int = 50) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def mellin_value(step292, z: mp.mpc) -> mp.mpc:
    centers, epsilons, coeffs = step292.moment_coefficients(step292.GENERATORS["G_star"])
    total = mp.mpc(0)
    for c, eps, coeff in zip(centers, epsilons, coeffs):
        lo, hi = c - eps, c + eps
        total += mp.quad(lambda t, cc=c, ee=eps, aa=coeff: aa * step292.beta_bump((t - cc) / ee) * (t ** (-z)), [lo, hi])
    return total


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    step292 = load_module("step292_for_step307_M", STEP292_SCRIPT)
    values = {
        "M_G_star_0": mellin_value(step292, mp.mpc(0)),
        "M_G_star_1": mellin_value(step292, mp.mpc(1)),
        "M_G_star_rho1": mellin_value(step292, RHO1),
    }
    rows = []
    for label, val in values.items():
        rows.append({
            "quantity": label,
            "value": cstr(val, 60),
            "abs": mp.nstr(abs(val), 60),
            "dps": MP_DPS,
        })
    with (ART / "M_G_at_1_step307.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    schema_fragment = {
        "M_G_star_1_abs": mp.nstr(abs(values["M_G_star_1"]), 60),
        "M_G_star_rho1_abs": mp.nstr(abs(values["M_G_star_rho1"]), 60),
    }
    (ART / "M_G_at_1_step307.json").write_text(json.dumps(schema_fragment, indent=2), encoding="utf-8")
    print("Step307 M(G_star) local values")
    for row in rows:
        print(f"{row['quantity']} abs={row['abs']} value={row['value']}")


if __name__ == "__main__":
    main()
