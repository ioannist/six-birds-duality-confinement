#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step237_CRCFT_modes_5_track_formalization_artifacts")

REQUIRED = [
    "step237_results_summary.md",
    "step237_schema.json",
    "content_classification_step237.csv",
    "nonclaim_boundary_step237.md",
    "step237_CRCFT_modes_5_track_formalization.tex",
    "run_step237_checks.py",
    "instance_table_step237.csv",
    "adaptation_step237.csv",
    "corpus_inclusion_step237.csv",
    "residual_tree_step237.csv",
    "route_status_step237.csv",
    "construction_tasks_step237.csv",
    "classical_theorems_cited_step237.csv",
]


def read_csv(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ROOT / "step237_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 237
    assert schema["orientation"] == "synthesis-case-3"
    assert schema["target"] == "CRCFT modes formalization as 5-track verified foundational typed condition"
    assert schema["final_verdict"] == "V_CRCFT_modes_formalized_5_track"
    assert schema["theorem_statement"]["verification_status"] == "verified-on-5-track-instances"
    assert len(schema["theorem_statement"]["modes"]) == 3
    assert {m["mode"] for m in schema["theorem_statement"]["modes"]} == {"TE", "CTMT", "BF"}
    assert len(schema["instance_table"]) == 5

    instance_rows = read_csv("instance_table_step237.csv")
    assert len(instance_rows) == 5
    assert {row["track"] for row in instance_rows} == {"RH", "BSD", "Hodge", "NS", "P-vs-NP"}

    adaptation_rows = read_csv("adaptation_step237.csv")
    assert len(adaptation_rows) == 5

    corpus_rows = read_csv("corpus_inclusion_step237.csv")
    assert any("corpus-pending" in row["status"] for row in corpus_rows)

    summary = (ROOT / "step237_results_summary.md").read_text(encoding="utf-8")
    tex = (ROOT / "step237_CRCFT_modes_5_track_formalization.tex").read_text(encoding="utf-8")
    nonclaim = (ROOT / "nonclaim_boundary_step237.md").read_text(encoding="utf-8")
    for token in ["TE", "CTMT", "BF", "verified-on-5-track-instances"]:
        assert token in summary
        assert token in tex
    assert "does not claim" in nonclaim

    print("step237 checks passed: all required artifacts present, schema valid, 5-track CRCFT formalization recorded.")


if __name__ == "__main__":
    main()
