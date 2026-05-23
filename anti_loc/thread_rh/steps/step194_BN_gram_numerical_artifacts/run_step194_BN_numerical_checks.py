#!/usr/bin/env python3
import csv
import json
import subprocess
import sys
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step194_BN_gram_numerical_artifacts")

REQUIRED = [
    "step194_results_summary.md",
    "step194_schema.json",
    "content_classification_step194.csv",
    "nonclaim_boundary_step194.md",
    "step194_BN_gram_numerical.tex",
    "compute_BN_gram_step194.py",
    "compute_BN_gram_output_step194.txt",
    "run_step194_BN_numerical_checks.py",
    "BN_gram_a_sets_step194.csv",
    "BN_gram_results_step194.csv",
    "decay_analysis_step194.csv",
    "residual_tree_step194.csv",
    "route_status_step194.csv",
    "construction_tasks_step194.csv",
]

VALID = {
    "V_BN_numerical_decay_consistent_with_RH",
    "V_BN_numerical_bounded_away",
    "V_BN_numerical_indeterminate",
    "V_BN_numerical_structural_pattern",
}

def fail(msg: str) -> None:
    print(f"FAIL step194 BN numerical checks: {msg}", file=sys.stderr)
    sys.exit(1)

def rows(name: str):
    with (BASE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).is_file()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step194_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "a_set_families",
        "gram_matrix_method",
        "numerical_results",
        "BN_numerical_verdict",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 194:
        fail("schema step must be 194")
    if schema["orientation"] != "adequacy":
        fail("orientation must be adequacy")
    verdict = schema["BN_numerical_verdict"]
    if verdict not in VALID:
        fail(f"invalid verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal BN_numerical_verdict")
    if len(schema["a_set_families"]) < 3:
        fail("must test at least three a-set families")

    result_rows = rows("BN_gram_results_step194.csv")
    families = {row["family"] for row in result_rows}
    if len(families) < 3:
        fail("results CSV must contain at least three families")
    if not any(row["family"] == "harmonic" and row["N"] == "80" for row in result_rows):
        fail("harmonic N=80 result missing")
    harmonic80 = next(float(row["delta_sq"]) for row in result_rows if row["family"] == "harmonic" and row["N"] == "80")
    if not (0 < harmonic80 < 0.02):
        fail("unexpected harmonic N=80 delta")

    decay_rows = rows("decay_analysis_step194.csv")
    if not any(row["family"] == "harmonic" and row["pattern"] == "slow_log_decay" for row in decay_rows):
        fail("decay analysis must record harmonic slow_log_decay")
    if not any(row["pattern"] == "plateau" for row in decay_rows):
        fail("decay analysis must record at least one plateau")

    tex = (BASE / "step194_BN_gram_numerical.tex").read_text(encoding="utf-8")
    for snippet in [
        "V\\_BN\\_numerical\\_structural\\_pattern",
        "X_{\\max}=200000",
        "\\delta_A^2",
        "0.010992095538",
        "0.127035826960",
        "0.207292597760",
    ]:
        if snippet not in tex:
            fail(f"TeX missing required snippet: {snippet}")

    # Re-run the script and verify the output file is refreshed and contains the key line.
    subprocess.run(["python3", str(BASE / "compute_BN_gram_step194.py")], cwd=str(BASE), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = (BASE / "compute_BN_gram_output_step194.txt").read_text(encoding="utf-8")
    if "harmonic,N=80,delta_sq=0.0109920955378" not in output:
        fail("compute output missing harmonic N=80 line")

    combined = "\n".join(
        (BASE / name).read_text(encoding="utf-8", errors="ignore")
        for name in REQUIRED
        if name != "run_step194_BN_numerical_checks.py"
        and (BASE / name).suffix in {".md", ".tex", ".json", ".csv", ".txt", ".py"}
    )
    forbidden = [
        "this proves RH",
        "we prove RH",
        "Xi_BN is closed",
        "finite-window proof of RH",
        "weakens any retained no-go",
    ]
    for phrase in forbidden:
        if phrase.lower() in combined.lower():
            fail(f"forbidden phrase found: {phrase}")

    print("PASS step194_BN_numerical_checks: BN Gram numerical artifacts validated")
    print(f"BN_numerical_verdict={verdict}")
    print(f"harmonic_N80_delta_sq={harmonic80:.12g}")

if __name__ == "__main__":
    main()

