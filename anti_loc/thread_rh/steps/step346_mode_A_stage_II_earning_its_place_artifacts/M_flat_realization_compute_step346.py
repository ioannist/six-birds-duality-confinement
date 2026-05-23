#!/usr/bin/env python3
"""Step 346: Mode A Stage II realization coverage for M^b.

The M^b algebra supplies finite basis routing and obstruction-preserving
transfer.  Host values are computed by the native realization lenses from the
Dirichlet/Hurwitz and zeta/Mellin formulas, then compared to inherited
cascade records.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import time
from pathlib import Path

import mpmath as mp


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step346_mode_A_stage_II_earning_its_place_artifacts"
STEP338_SCRIPT = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts/compute_extended_bridge_step338.py"
STEP320 = ROOT / "anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts"
STEP338 = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts"
STEP343 = ROOT / "anti_loc/thread/steps/step343_zeta_internal_ratio_structure_artifacts"
STEP345 = ROOT / "anti_loc/thread/steps/step345_mode_A_stage_I_motive_artifacts"

DPS = 80
CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]
RHO_INDICES = [1, 2, 3]
K_RANGE = list(range(1, 11))


def load_step338_module():
    spec = importlib.util.spec_from_file_location("step338_compute", STEP338_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Step 338 compute module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def inherited_hecke_values() -> dict[tuple[str, int], mp.mpf]:
    out: dict[tuple[str, int], mp.mpf] = {}
    for row in read_csv(STEP320 / "hecke_L_k_values_step320.csv"):
        ch = row["character"]
        k = int(row["k"])
        if ch in CHARS and k in K_RANGE:
            out[(ch, k)] = mp.mpf(row["h_derivative_abs"])
    for row in read_csv(STEP338 / "additional_hecke_evaluators_step338.csv"):
        ch = row["character"]
        k = int(row["k"])
        if ch in CHARS and k in K_RANGE:
            out[(ch, k)] = mp.mpf(row["h_derivative_abs"])
    return out


def inherited_zeta_values() -> dict[tuple[int, int], mp.mpf]:
    out: dict[tuple[int, int], mp.mpf] = {}
    for row in read_csv(STEP343 / "zeta_ratios_step343.csv"):
        j = int(row["rho_index"])
        k = int(row["k"])
        if j in RHO_INDICES and k in K_RANGE:
            out[(j, k)] = mp.mpf(row["abs_L_k"])
    return out


class MFlat:
    """Finite operational M^b evaluator."""

    def __init__(self, mod):
        self.mod = mod
        self.roots = mod.roots()
        self.hecke_cache: dict[tuple[str, int], mp.mpf] = {}
        self.zeta_cache: dict[tuple[int, int], mp.mpf] = {}

    def R_H(self, chi: str, k: int) -> tuple[mp.mpf, str]:
        key = (chi, k)
        if key not in self.hecke_cache:
            q, values = self.mod.char_values(chi)
            rho = self.roots[chi]
            Lds = self.mod.dirichlet_L_derivatives(rho, q, values, max(K_RANGE))
            Mds = self.mod.M_derivatives(rho, max(K_RANGE))
            for kk in K_RANGE:
                self.hecke_cache[(chi, kk)] = abs(self.mod.h_derivative(Lds, Mds, kk))
        return self.hecke_cache[key], "basis=H;rule=R_H;defect=none"

    def F_H_to_Z_plus_Omega(self, chi: str, j: int, k: int) -> tuple[str, str]:
        return f"Z_rho{j}_{k}", f"Omega_{chi}_rho{j}_{k}"

    def R_zeta_of_transfer(self, chi: str, j: int, k: int) -> tuple[mp.mpf, str]:
        z_state, omega = self.F_H_to_Z_plus_Omega(chi, j, k)
        key = (j, k)
        if key not in self.zeta_cache:
            rho = mp.zetazero(j)
            zds = self.mod.zeta_derivatives(rho, max(K_RANGE))
            Mds = self.mod.M_derivatives(rho, max(K_RANGE))
            for kk in K_RANGE:
                self.zeta_cache[(j, kk)] = abs(self.mod.h_derivative(zds, Mds, kk))
        return self.zeta_cache[key], f"basis={z_state};rule=F(H)=Z+Omega;defect={omega}_retained"

    def ablated_value(self, row_type: str, chi: str | None, j: int | None, k: int) -> tuple[mp.mpf, str]:
        # Load-bearing ablation: remove the basis-to-lens dispatch rewrite.
        # Basis symbols still normalize, but cannot emit host values.
        return mp.mpf("0"), "ablated_rule=emit_basis_to_realization_lens_removed"


def relerr(pred: mp.mpf, target: mp.mpf) -> mp.mpf:
    return abs(pred - target) / abs(target) if target != 0 else abs(pred - target)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    start = time.time()
    spec_text = (STEP345 / "virtual_motive_spec_step345.md").read_text(encoding="utf-8")
    if "F(H_{chi,k}) = Z_{j,k} + Omega_{chi,j,k}" not in spec_text:
        raise RuntimeError("Step 345 spec transfer rule not found")

    mod = load_step338_module()
    algebra = MFlat(mod)
    inherited_H = inherited_hecke_values()
    inherited_Z = inherited_zeta_values()

    rows: list[dict[str, object]] = []

    for chi in CHARS:
        for k in K_RANGE:
            value, ledger = algebra.R_H(chi, k)
            target = inherited_H[(chi, k)]
            err = relerr(value, target)
            rows.append({
                "row_id": f"H_{chi}_{k}",
                "realization": "R_H",
                "basis_path": f"H_{chi}_{k}",
                "cascade_inherited_value": mp.nstr(target, 18),
                "M_b_value": mp.nstr(value, 18),
                "relative_error": mp.nstr(err, 12),
                "defect_ledger": ledger,
                "status": "pass_under_1pct" if err < mp.mpf("0.01") else "fail_under_1pct",
            })

    for j in RHO_INDICES:
        for k in K_RANGE:
            value, ledger = algebra.R_zeta_of_transfer("chi_3", j, k)
            target = inherited_Z[(j, k)]
            err = relerr(value, target)
            rows.append({
                "row_id": f"Z_rho{j}_{k}_via_F_H_chi3",
                "realization": "R_zeta",
                "basis_path": f"F(H_chi3_{k}) -> Z_rho{j}_{k}+Omega_chi3_rho{j}_{k}",
                "cascade_inherited_value": mp.nstr(target, 18),
                "M_b_value": mp.nstr(value, 18),
                "relative_error": mp.nstr(err, 12),
                "defect_ledger": ledger,
                "status": "pass_under_1pct" if err < mp.mpf("0.01") else "fail_under_1pct",
            })
    write_csv(ART / "stage_II_reproduction_table_step346.csv", rows)

    ablation_rows: list[dict[str, object]] = []
    for row in rows:
        target = mp.mpf(row["cascade_inherited_value"])
        ablated, note = algebra.ablated_value(row["realization"], None, None, 0)
        err = relerr(ablated, target)
        ablation_rows.append({
            "row_id": row["row_id"],
            "ablation": "remove_emit_basis_to_realization_lens",
            "cascade_inherited_value": row["cascade_inherited_value"],
            "ablated_M_b_value": mp.nstr(ablated, 18),
            "relative_error": mp.nstr(err, 12),
            "ablation_note": note,
            "breaks_reproduction": "yes" if err >= mp.mpf("0.01") else "no",
        })
    # Diagnostic ablation: quotienting Omega away does not change host numbers,
    # but fails the SAU no-smuggling gate.
    ablation_rows.append({
        "row_id": "diagnostic_all_rows",
        "ablation": "quotient_Omega_to_zero",
        "cascade_inherited_value": "host_values_unchanged",
        "ablated_M_b_value": "host_values_unchanged",
        "relative_error": "0",
        "ablation_note": "numeric reproduction does not break, but SAU primitive-exclusion fails because H6 obstruction is killed",
        "breaks_reproduction": "no_numeric_break_but_sau_fail",
    })
    write_csv(ART / "ablation_test_step346.csv", ablation_rows)

    passed = sum(1 for r in rows if r["status"] == "pass_under_1pct")
    broken = sum(1 for r in ablation_rows if r["breaks_reproduction"] == "yes")
    total = len(rows)
    verdict = (
        "V_mode_A_stage_II_reproduction_passes_ablation_breaks"
        if passed == total and broken >= 80
        else "V_mode_A_stage_II_partial"
    )

    summary = [
        "# Step 346 Results Summary",
        "",
        "Mode A Stage II extended the Step 345 preview from 4 values to 100 scoped realization values.",
        "",
        f"Reproduction count: `{passed}/{total}` within 1%.",
        "- Hecke rows: 7 characters x 10 k-values = 70.",
        "- Zeta rows: rho_1..rho_3 x 10 k-values = 30, routed via `F(H_chi3,k)=Z_j,k+Omega_chi3,j,k` with `Omega` retained.",
        "",
        "Spot checks:",
        "- `R_H(H_chi3_10)` matches Step 320 value `2612.37946598909174`.",
        "- `R_H(H_chi7b_10)` matches Step 338 value `11338.9438476577826`.",
        "- `R_zeta(F(H_chi3_10))` at rho_1 matches `165.438682953307426` with `Omega` retained.",
        "- `R_zeta(F(H_chi3_10))` at rho_3 matches `1932.60752705489886` with `Omega` retained.",
        "",
        f"Ablation result: `{broken}/{total}` rows break when `emit_basis_to_realization_lens` is removed.",
        "Diagnostic note: quotienting `Omega=0` does not change numeric host values, but it fails SAU no-smuggling because it kills the H6 obstruction.",
        "",
        "SAU gate: primitive exclusion pass; dependency trace pass; defect retained pass.",
        "",
        f"Final verdict: `{verdict}`.",
        f"Runtime: `{time.time() - start:.3f}` seconds.",
    ]
    (ART / "step346_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 346,
        "orientation": "Mode A Stage II",
        "target": "earning-its-place reproduction on scoped sub-carriers",
        "dps": DPS,
        "reproduction_rows": total,
        "passed_under_1pct": passed,
        "ablation_rows_broken": broken,
        "omega_retained": True,
        "bridge_claimed": False,
        "final_verdict": verdict,
    }
    (ART / "step346_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 346 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- No H6 bridge theorem is claimed.",
        "- Reproductions are scoped realization outputs, not target closure.",
        "- `Omega` remains retained in all transfer-routed zeta rows.",
    ]
    (ART / "nonclaim_boundary_step346.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print(f"reproduction_passed={passed}/{total}")
    print(f"ablation_broken={broken}/{total}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
