#!/usr/bin/env python3
"""Step 272: classify Sarnak Mobius orthogonality in the framework."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step272_sarnak_mobius_orthogonality_artifacts")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)

    mo_declaration = [
        {
            "carrier": "Sarnak_Mobius_orthogonality",
            "domain": "arithmetic-dynamical correlations",
            "admissible_data": "zero topological entropy system (X,T), f in C(X), x in X",
            "residual": "Xi_MO(N;T,f,x)=N^{-1}|sum_{n<=N} mu(n) f(T^n x)|",
            "closure": "lim_{N->infty} Xi_MO=0 for all admissible data",
            "status": "open in full generality; proved in several structured cases",
        }
    ]
    write_csv(ART / "MO_declaration_step272.csv", mo_declaration)

    classification = [
        {
            "candidate_finding": "Cross-Correlation Extension",
            "fit": "yes_with_subtype_refinement",
            "reason": "MO is a correlation residual between an arithmetic multiplicative sequence and a deterministic zero-entropy sequence.",
            "decision": "Type Ia-arithmetic-dynamical",
        },
        {
            "candidate_finding": "Subconvexity Extension",
            "fit": "no",
            "reason": "MO is not a critical-line growth-rate residual. Qualitative MO implies PNT via the trivial system, not an RH-strength bound without quantitative rates.",
            "decision": "excluded",
        },
        {
            "candidate_finding": "Zero-Density Extension",
            "fit": "no",
            "reason": "MO is not a zero-count residual in right-half rectangles.",
            "decision": "excluded",
        },
        {
            "candidate_finding": "new_11th_finding",
            "fit": "not_needed",
            "reason": "Existing correlation typed condition absorbs MO after Type Ia subtype refinement.",
            "decision": "no_new_finding",
        },
    ]
    write_csv(ART / "classification_step272.csv", classification)

    subtype = [
        {
            "type": "Ia-pure-arithmetic",
            "description": "coefficient/coefficient correlations such as SOC and full Selberg orthonormality",
            "examples": "Selberg orthogonality; full Selberg orthonormality",
            "status_after_step272": "retained",
        },
        {
            "type": "Ia-arithmetic-dynamical",
            "description": "multiplicative arithmetic function against deterministic zero-entropy sequence",
            "examples": "Sarnak Mobius orthogonality",
            "status_after_step272": "new subtype refinement",
        },
        {
            "type": "Ib",
            "description": "single-L zero correlations",
            "examples": "Montgomery pair correlation; Hejhal triple correlation",
            "status_after_step272": "unchanged",
        },
        {
            "type": "II",
            "description": "multi-L or family zero correlations",
            "examples": "Rudnick-Sarnak; Katz-Sarnak n-level statistics",
            "status_after_step272": "unchanged",
        },
    ]
    write_csv(ART / "subtype_refinement_step272.csv", subtype)

    corpus = [
        {
            "file": "anti_loc/findings_framework.md",
            "action": "refine Cross-Correlation Extension Type Ia",
            "status": "updated",
            "notes": "added Type Ia-arithmetic-dynamical and Step 272 evidence",
        },
        {
            "file": "future corpus",
            "action": "preserve no-11th-finding decision",
            "status": "corpus-pending",
            "notes": "MO is classified under existing correlation extension, not as a separate framework finding",
        },
    ]
    write_csv(ART / "corpus_inclusion_step272.csv", corpus)

    residual_tree = [
        {"node": "MO", "parent": "root", "status": "classified", "notes": "arithmetic-dynamical correlation residual"},
        {"node": "Cross_Correlation_Type_Ia", "parent": "MO", "status": "fits", "notes": "new arithmetic-dynamical subtype"},
        {"node": "Subconvexity", "parent": "MO", "status": "excluded", "notes": "qualitative MO is not growth-rate closure"},
        {"node": "Zero_Density", "parent": "MO", "status": "excluded", "notes": "not a zero-count residual"},
        {"node": "11th_finding", "parent": "MO", "status": "not_needed", "notes": "existing typed condition absorbs it"},
    ]
    write_csv(ART / "residual_tree_step272.csv", residual_tree)

    route_status = [
        {"route": "declare MO residual", "status": "complete", "verdict": "carrier well-defined"},
        {"route": "test Cross-Correlation Extension", "status": "complete", "verdict": "fits Type Ia-arithmetic-dynamical"},
        {"route": "test Subconvexity", "status": "complete", "verdict": "excluded except quantitative consequences"},
        {"route": "test Zero-Density", "status": "complete", "verdict": "excluded"},
        {"route": "11th finding", "status": "complete", "verdict": "not needed"},
    ]
    write_csv(ART / "route_status_step272.csv", route_status)

    construction = [
        {"task": "create artifact directory", "status": "complete", "notes": "mkdir succeeded"},
        {"task": "audit MO statement", "status": "complete", "notes": "Sarnak lecture source checked"},
        {"task": "audit proved cases", "status": "complete", "notes": "BSZ horocycle, Liu-Sarnak distal classes, Tao-Teravainen correlations"},
        {"task": "classify against 10 findings", "status": "complete", "notes": "Cross-Correlation Type Ia refinement"},
        {"task": "update findings_framework.md", "status": "complete", "notes": "step 272 cross-reference deposited"},
    ]
    write_csv(ART / "construction_tasks_step272.csv", construction)

    sources = [
        {
            "source": "Peter Sarnak, Three Lectures on the Mobius Function: Randomness and Dynamics, IAS lecture notes, 2010/2011.",
            "used_for": "MO residual and PNT/RH-bound distinction",
            "url": "https://www.math.ias.edu/files/wam/2011/PSMobius.pdf",
            "quote": "mu(n) xi(n) = o(N) as N -> infinity",
        },
        {
            "source": "Jean Bourgain, Peter Sarnak, Tamar Ziegler, Disjointness of Mobius from horocycle flows, 2013.",
            "used_for": "structured proved case: horocycle flows",
            "url": "https://arxiv.org/abs/1110.0992",
            "quote": "prove that the Mobius function is disjoint from discrete horocycle flows",
        },
        {
            "source": "Jianya Liu and Peter Sarnak, The Mobius function and distal flows, Duke Math. J. 164 (2015), 1353-1399.",
            "used_for": "structured proved cases: distal homogeneous / skew-product flows",
            "url": "https://doi.org/10.1215/00127094-2916213",
            "quote": "The Mobius function is linearly disjoint",
        },
        {
            "source": "Terence Tao and Joni Teravainen, The structure of correlations of multiplicative functions at almost all scales, Algebra Number Theory 13 (2019), 2103-2150.",
            "used_for": "multiplicative-correlation comparison class",
            "url": "https://arxiv.org/abs/1809.02518",
            "quote": "higher order correlations",
        },
        {
            "source": "Ben Green and Terence Tao, The Mobius function is strongly orthogonal to nilsequences, Annals of Mathematics 175 (2012), 541-566.",
            "used_for": "nilsequence proved case correction",
            "url": "https://annals.math.princeton.edu/2012/175-2/p07",
            "quote": "strongly orthogonal to nilsequences",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step272.csv", sources)

    content = [
        {"artifact": "MO_declaration_step272.csv", "class": "carrier_declaration", "claim_boundary": "MO open in full generality"},
        {"artifact": "classification_step272.csv", "class": "framework_classification", "claim_boundary": "classification only"},
        {"artifact": "subtype_refinement_step272.csv", "class": "finding_refinement", "claim_boundary": "no proof of MO"},
        {"artifact": "classical_theorems_cited_step272.csv", "class": "literature_audit", "claim_boundary": "proved cases distinguished from full conjecture"},
    ]
    write_csv(ART / "content_classification_step272.csv", content)

    schema = {
        "step": 272,
        "orientation": "adequacy",
        "target": "Sarnak Möbius-orthogonality classification within framework",
        "MO_carrier_definition": mo_declaration[0],
        "classification_decision": "MO fits Cross-Correlation Extension Type Ia after arithmetic-dynamical subtype refinement.",
        "framework_finding_target": "Cross-Correlation Extension; no 11th finding required.",
        "retained_nogos": [
            "MO is not claimed proved in full generality.",
            "RH is not claimed.",
            "Qualitative MO implies PNT through the trivial system, not RH-strength bounds without quantitative rates.",
            "Subconvexity and zero-density extensions are not weakened or absorbed.",
        ],
        "final_verdict": "V_sarnak_in_cross_correlation_Ia",
    }
    (ART / "step272_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "compute_step272_output.txt").write_text(
        "verdict=V_sarnak_in_cross_correlation_Ia\n"
        "classification=Cross-Correlation Extension Type Ia-arithmetic-dynamical\n"
        "new_11th_finding=no\n",
        encoding="utf-8",
    )
    print("verdict=V_sarnak_in_cross_correlation_Ia")


if __name__ == "__main__":
    main()
