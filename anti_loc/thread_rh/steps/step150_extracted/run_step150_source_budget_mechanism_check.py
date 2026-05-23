from pathlib import Path
import csv

BASE = Path(__file__).resolve().parent
required = [
    "source_budget_mechanism_step150.tex",
    "step150_results_summary.md",
    "source_budget_gate_table_step150.csv",
    "source_budget_mechanism_table_step150.csv",
    "theorem_map_step150.csv",
    "route_status_step150.csv",
    "nonclaim_boundary_step150.md",
    "step150_schema.json",
]
missing = [f for f in required if not (BASE / f).exists()]
if missing:
    raise SystemExit(f"Missing files: {missing}")

tex = (BASE / "source_budget_mechanism_step150.tex").read_text()
for token in ["No-free source-budget", "Direct residual invisibility", "Trace cancellation"]:
    if token not in tex:
        raise SystemExit(f"Missing token in TeX: {token}")

with open(BASE / "source_budget_mechanism_table_step150.csv", newline="") as fh:
    rows = list(csv.DictReader(fh))
assert any(r["mechanism"] == "direct_residual_invisibility" and r["status"] == "viable" for r in rows)
assert any(r["mechanism"] == "trace_cancellation" and r["status"] == "blocked" for r in rows)
print("Step 150 structural checks passed.")
