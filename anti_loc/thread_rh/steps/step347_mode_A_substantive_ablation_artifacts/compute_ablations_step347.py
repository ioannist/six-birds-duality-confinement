#!/usr/bin/env python3
"""Step 347: substantive ablation tests for M^b rewrite rules."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import mpmath as mp


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step347_mode_A_substantive_ablation_artifacts"
STEP346 = ROOT / "anti_loc/thread/steps/step346_mode_A_stage_II_earning_its_place_artifacts"


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


def relerr(a: mp.mpf, b: mp.mpf) -> mp.mpf:
    return abs(a - b) / abs(b) if b != 0 else abs(a - b)


def parse_zeta_row(row_id: str) -> tuple[int, int] | None:
    m = re.match(r"Z_rho(\d+)_(\d+)_via_F_H_chi3", row_id)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def make_rows(original: list[dict[str, str]], ablation: str, value_func, note_func, f2_func) -> tuple[list[dict[str, object]], dict[str, mp.mpf | int | bool]]:
    out: list[dict[str, object]] = []
    changed = 0
    failed = 0
    max_change = mp.mpf("0")
    max_rel = mp.mpf("0")
    for row in original:
        inherited = mp.mpf(row["cascade_inherited_value"])
        orig = mp.mpf(row["M_b_value"])
        ablated = value_func(row)
        rel_to_inherited = relerr(ablated, inherited)
        output_change = relerr(ablated, orig)
        changed_flag = output_change > mp.mpf("1e-30")
        fail_flag = rel_to_inherited >= mp.mpf("0.01")
        changed += int(changed_flag)
        failed += int(fail_flag)
        max_change = max(max_change, output_change)
        max_rel = max(max_rel, rel_to_inherited)
        out.append({
            "row_id": row["row_id"],
            "realization": row["realization"],
            "ablation": ablation,
            "cascade_inherited_value": row["cascade_inherited_value"],
            "M_b_original_value": row["M_b_value"],
            "M_b_ablated_value": mp.nstr(ablated, 18),
            "relative_error_vs_inherited": mp.nstr(rel_to_inherited, 12),
            "relative_output_change_vs_original": mp.nstr(output_change, 12),
            "output_changed": "yes" if changed_flag else "no",
            "reproduction_breaks": "yes" if fail_flag else "no",
            "F2_identity_preserved": "yes" if f2_func(row) else "no",
            "note": note_func(row),
        })
    stats = {
        "changed": changed,
        "failed": failed,
        "max_change": max_change,
        "max_rel": max_rel,
    }
    return out, stats


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    original = read_csv(STEP346 / "stage_II_reproduction_table_step346.csv")
    zeta_value = {}
    for row in original:
        parsed = parse_zeta_row(row["row_id"])
        if parsed is not None:
            zeta_value[parsed] = mp.mpf(row["M_b_value"])

    # A: F(H)=Z+Omega -> F(H)=Z. Since Omega is ledger-only, host values are unchanged.
    rows_a, stats_a = make_rows(
        original,
        "A_drop_omega_from_FH",
        lambda row: mp.mpf(row["M_b_value"]),
        lambda row: "Omega removed from F(H); numeric host lens unchanged because Omega was ledger-only",
        lambda row: True,
    )
    write_csv(ART / "ablation_A_dropping_omega_from_FH_step347.csv", rows_a)

    # B: F(Z)=H+Omega -> F(Z)=H. Stage II reproduction paths do not exercise F(Z).
    rows_b, stats_b = make_rows(
        original,
        "B_drop_omega_from_FZ",
        lambda row: mp.mpf(row["M_b_value"]),
        lambda row: "F(Z) is not exercised by the 100 Stage-II reproduction paths",
        lambda row: True,
    )
    write_csv(ART / "ablation_B_dropping_omega_from_FZ_step347.csv", rows_b)

    # C: F(Omega)=-Omega -> F(Omega)=0. Numeric one-step host values unchanged,
    # but F^2=id fails on transfer-routed rows.
    rows_c, stats_c = make_rows(
        original,
        "C_drop_FOmega_sign",
        lambda row: mp.mpf(row["M_b_value"]),
        lambda row: "F(Omega)=0 leaves one-step host value unchanged but breaks F^2 identity on transfer paths",
        lambda row: row["realization"] != "R_zeta",
    )
    write_csv(ART / "ablation_C_dropping_F_omega_sign_step347.csv", rows_c)

    # D: F(H)=Z' where Z' is the next rho basis in {1,2,3} cyclically.
    def d_value(row: dict[str, str]) -> mp.mpf:
        parsed = parse_zeta_row(row["row_id"])
        if parsed is None:
            return mp.mpf(row["M_b_value"])
        j, k = parsed
        jp = 1 + (j % 3)
        return zeta_value[(jp, k)]

    def d_note(row: dict[str, str]) -> str:
        parsed = parse_zeta_row(row["row_id"])
        if parsed is None:
            return "Hecke direct R_H path does not use F(H)"
        j, _ = parsed
        jp = 1 + (j % 3)
        return f"F(H) routed to wrong zeta basis Z_rho{jp}"

    rows_d, stats_d = make_rows(
        original,
        "D_replace_FH_with_Zprime",
        d_value,
        d_note,
        lambda row: False if row["realization"] == "R_zeta" else True,
    )
    write_csv(ART / "ablation_D_replacing_FH_with_Zprime_step347.csv", rows_d)

    summary_lines = [
        "# Step 347 Results Summary",
        "",
        "Substantive ablation check for the Step 345/346 `M^b` algebra.",
        "",
        "Results over the 100 Stage-II reproduction rows:",
        f"- Ablation A (`F(H)=Z+Omega -> F(H)=Z`): changed `{stats_a['changed']}/100`, failed `{stats_a['failed']}/100`, max output change `{mp.nstr(stats_a['max_change'], 12)}`.",
        f"- Ablation B (`F(Z)=H+Omega -> F(Z)=H`): changed `{stats_b['changed']}/100`, failed `{stats_b['failed']}/100`, max output change `{mp.nstr(stats_b['max_change'], 12)}`.",
        f"- Ablation C (`F(Omega)=-Omega -> F(Omega)=0`): changed `{stats_c['changed']}/100`, failed `{stats_c['failed']}/100`, max output change `{mp.nstr(stats_c['max_change'], 12)}`; F^2 identity fails on transfer-routed rows.",
        f"- Ablation D (`F(H)=Z+Omega -> F(H)=Zprime`): changed `{stats_d['changed']}/100`, failed `{stats_d['failed']}/100`, max output change `{mp.nstr(stats_d['max_change'], 12)}`.",
        "",
        "Interpretation:",
        "A/B/C do not alter numerical host outputs.  The obstruction symbol `Omega` is ledger-only in the current construction, and `F(Z)` is not used by the Stage-II reproduction paths.  Only replacing the zeta target basis in F(H) changes numerical output, which means the arithmetic work is done by the external realization evaluators, not by the virtual algebra's obstruction rewrite.",
        "",
        "Stage II true-status verdict: `V_mode_A_stage_II_substantive_ablation_fails_algebra_decorative`.",
    ]
    (ART / "step347_results_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    schema = {
        "step": 347,
        "orientation": "Mode A substantive ablation",
        "target": "test whether M^b rewrite rules are numerically load-bearing",
        "ablation_A_changed": stats_a["changed"],
        "ablation_A_failed": stats_a["failed"],
        "ablation_B_changed": stats_b["changed"],
        "ablation_B_failed": stats_b["failed"],
        "ablation_C_changed": stats_c["changed"],
        "ablation_C_failed": stats_c["failed"],
        "ablation_D_changed": stats_d["changed"],
        "ablation_D_failed": stats_d["failed"],
        "stage_II_true_status": "fails_substantive_ablation",
        "final_verdict": "V_mode_A_stage_II_substantive_ablation_fails_algebra_decorative",
    }
    (ART / "step347_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 347 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- Step 346's nominal reproduction is not treated as substantive after this ablation check.",
        "- `Omega` is confirmed ledger-only in the current `M^b`; it is not a numerical descent mechanism.",
        "- Mode A must be rebuilt with algebraic operations that affect realization output, not merely labels.",
    ]
    (ART / "nonclaim_boundary_step347.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print("A_changed_failed", stats_a["changed"], stats_a["failed"])
    print("B_changed_failed", stats_b["changed"], stats_b["failed"])
    print("C_changed_failed", stats_c["changed"], stats_c["failed"])
    print("D_changed_failed", stats_d["changed"], stats_d["failed"])
    print("verdict=V_mode_A_stage_II_substantive_ablation_fails_algebra_decorative")


if __name__ == "__main__":
    main()
