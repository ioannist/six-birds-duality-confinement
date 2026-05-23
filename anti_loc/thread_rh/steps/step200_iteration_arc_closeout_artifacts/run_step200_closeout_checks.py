#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step200_iteration_arc_closeout_artifacts"
AUDIT = ROOT / "anti_loc/RH_framework_audit.md"
MANAGER_LOG = ROOT / "anti_loc/thread/manager_log.md"
CASCADE_MAP = ROOT / "anti_loc/thread/cascade_map_rh.md"
CANVAS = ROOT / "anti_loc/thread/cascade_rh.canvas"

REQUIRED = [
    "step200_results_summary.md",
    "step200_schema.json",
    "content_classification_step200.csv",
    "nonclaim_boundary_step200.md",
    "step200_iteration_arc_closeout.tex",
    "run_step200_closeout_checks.py",
    "iteration_arc_substantive_step200.csv",
    "iteration_arc_synthesis_step200.csv",
    "retained_typed_conditions_step200.csv",
    "retained_no_gos_step200.csv",
    "native_closure_step200.csv",
    "numerical_experiments_step200.csv",
    "strategic_paths_step200.csv",
    "next_directions_step200.csv",
    "residual_tree_step200.csv",
    "route_status_step200.csv",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def read_csv(name: str):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")
    for path, label in [(AUDIT, "audit"), (MANAGER_LOG, "manager log"), (CASCADE_MAP, "cascade map"), (CANVAS, "canvas")]:
        if not path.exists():
            fail(f"missing {label}: {path}")

    schema = json.loads((BASE / "step200_schema.json").read_text())
    if schema.get("step") != 200:
        fail("schema step must be 200")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("iteration_arc_substantive_count") != 17:
        fail("substantive count mismatch")
    if schema.get("iteration_arc_synthesis_count") != 5:
        fail("synthesis count mismatch")
    if len(schema.get("retained_typed_conditions", [])) != 4:
        fail("typed condition count mismatch")
    if schema.get("retained_no_gos_count") != 10:
        fail("no-go count mismatch")
    if schema.get("native_closure_count") != 3:
        fail("native closure count mismatch")
    if schema.get("numerical_experiments_count") != 2:
        fail("numerical experiment count mismatch")
    if schema.get("audit_document_path") != "anti_loc/RH_framework_audit.md":
        fail("audit path mismatch")
    if schema.get("final_verdict") != "V_arc_terminus_declared":
        fail("final verdict mismatch")

    if len(read_csv("iteration_arc_substantive_step200.csv")) != 17:
        fail("substantive CSV must have 17 rows")
    if len(read_csv("iteration_arc_synthesis_step200.csv")) != 5:
        fail("synthesis CSV must have 5 rows")
    if len(read_csv("retained_typed_conditions_step200.csv")) != 4:
        fail("typed conditions CSV must have 4 rows")
    if len(read_csv("retained_no_gos_step200.csv")) != 10:
        fail("no-go CSV must have 10 rows")
    if len(read_csv("native_closure_step200.csv")) != 3:
        fail("native closure CSV must have 3 rows")
    if len(read_csv("numerical_experiments_step200.csv")) != 2:
        fail("numerical experiment CSV must have 2 rows")

    audit_lines = sum(1 for _ in AUDIT.open())
    if audit_lines != 925:
        fail(f"audit line count changed: {audit_lines}")

    manager_text = MANAGER_LOG.read_text()
    if "### step200" not in manager_text or "V_arc_terminus_declared" not in manager_text:
        fail("manager log missing step200 closeout")

    map_text = CASCADE_MAP.read_text()
    if "ITERATION ARC TERMINUS DECLARED (step 200)" not in map_text or "arc_terminus" not in map_text:
        fail("cascade map missing terminus callout")

    canvas_text = CANVAS.read_text()
    if canvas_text.count("📍") != 1:
        fail("canvas must contain exactly one pin marker")
    if '"id": "arc_terminus"' not in canvas_text:
        fail("canvas missing arc_terminus node")
    json.loads(canvas_text)

    tex = (BASE / "step200_iteration_arc_closeout.tex").read_text()
    for token in ["V\\_arc\\_terminus\\_declared", "Path 1", "Burnol", "Riemann's RH remains open"]:
        if token not in tex:
            fail(f"tex missing token: {token}")

    print("PASS step200 iteration arc closeout checks")
    print("verdict=V_arc_terminus_declared")


if __name__ == "__main__":
    main()

