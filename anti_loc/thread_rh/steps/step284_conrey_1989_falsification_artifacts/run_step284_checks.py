#!/usr/bin/env python3
"""Validate Step 284 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step284_conrey_1989_falsification_artifacts")
FINDINGS = Path("/home/repos/six-birds-foundations-iii/anti_loc/findings_framework.md")


REQUIRED = [
    "step284_results_summary.md",
    "step284_schema.json",
    "content_classification_step284.csv",
    "nonclaim_boundary_step284.md",
    "step284_conrey_1989.tex",
    "conrey_paper_extract_step284.md",
    "derive_conrey_obstruction_step284.py",
    "run_step284_checks.py",
    "conrey_verbatim_step284.csv",
    "method_cap_step284.csv",
    "cascade_need_vs_supplied_step284.csv",
    "eight_of_eight_or_falsification_step284.csv",
    "residual_tree_step284.csv",
    "route_status_step284.csv",
    "construction_tasks_step284.csv",
    "classical_theorems_cited_step284.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step284_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 284
    assert schema["orientation"] == "falsification_attempt"
    assert schema["final_verdict"] == "V_conrey_RH_bridge_blocked"
    assert schema["falsification_outcome"] == "no falsification; Conrey does not derive RH"

    verbatim = "\n".join(row["verbatim"] for row in read_csv("conrey_verbatim_step284.csv"))
    for needle in ["2/5", "mollifier", "41.05%", "limitations"]:
        assert needle in verbatim, f"missing Conrey/BCY token: {needle}"

    method_cap = read_csv("method_cap_step284.csv")
    assert any("49" in row["bound_or_limit"] for row in method_cap)
    assert any(row["audit_status"] == "not_a_100_percent_path" for row in method_cap)

    comparison = read_csv("cascade_need_vs_supplied_step284.csv")
    assert any(row["status"] == "not_derivable" for row in comparison)
    assert any("100%" in row["cascade_need"] for row in comparison)

    pattern = read_csv("eight_of_eight_or_falsification_step284.csv")
    assert len(pattern) == 8
    assert all(row["audited_score"] == "1" for row in pattern)
    assert pattern[-1]["outcome"] == "downgrade_not_falsification"

    findings = FINDINGS.read_text(encoding="utf-8")
    assert "steps 267-284" in findings
    assert "Conrey 1989" in findings
    assert "8-of-8" in findings

    print("Step 284 checks passed")


if __name__ == "__main__":
    main()
