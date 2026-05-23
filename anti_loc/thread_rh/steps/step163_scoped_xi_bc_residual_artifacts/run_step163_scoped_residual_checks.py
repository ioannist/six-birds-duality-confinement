#!/usr/bin/env python3
"""Validate Step 163 scoped residual artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REQUIRED = [
    "step163_results_summary.md",
    "step163_schema.json",
    "content_classification_step163.csv",
    "nonclaim_boundary_step163.md",
    "step163_scoped_xi_bc_residual.tex",
    "run_step163_scoped_residual_checks.py",
    "bridge_gates_step163.csv",
    "retained_nogos_step163.csv",
    "route_status_step163.csv",
    "residual_tree_step163.csv",
    "construction_tasks_step163.csv",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def read_text(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def assert_presence() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        fail("missing required artifacts: " + ", ".join(missing))


def assert_schema() -> None:
    schema = json.loads(read_text("step163_schema.json"))
    if schema.get("step") != 163:
        fail("schema step must be 163")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if "Xi_BC" not in schema.get("active_residual", ""):
        fail("schema active_residual must contain Xi_BC")
    if schema.get("main_operator") != "C_l P_eta":
        fail("schema main_operator must be C_l P_eta")
    if "scoped_residual_theorem" not in schema.get("final_verdict", ""):
        fail("schema final_verdict must record scoped_residual_theorem")

    gates = schema.get("bridge_gates", {})
    expected = {
        "G1": "framework_defined",
        "G2": "open_external_proof",
        "G3": "open_external_proof",
        "G4": "open_external_proof",
        "G5": "open_external_proof",
    }
    for gate, status in expected.items():
        actual = gates.get(gate, {}).get("status")
        if actual != status:
            fail(f"{gate} status must be {status}, got {actual!r}")

    nogos = " ".join(schema.get("retained_nogos", [])).lower()
    for needed in ["public-shadow non-promotion", "finite-window Calkin blindness"]:
        if needed.lower() not in nogos:
            fail(f"schema retained_nogos missing {needed}")

    next_step = schema.get("next_step", {})
    if next_step.get("step") != 164:
        fail("schema next_step.step must be 164")
    lanes = " ".join(next_step.get("strategic_lanes", [])).lower()
    for needed in ["shifted co-poisson", "alternate burnol/sonine", "g2", "g3", "g4", "g5"]:
        if needed not in lanes:
            fail(f"schema next_step strategic_lanes missing {needed}")


def assert_forbidden_phrases() -> None:
    checked_files = [
        "step163_scoped_xi_bc_residual.tex",
        "step163_results_summary.md",
        "nonclaim_boundary_step163.md",
        "step163_schema.json",
    ]
    corpus = "\n".join(read_text(name) for name in checked_files)

    forbidden = [
        "proves " + "RH",
        "RH " + "proof",
        "essential norm " + "is positive",
        "unconditional " + "Xi_BC=0",
    ]
    for phrase in forbidden:
        if phrase in corpus:
            fail(f"forbidden phrase found: {phrase}")

    compact_phrase = "C_l P_eta " + "is compact"
    if compact_phrase in corpus:
        fail("standalone compactness phrase found")

    gate_patterns = [
        r"\bG[2-5]\b[^.\n]*(?:holds|proved|accepted|closed|verified|established|framework_defined)",
        r"(?:faithful symbol|normal form|lower-faithfulness|compact remainder)[^.\n]*(?:proved|accepted|closed|verified|established)",
    ]
    for pattern in gate_patterns:
        match = re.search(pattern, corpus, flags=re.IGNORECASE)
        if match:
            fail("possible unsupported gate-closure sentence: " + match.group(0))


def assert_csv_content() -> None:
    bridge = read_text("bridge_gates_step163.csv")
    for gate in ["G1", "G2", "G3", "G4", "G5"]:
        if gate not in bridge:
            fail(f"bridge_gates_step163.csv missing {gate}")
    if "framework_defined" not in bridge or bridge.count("open_external_proof") < 4:
        fail("bridge gate statuses incomplete")

    nogos = read_text("retained_nogos_step163.csv").lower()
    if "public-shadow non-promotion" not in nogos:
        fail("retained_nogos missing public-shadow non-promotion")
    if "finite-window calkin blindness" not in nogos:
        fail("retained_nogos missing finite-window Calkin blindness")

    residual_tree = read_text("residual_tree_step163.csv")
    for needed in ["Xi_BC", "Xi_BW", "diagnostic-complete"]:
        if needed not in residual_tree:
            fail(f"residual tree missing {needed}")


def main() -> None:
    assert_presence()
    assert_schema()
    assert_forbidden_phrases()
    assert_csv_content()
    print("Step 163 scoped residual checks passed.")


if __name__ == "__main__":
    main()
