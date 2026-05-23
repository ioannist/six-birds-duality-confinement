#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "U_flat_reg_design_step416.md",
    "SAU_6_of_6_check_step416.csv",
    "stage_III_translation_step416.md",
    "transfer_search_with_crossval_step416.csv",
    "constraint_engineering_audit_step416.md",
    "step416_results_summary.md",
    "mode_b_constraint_ledger_step416_snapshot.csv",
    "mode_b_target_lineage_step416_snapshot.csv",
    "mode_b_grammar_manifest_G_U_flat_reg_step416.csv",
    "step416_schema.json",
    "nonclaim_boundary_step416.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

sau = list(csv.DictReader((ROOT / "SAU_6_of_6_check_step416.csv").open()))
if len(sau) != 6 or any(r["status"] != "pass" for r in sau):
    raise SystemExit("SAU 6/6 check failed")

rows = list(csv.DictReader((ROOT / "transfer_search_with_crossval_step416.csv").open()))
passing = [r for r in rows if r["R_crossval_gate_pass"] == "True"]
if not passing:
    raise SystemExit("no crossval-passing setting")

best = min(passing, key=lambda r: float(r["holdout_log_RMSE"]))
if float(best["training_log_RMSE"]) >= 0.5:
    raise SystemExit("C5 failed for best passing setting")
if float(best["holdout_to_training_ratio"]) > 1.3:
    raise SystemExit("C6 failed for best passing setting")
if best["lambda_regularization"] != "3":
    raise SystemExit(f"unexpected best lambda: {best['lambda_regularization']}")

manifest = (ROOT / "mode_b_grammar_manifest_G_U_flat_reg_step416.csv").read_text()
if "next_grammar_delta" not in manifest or "R_crossval" not in manifest:
    raise SystemExit("grammar manifest missing delta or crossval")

print("Step 416 checks passed.")
print(f"best_lambda={best['lambda_regularization']}")
print(f"train={best['training_log_RMSE']}")
print(f"holdout={best['holdout_log_RMSE']}")
print(f"ratio={best['holdout_to_training_ratio']}")
