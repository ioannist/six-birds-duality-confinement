#!/usr/bin/env python3
"""Step 287 abc conjecture framework classification artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step287_abc_conjecture_artifacts")

VERDICT = "V_abc_11th_finding"


ABC_STATEMENT = (
    "For every epsilon > 0, only finitely many coprime positive integer triples "
    "(a,b,c) with a+b=c satisfy c > rad(abc)^(1+epsilon); equivalently, "
    "c <= K(epsilon) rad(abc)^(1+epsilon) for all such triples."
)


SOURCES = [
    {
        "key": "Oesterle_1987_1988",
        "citation": 'Joseph Oesterle, "Nouvelles approches du <<theoreme>> de Fermat," Seminaire Bourbaki 30 (1987-1988): 165-186.',
        "url": "https://eudml.org/doc/110094",
        "used_for": "Bourbaki source tying Fermat/Szpiro/abc context.",
    },
    {
        "key": "Masser_1985",
        "citation": 'D. W. Masser, "Open problems," in Proceedings of the Symposium on Analytic Number Theory, ed. W. W. L. Chen, Imperial College, London, 1985.',
        "url": "https://proofwiki.org/wiki/ABC_Conjecture",
        "used_for": "Masser origin citation; primary text not located in open full text during this step.",
    },
    {
        "key": "Vojta_1987",
        "citation": 'Paul Vojta, "Diophantine Approximations and Value Distribution Theory," Lecture Notes in Mathematics 1239, Springer, 1987.',
        "url": "https://link.springer.com/book/10.1007/BFb0072989",
        "used_for": "Height-theory and Vojta reformulation context.",
    },
    {
        "key": "Granville_Tucker_2002",
        "citation": 'Andrew Granville and Thomas J. Tucker, "It\'s As Easy As abc," Notices of the AMS 49 (10), 1224-1231, 2002.',
        "url": "https://www.ams.org/journals/notices/200210/fea-granville.pdf",
        "used_for": "Survey context and consequences.",
    },
    {
        "key": "Robert_Stewart_Tenenbaum_2014",
        "citation": 'O. Robert, C. L. Stewart and G. Tenenbaum, "A refinement of the abc conjecture," Bulletin of the London Mathematical Society 46 (2014), 1156-1166.',
        "url": "https://tenenb.perso.math.cnrs.fr/PPP/abc.pdf",
        "used_for": "Refinement, radical/squarefree-kernel formulation, computational-exception context.",
    },
    {
        "key": "Mochizuki_2021_IV",
        "citation": 'Shinichi Mochizuki, "Inter-universal Teichmuller Theory IV: Log-Volume Computations and Set-Theoretic Foundations," Publ. Res. Inst. Math. Sci. 57 (2021), no. 1/2, 627-723.',
        "url": "https://ems.press/journals/prims/articles/201528",
        "used_for": "IUT claimed proof context; classification does not rely on accepting the claim.",
    },
]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)

    schema = {
        "step": 287,
        "orientation": "adequacy",
        "target": "abc conjecture classification within framework",
        "abc_carrier_definition": {
            "carrier": "coprime integer triples (a,b,c) with a+b=c",
            "radical": "rad(n)=product of distinct prime divisors of n",
            "residual": "Xi_abc(K,epsilon)=count of coprime triples with c>K rad(abc)^(1+epsilon)",
            "closure": "for every epsilon>0, Xi_abc(K,epsilon) is finite for sufficiently large K",
        },
        "classification_decision": "not inside existing ten findings as a native instance; abstract meta-findings can audit abc strategies only after an abc carrier is supplied",
        "framework_finding_target": "candidate 11th finding: Integer-Diophantine Radical-Height Residual Family",
        "eleventh_finding_candidate": {
            "name": "Integer-Diophantine Radical-Height Residual Family",
            "status": "candidate; corpus-pending; verified-on-1-primary-instance plus adjacent Diophantine analogues",
            "primary_instance": "abc",
            "adjacent_instances": ["Hall", "Pillai", "Erdos-Straus", "Catalan/Mihailescu-style exponential Diophantine residuals"],
        },
        "retained_nogos": [
            "abc is not claimed solved",
            "Mochizuki IUT is recorded as a contested claimed proof, not as accepted closure",
            "existing L-function hierarchy is not stretched to absorb a Diophantine radical-height residual",
            "Attack Foreclosure remains strategy-level, not a theorem about abc truth",
        ],
        "final_verdict": VERDICT,
    }
    (ART / "step287_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")

    summary = f"""# Step 287 Results Summary

