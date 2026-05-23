#!/usr/bin/env python3
"""Declare the de Bruijn-Newman residual carrier for Step 253."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step253_de_bruijn_newman_pivot_artifacts")


def write_csv(name: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with (ART / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    declaration = [{
        "carrier": "de Bruijn-Newman Lambda",
        "H_t_definition": "H_t(z)=int_0^infty exp(t u^2) Phi(u) cos(z u) du",
        "Phi_definition": "sum_{n>=1}(2*pi^2*n^4*exp(9u)-3*pi*n^2*exp(5u))*exp(-pi*n^2*exp(4u))",
        "Lambda_definition": "inf{t in R: all zeros of H_t are real}",
        "residual": "Xi_DBN=max(Lambda,0) after Rodgers-Tao Lambda>=0; closure Lambda<=0 equivalently Lambda=0",
        "closure": "Lambda=0 iff RH, using Rodgers-Tao lower bound plus de Bruijn-Newman equivalence"
    }]
    cre = [{
        "claim": "RH iff Lambda <= 0; Rodgers-Tao proves Lambda >= 0; hence RH iff Lambda = 0",
        "CRE_status": "CRE",
        "notes": "Closure is target-equivalent to RH, not a weaker native theorem."
    }]
    mode = [{
        "mode": "TE",
        "status": "selected",
        "reason": "The remaining closure Lambda<=0 is precisely RH-equivalent."
    }, {
        "mode": "CTMT",
        "status": "not_selected",
        "reason": "Heat-flow real-zero carrier is not reduced here to a carrier-native matrix-element terminal family."
    }, {
        "mode": "BF",
        "status": "not_selected",
        "reason": "A bridge to Sonine/Burnol is not needed for classification; direct target-equivalence suffices."
    }]
    bounds = [
        {"year": "1950", "source": "N. G. de Bruijn, The roots of trigonometric integrals", "bound_or_result": "monotonicity/real-zero persistence under heat flow; real zeros for sufficiently large t"},
        {"year": "1976", "source": "C. M. Newman, Fourier transforms with only real zeros", "bound_or_result": "existence of finite Lambda threshold; Newman conjecture Lambda>=0"},
        {"year": "2018", "source": "B. Rodgers and T. Tao, The de Bruijn-Newman constant is non-negative", "bound_or_result": "Lambda>=0"},
        {"year": "2019", "source": "D. H. J. Polymath, Effective approximation of heat flow evolution of the Riemann xi function", "bound_or_result": "Lambda<=0.22 unconditional"}
    ]

    write_csv("dbn_declaration_step253.csv", list(declaration[0]), declaration)
    write_csv("CRE_audit_step253.csv", list(cre[0]), cre)
    write_csv("CRCFT_mode_audit_step253.csv", ["mode", "status", "reason"], mode)
    write_csv("bounds_history_step253.csv", ["year", "source", "bound_or_result"], bounds)

    payload = {
        "carrier": declaration[0],
        "CRE_audit": cre,
        "CRCFT_mode": "TE",
        "bounds": bounds,
        "verdict": "V_de_Bruijn_Newman_CRCFT_TE",
    }
    (ART / "derive_dbn_residual_step253.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("de_bruijn_newman_carrier_declared")
    print("CRE_status=CRE")
    print("CRCFT_mode=TE")
    print("verdict=V_de_Bruijn_Newman_CRCFT_TE")


if __name__ == "__main__":
    main()
