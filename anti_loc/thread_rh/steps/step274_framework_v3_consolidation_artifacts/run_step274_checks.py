#!/usr/bin/env python3
"""Validate Step 274 framework v3 consolidation artifacts."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step274_framework_v3_consolidation_artifacts"
V3 = ROOT / "anti_loc/findings_framework_v3_consolidated.md"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step274_results_summary.md",
    "step274_schema.json",
    "content_classification_step274.csv",
    "nonclaim_boundary_step274.md",
    "step274_framework_v3.tex",
    "run_step274_checks.py",
    "findings_catalog_step274.csv",
    "hierarchy_levels_step274.csv",
    "cross_track_matrix_step274.csv",
    "corpus_integration_step274.csv",
    "residual_tree_step274.csv",
    "route_status_step274.csv",
    "construction_tasks_step274.csv"
]

KNOWN_LINKS = {
    "CTMT",
    "CRCFT modes",
    "Carrier Dichotomy",
    "SCDG",
    "Bridge Impossibility",
    "CTMT recursion",
    "Cross-Correlation Extension",
    "Subconvexity Extension",
    "Zero-Density Extension",
    "Attack Foreclosure",
    "Independent Codification",
    "Scalar Identity No-Go",
    "Shadow Non-Promotion"
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")
    if not V3.exists():
        raise SystemExit("missing v3 consolidated document")

    schema = json.loads((ART / "step274_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 274:
        raise SystemExit("schema step mismatch")
    if schema.get("final_verdict") != "V_framework_v3_consolidated":
        raise SystemExit("unexpected verdict")
    for key in [
        "document_structure",
        "ten_findings_status",
        "hierarchy_summary",
        "corpus_integration_recommendations",
        "retained_nogos"
    ]:
        if key not in schema:
            raise SystemExit(f"schema missing key {key}")

    catalog = read_csv(ART / "findings_catalog_step274.csv")
    if len(catalog) != 10:
        raise SystemExit(f"expected 10 catalog rows, got {len(catalog)}")

    hierarchy = read_csv(ART / "hierarchy_levels_step274.csv")
    if len(hierarchy) != 5:
        raise SystemExit(f"expected 5 hierarchy rows, got {len(hierarchy)}")

    matrix = read_csv(ART / "cross_track_matrix_step274.csv")
    if len(matrix) != 10:
        raise SystemExit(f"expected 10 matrix rows, got {len(matrix)}")

    v3 = V3.read_text(encoding="utf-8")
    for heading in [
        "## Summary",
        "## 5-Level Selberg-Class Hierarchy",
        "## Per-Finding Catalog",
        "## Cross-Track Verification Matrix",
        "## RH Cascade State",
        "## Score-N Attack Interface Analysis",
        "## Corpus Integration Roadmap"
    ]:
        if heading not in v3:
            raise SystemExit(f"missing heading {heading}")

    links = set(re.findall(r"\[\[([^\]]+)\]\]", v3))
    broken = sorted(links - KNOWN_LINKS)
    if broken:
        raise SystemExit(f"broken wiki-style links: {broken}")

    findings_text = FINDINGS.read_text(encoding="utf-8")
    if "step 274 v3 consolidated deposit" not in findings_text:
        raise SystemExit("findings_framework timestamp not updated")

    print("run_step274_checks.py PASS")


if __name__ == "__main__":
    main()
