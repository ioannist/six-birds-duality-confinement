#!/usr/bin/env python3
import csv
import json
import subprocess
import sys
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step195_BN_arithmetic_refinement_artifacts")

REQUIRED = [
    "step195_results_summary.md",
    "step195_schema.json",
    "content_classification_step195.csv",
    "nonclaim_boundary_step195.md",
    "step195_BN_arithmetic_refinement.tex",
    "compute_BN_arithmetic_step195.py",
    "compute_BN_arithmetic_output_step195.txt",
    "run_step195_BN_refinement_checks.py",
    "arithmetic_gram_formula_step195.csv",
    "computed_data_step195.csv",
    "decay_fit_step195.csv",
    "residual_tree_step195.csv",
    "route_status_step195.csv",
    "construction_tasks_step195.csv",
]

VALID = {
    "V_BN_arithmetic_refined_RH_consistent",
    "V_BN_arithmetic_inconsistent",
    "V_BN_arithmetic_truncation_dominant",
    "V_BN_arithmetic_partial",
}

def fail(msg: str) -> None:
    print(f"FAIL step195 BN refinement checks: {msg}", file=sys.stderr)
    sys.exit(1)

def rows(name: str):
    with (BASE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).is_file()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step195_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "arithmetic_gram_formula",
        "mpmath_precision",
        "computed_data",
        "decay_fit",
        "BN_refinement_verdict",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 195:
        fail("schema step must be 195")
    if schema["orientation"] != "adequacy":
        fail("orientation must be adequacy")
    verdict = schema["BN_refinement_verdict"]
    if verdict not in VALID:
        fail(f"invalid verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal BN_refinement_verdict")
    if schema["mpmath_precision"].get("mpmath_dps", 0) < 50:
        fail("mpmath precision must be at least 50 dps")

    data = rows("computed_data_step195.csv")
    for n in ["200", "500", "1000"]:
        if not any(row["N"] == n for row in data):
            fail(f"computed data missing N={n}")
    d1000 = next(float(row["delta_sq"]) for row in data if row["N"] == "1000")
    if not (0.005 < d1000 < 0.008):
        fail("unexpected N=1000 delta")
    fit = rows("decay_fit_step195.csv")
    if not any(row["model"] == "C_over_logN" for row in fit):
        fail("decay fit missing C_over_logN")
    formula = rows("arithmetic_gram_formula_step195.csv")
    if not any(row.get("formula_id") == "periodized_digamma" for row in formula):
        fail("formula CSV missing periodized_digamma")

    tex = (BASE / "step195_BN_arithmetic_refinement.tex").read_text(encoding="utf-8")
    for snippet in [
        "V\\_BN\\_arithmetic\\_refined\\_RH\\_consistent",
        "G_{p,q}",
        "\\operatorname{lcm}",
        "0.00654423096394308",
        "0.0466828337786475",
        "\\alpha=1.0886679",
    ]:
        if snippet not in tex:
            fail(f"TeX missing snippet: {snippet}")

    subprocess.run(["python3", str(BASE / "compute_BN_arithmetic_step195.py")], cwd=str(BASE), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = (BASE / "compute_BN_arithmetic_output_step195.txt").read_text(encoding="utf-8")
    if "N=1000,delta_sq=0.00654423096394" not in output:
        fail("compute output missing N=1000 line")

    combined = "\n".join(
        (BASE / name).read_text(encoding="utf-8", errors="ignore")
        for name in REQUIRED
        if name != "run_step195_BN_refinement_checks.py"
        and (BASE / name).suffix in {".md", ".tex", ".json", ".csv", ".txt", ".py"}
    )
    forbidden = [
        "this proves RH",
        "we prove RH",
        "BN residual is closed",
        "delta_A^2 -> 0 proved",
        "weakens any retained no-go",
    ]
    for phrase in forbidden:
        if phrase.lower() in combined.lower():
            fail(f"forbidden phrase found: {phrase}")

    print("PASS step195_BN_refinement_checks: BN arithmetic refinement artifacts validated")
    print(f"BN_refinement_verdict={verdict}")
    print(f"N1000_delta_sq={d1000:.12g}")

if __name__ == "__main__":
    main()