## abc Carrier

{ABC_STATEMENT}

Framework residual:

`Xi_abc(K, epsilon) = #{{(a,b,c): a+b=c, gcd(a,b,c)=1, c > K rad(abc)^(1+epsilon)}}`.

Closure means that for every `epsilon > 0`, sufficiently large `K(epsilon)` leaves no unbounded exceptional family; equivalently, only finitely many exceptional triples remain.

## Classification Decision

abc does not natively fit SCDG, Cross-Correlation, Subconvexity, or Zero-Density. Those are L-function/automorphic residual families: zero location, coefficient or zero correlations, critical-line growth/moments, and zero counts.

The abstract strategy findings (CTMT, CRCFT modes, Carrier Dichotomy, Bridge Impossibility, CTMT recursion, Attack Foreclosure) can audit an abc proof strategy once an abc carrier is declared, but they do not classify abc itself.

## 11th Finding Candidate

**Integer-Diophantine Radical-Height Residual Family (candidate).** Diophantine conjectures governed by additive relations, radicals/squarefree kernels, heights, and finiteness of exceptional integer tuples form a distinct typed family parallel to the Selberg/L-function hierarchy.

Primary evidence is abc. Adjacent analogues include Hall-type gaps, Pillai-type exponential Diophantine gaps, Erdos-Straus-style integer-tuple residuals, and Catalan/Mihailescu-style exceptional-power residuals. Evidence is not theorem-grade and remains corpus-pending.

## Literature Audit

Oesterle's Bourbaki article is indexed as `"Nouvelles approches du <<theoreme>> de Fermat"` with keywords including `abc-conjecture`. Masser 1985 is cited in standard bibliographies as `"Open problems"` in the Analytic Number Theory symposium proceedings. Vojta 1987 supplies the height-theory reformulation setting. Robert-Stewart-Tenenbaum 2014 states the radical/squarefree-kernel form and refinements. Mochizuki 2021 is recorded as a published claimed IUT route; this step does not treat it as settled community closure.

## Verdict

`{VERDICT}`.
"""
    (ART / "step287_results_summary.md").write_text(summary, encoding="utf-8")

    (ART / "content_classification_step287.csv").write_text(
        "artifact,classification,notes\n"
        "step287_results_summary.md,framework_classification,abc residual and verdict\n"
        "step287_schema.json,machine_schema,step metadata and verdict\n"
        "nonclaim_boundary_step287.md,nonclaim_boundary,no solved-claim boundary\n"
        "step287_abc_conjecture.tex,tex_summary,latex statement and classification\n"
        "analyze_abc_step287.py,repro_script,artifact generator\n"
        "run_step287_checks.py,validator,contract validation\n",
        encoding="utf-8",
    )

    nonclaim = """# Step 287 Nonclaim Boundary

- This step does not prove abc.
- This step does not accept Mochizuki/IUT as settled proof of abc; it records the claim as contested/published context only.
- This step does not claim abc is equivalent to RH, GRH, SCDG, Cross-Correlation, Subconvexity, or Zero-Density.
- This step does not weaken the retained no-gos: shadow non-promotion, scalar identity non-promotion, Bridge Impossibility, CTMT recursion, and Attack Foreclosure remain intact.
- The 11th finding is a corpus-pending classification candidate, not theorem-grade framework law.
"""
    (ART / "nonclaim_boundary_step287.md").write_text(nonclaim, encoding="utf-8")

    tex = r"""\section*{Step 287: abc Conjecture Classification}

Let $\operatorname{rad}(n)=\prod_{p\mid n}p$.  The abc conjecture asserts that for every
$\varepsilon>0$ there are only finitely many coprime positive integer triples
$(a,b,c)$ with $a+b=c$ and
\[
  c>\operatorname{rad}(abc)^{1+\varepsilon}.
\]
Equivalently, for every $\varepsilon>0$ there is a constant $K(\varepsilon)$ such that
\[
  c\le K(\varepsilon)\operatorname{rad}(abc)^{1+\varepsilon}.
\]

Define the residual
\[
\Xi_{\mathrm{abc}}(K,\varepsilon)=
\#\{(a,b,c): a+b=c,\ (a,b,c)=1,\ c>K\operatorname{rad}(abc)^{1+\varepsilon}\}.
\]
Closure is finiteness of the exceptional locus for every $\varepsilon>0$.

