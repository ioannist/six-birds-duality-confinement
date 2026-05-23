#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
required = [
    "boundary_weyl_avoidance_step159.tex",
    "step159_results_summary.md",
    "boundary_weyl_gate_table_step159.csv",
    "boundary_weyl_classification_step159.csv",
    "theorem_map_step159.csv",
    "route_status_step159.csv",
    "construction_tasks_step159.csv",
    "bridge_atlas_step159.csv",
    "residual_tree_step159.csv",
    "nonclaim_boundary_step159.md",
    "step159_schema.json",
]

results = {"missing": [], "latex_balance": {}, "files_checked": required}
for name in required:
    if not (BASE / name).exists():
        results["missing"].append(name)

tex = (BASE / "boundary_weyl_avoidance_step159.tex").read_text(encoding="utf-8")
for left, right in [("\\begin{theorem}", "\\end{theorem}"), ("\\begin{definition}", "\\end{definition}"), ("\\[", "\\]")]:
    results["latex_balance"][left + " vs " + right] = tex.count(left) == tex.count(right)

schema = json.loads((BASE / "step159_schema.json").read_text(encoding="utf-8"))
results["schema_step"] = schema.get("step")
results["schema_orientation"] = schema.get("orientation")
results["passed"] = not results["missing"] and all(results["latex_balance"].values()) and schema.get("step") == 159

(BASE / "step159_check_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
