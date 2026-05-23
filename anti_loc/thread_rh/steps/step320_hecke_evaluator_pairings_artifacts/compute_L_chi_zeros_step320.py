#!/usr/bin/env python3
"""Step 320: locate first critical-line zeros for the mod 3,4,5 characters.

The characters are the primitive subfamily whose H5 ledger was constructed in
Step 319.  Values are computed from the residue-class Hurwitz zeta expression

    L(s, chi) = q^{-s} sum_{a=1}^q chi(a) zeta(s, a/q).
"""

from __future__ import annotations

import csv
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts")
DPS = 50


def cstr(z: mp.mpc, digits: int = 32) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def character_data() -> dict[str, tuple[int, list[mp.mpc], mp.mpf, mp.mpf]]:
    I = mp.mpc(0, 1)
    return {
        "chi_3": (3, [0, 1, -1], mp.mpf("8.04"), mp.mpf("8.04")),
        "chi_4": (4, [0, 1, 0, -1], mp.mpf("6.02"), mp.mpf("6.02")),
        "chi_5a": (5, [0, 1, -1, -1, 1], mp.mpf("6.64"), mp.mpf("6.64")),
        # The prompt's rough 3.671 value is recorded, but for this character
        # the two-variable Newton solver's first nontrivial critical-line basin
        # is near t=6.18 for the Step 319 convention chi(2)=i.
        "chi_5b": (5, [0, 1, I, -I, -1], mp.mpf("3.67"), mp.mpf("6.18")),
    }


def L_chi(s: mp.mpc, q: int, chi: list[mp.mpc]) -> mp.mpc:
    return (mp.mpf(q) ** (-s)) * mp.fsum(
        [chi[a % q] * mp.zeta(s, mp.mpf(a) / q) for a in range(1, q + 1)]
    )


def root_from_guess(q: int, chi: list[mp.mpc], guess_t: mp.mpf) -> mp.mpc:
    def f(x: mp.mpf, y: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
        value = L_chi(mp.mpc(x, y), q, chi)
        return mp.re(value), mp.im(value)

    # The rough prompt value for chi_5b belongs to the right search basin only
    # after the two-variable Newton solve is allowed to move freely.
    x, y = mp.findroot(f, (mp.mpf("0.5"), guess_t), tol=mp.mpf("1e-30"), maxsteps=30, solver="mnewton")
    return mp.mpc(x, y)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    rows: list[dict[str, object]] = []
    for label, (q, chi, prompt_guess_t, solver_guess_t) in character_data().items():
        rho = root_from_guess(q, chi, solver_guess_t)
        residual = abs(L_chi(rho, q, chi))
        rows.append(
            {
                "character": label,
                "conductor": q,
                "prompt_initial_t_guess": mp.nstr(prompt_guess_t, 20),
                "solver_t_guess": mp.nstr(solver_guess_t, 20),
                "rho_chi": cstr(rho, 40),
                "Re_rho": mp.nstr(mp.re(rho), 32),
                "Im_rho": mp.nstr(mp.im(rho), 32),
                "L_abs_at_rho": mp.nstr(residual, 18),
                "method": "mpmath two-variable Newton solve on Re/Im of residue-class Hurwitz L(s,chi)",
            }
        )
    write_csv(ART / "L_chi_first_zeros_step320.csv", rows)
    for row in rows:
        print(f"{row['character']}: rho={row['rho_chi']} |L|={row['L_abs_at_rho']}")


if __name__ == "__main__":
    main()
