#!/usr/bin/env python3
"""Step 275: classify arithmetic QUE in the framework findings."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step275_QUE_classification_artifacts")


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
            "carrier": "Quantum_Unique_Ergodicity_Hecke_Maass",
            "space": "Gamma\\H with Gamma arithmetic, e.g. SL2(Z)",
            "data": "Hecke-Maass cusp forms phi_j with Laplace eigenvalue 1/4+t_j^2",
            "residual": "Xi_QUE(j;f)=|int f(z)|phi_j(z)|^2 dvol - vol^{-1} int f dvol|",
            "closure": "Xi_QUE(j;f)->0 for every continuous test function f as t_j->infty",
            "status": "arithmetic Hecke QUE proved in key settings; general non-arithmetic QUE open",
        }
    ]
    write_csv(ART / "QUE_declaration_step275.csv", declaration)

    classification = [
        {
            "candidate_finding": "Subconvexity Extension",
            "fit": "primary",
            "subtype": "Type alpha subconvexity-bridge",
            "reason": "Watson/triple-product formulas convert quantitative QUE matrix coefficients into central L-value size estimates.",
            "decision": "V_que_in_subconvexity",
        },
        {
            "candidate_finding": "Cross-Correlation Extension",
            "fit": "secondary",
            "subtype": "Type Ia correlation shadow",
            "reason": "The QUE residual is an eigenfunction/eigenform mass-correlation test, but the effective arithmetic bridge is through L-value subconvexity.",
            "decision": "secondary_not_primary",
        },
        {
            "candidate_finding": "SCDG",
            "fit": "no",
            "subtype": "not a zero-location RH analogue",
            "reason": "QUE is mass equidistribution for eigenstates, not a per-L zero-line defect.",
            "decision": "excluded",
        },
        {
            "candidate_finding": "new_11th_finding",
            "fit": "not_needed",
            "subtype": "none",
            "reason": "The Watson bridge places the arithmetic QUE route inside existing Subconvexity Extension; no fresh typed family is required.",
            "decision": "no_new_finding",
        },
    ]
    write_csv(ART / "classification_step275.csv", classification)

    watson = [
        {
            "bridge": "Watson triple product",
            "input": "matrix coefficient / period int phi_j^2 psi",
            "output": "central triple product L-value, e.g. L(1/2, sym^2 phi_j x psi) with local factors",
            "framework_role": "turns quantitative QUE into a Subconvexity Type alpha route",
            "status": "literature bridge; exact normalization depends on chosen forms and local factors",
        },
        {
            "bridge": "ergodic arithmetic QUE",
            "input": "Hecke recurrence and invariant measure rigidity",
            "output": "arithmetic QUE in proved settings",
            "framework_role": "native closure for arithmetic QUE, not an SCDG/RH analogue",
            "status": "proved by Lindenstrauss/Soundararajan in arithmetic settings",
        },
    ]
    write_csv(ART / "watson_bridge_step275.csv", watson)

    corpus = [
        {
            "file": "anti_loc/findings_framework.md",
            "action": "add QUE to Subconvexity Extension Type alpha evidence and Cross-Correlation secondary note",
            "status": "updated",
            "notes": "no 11th finding introduced",
        }
    ]
    write_csv(ART / "corpus_inclusion_step275.csv", corpus)

    residual_tree = [
        {"node": "QUE", "parent": "root", "status": "classified", "notes": "mass equidistribution residual"},
        {"node": "Subconvexity_Type_alpha", "parent": "QUE", "status": "primary", "notes": "Watson/triple-product central L-values"},
        {"node": "Cross_Correlation_Type_Ia", "parent": "QUE", "status": "secondary", "notes": "mass/eigenform correlation shadow"},
        {"node": "SCDG", "parent": "QUE", "status": "excluded", "notes": "not zero-location"},
        {"node": "11th_finding", "parent": "QUE", "status": "not_needed", "notes": "existing findings cover it"},
    ]
    write_csv(ART / "residual_tree_step275.csv", residual_tree)

    route = [
        {"route": "declare QUE residual", "status": "complete", "verdict": "carrier well-defined"},
        {"route": "test SCDG", "status": "complete", "verdict": "excluded"},
        {"route": "test Cross-Correlation", "status": "complete", "verdict": "secondary Type Ia shadow"},
        {"route": "test Subconvexity", "status": "complete", "verdict": "primary Type alpha via Watson"},
        {"route": "test 11th finding", "status": "complete", "verdict": "not needed"},
    ]
    write_csv(ART / "route_status_step275.csv", route)

    construction = [
        {"task": "create artifact directory", "status": "complete", "notes": "mkdir succeeded"},
        {"task": "declare QUE carrier", "status": "complete", "notes": "mass measure residual"},
        {"task": "audit Watson bridge", "status": "complete", "notes": "triple product central L-value route"},
        {"task": "classify", "status": "complete", "notes": "Subconvexity primary, Cross-Correlation secondary"},
        {"task": "update findings_framework.md", "status": "complete", "notes": "QUE evidence added"},
    ]
    write_csv(ART / "construction_tasks_step275.csv", construction)

    sources = [
        {
            "source": "Ze'ev Rudnick and Peter Sarnak, The behaviour of eigenstates of arithmetic hyperbolic manifolds, Comm. Math. Phys. 161 (1994), 195-213.",
            "used_for": "QUE conjecture origin",
            "url": "https://doi.org/10.1007/BF02101648",
            "quote": "The behaviour of eigenstates of arithmetic hyperbolic manifolds",
        },
        {
            "source": "Thomas C. Watson, Rankin Triple Products and Quantum Chaos, Ph.D. thesis, Princeton University, 2002.",
            "used_for": "triple product / central L-value bridge",
            "url": "https://arxiv.org/abs/0810.0425",
            "quote": "central value of the corresponding Rankin triple product L-function",
        },
        {
            "source": "Elon Lindenstrauss, Invariant measures and arithmetic quantum unique ergodicity, Annals of Mathematics 163 (2006), 165-219.",
            "used_for": "arithmetic QUE proof in compact arithmetic setting and measure rigidity route",
            "url": "https://annals.math.princeton.edu/wp-content/uploads/annals-v163-n1-p03.pdf",
            "quote": "arithmetic quantum unique ergodicity",
        },
        {
            "source": "Kannan Soundararajan, Quantum unique ergodicity for SL2(Z)\\H, Annals of Mathematics 172 (2010), 1529-1538.",
            "used_for": "nonescape of mass for Hecke-Maass forms on modular surface",
            "url": "https://arxiv.org/abs/0901.4060",
            "quote": "eliminate the possibility of escape of mass",
        },
        {
            "source": "Roman Holowinsky and Kannan Soundararajan, Mass equidistribution for Hecke eigenforms, Annals of Mathematics 172 (2010), 1517-1528.",
            "used_for": "holomorphic Hecke eigenform QUE",
            "url": "https://annals.math.princeton.edu/2010/172-2/p18",
            "quote": "Mass equidistribution for Hecke eigenforms",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step275.csv", sources)

    content = [
        {"artifact": "QUE_declaration_step275.csv", "class": "carrier_declaration", "claim_boundary": "general QUE open"},
        {"artifact": "classification_step275.csv", "class": "framework_classification", "claim_boundary": "classification only"},
        {"artifact": "watson_bridge_step275.csv", "class": "bridge_audit", "claim_boundary": "normalization not rederived"},
        {"artifact": "classical_theorems_cited_step275.csv", "class": "literature_audit", "claim_boundary": "proved arithmetic cases distinguished from general QUE"},
    ]
    write_csv(ART / "content_classification_step275.csv", content)

    schema = {
        "step": 275,
        "orientation": "adequacy",
        "target": "QUE classification within framework",
        "QUE_carrier_definition": declaration[0],
        "classification_decision": "primary Subconvexity Extension Type alpha via Watson; secondary Cross-Correlation Type Ia shadow",
        "watson_bridge": watson[0],
        "framework_finding_target": "Subconvexity Extension; no 11th finding required",
        "retained_nogos": [
            "General QUE is not claimed solved.",
            "RH/GRH are not claimed.",
            "Arithmetic QUE proofs are distinguished from the Watson/subconvexity route.",
            "SCDG remains a zero-location family and is not widened to mass equidistribution.",
        ],
        "final_verdict": "V_que_in_subconvexity",
    }
    (ART / "step275_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "compute_step275_output.txt").write_text(
        "verdict=V_que_in_subconvexity\n"
        "primary=Subconvexity Extension Type alpha via Watson\n"
        "secondary=Cross-Correlation Type Ia shadow\n",
        encoding="utf-8",
    )
    print("verdict=V_que_in_subconvexity")


if __name__ == "__main__":
    main()
