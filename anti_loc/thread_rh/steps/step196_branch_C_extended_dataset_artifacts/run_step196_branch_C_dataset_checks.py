#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts")

REQUIRED = [
    "step196_results_summary.md",
    "step196_schema.json",
    "content_classification_step196.csv",
    "nonclaim_boundary_step196.md",
    "step196_branch_C_extended_dataset.tex",
    "compute_branch_C_dataset_step196.py",
    "compute_branch_C_dataset_output_step196.txt",
    "run_step196_branch_C_dataset_checks.py",
    "dataset_triples_step196.csv",
    "new_G_generators_step196.csv",
    "structural_patterns_step196.csv",
    "residual_tree_step196.csv",
    "route_status_step196.csv",
    "construction_tasks_step196.csv",
]

VALID_VERDICTS = {
    "V_branch_C_dataset_generic_foreclosure",
    "V_branch_C_dataset_subclass_pattern",
    "V_branch_C_dataset_structural_law",
    "V_branch_C_dataset_partial",
}

FORBIDDEN = [
    "proves RH",
    "proved RH",
    "disproves RH",
    "closes Xi_BC",
    "jet-surjectivity proved",
]


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step196_schema.json").read_text())
    if schema.get("step") != 196:
        fail("schema step must be 196")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("target") != "extended Branch C L_{rho,k}(G) dataset":
        fail("schema target mismatch")
    verdict = schema.get("branch_C_dataset_verdict")
    if verdict not in VALID_VERDICTS:
        fail(f"invalid branch_C_dataset_verdict: {verdict}")
    if schema.get("final_verdict") != verdict:
        fail("final_verdict must equal branch_C_dataset_verdict")
    triples = schema.get("dataset_triples", [])
    if schema.get("dataset_size") != len(triples):
        fail("dataset_size does not match dataset_triples length")
    if len(triples) < 10:
        fail("dataset must contain at least 10 triples")
    if len({t["G_id"] for t in triples}) < 3:
        fail("dataset must contain at least 3 generators")
    if len({t["rho_index"] for t in triples}) < 5:
        fail("dataset must contain at least 5 zeta zeros")
    if 1 not in {t["k"] for t in triples}:
        fail("dataset must include k=1 diagnostics")
    if verdict == "V_branch_C_dataset_generic_foreclosure":
        nonpositive = [t["case_id"] for t in triples if float(t["L_abs"]) <= float(t["error_bound"])]
        if nonpositive:
            fail(f"generic foreclosure requires positive lower bounds: {nonpositive}")

    with (BASE / "dataset_triples_step196.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != len(triples):
        fail("dataset CSV row count mismatch")

    generator_text = (BASE / "new_G_generators_step196.csv").read_text()
    for required_gen in ["G_spread", "G_low", "G_high"]:
        if required_gen not in generator_text:
            fail(f"missing new generator {required_gen}")

    tex = (BASE / "step196_branch_C_extended_dataset.tex").read_text()
    if "V\\_branch\\_C\\_dataset\\_generic\\_foreclosure" not in tex:
        fail("tex missing verdict statement")
    if "min(|L|-\\mathrm{error})" not in tex:
        fail("tex missing certified lower-bound expression")

    combined = "\n".join((BASE / name).read_text(errors="ignore") for name in REQUIRED if name.endswith((".md", ".tex", ".json", ".csv")))
    for phrase in FORBIDDEN:
        if phrase in combined:
            fail(f"forbidden phrase found: {phrase}")

    print("PASS step196 Branch C dataset checks")
    print(f"dataset_size={len(triples)} verdict={verdict}")


if __name__ == "__main__":
    main()
