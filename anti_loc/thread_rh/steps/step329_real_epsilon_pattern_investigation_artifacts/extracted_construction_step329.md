# Step 329 Extracted Construction From Step 328

The following are verbatim snippets from `/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step328_hecke_H4_constructive_subfamily_artifacts/compute_H4_constructive_subfamily_step328.py`.

The construction is explicitly labelled as a cascade-internal natural extrapolation, not as a Burnol-derived theorem.

## Extract 1

```python
"""Step 328: constructive H4 finite model for primitive chars mod 3/4/5.

Burnol 2004 gives a Dirichlet-Sonine framework, but not an explicit finite
P_infty,chi / kernel residual formula.  This script therefore builds a labelled
cascade-internal finite Galerkin extrapolation using completed Dirichlet L-functions
as the E_chi input in the Burnol kernel shape.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step328_hecke_H4_constructive_subfamily_artifacts")
STEP320 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts")
DPS = 80
OFFSETS = [mp.mpf("-3"), mp.mpf("-2"), mp.mpf("-1"), mp.mpf("0"), mp.mpf("1"), mp.mpf("2"), mp.mpf("3")]
CENTER_OFFSETS = [mp.mpf("-0.75"), mp.mpf("0"), mp.mpf("0.75")]


de
```

## Extract 2

```python
def completed_E(s: mp.mpc, q: int, parity_a: int, chi: list[mp.mpc]) -> mp.mpc:
    return (mp.mpf(q) / mp.pi) ** ((s + parity_a) / 2) * mp.gamma((s + parity_a) / 2) * L_chi(s, q, chi)


def kernel(z: mp.mpc, w: mp.mpc, q: int, parity_a: int, chi: list[mp.mpc]) -> mp.mpc:
    Ez = completed_E(z, q, parity_a, chi)
    Ew = completed_E(w, q, parity_a, chi)
    E1z = completed_E(1 - z, q, parity_a, chi)
    E1w = completed_E(1 - w, q, parity_a, chi)
    denom = z + mp.conj(w) - 1
    return (Ez * mp.conj(Ew) - E1z * mp.conj(E1w)) / denom


def roots_from_step320() -> dict[str, mp.mpc]:
    rows = read_csv(STEP320 / "L_chi_first_zeros_step320.csv")
    return {r["character"]: mp.mpc(mp.mpf(r["Re_rho"]), mp.mpf(r["Im_rho"])) for r in rows}


def mat_conj_transpose(M: mp.matrix) -> mp.matrix:
    return M.T.apply(mp.conj)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.
```

## Extract 3

```python
def kernel(z: mp.mpc, w: mp.mpc, q: int, parity_a: int, chi: list[mp.mpc]) -> mp.mpc:
    Ez = completed_E(z, q, parity_a, chi)
    Ew = completed_E(w, q, parity_a, chi)
    E1z = completed_E(1 - z, q, parity_a, chi)
    E1w = completed_E(1 - w, q, parity_a, chi)
    denom = z + mp.conj(w) - 1
    return (Ez * mp.conj(Ew) - E1z * mp.conj(E1w)) / denom


def roots_from_step320() -> dict[str, mp.mpc]:
    rows = read_csv(STEP320 / "L_chi_first_zeros_step320.csv")
    return {r["character"]: mp.mpc(mp.mpf(r["Re_rho"]), mp.mpf(r["Im_rho"])) for r in rows}


def mat_conj_transpose(M: mp.matrix) -> mp.matrix:
    return M.T.apply(mp.conj)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    roots = roots_from_step320()
    kappa_rows: list[dict[str, object]] = []
    p_rows: list[dict[str, object]] = []
    residual_rows: list[dict[str, object]] = []
    sum
```

## Extract 4

```python
construction_status": "cascade_internal_natural_extrapolation_from_Burnol_kernel_shape",
                    }
                )

        W = mp.eye(m)  # unit grid weights
        G = mat_conj_transpose(V) * W * V
        G_inv = mp.inverse(G)
        P = V * G_inv * mat_conj_transpose(V) * W
        I_m = mp.eye(m)
        M_diag = mp.diag([L_chi(z, q, chi) for z in z_grid])
        C = mat_conj_transpose(V) * W * (I_m - P) * M_diag * V
        trace = mp.fsum([C[i, i] for i in range(n)])
        frob = mp.sqrt(mp.fsum([abs(C[i, j]) ** 2 for i in range(n) for j in range(n)]))
        p_rows.append(
            {
                "character": label,
                "q": q,
                "parity_a": parity_a,
                "root_number_epsilon": cstr(epsilon, 24),
                "projection_model": "finite Galerkin P_infty_chi proxy onto span{kappa_chi(w_j)}",
                "tau_gr
```

## Extract 5

```python
Burnol 2004 supplies the paper-grounded Dirichlet-Sonine framework: `P_chi`/`P'_chi`, `W_lambda^chi`, and zero-attached `Z_{rho,k}` vectors.",
            "Burnol does not provide an explicit `E_lambda^chi`, `P_infty,chi`, or finite matrix residual in the form required here.",
            "Therefore this construction is labelled a cascade-internal natural extrapolation using the completed Dirichlet L-function in the Burnol kernel shape.",
            "",
            "Score update: subfamily H4 advances from 1.5 to 2.0, not 2.5. Concrete finite residual content exists, but it is not a Burnol-derived theorem.",
            "",
            "Final verdict: `V_hecke_H4_subfamily_constructed_extrapolated_score_2_0`.",
        ]
    )
    (ART / "step328_results_summary.md").write_text("\n".join(summary_lines), encoding="utf-8")
    schema = {
        "step": 328,
        "orientation": "constr
```

## Cancellation Mechanism Tested In Step 329

For a real self-dual character with root number epsilon = 1, the completed function satisfies the self-dual critical-line symmetry used by the extrapolated kernel. In the Step 328 kernel shape, this makes the two numerator terms nearly identical on the sampled boundary grid, so their difference is numerically zero. For non-self-dual characters, the construction compares the character with the wrong conjugation structure for exact cancellation, so the numerator remains nontrivial.
