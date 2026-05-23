#!/usr/bin/env python3
"""Validate Step 167 Hecke carrier pivot artifacts."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step167_hecke_carrier_pivot_artifacts")

REQUIRED = [
    "step167_results_summary.md",
    "step167_schema.json",
    "content_classification_step167.csv",
    "nonclaim_boundary_step167.md",
    "step167_hecke_carrier_pivot.tex",
    "run_step167_hecke_pivot_checks.py",
    "hecke_carrier_declaration_step167.csv",
    "bridge_to_Xi_BC_step167.csv",
    "no_go_transfer_step167.csv",
    "source_audit_step167.csv",
    "initial_branches_step167.csv",
    "residual_tree_step167.csv",
    "route_status_step167.csv",
    "construction_tasks_step167.csv",
]

FORBIDDEN_PHRASES = [
    "proves RH",
    "RH proof",
    "essential norm is positive",
    "C_l P_eta is compact",
    "unconditional Xi_BC=0",
]

FORBIDDEN_PATTERNS = [
    re.compile(r"\bbranch\s+a\b.{0,60}\b(is|was|has been|becomes)\s+closed\b", re.I | re.S),
    re.compile(r"\bbranch\s+b\b.{0,60}\b(is|was|has been|becomes)\s+closed\b", re.I | re.S),
    re.compile(r"\bbranch\s+c\b.{0,60}\b(is|was|has been|becomes)\s+closed\b", re.I | re.S),
    re.compile(r"\bclosed\s+branch\s+[abc]\b", re.I),
    re.compile(r"\bhecke[- ]side branch\b.{0,60}\b(is|was|has been|becomes)\s+closed\b", re.I | re.S),
    re.compile(r"\bpublic[- ]shadow evidence promotes\b", re.I),
    re.compile(r"\bfinite[- ]window evidence promotes\b", re.I),
    re.compile(r"\bpromotes\s+(public[- ]shadow|finite[- ]window)\s+evidence\b", re.I),
]


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR: {error}")
    return 1


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_csv_nonempty(path: Path, errors: list[str]) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if len(rows) < 2:
        errors.append(f"{path.name} must have a header and at least one data row")
    if not rows or not all(cell.strip() for cell in rows[0]):
        errors.append(f"{path.name} has an empty CSV header cell")


def main() -> int:
    errors: list[str] = []

    if not BASE.is_dir():
        return fail([f"missing artifact directory: {BASE}"])

    for name in REQUIRED:
        path = BASE / name
        if not path.is_file():
            errors.append(f"missing required artifact: {path}")
        elif path.stat().st_size == 0:
            errors.append(f"empty required artifact: {path}")

    if errors:
        return fail(errors)

    schema_path = BASE / "step167_schema.json"
    try:
        schema = json.loads(read_text(schema_path))
    except json.JSONDecodeError as exc:
        return fail([f"invalid JSON in {schema_path}: {exc}"])

    expected_pairs = {
        "step": 167,
        "orientation": "adequacy",
        "primary_carrier": "Hecke L-functions over algebraic number field K with character class chi",
        "inherited_carrier": "Burnol/Sonine pulled-evaluator carrier (carried forward, not modified)",
        "inherited_residual": "Xi_BC",
        "new_residual": "Xi_BC_Hecke",
        "pivot_verdict": "hecke_carrier_pivot_partial",
        "final_verdict": "hecke_carrier_pivot_partial",
        "next_step": 168,
    }
    for key, expected in expected_pairs.items():
        if schema.get(key) != expected:
            errors.append(f"schema field {key!r} expected {expected!r}, found {schema.get(key)!r}")

    if schema.get("pivot_verdict") not in {
        "hecke_carrier_pivot_established",
        "hecke_carrier_pivot_blocked",
        "hecke_carrier_pivot_partial",
    }:
        errors.append("pivot_verdict is not in the allowed enum")

    bridge = schema.get("bridge_to_Xi_BC", {})
    if bridge.get("status") not in {"framework_defined", "open_external_bridge", "typed_obligation"}:
        errors.append("bridge_to_Xi_BC.status has an unexpected value")

    no_go = schema.get("no_go_transfer", {})
    for key in ["public_shadow_non_promotion", "finite_window_calkin_blindness"]:
        item = no_go.get(key, {})
        if item.get("transfers") is not True:
            errors.append(f"no_go_transfer.{key}.transfers must be true")

    retained = set(schema.get("retained_nogos", []))
    for required in ["public-shadow non-promotion", "finite-window Calkin blindness"]:
        if required not in retained:
            errors.append(f"retained_nogos missing {required!r}")

    if not schema.get("source_audit"):
        errors.append("source_audit must be nonempty")
    if not schema.get("initial_branches"):
        errors.append("initial_branches must be nonempty")
    if len(schema.get("strategic_lanes", [])) < 3:
        errors.append("strategic_lanes should include multiple step 168 candidates")

    for path in BASE.glob("*.csv"):
        check_csv_nonempty(path, errors)

    for path in BASE.iterdir():
        if path.name == "run_step167_hecke_pivot_checks.py" or not path.is_file():
            continue
        text = read_text(path)
        lower = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lower:
                errors.append(f"forbidden phrase {phrase!r} found in {path.name}")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"forbidden closure/promotion pattern {pattern.pattern!r} found in {path.name}")

    if errors:
        return fail(errors)

    print("Step 167 Hecke pivot checks passed: all required artifacts present, schema valid, no forbidden claims detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
