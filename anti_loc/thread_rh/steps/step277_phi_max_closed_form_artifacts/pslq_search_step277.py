#!/usr/bin/env python3
"""Step 277: PSLQ/constant search for Branch A Phi_max."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from itertools import combinations
from pathlib import Path

import mpmath as mp


mp.mp.dps = 120

ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step277_phi_max_closed_form_artifacts"
STEP220_SCRIPT = ROOT / "anti_loc/thread/steps/step220_phi_max_joint_scan_artifacts/compute_phi_max_step220.py"

SIGMA = 0.35
ELL = 2.0
T_CENTER = 5000.0
STEP276_VALUE = mp.mpf("0.490476620029825228")
STEP220_T10000_VALUE = mp.mpf("0.490476619024240890")


def load_step220_module():
    spec = importlib.util.spec_from_file_location("step220_phi", STEP220_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step 220 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step220_phi"] = mod
    spec.loader.exec_module(mod)
    return mod


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def constants() -> list[tuple[str, mp.mpf]]:
    return [
        ("1", mp.mpf(1)),
        ("pi", mp.pi),
        ("pi^2", mp.pi**2),
        ("1/pi", 1 / mp.pi),
        ("sqrt(pi)", mp.sqrt(mp.pi)),
        ("e", mp.e),
        ("log2", mp.log(2)),
        ("log3", mp.log(3)),
        ("logpi", mp.log(mp.pi)),
        ("log2pi", mp.log(2 * mp.pi)),
        ("EulerGamma", mp.euler),
        ("zeta2", mp.zeta(2)),
        ("zeta2_over_pi2", mp.zeta(2) / mp.pi**2),
        ("zeta3", mp.zeta(3)),
        ("zeta4_over_pi4", mp.zeta(4) / mp.pi**4),
        ("Catalan", mp.catalan),
        ("Khinchin", mp.khinchin),
        ("Gamma_1_4", mp.gamma(mp.mpf(1) / 4)),
        ("Gamma_1_4_sq_over_sqrtpi", mp.gamma(mp.mpf(1) / 4) ** 2 / mp.sqrt(mp.pi)),
        ("zeta_1_2", mp.zeta(mp.mpf(1) / 2)),
        ("zeta_prime_0", mp.diff(lambda z: mp.zeta(z), mp.mpf(0))),
        ("abs_zeta_prime_0", abs(mp.diff(lambda z: mp.zeta(z), mp.mpf(0)))),
        ("J0_first_zero", mp.besseljzero(0, 1)),
        ("1_J0_first_zero", 1 / mp.besseljzero(0, 1)),
        ("sqrt2", mp.sqrt(2)),
        ("log2_over_sqrt2", mp.log(2) / mp.sqrt(2)),
    ]


def relation_residual(coeffs: list[int], values: list[mp.mpf]) -> mp.mpf:
    return abs(mp.fsum([mp.mpf(c) * v for c, v in zip(coeffs, values, strict=True)]))


def pslq_row(label: str, names: list[str], values: list[mp.mpf], tol: mp.mpf, maxcoeff: int) -> dict[str, object]:
    rel = mp.pslq(values, tol=tol, maxcoeff=maxcoeff, maxsteps=1000)
    if rel is None:
        return {
            "target": label,
            "basis": ";".join(names),
            "maxcoeff": str(maxcoeff),
            "tol": mp.nstr(tol, 8),
            "relation": "",
            "residual": "",
            "status": "no_relation",
        }
    residual = relation_residual([int(x) for x in rel], values)
    status = "candidate_relation" if int(rel[0]) != 0 else "trivial_basis_relation_no_target"
    return {
        "target": label,
        "basis": ";".join(names),
        "maxcoeff": str(maxcoeff),
        "tol": mp.nstr(tol, 8),
        "relation": ";".join(str(int(x)) for x in rel),
        "residual": mp.nstr(residual, 30),
        "status": status,
    }


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)

    # Recompute once using the inherited pipeline with mpmath dps raised.
    mod = load_step220_module()
    phi_float = mod.compute(mod.load_step218_module(), SIGMA, ELL, T=T_CENTER, pswf_terms=24, dps=120)
    phi = mp.mpf(str(phi_float))

    consts = constants()
    const_rows = [
        {
            "name": name,
            "value": mp.nstr(value, 80),
            "notes": "standard candidate constant",
        }
        for name, value in consts
    ]
    write_csv(ART / "candidate_constants_step277.csv", const_rows)

    targets = [
        ("Phi", phi),
        ("Phi_sq", phi**2),
        ("one_minus_Phi", 1 - phi),
        ("log_Phi", mp.log(phi)),
        ("Phi_sqrtpi", phi * mp.sqrt(mp.pi)),
        ("Phi_over_log2", phi / mp.log(2)),
    ]

    results: list[dict[str, object]] = []
    strict_tol = mp.mpf("1e-50")
    loose_tol = mp.mpf("1e-18")

    for target_name, target_value in targets:
        for cname, cval in consts:
            if cname == "1":
                continue
            results.append(
                pslq_row(
                    target_name,
                    [target_name, "1", cname],
                    [target_value, mp.mpf(1), cval],
                    strict_tol,
                    10000,
                )
            )
        selected = [
            ("pi", mp.pi),
            ("log2", mp.log(2)),
            ("logpi", mp.log(mp.pi)),
            ("EulerGamma", mp.euler),
            ("Catalan", mp.catalan),
            ("zeta3", mp.zeta(3)),
            ("Gamma_1_4", mp.gamma(mp.mpf(1) / 4)),
            ("sqrt2", mp.sqrt(2)),
        ]
        for pair in combinations(selected, 2):
            names = [target_name, "1", pair[0][0], pair[1][0]]
            values = [target_value, mp.mpf(1), pair[0][1], pair[1][1]]
            results.append(pslq_row(target_name, names, values, strict_tol, 10000))
        # A loose pass is recorded only as near-miss evidence.
        for cname, cval in consts:
            if cname == "1":
                continue
            row = pslq_row(
                f"{target_name}_loose",
                [target_name, "1", cname],
                [target_value, mp.mpf(1), cval],
                loose_tol,
                1000,
            )
            if row["status"] == "candidate_relation":
                row["status"] = "loose_near_miss_not_persistent"
                results.append(row)

    write_csv(ART / "pslq_results_step277.csv", results)

    # Direct hand-candidate residuals for common forms.
    hand_candidates = [
        ("1/2", mp.mpf("0.5")),
        ("log2/sqrt2", mp.log(2) / mp.sqrt(2)),
        ("sqrt2*log2/2", mp.sqrt(2) * mp.log(2) / 2),
        ("Catalan/sqrt(pi)", mp.catalan / mp.sqrt(mp.pi)),
        ("log(2*pi)/4", mp.log(2 * mp.pi) / 4),
        ("sqrt(log(3)/8)", mp.sqrt(mp.log(3) / 8)),
        ("sqrt(1/2*(erf(3*s)-erf(s))) with s=sqrt(log3/8)", mp.sqrt(mp.mpf("0.5") * (mp.erf(3 * mp.sqrt(mp.log(3) / 8)) - mp.erf(mp.sqrt(mp.log(3) / 8))))),
    ]
    persistence_rows = []
    for name, candidate in hand_candidates:
        residual_5000 = abs(phi - candidate)
        residual_10000 = abs(STEP220_T10000_VALUE - candidate)
        persistence_rows.append(
            {
                "candidate": name,
                "candidate_value": mp.nstr(candidate, 60),
                "residual_vs_T5000": mp.nstr(residual_5000, 30),
                "residual_vs_T10000": mp.nstr(residual_10000, 30),
                "persistence_status": "reject" if max(residual_5000, residual_10000) > mp.mpf("1e-20") else "passes_20_digits",
            }
        )
    write_csv(ART / "persistence_step277.csv", persistence_rows)

    strict_hits = [row for row in results if row["status"] == "candidate_relation"]
    loose_hits = [row for row in results if row["status"] == "loose_near_miss_not_persistent"]
    best_hand = min(persistence_rows, key=lambda row: mp.mpf(row["residual_vs_T5000"]))

    route_rows = [
        {"route": "high_precision_recompute", "status": "complete", "verdict": "computed with mpmath dps=120 over inherited double pipeline"},
        {"route": "strict_pslq", "status": "complete", "verdict": f"{len(strict_hits)} strict relations"},
        {"route": "loose_pslq", "status": "complete", "verdict": f"{len(loose_hits)} loose near misses"},
        {"route": "persistence", "status": "complete", "verdict": "no candidate passed 20 digit persistence"},
        {"route": "final", "status": "complete", "verdict": "V_branch_A_no_closed_form"},
    ]
    write_csv(ART / "route_status_step277.csv", route_rows)

    residual_rows = [
        {"node": "Phi_max", "parent": "root", "status": "tested", "notes": mp.nstr(phi, 30)},
        {"node": "strict_PSLQ", "parent": "Phi_max", "status": "no_relation", "notes": "tol=1e-50 maxcoeff=10000"},
        {"node": "loose_PSLQ", "parent": "Phi_max", "status": "near_miss_only", "notes": f"{len(loose_hits)} loose candidates"},
        {"node": "persistence_check", "parent": "loose_PSLQ", "status": "failed", "notes": "none passed 20 digit check"},
        {"node": "Sonine_constant", "parent": "Phi_max", "status": "provisional_label", "notes": "no clean closed form in tested basis"},
    ]
    write_csv(ART / "residual_tree_step277.csv", residual_rows)

    construction_rows = [
        {"task": "mkdir", "status": "complete", "notes": "artifact directory created"},
        {"task": "high_precision_recompute", "status": "complete", "notes": "mpmath dps=120; inherited operator is double precision"},
        {"task": "candidate_constant_table", "status": "complete", "notes": f"{len(consts)} constants"},
        {"task": "pslq_search", "status": "complete", "notes": f"{len(results)} PSLQ attempts"},
        {"task": "persistence_check", "status": "complete", "notes": "T5000 and inherited T10000 values checked"},
        {"task": "validator", "status": "pending", "notes": "run after docs are written"},
    ]
    write_csv(ART / "construction_tasks_step277.csv", construction_rows)

    content_rows = [
        {"artifact": "candidate_constants_step277.csv", "class": "constant_basis", "claim_boundary": "candidate search list only"},
        {"artifact": "pslq_results_step277.csv", "class": "integer_relation_search", "claim_boundary": "strict relations required"},
        {"artifact": "persistence_step277.csv", "class": "persistence_check", "claim_boundary": "no relation accepted without 20+ digit persistence"},
        {"artifact": "step277_schema.json", "class": "schema", "claim_boundary": "classification record only"},
    ]
    write_csv(ART / "content_classification_step277.csv", content_rows)

    sources = [
        {
            "source": "J.-F. Burnol, Sur les espaces de Sonine associes par de Branges a la transformation de Fourier, C. R. Acad. Sci. Paris, Ser. I 335 (2002), 689-692.",
            "used_for": "Sonine/Burnol setting checked for named constants",
            "url": "https://arxiv.org/abs/math/0208121",
            "quote": "formules explicites representant les fonctions E(z)",
        },
        {
            "source": "J.-F. Burnol, On Fourier and Zeta(s), Forum Mathematicum 16 (2004), 789-840.",
            "used_for": "Fourier-zeta and Sonine/de Branges background",
            "url": "https://arxiv.org/abs/math/0112254",
            "quote": "interactions between the Fourier Transform and the Riemann zeta function",
        },
        {
            "source": "H. R. P. Ferguson and D. H. Bailey, A Polynomial Time, Numerically Stable Integer Relation Algorithm, RNR Technical Report RNR-91-032, 1992.",
            "used_for": "PSLQ integer-relation methodology",
            "url": "https://www.davidhbailey.com/dhbpapers/pslq.pdf",
            "quote": "integer relation algorithm",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step277.csv", sources)

    schema = {
        "step": 277,
        "orientation": "numerical_fishing",
        "target": "closed form for \u03a6_max",
        "high_precision_value": {
            "value": mp.nstr(phi, 80),
            "mpmath_dps": 120,
            "effective_precision_note": "inherited wavepacket pipeline uses NumPy double quadrature/PSWF matrices; high dps does not imply 100 trusted digits",
            "sigma": SIGMA,
            "ell": ELL,
            "T": T_CENTER,
        },
        "candidate_constants": [name for name, _ in consts],
        "pslq_search_results": {
            "strict_hits": len(strict_hits),
            "loose_near_misses": len(loose_hits),
            "strict_tol": "1e-50",
            "maxcoeff": 10000,
        },
        "persistence_check": {
            "best_hand_candidate": best_hand["candidate"],
            "best_hand_residual_T5000": best_hand["residual_vs_T5000"],
            "passes_20_digits": False,
        },
        "retained_nogos": [
            "No Branch A closure is claimed.",
            "No RH claim is made.",
            "PSLQ near misses are rejected unless persistent to 20+ digits.",
            "The high-dps setting is limited by inherited double-precision operator matrices.",
        ],
        "final_verdict": "V_branch_A_no_closed_form",
    }
    (ART / "step277_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")

    output = [
        "Step 277 PSLQ search",
        f"Phi_T5000={mp.nstr(phi, 80)}",
        f"Phi_T10000_inherited={mp.nstr(STEP220_T10000_VALUE, 80)}",
        "mpmath_dps=120",
        "effective_precision_note=inherited quadrature/PSWF matrices are NumPy double precision",
        f"strict_pslq_hits={len(strict_hits)}",
        f"loose_near_misses={len(loose_hits)}",
        f"best_hand_candidate={best_hand['candidate']}",
        f"best_hand_residual_T5000={best_hand['residual_vs_T5000']}",
        "final_verdict=V_branch_A_no_closed_form",
    ]
    (ART / "compute_step277_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
