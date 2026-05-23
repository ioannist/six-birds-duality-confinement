#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step193_beurling_nyman_pivot_artifacts")

REQUIRED = [
    "step193_results_summary.md",
    "step193_schema.json",
    "content_classification_step193.csv",
    "nonclaim_boundary_step193.md",
    "step193_beurling_nyman_pivot.tex",
    "run_step193_BN_checks.py",
    "BN_declaration_step193.csv",
    "CRE_audit_step193.csv",
    "CRCFT_mode_audit_step193.csv",
    "gram_matrix_structure_step193.csv",
    "cascade_initial_branches_step193.csv",
    "residual_tree_step193.csv",
    "route_status_step193.csv",
    "construction_tasks_step193.csv",
    "classical_theorems_cited_step193.csv",
]

VALID = {
    "V_BN_CRCFT_CTMT",
    "V_BN_CRCFT_TE",
    "V_BN_CRCFT_BF",
    "V_BN_substantively_new",
    "V_BN_partial",
}

def fail(msg: str) -> None:
    print(f"FAIL step193 BN checks: {msg}", file=sys.stderr)
    sys.exit(1)

def rows(name: str):
    with (BASE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).is_file()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step193_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "primary_carrier",
        "carrier_definition",
        "muntz_subspace",
        "native_probes",
        "parent_residual_on_BN",
        "CRE_status",
        "CRCFT_mode_classification",
        "BN_verdict",
        "classical_theorems_cited",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 193:
        fail("step must be 193")
    if schema["orientation"] != "adequacy":
        fail("orientation must be adequacy")
    if schema["CRE_status"] != "CRE":
        fail("CRE_status must be CRE")
    verdict = schema["BN_verdict"]
    if verdict not in VALID:
        fail(f"invalid BN verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal BN_verdict")
    if verdict == "V_BN_CRCFT_TE" and schema["CRCFT_mode_classification"].get("mode") != "CRCFT-TE":
        fail("TE verdict must have CRCFT-TE mode")

    tex = (BASE / "step193_beurling_nyman_pivot.tex").read_text(encoding="utf-8")
    for snippet in [
        "V\\_BN\\_CRCFT\\_TE",
        "\\HBN=L^2(0,1)",
        "\\rho_a(t)",
        "\\XiBN=(I-P_{\\MBN})\\one",
        "G_A(i,j)",
        "a_i\\log(1/a_i)",
        "\\CRCFT\\text{-TE}",
    ]:
        if snippet not in tex:
            fail(f"TeX missing snippet: {snippet}")

    gram = rows("gram_matrix_structure_step193.csv")
    if not any(row.get("object") == "finite_distance" for row in gram):
        fail("Gram CSV missing finite_distance row")
    cre = rows("CRE_audit_step193.csv")
    if not any(row.get("result") == "CRE" for row in cre):
        fail("CRE audit must record CRE")
    mode = rows("CRCFT_mode_audit_step193.csv")
    if not any(row.get("mode") == "CRCFT-TE" and row.get("selected") == "yes" for row in mode):
        fail("CRCFT audit must select TE")

    citations = rows("classical_theorems_cited_step193.csv")
    cite_text = " ".join(row.get("source", "") for row in citations)
    for token in ["Beurling", "Nyman", "Bae z-Duarte"]:
        if token not in cite_text:
            fail(f"citation missing {token}")

    combined = "\n".join(
        (BASE / name).read_text(encoding="utf-8", errors="ignore")
        for name in REQUIRED
        if name != "run_step193_BN_checks.py"
        and (BASE / name).suffix in {".md", ".tex", ".json", ".csv"}
    )
    forbidden = [
        "this step proves RH",
        "we prove RH",
        "Xi_BN is closed",
        "finite computations prove the limit",
        "weakens any retained no-go",
    ]
    for phrase in forbidden:
        if phrase.lower() in combined.lower():
            fail(f"forbidden phrase found: {phrase}")

    print("PASS step193_BN_checks: Beurling-Nyman carrier artifacts validated")
    print(f"BN_verdict={verdict}")
    print(f"CRCFT_mode={schema['CRCFT_mode_classification']['mode']}")

if __name__ == "__main__":
    main()

