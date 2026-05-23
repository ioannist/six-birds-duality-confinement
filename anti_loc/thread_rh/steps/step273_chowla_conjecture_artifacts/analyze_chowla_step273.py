#!/usr/bin/env python3
"""Step 273: classify Chowla's conjecture in Cross-Correlation Type Ia."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step273_chowla_conjecture_artifacts")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)

    declaration = [
        {
            "carrier": "Chowla_multi_shift_Mobius_correlation",
            "standard_exponent_convention": "e_i in {1,2}, not epsilon_i=-1, because mu(n)^{-1} is undefined when mu(n)=0",
            "residual": "Xi_chowla(a,e;N)=N^{-1}|sum_{n<=N} prod_i mu(n+a_i)^{e_i}|",
            "closure": "Xi_chowla -> 0 for all distinct shifts a_i and nontrivial exponent pattern",
            "status": "open in full ordinary form; logarithmic and averaged cases known",
        }
    ]
    write_csv(ART / "chowla_declaration_step273.csv", declaration)

    classification = [
        {
            "finding": "Cross-Correlation Extension",
            "type": "Type Ia-pure-arithmetic",
            "sub_sub_type": "k-correlation / multi-shift",
            "fit": "yes",
            "reason": "Chowla is a pure arithmetic multi-correlation of shifted values of the same multiplicative function.",
            "verdict": "V_chowla_in_Ia_pure_arithmetic_k_correlation",
        },
        {
            "finding": "Cross-Correlation Type Ia-pure-arithmetic 2-correlation",
            "type": "subcase",
            "sub_sub_type": "2-correlation",
            "fit": "contains k=2 only",
            "reason": "SOC and Selberg orthonormality are pairwise; Chowla needs arbitrary k and shifts.",
            "verdict": "refine_needed",
        },
        {
            "finding": "new framework finding",
            "type": "not_needed",
            "sub_sub_type": "none",
            "fit": "no",
            "reason": "The existing Cross-Correlation Extension already has a natural place for pure arithmetic k-correlations.",
            "verdict": "no_new_finding",
        },
    ]
    write_csv(ART / "classification_step273.csv", classification)

    refinement = [
        {
            "type": "Ia-pure-arithmetic",
            "sub_sub_type": "2-correlation",
            "examples": "SOC; full Selberg orthonormality",
            "status_after_step273": "retained",
        },
        {
            "type": "Ia-pure-arithmetic",
            "sub_sub_type": "k-correlation / multi-shift",
            "examples": "Chowla; Elliott",
            "status_after_step273": "new sub-sub-type",
        },
        {
            "type": "Ia-arithmetic-dynamical",
            "sub_sub_type": "single arithmetic sequence vs deterministic sequence",
            "examples": "Sarnak Mobius orthogonality",
            "status_after_step273": "retained from step272",
        },
        {
            "type": "Ib",
            "sub_sub_type": "zero pair/n-level within one L",
            "examples": "Montgomery; Hejhal",
            "status_after_step273": "unchanged",
        },
        {
            "type": "II",
            "sub_sub_type": "multi-L/family zero correlations",
            "examples": "Rudnick-Sarnak; Katz-Sarnak",
            "status_after_step273": "unchanged",
        },
    ]
    write_csv(ART / "sub_sub_type_refinement_step273.csv", refinement)

    corpus = [
        {
            "file": "anti_loc/findings_framework.md",
            "action": "add Chowla as Type Ia-pure-arithmetic k-correlation evidence",
            "status": "updated",
            "notes": "Cross-Correlation Extension status raised to 6 correlation instances",
        }
    ]
    write_csv(ART / "corpus_inclusion_step273.csv", corpus)

    residual_tree = [
        {"node": "Chowla", "parent": "root", "status": "classified", "notes": "pure arithmetic multi-shift correlation"},
        {"node": "Type_Ia_pure_arithmetic", "parent": "Chowla", "status": "fits", "notes": "same arithmetic correlation family as SOC but higher arity"},
        {"node": "k_correlation_subtype", "parent": "Type_Ia_pure_arithmetic", "status": "new", "notes": "captures Chowla and Elliott"},
        {"node": "new_framework_finding", "parent": "Chowla", "status": "not_needed", "notes": "sub-sub-type refinement sufficient"},
    ]
    write_csv(ART / "residual_tree_step273.csv", residual_tree)

    route = [
        {"route": "declare Chowla residual", "status": "complete", "verdict": "standard exponent convention recorded"},
        {"route": "classify under Type Ia", "status": "complete", "verdict": "fits pure-arithmetic k-correlation"},
        {"route": "test need for new finding", "status": "complete", "verdict": "not needed"},
        {"route": "update findings framework", "status": "complete", "verdict": "sub-sub-type tree deposited"},
    ]
    write_csv(ART / "route_status_step273.csv", route)

    construction = [
        {"task": "create artifact directory", "status": "complete", "notes": "mkdir succeeded"},
        {"task": "audit Chowla statement", "status": "complete", "notes": "standard exponent convention applied"},
        {"task": "audit known cases", "status": "complete", "notes": "Tao 2016, Tao-Teravainen 2019 logarithmic cases"},
        {"task": "classify", "status": "complete", "notes": "Type Ia-pure-arithmetic-k-correlation"},
        {"task": "update corpus holding file", "status": "complete", "notes": "findings_framework.md updated"},
    ]
    write_csv(ART / "construction_tasks_step273.csv", construction)

    sources = [
        {
            "source": "S. Chowla, The Riemann Hypothesis and Hilbert's Tenth Problem, Gordon and Breach, 1965.",
            "used_for": "origin of Chowla conjecture family",
            "url": "https://openlibrary.org/books/OL5946024M/The_Riemann_hypothesis_and_Hilbert%27s_tenth_problem",
            "quote": "The Riemann hypothesis and Hilbert's tenth problem",
        },
        {
            "source": "Terence Tao, The logarithmically averaged Chowla and Elliott conjectures for two-point correlations, Forum Math. Pi 4 (2016), e8.",
            "used_for": "logarithmically averaged k=2 case",
            "url": "https://arxiv.org/abs/1509.05422",
            "quote": "two-point correlation case",
        },
        {
            "source": "Terence Tao and Joni Teravainen, Odd order cases of the logarithmically averaged Chowla conjecture, J. Theorie des Nombres de Bordeaux 30 (2018/2019).",
            "used_for": "logarithmically averaged odd-order cases",
            "url": "https://arxiv.org/abs/1710.02112",
            "quote": "odd order cases",
        },
        {
            "source": "Terence Tao and Joni Teravainen, The structure of logarithmically averaged correlations of multiplicative functions, Algebra Number Theory 13 (2019).",
            "used_for": "Elliott/Chowla multiplicative-correlation structure",
            "url": "https://arxiv.org/abs/1708.02610",
            "quote": "correlations of multiplicative functions",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step273.csv", sources)

    content = [
        {"artifact": "chowla_declaration_step273.csv", "class": "carrier_declaration", "claim_boundary": "full Chowla open"},
        {"artifact": "classification_step273.csv", "class": "framework_classification", "claim_boundary": "classification only"},
        {"artifact": "sub_sub_type_refinement_step273.csv", "class": "finding_refinement", "claim_boundary": "no proof"},
        {"artifact": "classical_theorems_cited_step273.csv", "class": "literature_audit", "claim_boundary": "known logarithmic cases separated from full conjecture"},
    ]
    write_csv(ART / "content_classification_step273.csv", content)

    schema = {
        "step": 273,
        "orientation": "adequacy",
        "target": "Chowla conjecture classification within Cross-Correlation Type Ia",
        "chowla_carrier_definition": declaration[0],
        "classification_decision": "Type Ia-pure-arithmetic-k-correlation",
        "sub_sub_type_refinement": "Type Ia-pure-arithmetic splits into 2-correlation and k-correlation/multi-shift.",
        "framework_finding_target": "Cross-Correlation Extension; no new finding required.",
        "retained_nogos": [
            "Full Chowla is not claimed proved.",
            "RH is not claimed.",
            "Known logarithmic/averaged cases are not promoted to the ordinary full conjecture.",
            "Sarnak/Chowla implication relations are not used as equivalences.",
        ],
        "final_verdict": "V_chowla_in_Ia_pure_arithmetic_k_correlation",
    }
    (ART / "step273_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "compute_step273_output.txt").write_text(
        "verdict=V_chowla_in_Ia_pure_arithmetic_k_correlation\n"
        "classification=Cross-Correlation Type Ia-pure-arithmetic-k-correlation\n",
        encoding="utf-8",
    )
    print("verdict=V_chowla_in_Ia_pure_arithmetic_k_correlation")


if __name__ == "__main__":
    main()
