#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step182_hilbert_polya_pivot_artifacts")

REQUIRED = [
    "step182_results_summary.md",
    "step182_schema.json",
    "content_classification_step182.csv",
    "nonclaim_boundary_step182.md",
    "step182_hilbert_polya_pivot.tex",
    "run_step182_HP_checks.py",
    "HP_declaration_step182.csv",
    "no_go_transfer_step182.csv",
    "cascade_initial_branches_step182.csv",
    "residual_tree_step182.csv",
    "route_status_step182.csv",
    "construction_tasks_step182.csv",
    "classical_theorems_cited_step182.csv",
    "meta_pattern_status_step182.csv",
]

ALLOWED_VERDICTS = {
    "V_HP_substantively_new",
    "V_HP_CTMT_instance",
    "V_HP_target_equivalent",
    "V_HP_bridge_failure",
    "V_HP_partial",
    "V_HP_meta_pattern_confirmed",
}


def fail(msg: str) -> None:
    print(f"FAIL step182 HP checks: {msg}", file=sys.stderr)
    sys.exit(1)


def text(name: str) -> str:
    try:
        return (ROOT / name).read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"could not read {name}: {exc}")


def rows(name: str):
    try:
        with (ROOT / name).open(newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    except Exception as exc:
        fail(f"could not parse {name}: {exc}")


def main() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        fail("missing artifacts: " + ", ".join(missing))

    try:
        schema = json.loads(text("step182_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"invalid schema JSON: {exc}")

    if schema.get("step") != 182:
        fail("schema step must be 182")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("primary_carrier") != "Hilbert-Polya / Berry-Keating H_xp on L²(ℝ_+)":
        fail("primary_carrier mismatch")

    verdict = schema.get("HP_verdict")
    if verdict not in ALLOWED_VERDICTS:
        fail(f"HP_verdict not allowed: {verdict}")
    if schema.get("final_verdict") != verdict:
        fail("final_verdict must equal HP_verdict")
    if verdict != "V_HP_meta_pattern_confirmed":
        fail("this dispatch must record V_HP_meta_pattern_confirmed")

    carrier = schema.get("carrier_definition", {})
    operator = schema.get("operator_definition", {})
    extensions = schema.get("self_adjoint_extension_family", {})
    residual = schema.get("parent_residual_on_HP", {})
    if carrier.get("chosen_space") != "H_HP = L^2(R_+, dx)":
        fail("carrier_definition.chosen_space mismatch")
    if "U H_xp U^{-1}" not in operator.get("log_model", ""):
        fail("operator log_model missing unitary equivalence")
    if "continuous spectrum" not in residual.get("standard_xp_status", ""):
        fail("parent residual must record standard xp bridge failure")
    if "deficiency indices (0,0)" not in extensions.get("full_half_line", ""):
        fail("full half-line extension audit must record deficiency indices (0,0)")
    if "arithmetic" not in extensions.get("finite_log_interval_variant", ""):
        fail("finite log interval extension audit must record arithmetic spectrum")

    new_nogo = "Hilbert-Polya/Berry-Keating standard xp bridge failure and modified-operator target-equivalence"
    retained = schema.get("retained_nogos", [])
    if new_nogo not in retained:
        fail("new HP no-go missing from retained_nogos")
    if len(retained) < 9:
        fail("retained_nogos must contain at least 9 entries")
    if schema.get("new_no_gos_count") != 1:
        fail("new_no_gos_count must be 1")
    if schema.get("meta_pattern_status") != "meta_pattern_confirmed":
        fail("meta_pattern_status must be meta_pattern_confirmed")

    branches = {row.get("branch") for row in schema.get("cascade_initial_branches", [])}
    for expected in {"HP-spectrum", "HP-extension", "HP-modification", "HP-ledger"}:
        if expected not in branches:
            fail(f"missing schema branch {expected}")

    cited = " ".join(row.get("source", "") for row in schema.get("classical_theorems_cited", []))
    for expected in ["Berry", "Keating", "Connes", "Spectral theorem", "von Neumann"]:
        if expected not in cited:
            fail(f"classical theorem citation missing {expected}")

    for csv_name in [
        "HP_declaration_step182.csv",
        "no_go_transfer_step182.csv",
        "cascade_initial_branches_step182.csv",
        "residual_tree_step182.csv",
        "route_status_step182.csv",
        "construction_tasks_step182.csv",
        "classical_theorems_cited_step182.csv",
        "meta_pattern_status_step182.csv",
    ]:
        if not rows(csv_name):
            fail(f"{csv_name} has no data rows")

    no_go_rows = rows("no_go_transfer_step182.csv")
    if not any(row.get("no_go") == new_nogo and row.get("transfer_status") == "new" for row in no_go_rows):
        fail("no_go_transfer_step182.csv must record new HP no-go")

    meta_rows = rows("meta_pattern_status_step182.csv")
    if not any(row.get("status") == "meta_pattern_confirmed" for row in meta_rows):
        fail("meta_pattern_status_step182.csv must record meta_pattern_confirmed")

    tex = text("step182_hilbert_polya_pivot.tex")
    required_snippets = [
        "V_{\\mathrm{HP\\_meta\\_pattern\\_confirmed}}",
        "H_{xp}",
        "-i\\frac{d}{dt}",
        "purely absolutely continuous spectrum",
        "deficiency indices",
        "arithmetic progressions",
        "target-equivalence",
        "meta\\_pattern\\_status",
    ]
    for snippet in required_snippets:
        if snippet not in tex:
            fail(f"TeX missing snippet: {snippet}")

    combined = "\n".join(
        text(name)
        for name in [
            "step182_results_summary.md",
            "nonclaim_boundary_step182.md",
            "step182_hilbert_polya_pivot.tex",
        ]
    )
    forbidden = [
        r"\bthis is an RH proof\b",
        r"\bwe assume RH\b",
        r"\bassume the Riemann Hypothesis\b",
        r"\btherefore proves RH\b",
        r"\bconstructs a Hilbert-Polya operator\b",
        r"\bcloses Xi_HP\b",
    ]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")

    print("PASS step182 HP checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"HP_verdict={verdict}")
    print(f"new_no_gos_count={schema.get('new_no_gos_count')}")
    print(f"meta_pattern_status={schema.get('meta_pattern_status')}")


if __name__ == "__main__":
    main()
