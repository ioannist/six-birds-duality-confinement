#!/usr/bin/env python3
"""Mode B Stage III admissibility transfer search."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean, median

import numpy as np


ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step358_mode_B_stage_III_admissibility_artifacts"
STEP357 = ROOT / "anti_loc/thread/steps/step357_mode_B_stage_II_at_scale_artifacts/reproduction_at_scale_step357.csv"

CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]
KS = list(range(1, 11))
RHOS = ["rho_1", "rho_2", "rho_3"]


def parse_complex(s: str) -> complex:
    return complex(s.replace(" ", ""))


def principal_phase_delta(a: float, b: float) -> float:
    return abs(math.atan2(math.sin(a - b), math.cos(a - b)))


def unwrap(vals: list[float]) -> np.ndarray:
    return np.unwrap(np.array(vals, dtype=float))


def load_data():
    H: dict[tuple[str, int], complex] = {}
    Z: dict[tuple[str, int], complex] = {}
    with STEP357.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["cell_type"] == "hecke_atom":
                H[(row["character"], int(row["k"]))] = parse_complex(row["observed"])
            elif row["cell_type"] == "zeta_atom":
                Z[(row["rho_target"], int(row["k"]))] = parse_complex(row["observed"])
    return H, Z


def residuals(pred: dict[tuple[str, int, str], complex], Z: dict[tuple[str, int], complex], rho: str):
    mag, phase, combined = [], [], []
    for ch in CHARS:
        for k in KS:
            p = pred[(ch, k, rho)]
            z = Z[(rho, k)]
            lm = abs(math.log(abs(p)) - math.log(abs(z)))
            lp = principal_phase_delta(math.atan2(p.imag, p.real), math.atan2(z.imag, z.real))
            mag.append(lm)
            phase.append(lp)
            combined.append(math.sqrt(lm * lm + lp * lp))
    return {
        "cell_count": len(combined),
        "mean_mag": mean(mag),
        "mean_phase": mean(phase),
        "mean_combined": mean(combined),
        "median_combined": median(combined),
        "rmse_combined": math.sqrt(mean([x * x for x in combined])),
        "max_combined": max(combined),
    }


def write_csv(path: Path, rows: list[dict[str, object]]):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    BASE.mkdir(parents=True, exist_ok=True)
    H, Z = load_data()

    search_rows = []
    cv_rows = []

    # Candidate 1: per-character scalar rewrite T_chi(H)=C_chi H.
    scalar_params = {}
    for ch in CHARS:
        ratios = [Z[("rho_1", k)] / H[(ch, k)] for k in KS]
        C = sum(ratios) / len(ratios)
        scalar_params[ch] = C
        search_rows.append(
            {
                "candidate": "tau_character_scalar",
                "train_target": "rho_1",
                "character": ch,
                "param_1": C.real,
                "param_2": C.imag,
                "param_description": "complex_C_chi_for_T(H)=C_chi_H",
                "operator_status": "missing_operator_certificate",
            }
        )

    # Candidate 2: per-character affine log rewrite, magnitude and unwrapped phase separately.
    affine_params = {}
    for ch in CHARS:
        h_abs_log = np.array([math.log(abs(H[(ch, k)])) for k in KS])
        z_abs_log = np.array([math.log(abs(Z[("rho_1", k)])) for k in KS])
        X_mag = np.column_stack([np.ones(len(KS)), h_abs_log])
        a_mag, b_mag = np.linalg.lstsq(X_mag, z_abs_log, rcond=None)[0]

        h_phase = unwrap([math.atan2(H[(ch, k)].imag, H[(ch, k)].real) for k in KS])
        z_phase = unwrap([math.atan2(Z[("rho_1", k)].imag, Z[("rho_1", k)].real) for k in KS])
        X_phase = np.column_stack([np.ones(len(KS)), h_phase])
        a_phase, b_phase = np.linalg.lstsq(X_phase, z_phase, rcond=None)[0]
        affine_params[ch] = (a_mag, b_mag, a_phase, b_phase)
        search_rows.append(
            {
                "candidate": "tau_character_affine_log",
                "train_target": "rho_1",
                "character": ch,
                "param_1": a_mag,
                "param_2": b_mag,
                "param_description": f"a_phase={a_phase};b_phase={b_phase}",
                "operator_status": "missing_operator_certificate",
            }
        )

    def scalar_predict(rho: str):
        return {(ch, k, rho): scalar_params[ch] * H[(ch, k)] for ch in CHARS for k in KS}

    def affine_predict(rho: str):
        out = {}
        for ch in CHARS:
            a_mag, b_mag, a_phase, b_phase = affine_params[ch]
            for k in KS:
                h = H[(ch, k)]
                mag = math.exp(a_mag + b_mag * math.log(abs(h)))
                ph = a_phase + b_phase * math.atan2(h.imag, h.real)
                out[(ch, k, rho)] = mag * complex(math.cos(ph), math.sin(ph))
        return out

    for candidate, predict in [
        ("tau_character_scalar", scalar_predict),
        ("tau_character_affine_log", affine_predict),
    ]:
        for rho in RHOS:
            stats = residuals(predict(rho), Z, rho)
            cv_rows.append(
                {
                    "candidate": candidate,
                    "train_target": "rho_1",
                    "test_target": rho,
                    **stats,
                    "operator_status": "missing_operator_certificate",
                    "admissible": "no",
                }
            )

    write_csv(BASE / "transfer_search_step358.csv", search_rows)
    write_csv(BASE / "cross_validation_step358.csv", cv_rows)

    print("wrote search rows", len(search_rows))
    print("wrote cross-validation rows", len(cv_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
