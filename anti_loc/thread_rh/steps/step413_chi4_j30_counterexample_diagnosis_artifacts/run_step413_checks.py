#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "counterexample_decomposition_step413.md",
    "g_prime_per_term_step413.csv",
    "step413_results_summary.md",
    "step413_schema.json",
    "nonclaim_boundary_step413.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

rows = list(csv.DictReader((ROOT / "g_prime_per_term_step413.csv").open()))
if len(rows) != 4:
    raise SystemExit(f"expected 4 term rows, found {len(rows)}")

terms = {r["term"]: float(r["Re_2Lprime_term"]) for r in rows}
required_terms = {"arch_chi4_prime", "close_pair_nearest_above", "regular_far_zero_residual", "total_g_prime"}
if set(terms) != required_terms:
    raise SystemExit(f"unexpected terms: {set(terms)}")

total_parts = terms["arch_chi4_prime"] + terms["close_pair_nearest_above"] + terms["regular_far_zero_residual"]
if abs(total_parts - terms["total_g_prime"]) > 1e-10:
    raise SystemExit("term sum does not match total")
if terms["close_pair_nearest_above"] <= 0:
    raise SystemExit("close-pair term should be positive after T31 correction")
if terms["arch_chi4_prime"] >= 0:
    raise SystemExit("arch term should be negative")

summary = (ROOT / "step413_results_summary.md").read_text()
if "boundary truncation artifact" not in summary:
    raise SystemExit("summary did not record truncation diagnosis")

print("Step 413 checks passed.")
print(f"Re_Lpp_total={terms['total_g_prime']}")
print(f"close_pair_contribution={terms['close_pair_nearest_above']}")
