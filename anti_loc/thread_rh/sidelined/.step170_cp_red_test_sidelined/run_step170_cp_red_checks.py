#!/usr/bin/env python3
"""Validation checks for Step 170 CP-RED test-generator artifacts."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step170_cp_red_test_generators_artifacts/")

REQUIRED = [
    "step170_results_summary.md",
    "step170_schema.json",
    "content_classification_step170.csv",
    "nonclaim_boundary_step170.md",
    "step170_cp_red_test.tex",
    "run_step170_cp_red_checks.py",
    "test_generators_step170.csv",
    "per_generator_computation_step170.csv",
    "verdict_step170.csv",
    "branch_C_status_step170.csv",
    "residual_tree_step170.csv",
    "route_status_step170.csv",
    "construction_tasks_step170.csv",
]

FORBIDDEN = [
    "proves " + "RH",
    "RH " + "proof",
    "essential norm is " + "positive",
    "unconditional Xi_BC" + "=0",
    "split_" + "external_" + "theorem",
    "external work " + "needed",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    if not OUT.exists():
        fail(f"artifact directory missing: {OUT}")

    missing = [name for name in REQUIRED if not (OUT / name).exists()]
    if missing:
        fail(f"missing required artifacts: {missing}")

    for path in OUT.iterdir():
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".csv", ".tex", ".py"}:
            text = path.read_text(errors="replace")
            for phrase in FORBIDDEN:
                if phrase in text:
                    fail(f"forbidden phrase {phrase!r} found in {path.name}")

    schema = json.loads((OUT / "step170_schema.json").read_text())
    required_schema_fields = [
        "step",
        "orientation",
        "active_residual",
        "main_object",
        "inherited_records",
        "test_generators",
        "per_generator_computation",
        "factorization_verdict",
        "retained_nogos",
        "branch_C_status_update",
        "final_verdict",
        "next_step",
    ]
    for field in required_schema_fields:
        if field not in schema:
            fail(f"schema missing field: {field}")

    if schema["step"] != 170:
        fail("schema step must be 170")
    if schema["orientation"] != "adequacy":
        fail("schema orientation must be adequacy")
    if schema["factorization_verdict"] != schema["final_verdict"]:
        fail("final verdict must equal factorization verdict")
    if schema["factorization_verdict"] not in {
        "V_CPRED_POS",
        "V_CPRED_NEG",
        "V_CPRED_PART",
        "V_CPRED_STUCK",
    }:
        fail("schema factorization verdict is not an allowed Step 170 verdict")

    computations = schema.get("per_generator_computation", [])
    if not computations:
        fail("per_generator_computation must contain at least one entry")
    nontrivial = False
    for row in computations:
        packet = str(row.get("transported_packet", "")).strip()
        comparison = str(row.get("comparison", "")).strip()
        if (
            packet
            and comparison
            and packet.upper() != "TBD"
            and comparison.upper() != "TBD"
            and "T_" in packet
            and "mathsf P_infty" in packet
            and "zeta" in comparison
        ):
            nontrivial = True
    if not nontrivial:
        fail("no non-trivial transported_packet/comparison entry found")

    gen_rows = read_csv_rows(OUT / "test_generators_step170.csv")
    if not gen_rows:
        fail("test_generators_step170.csv has no rows")
    for row in gen_rows:
        if "TBD" in row.get("formula", "").upper():
            fail("generator formula is TBD")
        for key in ("moment_ghat_0", "moment_ghat_1"):
            try:
                value = abs(float(row[key]))
            except Exception as exc:
                fail(f"bad numeric {key}: {exc}")
            if value > 1e-8:
                fail(f"{key} too large for legal moment check: {value}")

    per_rows = read_csv_rows(OUT / "per_generator_computation_step170.csv")
    if not per_rows:
        fail("per_generator_computation_step170.csv has no rows")
    for row in per_rows:
        if not row.get("transported_packet_symbolic_form", "").strip():
            fail("empty transported packet in per-generator CSV")
        if not row.get("comparison", "").strip():
            fail("empty comparison in per-generator CSV")

    class_rows = read_csv_rows(OUT / "content_classification_step170.csv")
    if not class_rows:
        fail("content classification CSV has no rows")
    diagnostic_rows = [
        r
        for r in class_rows
        if r.get("grade") in {"theorem-grade", "finite-carrier diagnostic"}
    ]
    if not diagnostic_rows:
        fail("no theorem-grade or finite-carrier diagnostic rows in classification")
    for row in diagnostic_rows:
        if not row.get("actual_computation_rows", "").strip():
            fail(f"classification diagnostic row lacks computation pointer: {row}")
        if row.get("status", "").lower().startswith("declared"):
            fail(f"classification row is only declared: {row}")

    print(
        json.dumps(
            {
                "status": "ok",
                "required_artifacts": len(REQUIRED),
                "schema_verdict": schema["factorization_verdict"],
                "generators": len(gen_rows),
                "per_generator_computations": len(per_rows),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