This residual is not an $L$-function zero-location, correlation, growth, moment, or
zero-density residual.  The abstract framework findings can audit proof strategies, but
they do not classify abc as a native instance.  The step therefore records a candidate
eleventh family: integer-Diophantine radical-height residuals, with abc as the primary
instance and Hall/Pillai/Erdos--Straus style residuals as adjacent analogues.

\[
\boxed{\texttt{V\_abc\_11th\_finding}}
\]
"""
    (ART / "step287_abc_conjecture.tex").write_text(tex, encoding="utf-8")

    write_csv(
        ART / "abc_declaration_step287.csv",
        [
            {
                "field": "carrier",
                "value": "coprime positive integer triples (a,b,c) with a+b=c",
                "status": "declared",
            },
            {"field": "radical", "value": "rad(n)=product of distinct prime divisors of n", "status": "declared"},
            {
                "field": "residual",
                "value": "Xi_abc(K,epsilon)=exceptional triple count above K rad(abc)^(1+epsilon)",
                "status": "declared",
            },
            {
                "field": "closure",
                "value": "finite exceptional set for every epsilon>0",
                "status": "open",
            },
        ],
    )

    write_csv(
        ART / "classification_step287.csv",
        [
            {"finding": "SCDG", "fit": "no", "reason": "abc is not per-L RH-analogue zero-location"},
            {"finding": "Cross-Correlation Extension", "fit": "no", "reason": "abc is not coefficient or zero correlation"},
            {"finding": "Subconvexity Extension", "fit": "no", "reason": "abc is not critical-line growth/moment residual"},
            {"finding": "Zero-Density Extension", "fit": "no", "reason": "abc is not zero-count residual"},
            {"finding": "CTMT/CRCFT/Carrier Dichotomy/Bridge/Attack Foreclosure", "fit": "abstract_only", "reason": "can audit proof strategies but do not natively type abc"},
            {"finding": "new candidate 11th", "fit": "yes", "reason": "integer triple radical-height finiteness residual is distinct"},
        ],
    )

    write_csv(
        ART / "eleventh_finding_audit_step287.csv",
        [
            {
                "candidate_name": "Integer-Diophantine Radical-Height Residual Family",
                "statement": "Additive integer relations plus radical/height controls define finiteness residuals distinct from Selberg/L-function residuals.",
                "primary_instance": "abc",
                "adjacent_instances": "Hall; Pillai; Erdos-Straus; Catalan/Mihailescu-style exceptional-power residuals",
                "status": "candidate_corpus_pending",
                "verdict": VERDICT,
            }
        ],
    )

    write_csv(
        ART / "residual_tree_step287.csv",
        [
            {"node": "abc_residual", "parent": "integer_diophantine_family", "status": "open", "note": "exceptional coprime triples"},
            {"node": "height_theory_bridge", "parent": "abc_residual", "status": "literature_adjacent", "note": "Vojta formulation context"},
            {"node": "IUT_claim", "parent": "abc_residual", "status": "contested", "note": "not promoted to closure"},
            {"node": "framework_11th_candidate", "parent": "abc_residual", "status": "candidate", "note": "classification output"},
        ],
    )

    write_csv(
        ART / "route_status_step287.csv",
        [
            {"route": "existing_L_function_hierarchy", "status": "blocked", "verdict": "not_native"},
            {"route": "abstract_strategy_findings", "status": "available_for_future_audit", "verdict": "not_classification"},
            {"route": "new_diophantine_family", "status": "candidate", "verdict": VERDICT},
        ],
    )

    write_csv(
        ART / "construction_tasks_step287.csv",
        [
            {"task": "mkdir_artifact_dir", "status": "complete", "note": str(ART)},
            {"task": "web_literature_audit", "status": "complete", "note": "Oesterle/Masser/Vojta/Granville-Tucker/Robert-Stewart-Tenenbaum/Mochizuki"},
            {"task": "classification_audit", "status": "complete", "note": VERDICT},
            {"task": "write_artifacts", "status": "complete", "note": "contract files generated"},
            {"task": "run_validator", "status": "pending", "note": "run_step287_checks.py"},
        ],
    )

    write_csv(ART / "classical_theorems_cited_step287.csv", SOURCES)

    print(VERDICT)


if __name__ == "__main__":
    main()
