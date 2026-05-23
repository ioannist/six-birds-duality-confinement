#!/usr/bin/env python3
"""Step 212 structural audit of Connes--Consani 2020.

The script records the translation from the paper's Sonin/Toeplitz objects to
the cascade's Branch A Calkin objects.  It uses short source snippets only.
"""

from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step212_connes_consani_audit_artifacts")
SOURCE = Path("/tmp/burnol_audit/connes_weil_archimedean.txt")


def write_csv(name: str, rows: list[dict[str, str]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for k in row:
            if k not in fieldnames:
                fieldnames.append(k)
    with (BASE / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def ensure_source() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"missing manager-extracted source: {SOURCE}")


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    ensure_source()

    write_csv(
        "connes_consani_theorems_step212.csv",
        [
            {
                "item": "Definition 4.4",
                "line_ref": "1594",
                "short_quote": "Sonin's space S(alpha,beta)",
                "audit_use": "Identifies S(1,1) as the Sonin space matching Burnol K_1.",
            },
            {
                "item": "Theorem 4.7",
                "line_ref": "1766-1768",
                "short_quote": "The following functional is positive",
                "audit_use": "Positivity of Tr(vartheta(f)S), not compactness of off-diagonal C_l P_eta.",
            },
            {
                "item": "Equation 83",
                "line_ref": "1768-1771",
                "short_quote": "Tr(vartheta(f)S)=W_infty(f)+integral",
                "audit_use": "Trace formula for compressed scaling on Sonin subspace.",
            },
            {
                "item": "Section 6 opening",
                "line_ref": "2217-2224",
                "short_quote": "natural discretization ... is a Toeplitz matrix",
                "audit_use": "Finite q approximation of compact operator K_I.",
            },
            {
                "item": "Section 6.2",
                "line_ref": "2345-2355",
                "short_quote": "Discrete approximation and Toeplitz matrices",
                "audit_use": "Toeplitz spectral theory for largest eigenvalue/eigenvector of T_q.",
            },
            {
                "item": "Equation 110-111",
                "line_ref": "2428-2444",
                "short_quote": "S=lambda Id - ... T_q",
                "audit_use": "Co-rank-one Toeplitz decomposition; finite-dimensional approximation.",
            },
        ],
    )

    write_csv(
        "translation_table_step212.csv",
        [
            {
                "cascade_object": "K_lambda / Burnol Sonine subspace at lambda=1",
                "connes_consani_object": "S(1,1), Sonin's space",
                "match_status": "identified_at_lambda_1",
                "notes": "Definition 4.4 matches the support and Fourier-support vanishing conditions.",
            },
            {
                "cascade_object": "P_infty projection onto K_lambda",
                "connes_consani_object": "S, orthogonal projection onto S(1,1)",
                "match_status": "identified_at_lambda_1",
                "notes": "Parameter mismatch remains for cascade runs at lambda=1/2, but Branch A structure is Sonine-projection type.",
            },
            {
                "cascade_object": "M_{m_l} / multiplicative log-shift",
                "connes_consani_object": "vartheta(f), scaling action",
                "match_status": "related",
                "notes": "Test-function integrated scaling action is broader than a single multiplier m_l.",
            },
            {
                "cascade_object": "C_l=(I-P_infty)M_{m_l}P_infty",
                "connes_consani_object": "(I-S)vartheta(f)S",
                "match_status": "structural_match_off_diagonal",
                "notes": "Off-Sonin compression is related to but not the same as Tr(vartheta(f)S).",
            },
            {
                "cascade_object": "q_eta(C_l P_eta) in A_eta/K_eta",
                "connes_consani_object": "Tr(vartheta(f)S), K_I Toeplitz approximants",
                "match_status": "not_identified",
                "notes": "Trace positivity and finite Toeplitz approximants do not supply a faithful Calkin symbol for A_eta/K_eta.",
            },
        ],
    )

    write_csv(
        "branch_A_supplied_status_step212.csv",
        [
            {
                "branch_A_gate": "G2 faithful boundary symbol",
                "connes_consani_supply": "not supplied",
                "reason": "Section 6.2 gives finite Toeplitz matrices for K_I, not an infinite-dimensional faithful symbol on A_eta/K_eta.",
            },
            {
                "branch_A_gate": "G3 normal form C_l=U_l W_l+K_l",
                "connes_consani_supply": "not supplied",
                "reason": "Toeplitz co-rank-one decomposition applies to T_q/lambda Id - T_q, not to the cascade commutator C_l.",
            },
            {
                "branch_A_gate": "G4 lower-faithfulness",
                "connes_consani_supply": "not supplied",
                "reason": "No symbol map means no lower-faithfulness test for q_eta(C_l P_eta).",
            },
            {
                "branch_A_gate": "G5 compact remainder",
                "connes_consani_supply": "partial analogy only",
                "reason": "Their K_I is Hilbert-Schmidt/compact, but this does not identify the remainder in a normal form for C_l P_eta.",
            },
            {
                "branch_A_gate": "Calkin decision",
                "connes_consani_supply": "not decided",
                "reason": "Positivity of Tr(vartheta(f)S) is not equivalent to q_eta(C_l P_eta)=0 or nonzero.",
            },
        ],
    )

    write_csv(
        "relation_to_step_184_step212.csv",
        [
            {
                "topic": "Connes carrier status",
                "step_184_classification": "CRCFT-TE",
                "step_212_relation": "consistent",
                "notes": "Weil positivity is RH-equivalent in Connes-style programs; this paper strengthens/approximates that route but does not bypass target equivalence.",
            },
            {
                "topic": "Branch A Calkin symbol",
                "step_184_classification": "not a Branch A closure theorem",
                "step_212_relation": "related_but_not_sufficient",
                "notes": "The paper is valuable for Sonin/scaling positivity but does not construct the cascade quotient symbol.",
            },
        ],
    )

    print("Step 212 Connes-Consani audit")
    print(f"source={SOURCE}")
    print("Theorem 4.7: related positivity trace functional")
    print("Section 6.2: finite Toeplitz approximation for K_I")
    print("final_verdict=V_connes_consani_related_but_not_sufficient")


if __name__ == "__main__":
    main()
