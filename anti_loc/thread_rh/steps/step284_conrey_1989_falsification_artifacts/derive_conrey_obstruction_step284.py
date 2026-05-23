#!/usr/bin/env python3
"""Step 284: falsification attempt using Conrey 1989."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step284_conrey_1989_falsification_artifacts")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)

    conrey_verbatim = [
        {
            "source": "Conrey 1989, J. reine angew. Math. 399",
            "location": "Introduction",
            "verbatim": "at least 2/5 of the zeros of the Riemann zeta-function are simple and on the critical line.",
            "role": "main result",
        },
        {
            "source": "Conrey 1989",
            "location": "Introduction",
            "verbatim": "Our method is a refinement of the method Levinson",
            "role": "method provenance",
        },
        {
            "source": "Conrey 1989",
            "location": "Introduction",
            "verbatim": "the main new element here is the use of a mollifier",
            "role": "mollifier input",
        },
        {
            "source": "Conrey Bulletin 1989 announcement",
            "location": "Theorem 1",
            "verbatim": "At least 2/5 of the zeros of zeta(s) are simple and on the critical line.",
            "role": "announcement theorem",
        },
        {
            "source": "Bui-Conrey-Young 2011",
            "location": "Abstract",
            "verbatim": "at least 41.05% of the zeros of the Riemann zeta function are on the critical line.",
            "role": "later refinement",
        },
        {
            "source": "Bui-Conrey-Young 2011",
            "location": "Introduction",
            "verbatim": "With the use of a new two-piece mollifier, we make a modest improvement",
            "role": "incremental nature of refinement",
        },
        {
            "source": "Radziwill, Limitations to mollifying zeta(s)",
            "location": "Abstract",
            "verbatim": "We establish limitations to how well one can mollify zeta(s) on the critical line",
            "role": "method limitation context",
        },
    ]
    write_csv(ART / "conrey_verbatim_step284.csv", conrey_verbatim)

    method_cap = [
        {
            "method_feature": "Conrey 1989 certified output",
            "bound_or_limit": "2/5 = 40%",
            "evidence": "main theorem",
            "audit_status": "proved_positive_proportion_not_100",
        },
        {
            "method_feature": "Conrey numerical constant in later literature",
            "bound_or_limit": "kappa >= .4088",
            "evidence": "BCY 2011 introduction records current Conrey record",
            "audit_status": "below_half",
        },
        {
            "method_feature": "BCY 2011 two-piece mollifier",
            "bound_or_limit": "kappa >= .4105",
            "evidence": "BCY Theorem 1.1",
            "audit_status": "incremental_gain",
        },
        {
            "method_feature": "Feng/Robles-style refinements",
            "bound_or_limit": "about .4129 in cited conditional/refined computations",
            "evidence": "Levinson-Conrey refinement literature",
            "audit_status": "still_far_below_half",
        },
        {
            "method_feature": "audited mollifier-family practical ceiling",
            "bound_or_limit": "heuristic/asymptotic cap below 50%, often described around 49%",
            "evidence": "Bombieri-Hejhal/Levinson-Conrey method-cap folklore plus later limitation papers",
            "audit_status": "not_a_100_percent_path",
        },
        {
            "method_feature": "Radziwill limitation",
            "bound_or_limit": "nontrivial lower bound on mollified error I(M_theta)",
            "evidence": "limitations to mollifying zeta on the critical line",
            "audit_status": "mollifier_not_exact_inverse",
        },
    ]
    write_csv(ART / "method_cap_step284.csv", method_cap)

    comparison = [
        {
            "cascade_need": "RH closure: N0(T)/N(T) -> 1 and no off-line zeros",
            "conrey_supplies": "at least 2/5 critical-line zeros, simple",
            "status": "insufficient",
            "gap": "positive proportion does not exclude remaining off-line zeros",
        },
        {
            "cascade_need": "extend X% to 100%",
            "conrey_supplies": "Levinson-style mollifier refinement",
            "status": "not_derivable",
            "gap": "method gives lower bound, not equality of all zeros",
        },
        {
            "cascade_need": "Attack Foreclosure falsifier",
            "conrey_supplies": "strong literature theorem but below-half proportion",
            "status": "blocked",
            "gap": "requires fundamentally new idea or theorem beyond Conrey mollification",
        },
        {
            "cascade_need": "carrier closure for RH",
            "conrey_supplies": "mollified second-moment estimates and critical-line count",
            "status": "score_1",
            "gap": "no route from 40/41% to 100% in audited text",
        },
    ]
    write_csv(ART / "cascade_need_vs_supplied_step284.csv", comparison)

    pattern = [
        {"step": "267", "track": "RH", "candidate": "Burnol transport-sampling", "prior_score": "2", "audited_score": "1", "outcome": "downgrade"},
        {"step": "268", "track": "RH", "candidate": "Connes-Consani recoverability", "prior_score": "2", "audited_score": "1", "outcome": "downgrade"},
        {"step": "279", "track": "RH", "candidate": "Burnol a<1 form", "prior_score": "2", "audited_score": "1", "outcome": "downgrade"},
        {"step": "280", "track": "BSD", "candidate": "Skinner-Urban GL2 Iwasawa bridge", "prior_score": "2", "audited_score": "1", "outcome": "downgrade"},
        {"step": "281", "track": "Hodge", "candidate": "CDK Hodge-locus bridge", "prior_score": "2", "audited_score": "1", "outcome": "downgrade"},
        {"step": "282", "track": "NS", "candidate": "BKM blowup criterion", "prior_score": "2", "audited_score": "1", "outcome": "downgrade"},
        {"step": "283", "track": "P-vs-NP", "candidate": "Williams ACC lower bound", "prior_score": "2", "audited_score": "1", "outcome": "downgrade"},
        {"step": "284", "track": "RH", "candidate": "Conrey 1989 >2/5 critical zeros", "prior_score": "2", "audited_score": "1", "outcome": "downgrade_not_falsification"},
    ]
    write_csv(ART / "eight_of_eight_or_falsification_step284.csv", pattern)

    residual = [
        {"node": "Conrey_1989", "parent": "root", "status": "audited", "notes": "2/5 theorem extracted"},
        {"node": "positive_proportion", "parent": "Conrey_1989", "status": "proved", "notes": "critical-line lower bound"},
        {"node": "all_zeros_on_line", "parent": "positive_proportion", "status": "not_supplied", "notes": "remaining proportion uncontrolled"},
        {"node": "mollifier_extension_to_100", "parent": "all_zeros_on_line", "status": "blocked", "notes": "requires new method beyond audited Conrey/BCY program"},
        {"node": "RH_closure", "parent": "mollifier_extension_to_100", "status": "blocked", "notes": "no RH proof claimed"},
    ]
    write_csv(ART / "residual_tree_step284.csv", residual)

    route = [
        {"route": "fetch_Conrey", "status": "complete", "verdict": "J. reine/announcement PDFs fetched and text extracted"},
        {"route": "extract_theorem", "status": "complete", "verdict": "2/5 theorem and mollifier method recorded"},
        {"route": "fetch_BCY", "status": "complete", "verdict": "41.05% refinement recorded"},
        {"route": "test_100_percent_extension", "status": "blocked", "verdict": "no 100% route in audited literature"},
        {"route": "final", "status": "complete", "verdict": "V_conrey_RH_bridge_blocked"},
    ]
    write_csv(ART / "route_status_step284.csv", route)

    construction = [
        {"task": "mkdir", "status": "complete", "notes": "artifact directory created"},
        {"task": "fetch_sources", "status": "complete", "notes": "Conrey, BCY, Radziwill sources fetched"},
        {"task": "extract_theorem", "status": "complete", "notes": "Conrey 2/5 and BCY 41.05 recorded"},
        {"task": "falsification_test", "status": "complete", "notes": "no 100% path identified"},
        {"task": "write_docs", "status": "pending", "notes": "done after generator"},
        {"task": "run_validator", "status": "pending", "notes": "run after docs"},
    ]
    write_csv(ART / "construction_tasks_step284.csv", construction)

    sources = [
        {
            "source": "J. B. Conrey, More than two fifths of the zeros of the Riemann zeta-function are on the critical line, J. reine angew. Math. 399 (1989), 1-26.",
            "used_for": "primary 2/5 theorem and Levinson-mollifier method",
            "url": "https://www.maths.dur.ac.uk/users/herbert.gangl/morethan2_5.PDF",
            "quote": "at least 2/5 of the zeros",
        },
        {
            "source": "N. Levinson, More than one third of zeros of Riemann's zeta-function are on sigma=1/2, Adv. Math. 13 (1974), 383-436.",
            "used_for": "method provenance",
            "url": "https://doi.org/10.1016/0001-8708(74)90074-7",
            "quote": "more than one third",
        },
        {
            "source": "H. M. Bui, Brian Conrey, Matthew P. Young, More than 41% of the zeros of the zeta function are on the critical line, Acta Arith. 150 (2011), 35-64.",
            "used_for": "later refinement and current Conrey record context",
            "url": "https://arxiv.org/abs/1002.4127",
            "quote": "at least 41.05%",
        },
        {
            "source": "Maksym Radziwill, Limitations to mollifying zeta(s).",
            "used_for": "mollifier limitation context",
            "url": "https://www.math.mcgill.ca/radziwill/molliff43.pdf",
            "quote": "limitations to how well one can mollify",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step284.csv", sources)

    content = [
        {"artifact": "conrey_paper_extract_step284.md", "class": "paper_extract", "claim_boundary": "short theorem/method excerpts"},
        {"artifact": "conrey_verbatim_step284.csv", "class": "verbatim_ledger", "claim_boundary": "Conrey theorem recorded without promotion to RH"},
        {"artifact": "method_cap_step284.csv", "class": "method_limit_audit", "claim_boundary": "cap is heuristic/status audit, not a new theorem"},
        {"artifact": "cascade_need_vs_supplied_step284.csv", "class": "falsification_test", "claim_boundary": "no RH proof claimed"},
        {"artifact": "eight_of_eight_or_falsification_step284.csv", "class": "attack_foreclosure_evidence", "claim_boundary": "empirical pattern not theorem-grade"},
    ]
    write_csv(ART / "content_classification_step284.csv", content)

    schema = {
        "step": 284,
        "orientation": "falsification_attempt",
        "target": "Conrey 1989 positive-proportion critical-line zeros as RH bridge",
        "conrey_supplied": {
            "theorem": "at least 2/5 of the zeros are simple and on the critical line",
            "method": "Levinson-Conrey mollifier refinement",
        },
        "cascade_need": "100% of nontrivial zeta zeros on the critical line / RH closure",
        "method_cap_analysis": "Conrey/BCY/Feng-family refinements remain around 40-41%; audited mollifier-family status remains below 50 and no 100% path is supplied",
        "falsification_outcome": "no falsification; Conrey does not derive RH",
        "retained_nogos": [
            "No RH proof is claimed.",
            "Conrey's theorem is retained exactly as a positive-proportion theorem.",
            "BCY and related refinements remain positive-proportion results.",
            "The Attack Foreclosure Conjecture remains candidate/meta, not theorem-grade.",
        ],
        "final_verdict": "V_conrey_RH_bridge_blocked",
    }
    (ART / "step284_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print("verdict=V_conrey_RH_bridge_blocked")


if __name__ == "__main__":
    main()
