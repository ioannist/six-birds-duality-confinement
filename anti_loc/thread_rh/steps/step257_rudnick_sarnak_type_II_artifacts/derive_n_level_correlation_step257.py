#!/usr/bin/env python3
"""Declare Rudnick-Sarnak n-level correlations as Type II instance."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step257_rudnick_sarnak_type_II_artifacts")


def write_csv(name: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with (ART / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    declaration = [{
        "carrier": "Rudnick-Sarnak n-level correlations",
        "objects": "families or principal/cuspidal automorphic L-functions, especially GL(N)",
        "zero_data": "rho_j(pi)=1/2+i gamma_j(pi)",
        "test_function": "Schwartz f with restricted Fourier support",
        "residual": "Xi_RS(f;T)=|R_n^family(f;T)-GUE_n_level(f)|",
        "closure": "lim_{T->infty} Xi_RS(f;T)=0 for all admissible f, with full conjectural support beyond proved ranges"
    }]
    classification = [{
        "case": "single_pi_n_level",
        "subtype": "Type Ib",
        "classification": "single-L zero correlation",
        "notes": "same zero-correlation subtype as Montgomery, but higher n"
    }, {
        "case": "multi_pi_or_family_n_level",
        "subtype": "Type II",
        "classification": "multi-L/family zero correlation",
        "notes": "completes the Type Ia/Ib/II subtype matrix"
    }]
    matrix = [
        {"subtype": "Type Ia", "meaning": "multi-L coefficient correlations", "instances": "SOC; full Selberg orthonormality", "count": "2"},
        {"subtype": "Type Ib", "meaning": "single-L zero correlations", "instances": "Montgomery pair correlation", "count": "1"},
        {"subtype": "Type II", "meaning": "multi-L/family zero correlations", "instances": "Rudnick-Sarnak n-level/family zero correlations", "count": "1"}
    ]
    evidence = [
        {"instance": "SOC off-diagonal coefficient correlation", "step": "254", "subtype": "Type Ia", "status": "open"},
        {"instance": "full Selberg orthonormality", "step": "255", "subtype": "Type Ia", "status": "open"},
        {"instance": "Montgomery pair correlation", "step": "256", "subtype": "Type Ib", "status": "open beyond RH-conditional restricted range"},
        {"instance": "Rudnick-Sarnak n-level/family zero correlations", "step": "257", "subtype": "Type II", "status": "proved restricted support; full conjecture open"}
    ]
    corpus = [{
        "finding": "Selberg-Class Cross-Correlation Extension",
        "update": "verified-on-4-Selberg-instances, all-three-subtypes-covered",
        "status": "candidate corpus-pending",
        "file_updated": "anti_loc/findings_framework.md"
    }]
    route = [
        {"route": "Rudnick_Sarnak_Type_II", "status": "classified", "verdict": "V_rudnick_sarnak_type_II_instance", "notes": "multi-L/family zero-correlation subtype"},
        {"route": "Cross_Correlation_Extension", "status": "subtype_matrix_complete", "verdict": "verified_on_4_instances", "notes": "Ia x2, Ib x1, II x1"},
        {"route": "RH_GRH_closure", "status": "not_claimed", "verdict": "not_applicable", "notes": "n-level statistics not claimed RH-equivalent"}
    ]
    tree = [
        {"node": "Selberg_cross_correlation_extension", "parent": "root", "status": "candidate_refined", "notes": "all subtype lanes populated"},
        {"node": "Type_Ia_coefficient_correlations", "parent": "Selberg_cross_correlation_extension", "status": "2_instances", "notes": "SOC and orthonormality"},
        {"node": "Type_Ib_single_L_zero_correlations", "parent": "Selberg_cross_correlation_extension", "status": "1_instance", "notes": "Montgomery"},
        {"node": "Type_II_family_zero_correlations", "parent": "Selberg_cross_correlation_extension", "status": "1_instance", "notes": "Rudnick-Sarnak"}
    ]
    sources = [
        {"source": "Z. Rudnick and P. Sarnak, Zeros of principal L-functions and random matrix theory, Duke Math. J. 81 (1996), 269-322", "role": "n-level correlations for principal L-functions in restricted Fourier support"},
        {"source": "N. M. Katz and P. Sarnak, Random Matrices, Frobenius Eigenvalues, and Monodromy, AMS Colloquium Publications 45, 1999", "role": "family symmetry and random-matrix framework"},
        {"source": "H. Iwaniec, W. Luo, and P. Sarnak, Low lying zeros of families of L-functions, Publ. Math. IHES 91 (2000), 55-131", "role": "low-lying zeros in families of L-functions"},
        {"source": "J. B. Conrey and N. C. Snaith, Applications of the L-functions ratios conjectures, Proc. Lond. Math. Soc. 94 (2007), 594-646", "role": "ratios-conjecture approach to zero statistics"}
    ]

    write_csv("rs_declaration_step257.csv", list(declaration[0]), declaration)
    write_csv("type_II_classification_step257.csv", ["case", "subtype", "classification", "notes"], classification)
    write_csv("subtype_matrix_step257.csv", ["subtype", "meaning", "instances", "count"], matrix)
    write_csv("instance_evidence_step257.csv", ["instance", "step", "subtype", "status"], evidence)
    write_csv("corpus_inclusion_step257.csv", ["finding", "update", "status", "file_updated"], corpus)
    write_csv("route_status_step257.csv", ["route", "status", "verdict", "notes"], route)
    write_csv("residual_tree_step257.csv", ["node", "parent", "status", "notes"], tree)
    write_csv("classical_theorems_cited_step257.csv", ["source", "role"], sources)

    payload = {
        "carrier": declaration[0],
        "classification": classification,
        "subtype_matrix": matrix,
        "evidence": evidence,
        "final_verdict": "V_rudnick_sarnak_type_II_instance",
    }
    (ART / "derive_n_level_correlation_step257.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("rudnick_sarnak_n_level_declared")
    print("classification=Type_II_multi_L_family_zero_correlation")
    print("verdict=V_rudnick_sarnak_type_II_instance")


if __name__ == "__main__":
    main()
