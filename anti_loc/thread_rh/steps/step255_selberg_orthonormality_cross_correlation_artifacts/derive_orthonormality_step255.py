#!/usr/bin/env python3
"""Declare full Selberg orthonormality and the cross-correlation extension."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step255_selberg_orthonormality_cross_correlation_artifacts")


def write_csv(name: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with (ART / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    declaration = [{
        "carrier": "Full Selberg orthonormality",
        "objects": "primitive Selberg-class L-functions L1,L2",
        "prime_correlation": "S_12(x)=sum_{p<=x} a_p(L1) conjugate(a_p(L2))/p",
        "diagonal": "S_LL(x)=n_L log log x + O(1)",
        "off_diagonal": "S_12(x)=O(1) for L1 != L2",
        "normalization_note": "standard Selberg diagonal constant is n_L, expected n_L=1 for primitive functions; this is not the pole order at s=1",
        "residual": "Xi_orth(L1,L2)=limsup_x |S_12(x)-n_L delta_{L1,L2} log log x|/(1+log log x)",
        "closure": "bounded diagonal remainder and bounded off-diagonal correlations for all primitive pairs"
    }]
    extension = [{
        "finding": "Selberg-Class Cross-Correlation Extension",
        "statement": "Beyond per-L RH analogues, Selberg-class typed cascades admit multi-L residuals measuring correlations between distinct primitive L-functions.",
        "scope": "second-order Selberg-class family: pairwise/multiway coefficient correlations, joint zeros, and orthonormality conditions",
        "status": "candidate verified-on-2-instances corpus-pending",
        "relation_to_step232": "extends SCDG from single-L RH-analogue residuals to multi-L correlation residuals",
        "relation_to_step254": "SOC is the off-diagonal instance"
    }]
    evidence = [{
        "instance": "SOC off-diagonal",
        "step": "254",
        "residual": "sum_{p<=x} a_p(L1) conjugate(a_p(L2))/p",
        "closure": "O(1) or normalized limit zero for L1 != L2",
        "status": "open cross-correlation carrier"
    }, {
        "instance": "diagonal orthonormality",
        "step": "255",
        "residual": "sum_{p<=x} |a_p(L)|^2/p - n_L log log x",
        "closure": "O(1) for primitive L",
        "status": "open diagonal norm carrier"
    }]
    corpus = [{
        "finding": "Selberg-Class Cross-Correlation Extension",
        "recommended_location": "findings_framework.md now; future corpus integration in adequacy.tex or Selberg-class section",
        "status": "candidate corpus-pending",
        "do_not_claim": "not theorem-grade; does not solve SOC, orthonormality, GRH, or RH"
    }]
    sources = [
        {"source": "A. Selberg, Old and new conjectures and results about a class of Dirichlet series, Amalfi conference 1989, Univ. Salerno 1992", "role": "origin of Selberg-class orthogonality/orthonormality conjectural framework"},
        {"source": "J. B. Conrey and A. Ghosh, On the Selberg class of Dirichlet series: small degrees, Duke Math. J. 72 (1993), 673-693", "role": "Selberg class axioms and small-degree structural consequences"},
        {"source": "J. Liu, Y. Wang, and Y. Ye, A proof of Selberg's orthogonality for automorphic L-functions", "role": "automorphic L-function orthogonality evidence"},
        {"source": "J. Kaczorowski and A. Perelli, The Selberg class: a survey, Number Theory in Progress, 1999, 953-992", "role": "survey and structural context"},
        {"source": "J. Kaczorowski and A. Perelli, On the structure of the Selberg class, VII: 1<d<2, Ann. of Math. 173 (2011), 1397-1441", "role": "Selberg-class structural program"}
    ]
    route = [
        {"route": "SOC_off_diagonal", "status": "classified_step254", "verdict": "outside_Riemann_and_single_L_Dichotomy"},
        {"route": "diagonal_orthonormality", "status": "declared_step255", "verdict": "cross_correlation_extension_instance"},
        {"route": "cross_correlation_extension", "status": "candidate_corpus_pending", "verdict": "V_selberg_orthonormality_cross_correlation_typed"}
    ]
    tree = [
        {"node": "SCDG", "parent": "root", "status": "single_L_family", "notes": "step 232 per-L RH analogue"},
        {"node": "Selberg_cross_correlation_extension", "parent": "SCDG", "status": "candidate", "notes": "multi-L second-order residuals"},
        {"node": "SOC_off_diagonal", "parent": "Selberg_cross_correlation_extension", "status": "open", "notes": "step 254 instance"},
        {"node": "diagonal_orthonormality", "parent": "Selberg_cross_correlation_extension", "status": "open", "notes": "step 255 instance"},
        {"node": "full_orthonormality", "parent": "Selberg_cross_correlation_extension", "status": "open", "notes": "diagonal plus off-diagonal"}
    ]

    write_csv("orthonormality_declaration_step255.csv", list(declaration[0]), declaration)
    write_csv("cross_correlation_extension_step255.csv", list(extension[0]), extension)
    write_csv("instance_evidence_step255.csv", list(evidence[0]), evidence)
    write_csv("corpus_inclusion_step255.csv", list(corpus[0]), corpus)
    write_csv("classical_theorems_cited_step255.csv", ["source", "role"], sources)
    write_csv("route_status_step255.csv", ["route", "status", "verdict"], route)
    write_csv("residual_tree_step255.csv", ["node", "parent", "status", "notes"], tree)

    payload = {
        "orthonormality_carrier": declaration[0],
        "extension": extension[0],
        "evidence": evidence,
        "final_verdict": "V_selberg_orthonormality_cross_correlation_typed",
    }
    (ART / "derive_orthonormality_step255.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("orthonormality_carrier_declared")
    print("cross_correlation_extension=candidate_verified_on_2_instances_corpus_pending")
    print("verdict=V_selberg_orthonormality_cross_correlation_typed")


if __name__ == "__main__":
    main()
