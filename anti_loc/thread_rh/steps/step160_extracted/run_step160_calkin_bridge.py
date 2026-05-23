
from pathlib import Path
import json, pandas as pd
base = Path(__file__).parent
required = [
    "calkin_faithful_boundary_symbol_step160.tex",
    "step160_results_summary.md",
    "calkin_bridge_gate_table_step160.csv",
    "content_classification_step160.csv",
    "bridge_atlas_step160.csv",
    "residual_tree_step160.csv",
    "theorem_map_step160.csv",
    "route_status_step160.csv",
    "construction_tasks_step160.csv",
    "nonclaim_boundary_step160.md",
    "step160_schema.json"
]
missing = [f for f in required if not (base/f).exists()]
assert not missing, f"missing: {missing}"
schema=json.loads((base/"step160_schema.json").read_text())
assert schema["orientation"]=="adequacy"
gate=pd.read_csv(base/"calkin_bridge_gate_table_step160.csv")
assert "public_shadow_no_go" in set(gate["gate"])
assert "finite_window_no_go" in set(gate["gate"])
print("Step 160 checks passed.")
