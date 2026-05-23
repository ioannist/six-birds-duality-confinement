#!/usr/bin/env python3
"""Step 280: audit Skinner-Urban 2014 as BSD score-2 bridge."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step280_BSD_score2_skinner_urban_artifacts")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)

    verbatim = [
        {
            "location": "Skinner-Urban 2014 abstract / Princeton record",
            "verbatim": "We prove the one-, two-, and three-variable Iwasawa-Greenberg Main Conjectures for a large class of modular forms that are ordinary with respect to an odd prime p.",
            "role": "scope of theorem",
        },
        {
            "location": "Introduction to Theorem 1",
            "verbatim": "Suppose f is ordinary; that is, a(p, f) is a p-adic unit",
            "role": "ordinary-at-p hypothesis",
        },
        {
            "location": "Theorem 1",
            "verbatim": "the reduction rho_bar_f of rho_f modulo the maximal ideal of O_L is irreducible",
            "role": "residual irreducibility hypothesis",
        },
        {
            "location": "Theorem 1",
            "verbatim": "there exists a prime q != p such that q||N and rho_bar_f is ramified at q",
            "role": "auxiliary ramification hypothesis",
        },
        {
            "location": "Theorem 1",
            "verbatim": "p does not divide N",
            "role": "good ordinary / level restriction",
        },
        {
            "location": "Theorem 1 conclusion",
            "verbatim": "Then Ch_Q_infty,L(f) = (L_f) in Lambda_Q,O_L tensor_Zp Q_p.",
            "role": "rationalized characteristic ideal equality",
        },
        {
            "location": "Theorem 1 integral equality add-on",
            "verbatim": "there exists an O_L-basis of T_f with respect to which the image of rho_f contains SL_2(Z_p)",
            "role": "big image condition for equality in Lambda",
        },
        {
            "location": "Theorem 2 elliptic curve hypotheses",
            "verbatim": "E has good ordinary reduction at p; rho_bar_E,p is irreducible; there exists a prime q != p such that q||N_E and rho_bar_E,p is ramified at q.",
            "role": "elliptic-curve application restrictions",
        },
        {
            "location": "Application note",
            "verbatim": "the hypotheses of the theorem are satisfied if E is semistable and p >= 11 is a prime of good ordinary reduction.",
            "role": "large but not all-primes scope",
        },
    ]
    write_csv(ART / "skinner_urban_verbatim_step280.csv", verbatim)

    excluded = [
        {
            "excluded_case": "non-ordinary primes",
            "reason": "the theorem assumes ordinary at p, e.g. a(p,f) is a p-adic unit / good ordinary reduction",
            "cascade_effect": "b-52a needs all-prime p-adic component control",
        },
        {
            "excluded_case": "bad or multiplicative primes not covered by the chosen theorem",
            "reason": "Theorem 1 assumes p does not divide N; elliptic application assumes good ordinary reduction",
            "cascade_effect": "does not close every local E_p component",
        },
        {
            "excluded_case": "residually reducible cases",
            "reason": "Theorem 1 and Theorem 2 require residual irreducibility",
            "cascade_effect": "global BSD bridge cannot exclude these cases",
        },
        {
            "excluded_case": "missing auxiliary ramification",
            "reason": "requires q||N with residual representation ramified at q",
            "cascade_effect": "does not apply uniformly to all elliptic curves",
        },
        {
            "excluded_case": "integral equality without big image",
            "reason": "equality in Lambda requires image containing SL_2(Z_p)",
            "cascade_effect": "component-level determinant identity remains conditional",
        },
    ]
    write_csv(ART / "hypotheses_excluded_step280.csv", excluded)

    comparison = [
        {
            "cascade_need": "all-primes E_p closure in b-52a residual",
            "skinner_urban_supplies": "p-ordinary Iwasawa-Greenberg main conjecture under hypotheses",
            "status": "insufficient",
            "gap": "non-ordinary and excluded primes/cases remain",
        },
        {
            "cascade_need": "unconditional determinant-line component vanishing",
            "skinner_urban_supplies": "Selmer characteristic ideal equals p-adic L-function in specified Iwasawa setting",
            "status": "partial_bridge",
            "gap": "ETNC/Bloch-Kato determinant identity not globally closed",
        },
        {
            "cascade_need": "BSD formula for all elliptic curves and ranks",
            "skinner_urban_supplies": "applications in rank-zero and Selmer corank consequence under hypotheses",
            "status": "insufficient",
            "gap": "does not prove full BSD for all curves/ranks",
        },
        {
            "cascade_need": "bridge from Iwasawa side to b-52a full residual zero",
            "skinner_urban_supplies": "strong external theorem for many ordinary GL2 forms",
            "status": "not_derivable",
            "gap": "requires new all-primes/all-cases bridge theorem",
        },
    ]
    write_csv(ART / "cascade_need_vs_supplied_step280.csv", comparison)

    pattern = [
        {"step": "267", "track": "RH", "candidate": "Burnol transport-sampling", "prior_score": "2", "audited_score": "1", "verdict": "blocked"},
        {"step": "268", "track": "RH", "candidate": "Connes-Consani recoverability", "prior_score": "2", "audited_score": "1", "verdict": "blocked"},
        {"step": "279", "track": "RH", "candidate": "Burnol a<1 form", "prior_score": "2", "audited_score": "1", "verdict": "blocked"},
        {"step": "280", "track": "BSD", "candidate": "Skinner-Urban GL2 Iwasawa bridge", "prior_score": "2", "audited_score": "1", "verdict": "blocked_for_full_bsd"},
    ]
    write_csv(ART / "four_of_four_pattern_step280.csv", pattern)

    residual = [
        {"node": "Skinner_Urban_2014", "parent": "root", "status": "audited", "notes": "paper theorem/hypotheses extracted"},
        {"node": "ordinary_GL2_IMC", "parent": "Skinner_Urban_2014", "status": "proved_under_hypotheses", "notes": "large class ordinary at odd p"},
        {"node": "all_primes_BSD_Ep", "parent": "ordinary_GL2_IMC", "status": "not_closed", "notes": "non-ordinary and excluded cases remain"},
        {"node": "b52a_global_residual", "parent": "all_primes_BSD_Ep", "status": "blocked", "notes": "requires new bridge theorem"},
    ]
    write_csv(ART / "residual_tree_step280.csv", residual)

    route = [
        {"route": "fetch_Skinner_Urban", "status": "complete", "verdict": "paper PDF/text fetched"},
        {"route": "extract_theorem", "status": "complete", "verdict": "Theorem 1 and elliptic application hypotheses recorded"},
        {"route": "compare_to_b52a", "status": "complete", "verdict": "partial bridge not all-primes closure"},
        {"route": "derive_full_BSD_bridge", "status": "blocked", "verdict": "requires extending excluded cases"},
        {"route": "final", "status": "complete", "verdict": "V_skinner_urban_BSD_bridge_blocked"},
    ]
    write_csv(ART / "route_status_step280.csv", route)

    construction = [
        {"task": "mkdir", "status": "complete", "notes": "artifact directory created"},
        {"task": "fetch_paper", "status": "complete", "notes": "Skinner-Urban PDF fetched from Urban Columbia page"},
        {"task": "extract_theorem", "status": "complete", "notes": "Theorem 1 and Theorem 2 restrictions recorded"},
        {"task": "gap_assessment", "status": "complete", "notes": "all-primes BSD bridge blocked"},
        {"task": "write_docs", "status": "pending", "notes": "done after generator"},
        {"task": "run_validator", "status": "pending", "notes": "run after docs"},
    ]
    write_csv(ART / "construction_tasks_step280.csv", construction)

    sources = [
        {
            "source": "Christopher Skinner and Eric Urban, The Iwasawa Main Conjectures for GL2, Inventiones Mathematicae 195 (2014), 1-277.",
            "used_for": "primary theorem and hypotheses",
            "url": "https://doi.org/10.1007/s00222-013-0448-1",
            "quote": "large class of modular forms that are ordinary with respect to an odd prime p",
        },
        {
            "source": "Skinner-Urban PDF, Columbia/Urban copy MC.pdf",
            "used_for": "Theorem 1 and Theorem 2 text extraction",
            "url": "https://www.math.columbia.edu/~urban/eurp/MC.pdf",
            "quote": "Theorem 1 (Theorem 3.6.4)",
        },
        {
            "source": "Xin Wan, Introduction to Skinner-Urban's Work on the Iwasawa Main Conjecture for GL2.",
            "used_for": "secondary orientation on proof scope",
            "url": "https://docslib.org/doc/11699480/introduction-to-skinner-urbans-work-on-the-iwasawa-main-conjecture-for",
            "quote": "proving (one divisibility of) the Iwasawa main conjecture for GL2/Q",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step280.csv", sources)

    content = [
        {"artifact": "skinner_urban_paper_extract_step280.md", "class": "paper_extract", "claim_boundary": "short theorem/hypothesis excerpts"},
        {"artifact": "skinner_urban_verbatim_step280.csv", "class": "verbatim_ledger", "claim_boundary": "hypotheses recorded without extension"},
        {"artifact": "hypotheses_excluded_step280.csv", "class": "exclusion_audit", "claim_boundary": "does not claim excluded cases impossible"},
        {"artifact": "cascade_need_vs_supplied_step280.csv", "class": "bridge_gap", "claim_boundary": "classification only"},
        {"artifact": "four_of_four_pattern_step280.csv", "class": "attack_foreclosure_evidence", "claim_boundary": "empirical pattern not theorem-grade"},
    ]
    write_csv(ART / "content_classification_step280.csv", content)

    schema = {
        "step": 280,
        "orientation": "cross_track_score2_audit",
        "target": "BSD score-2 Skinner-Urban Iwasawa bridge",
        "skinner_urban_supplied": {
            "theorem": "Iwasawa-Greenberg Main Conjecture for a large class of ordinary GL2 modular forms",
            "hypotheses": [
                "ordinary at odd p",
                "residual irreducibility",
                "auxiliary q||N ramification",
                "p not dividing N / good ordinary reduction in elliptic application",
                "big image for integral equality",
            ],
        },
        "cascade_need": "all-primes all-cases b-52a p-adic component and determinant residual closure",
        "gap_assessment": "NOT DERIVABLE as full BSD bridge; excluded cases remain; audited score-1",
        "four_of_four_pattern": pattern,
        "retained_nogos": [
            "No BSD proof is claimed.",
            "No RH proof is claimed.",
            "Skinner-Urban's theorem is not weakened; it is recorded as a strong conditional-scope external theorem.",
            "The b-52a all-primes bridge remains a new theorem obligation.",
        ],
        "final_verdict": "V_skinner_urban_BSD_bridge_blocked",
    }
    (ART / "step280_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "compute_step280_output.txt").write_text(
        "verdict=V_skinner_urban_BSD_bridge_blocked\n"
        "audited_score=1\n"
        "pattern=4_of_4_score2_downgrades_across_RH_and_BSD\n",
        encoding="utf-8",
    )
    print("verdict=V_skinner_urban_BSD_bridge_blocked")


if __name__ == "__main__":
    main()
