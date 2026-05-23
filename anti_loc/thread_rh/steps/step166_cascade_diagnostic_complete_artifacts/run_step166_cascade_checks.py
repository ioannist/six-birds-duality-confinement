#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step166_cascade_diagnostic_complete_artifacts")

REQUIRED = [
    "step166_results_summary.md",
    "step166_schema.json",
    "content_classification_step166.csv",
    "nonclaim_boundary_step166.md",
    "step166_cascade_diagnostic_complete.tex",
    "run_step166_cascade_checks.py",
    "cascade_branches_step166.csv",
    "external_content_interface_step166.csv",
    "residual_tree_step166.csv",
    "retained_nogos_step166.csv",
    "route_status_step166.csv",
    "construction_tasks_step166.csv",
]

TEXT_TARGETS = [
    "step166_results_summary.md",
    "step166_schema.json",
    "nonclaim_boundary_step166.md",
    "step166_cascade_diagnostic_complete.tex",
]

BRANCH_KEYS = {
    "A_Calkin_bridge_G2_G5",
    "B_per_zero_finite_carrier_SL164_1",
    "C_shifted_co_Poisson_H1_H5",
}

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

def assert_presence() -> None:
    if not BASE.exists():
        fail(f"missing artifact directory: {BASE}")
    missing = [name for name in REQUIRED if not (BASE / name).is_file()]
    if missing:
        fail(f"missing artifacts: {missing}")

def assert_schema() -> None:
    path = BASE / "step166_schema.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("step") != 166:
        fail("schema step must be 166")
    if data.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if "Xi_BC" not in data.get("active_residual", ""):
        fail("schema active_residual must contain Xi_BC")
    if data.get("main_operator") != "C_l P_eta":
        fail("schema main_operator must be C_l P_eta")
    if data.get("final_verdict") != "cascade_diagnostic_complete":
        fail("schema final_verdict mismatch")
    if data.get("cascade_diagnostic_complete") is not True:
        fail("schema cascade_diagnostic_complete must be true")
    branches = data.get("open_branches")
    if not isinstance(branches, dict):
        fail("schema open_branches must be an object")
    if set(branches.keys()) != BRANCH_KEYS:
        fail(f"schema open_branches keys mismatch: {set(branches.keys())}")
    for key, branch in branches.items():
        for field in ("typed_context", "sub_obligations", "status", "source_step"):
            if field not in branch:
                fail(f"branch {key} missing {field}")
        if not branch["typed_context"]:
            fail(f"branch {key} typed_context is empty")
        if not branch["sub_obligations"]:
            fail(f"branch {key} sub_obligations is empty")
        if not branch["status"]:
            fail(f"branch {key} status is empty")
        if not branch["source_step"]:
            fail(f"branch {key} source_step is empty")
    nogos = set(data.get("retained_nogos", []))
    for required in ("public-shadow non-promotion", "finite-window Calkin blindness"):
        if required not in nogos:
            fail(f"schema retained_nogos missing {required}")

def sentence_iter(text: str):
    for sentence in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")):
        sentence = sentence.strip()
        if sentence:
            yield sentence

def assert_forbidden_phrases() -> None:
    literal_forbidden = [
        "proves RH",
        "RH proof",
        "essential norm is positive",
        "unconditional Xi_BC=0",
        "cascade summary proves Xi_BC closure",
    ]
    weakening_patterns = [
        r"public-shadow[^.?!]*(?:bypass|removed|weakened|waived|promoted)",
        r"finite-window[^.?!]*(?:bypass|removed|weakened|waived|certificate accepted)",
        r"finite-section[^.?!]*(?:bypass|removed|weakened|waived|certificate accepted)",
    ]
    branch_closed_patterns = [
        r"\bBranch [ABC]\b[^.?!]*(?:is|was|has been)\s+closed\b",
        r"\b[A-C]\b[^.?!]*\bbranch\b[^.?!]*(?:is|was|has been)\s+closed\b",
        r"\b(?:A|B|C)\s+closed\b",
    ]
    external_supplied_patterns = [
        r"\bG2-G5\b[^.?!]*(?:supplied|proved|established)\b",
        r"\bG2--G5\b[^.?!]*(?:supplied|proved|established)\b",
        r"\bSL164\.1\b[^.?!]*(?:supplied|proved|established|accepted_bridge_source)\b",
        r"\bH1-H5\b[^.?!]*(?:supplied|proved|established)\b",
        r"\bH1--H5\b[^.?!]*(?:supplied|proved|established)\b",
        r"\bexternal content\b[^.?!]*(?:is|was|has been)\s+(?:supplied|proved|established)\b",
    ]
    closure_patterns = [
        r"\bcascade summary\b[^.?!]*(?:proves|establishes|supplies)\s+\S*\s*Xi_BC\s+closure\b",
        r"\bcascade\b[^.?!]*(?:closes|closed)\s+\S*\s*Xi_BC\b",
    ]

    for target in TEXT_TARGETS:
        text = (BASE / target).read_text(encoding="utf-8")
        for phrase in literal_forbidden:
            if phrase in text:
                fail(f"{target} contains forbidden phrase: {phrase}")
        for sentence in sentence_iter(text):
            if re.search(r"(?<!not )(?<!NOT )\bC_l P_eta is compact\b", sentence):
                fail(f"{target} asserts compactness of C_l P_eta: {sentence}")
            for pattern in branch_closed_patterns:
                if re.search(pattern, sentence):
                    fail(f"{target} asserts a branch is closed: {sentence}")
            for pattern in external_supplied_patterns:
                if re.search(pattern, sentence):
                    fail(f"{target} asserts external content is supplied: {sentence}")
            for pattern in weakening_patterns:
                if re.search(pattern, sentence, flags=re.IGNORECASE):
                    fail(f"{target} weakens a retained no-go: {sentence}")
            for pattern in closure_patterns:
                if re.search(pattern, sentence):
                    fail(f"{target} asserts cascade closure of Xi_BC: {sentence}")

def assert_csv_readable() -> None:
    for name in [
        "content_classification_step166.csv",
        "cascade_branches_step166.csv",
        "external_content_interface_step166.csv",
        "residual_tree_step166.csv",
        "retained_nogos_step166.csv",
        "route_status_step166.csv",
        "construction_tasks_step166.csv",
    ]:
        path = BASE / name
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if len(rows) < 2:
            fail(f"{name} must contain a header and at least one row")

def main() -> None:
    assert_presence()
    assert_schema()
    assert_csv_readable()
    assert_forbidden_phrases()
    print("PASS: step166 cascade checks completed")

if __name__ == "__main__":
    main()

