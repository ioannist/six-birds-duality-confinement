import json, math, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step129_shifted_main_term_audit')
OUT.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Toy models: NOT RH evidence.
# -----------------------------
# We model the shifted main term after pole cancellation as
#     M_q ~= log(q) S_N + D_N,
# where S_N is the principal positive kernel and D_N is a bounded derivative/log kernel.
# Positivity is certified when log(q) * lambda_min(S_N) > ||D_N^-||.

rng = np.random.default_rng(129)

# Scenario grid for principal kernel floors and derivative defects
q_values = np.logspace(3, 18, 120)
scenarios = [
    {"name": "fixed_visibility_good", "s_floor": 0.35, "defect": 2.0},
    {"name": "fixed_visibility_low", "s_floor": 0.05, "defect": 2.0},
    {"name": "shrinking_visibility_poly", "s_floor": None, "defect": 2.0, "decay_exp": 0.15},
    {"name": "large_derivative_defect", "s_floor": 0.10, "defect": 8.0},
]

records = []
for sc in scenarios:
    for q in q_values:
        if sc.get("s_floor") is None:
            # Treat N ~ log q for the toy: s_floor shrinks polynomially in log q.
            N = max(2.0, math.log(q))
            s = N ** (-sc["decay_exp"])
        else:
            s = sc["s_floor"]
        defect = sc["defect"]
        lower = math.log(q) * s - defect
        gamma = max(lower, 0.0)
        records.append({
            "scenario": sc["name"],
            "q": q,
            "log_q": math.log(q),
            "principal_floor_s_N": s,
            "derivative_defect_norm": defect,
            "certified_lower_eigenvalue_model": lower,
            "positive_part_gamma_model": gamma,
            "passes_model_gate": lower > 0,
        })
phase_df = pd.DataFrame(records)
phase_df.to_csv(OUT / 'shifted_main_term_lower_frame_scenarios_step129.csv', index=False)

# Matrix sanity checks: construct random positive S and Hermitian defect D with known norm.
mat_records = []
for dim in [8, 16, 32, 64]:
    for s_floor in [0.02, 0.05, 0.1, 0.2]:
        for defect_norm in [1.0, 3.0, 6.0]:
            # random PSD perturbation plus floor
            X = rng.normal(size=(dim, dim))
            S = X.T @ X / dim
            eigS = np.linalg.eigvalsh(S)
            S += (s_floor - eigS.min()) * np.eye(dim)
            eigS = np.linalg.eigvalsh(S)
            # random Hermitian defect scaled to defect_norm with both signs
            Y = rng.normal(size=(dim, dim))
            D = (Y + Y.T) / 2
            normD = max(abs(np.linalg.eigvalsh(D)))
            if normD > 0:
                D *= defect_norm / normD
            for logq in [10, 25, 50, 100]:
                M = logq * S + D
                minM = np.linalg.eigvalsh(M).min()
                cert = logq * eigS.min() - defect_norm
                mat_records.append({
                    "dim": dim,
                    "s_floor_target": s_floor,
                    "s_min_actual": eigS.min(),
                    "defect_norm": defect_norm,
                    "log_q": logq,
                    "actual_min_eigenvalue": minM,
                    "weyl_certificate": cert,
                    "certificate_passes": cert > 0,
                    "actual_passes": minM > 0,
                })
mat_df = pd.DataFrame(mat_records)
mat_df.to_csv(OUT / 'matrix_main_term_weyl_checks_step129.csv', index=False)

# Gate tables
main_term_gate_rows = [
    ["G1_shifted_import", "Use BPRZ shifted theorem, not rederive AFE/off-diagonal analysis", "accepted import", "q prime, even primitive characters, kappa < 51/101, arbitrary coefficients with growth bounds"],
    ["G2_limit_alpha_beta", "Pass alpha,beta -> 0 without losing uniformity", "open/technical", "requires pole cancellation and derivative control on coefficient window"],
    ["G3_pole_cancellation", "Cancel zeta pole pair and extract finite central main term", "formula-level accepted", "must keep gamma/conductor factor and both zeta terms"],
    ["G4_principal_kernel_positive", "Show principal kernel S_N is positive with lower floor s_N", "open on residual class", "finite unweighted character identity helps but source-weighted main term needs eigenvalue audit"],
    ["G5_log_derivative_subordinate", "Bound derivative/log kernels by o(log q)*S_N or bounded H_N norm", "open", "main obstruction after pole cancellation"],
    ["G6_error_operator", "Published error term must be uniform in coefficient vector as operator norm", "open import", "scalar asymptotic is insufficient unless error is subordinate for all a"],
    ["G7_visibility_coupling", "Combine with c_hyb,N visibility floor", "conditional", "requires Burnol/Muentz shadow residual floor from prior steps"],
    ["G8_completed_tail", "Promote finite q,N windows to completed residual sector", "open", "requires fixed/exhaustive ledger tail"],
]
pd.DataFrame(main_term_gate_rows, columns=["gate", "description", "status", "record_needed"]).to_csv(OUT / 'shifted_main_term_gate_table_step129.csv', index=False)

platform_rows = [
    ["BPRZ 2018 twisted second moment", "Primary import", "arbitrary coefficients, q prime, even primitive characters, length q^kappa with kappa < 51/101", "Need main-term lower eigenvalue and uniform operator error"],
    ["CIS asymptotic large sieve", "Bilinear infrastructure", "primitive-character linear forms and conductor aspect", "Need lower-frame orientation, not only asymptotic/upper control"],
    ["Pratt-Robles perturbed moments", "t-aspect uniform-polynomial model", "general Dirichlet polynomial in perturbed moments", "Transfer to q-source carrier not automatic"],
    ["Tang-Wu 2025 hybrid mixed moments", "Later richer source weights", "hybrid/q aspect, primitive characters, power-saving asymptotic", "Requires matrix lower-frame translation"],
    ["Burnol Sonine/co-Poisson", "Carrier and visibility side", "L_a,K_a,P_a,Y_a and zero-evaluator completeness/minimality", "Supplies residual window and c_hyb,N, not gamma_q"],
]
pd.DataFrame(platform_rows, columns=["source", "role", "what_it_supplies", "remaining_framework_gate"]).to_csv(OUT / 'literature_import_table_step129.csv', index=False)

arith_rows = [
    ["alpha_beta_uniformity", "shift uniformity", "BPRZ supports small real parts and imaginary parts up to log q", "need controlled alpha,beta -> 0 expansion"],
    ["main_kernel", "principal main term", "two zeta-pole terms plus conductor/gamma factor", "prove lower eigenvalue on residual coefficient class"],
    ["derivative_kernel", "log/gamma/gcd derivative terms", "comes from pole cancellation expansion", "operator norm must be subordinate"],
    ["error", "published remainder", "O(q^-delta0) at asymptotic level", "need uniform operator-norm interpretation"],
    ["length", "coefficient support", "kappa < 51/101 for arbitrary coefficients", "must match Step 123/124 balanced length"],
    ["parity", "even characters", "theorem treats parity separately", "residual source must use matching parity sector"],
]
pd.DataFrame(arith_rows, columns=["input", "role", "imported_status", "framework_obligation"]).to_csv(OUT / 'arithmetic_input_table_step129.csv', index=False)

theorem_rows = [
    ["T1_shifted_import", "BPRZ shifted theorem gives source-weighted asymptotic for arbitrary coefficients", "imported", "not a lower frame by itself"],
    ["T2_pole_cancelled_main", "alpha,beta -> 0 yields finite main-term kernel M_q(0)", "derived/audit", "requires uniform expansion"],
    ["T3_lower_frame_certificate", "If M_q(0) >= c log(q) H_N and error subordinate, then G_q,w >= gamma H_N", "framework theorem", "conditional on T2 and positivity"],
    ["T4_visibility_coupled_source", "If R^*H R >= c_hyb G_R, then residual frame >= gamma c_hyb G_R", "accepted finite calculus", "completed tail remains"],
]
pd.DataFrame(theorem_rows, columns=["theorem", "statement", "status", "remarks"]).to_csv(OUT / 'theorem_map_step129.csv', index=False)

route_rows = [
    ["finite_unweighted_frame", "closed", "Step 125"],
    ["source_weighted_matrix_import", "partially imported", "BPRZ platform chosen"],
    ["shifted_main_term_positivity", "active/open", "Step 129"],
    ["operator_norm_error", "open", "must audit BPRZ remainder uniformly in a"],
    ["visibility_floor", "conditional", "from Burnol/Muentz shadow route"],
    ["completed_tail_promotion", "open", "fixed/exhaustive residual ledger"],
]
pd.DataFrame(route_rows, columns=["route_component", "status", "source_step"]).to_csv(OUT / 'route_status_step129.csv', index=False)

# Plots
plt.figure(figsize=(8,5))
for name, grp in phase_df.groupby('scenario'):
    plt.plot(grp['log_q'], grp['certified_lower_eigenvalue_model'], label=name)
plt.axhline(0, linestyle='--', linewidth=1)
plt.xlabel('log q')
plt.ylabel('model lower bound: log(q) s_N - ||D_N||')
plt.title('Shifted main-term lower-frame margin')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT / 'shifted_main_term_lower_frame_margin_step129.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
for name, grp in phase_df.groupby('scenario'):
    plt.plot(grp['log_q'], grp['positive_part_gamma_model'], label=name)
plt.xlabel('log q')
plt.ylabel('positive source strength model')
plt.title('Positive part after shifted main-term audit')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT / 'shifted_source_strength_model_step129.png', dpi=180)
plt.close()

# Heatmap phase for length/exponent type lower frame; here x-axis s_floor, y-axis defect/logq threshold
s_vals = np.linspace(0.01, 0.4, 80)
def_vals = np.linspace(0.5, 10, 80)
logq_fixed = 40
Z = np.zeros((len(def_vals), len(s_vals)))
for i,d in enumerate(def_vals):
    for j,s in enumerate(s_vals):
        Z[i,j] = logq_fixed*s - d
plt.figure(figsize=(7,5))
plt.imshow(Z, origin='lower', aspect='auto', extent=[s_vals.min(), s_vals.max(), def_vals.min(), def_vals.max()])
plt.colorbar(label='margin at log q=40')
plt.contour(s_vals, def_vals, Z, levels=[0], linewidths=1)
plt.xlabel('principal kernel floor s_N')
plt.ylabel('derivative/log defect norm')
plt.title('Main-term positivity phase diagram')
plt.tight_layout()
plt.savefig(OUT / 'main_term_positivity_phase_step129.png', dpi=180)
plt.close()

# Coupling with visibility floor
visibility = np.linspace(0.01, 1.0, 120)
logq = np.linspace(5, 80, 120)
VV, LL = np.meshgrid(visibility, logq)
Gamma = VV * LL  # if gamma_q ~ log q
plt.figure(figsize=(7,5))
plt.imshow(Gamma, origin='lower', aspect='auto', extent=[visibility.min(), visibility.max(), logq.min(), logq.max()])
plt.colorbar(label='effective gamma*c_hyb')
plt.contour(visibility, logq, Gamma, levels=[1,5,10,20], linewidths=0.8)
plt.xlabel('visibility floor c_hyb')
plt.ylabel('log q')
plt.title('Visibility-floor coupling to log q source growth')
plt.tight_layout()
plt.savefig(OUT / 'visibility_floor_coupling_step129.png', dpi=180)
plt.close()

# Nonclaim boundary
nonclaim = """# Step 129 nonclaim boundary

Step 129 does not prove RH and does not prove the source-weighted lower frame.

It does not claim that the Bui--Pratt--Robles--Zaharescu twisted second moment automatically implies a matrix lower frame. The imported theorem is scalar/bilinear in form; the project still needs a lower-eigenvalue audit of the shifted main term and an operator-norm subordinate error.

It does not re-derive the approximate functional equation, smooth cutoff error bounds, mollifier-length theory, or q-aspect off-diagonal analysis. Those are imported analytic-number-theory infrastructure.

It does not assume that the Burnol/Muentz visibility floor is positive. That remains the output of the prior residual-adequacy route.

It does not use target-selected source weights or zero-simplicity assumptions.
"""
(OUT / 'nonclaim_boundary_step129.md').write_text(nonclaim)

# Summary markdown
summary = r"""# Step 129 results summary

## Verdict

Step 129 audits the shifted main term from the q-aspect twisted second moment as a possible source-weighted matrix lower frame. The Bui--Pratt--Robles--Zaharescu theorem is the right import platform, but the lower-frame claim remains unearned until the shifted main term is shown to have a uniform lower eigenvalue and the error is subordinate in operator norm.

## Main reduction

Let

\[
G_{q,w}(m,n)=\sum_{\chi\in\mathcal X_q}w_\chi\chi(n)\overline{\chi(m)}.
\]

For the L-weighted source,

\[
w_\chi=|L(1/2,\chi)|^2.
\]

The BPRZ theorem gives an asymptotic for

\[
\frac{1}{\varphi^+(q)}\sum_{\chi\bmod q}^{+}
L(1/2+\alpha,\chi)L(1/2+\beta,\bar\chi)|A(\chi)|^2
\]

with arbitrary Dirichlet-polynomial coefficients and length \(q^\kappa\), \(\kappa<51/101\).

The framework needs this asymptotic in the matrix form

\[
a^*G_{q,w}a=M_q(a)+E_q(a),
\]

with

\[
M_q(a)\ge c_0\log q\,\|a\|_{H_q}^2,
\qquad
|E_q(a)|\le \varepsilon_q c_0\log q\,\|a\|_{H_q}^2
\]

for every residual coefficient vector \(a\).

## Shifted main-term audit

The BPRZ shifted main term has two pole-bearing pieces:

\[
\zeta(1+\alpha+\beta)S_{\alpha,\beta}(a)
+
X_q(\alpha,\beta)\zeta(1-\alpha-\beta)S_{-\beta,-\alpha}(a).
\]

As \(\alpha,\beta\to0\), the zeta poles must cancel. The finite main term should have the schematic shape

\[
M_q(0)= (\log q)S_0 + D_{\log}+O(1),
\]

where \(S_0\) is the principal positive kernel and \(D_{\log}\) is the derivative/log kernel.

A sufficient lower-frame certificate is

\[
\lambda_{\min}(S_0)\ge s_N>0,
\qquad
\|D_{\log}\|_{H_N}\le C_N,
\qquad
(\log q)s_N>C_N.
\]

Then

\[
M_q(0)\succeq ((\log q)s_N-C_N)H_N.
\]

## Main obstruction

The active task is not another finite character-orthogonality calculation.

It is:

\[
\boxed{\lambda_{\min}(H_N^{-1/2}M_q(0)H_N^{-1/2})\gg\log q.}
\]

This is the shifted main-term positivity gate.

## Coupling to the membrane route

If this gives

\[
G_{q,w}\succeq\gamma_qH_N,
\qquad \gamma_q\asymp\log q,
\]

and the Burnol/Muentz visibility route gives

\[
R_N^*H_NR_N\succeq c_{\rm hyb,N}G_{R,N},
\]

then

\[
R_N^*G_{q,w}R_N\succeq
\gamma_qc_{\rm hyb,N}G_{R,N}.
\]

A positive visibility floor is enough:

\[
c_{\rm hyb,N}\ge c_*>0
\quad\Rightarrow\quad
\gamma_qc_{\rm hyb,N}\to\infty.
\]

## Nonclaim

Step 129 does not prove the lower frame. It identifies exactly what must be checked in the shifted main term.
"""
(OUT / 'step129_results_summary.md').write_text(summary)

# LaTeX note
tex = r"""\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,enumitem,geometry,booktabs}
\geometry{margin=1in}
\title{Step 129: Shifted Main-Term Positivity Audit}
\author{Six Birds RH Membrane Program}
\date{}

\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newtheorem{warning}{Warning}

\begin{document}
\maketitle

\section{Purpose}
Step 128 selected the $q$-aspect twisted second moment with an arbitrary Dirichlet polynomial as the first source-weighted matrix-lower-frame import platform. Step 129 audits the shifted main term and asks whether it can be promoted to
\[
G_{q,w}\succeq \gamma_{q,w}H_N.
\]
The finite character frame is already settled. The analytic-number-theory infrastructure is imported, not re-derived.

\section{Imported theorem shape}
Let $q$ be prime and let
\[
A(\chi)=\sum_{n\le q^\kappa}\frac{a_n\chi(n)}{\sqrt n}.
\]
The imported Bui--Pratt--Robles--Zaharescu theorem studies
\[
I_{\alpha,\beta}
=
\frac{1}{\varphi^+(q)}\sum_{\chi\bmod q}^{+}
L(1/2+\alpha,\chi)L(1/2+\beta,\bar\chi)|A(\chi)|^2,
\]
for $\kappa<51/101$ and small shifts. Its main term has two zeta-pole pieces, schematically
\[
\zeta(1+\alpha+\beta)S_{\alpha,\beta}(a)
+
X_q(\alpha,\beta)\zeta(1-\alpha-\beta)S_{-\beta,-\alpha}(a).
\]

\section{Pole-cancelled central kernel}
Let $u=\alpha+\beta$. The pair
\[
\zeta(1+u),\qquad X_q(\alpha,\beta)\zeta(1-u)
\]
has cancelling simple poles as $u\to0$ once the two sides of the approximate functional equation are kept together. Therefore the central main term should be analyzed as a finite pole-cancelled matrix
\[
\mathsf M_q(0)=\lim_{\alpha,\beta\to0}\mathsf M_q(\alpha,\beta).
\]

\begin{definition}[Shifted main-term positivity gate]
The shifted main-term positivity gate passes on a coefficient window $(Y_N,H_N)$ if there are $s_N>0$ and $C_N\ge0$ such that
\[
\mathsf M_q(0)=(\log q)\mathsf S_N+\mathsf D_N,
\qquad
\mathsf S_N\succeq s_N H_N,
\qquad
\|\mathsf D_N\|_{H_N\to H_N}\le C_N,
\]
and
\[
(\log q)s_N>C_N.
\]
\end{definition}

\begin{proposition}[Weyl lower-frame certificate]
If the shifted main-term positivity gate passes, then
\[
\mathsf M_q(0)\succeq ((\log q)s_N-C_N)H_N.
\]
\end{proposition}
\begin{proof}
For any coefficient vector $a$,
\[
a^*\mathsf M_q(0)a
=(\log q)a^*\mathsf S_Na+a^*\mathsf D_Na
\ge ((\log q)s_N-C_N)\|a\|_{H_N}^2.
\]
\end{proof}

\section{What remains unearned}
The imported theorem is not automatically a lower-frame theorem. The framework still needs:
\begin{enumerate}[label=(\arabic*)]
\item uniform passage $\alpha,\beta\to0$;
\item explicit pole cancellation with both main-term pieces retained;
\item lower eigenvalue of the principal kernel $\mathsf S_N$;
\item operator-norm subordination of the derivative/log kernel $\mathsf D_N$;
\item operator-norm subordinate asymptotic error;
\item parity, primitive, and principal-character records;
\item completed residual-tail promotion.
\end{enumerate}

\section{Coupling to residual visibility}
If
\[
G_{q,w}\succeq\gamma_qH_N
\]
and the residual coefficient map satisfies
\[
R_N^*H_NR_N\succeq c_{\rm hyb,N}G_{R,N},
\]
then
\[
R_N^*G_{q,w}R_N\succeq \gamma_qc_{\rm hyb,N}G_{R,N}.
\]
Thus a positive visibility floor $c_{\rm hyb,N}\ge c_*>0$ suffices if $\gamma_q\to\infty$.

\section{Conclusion}
Step 129 reduces the BPRZ import to a precise question:
\[
\boxed{\lambda_{\min}\bigl(H_N^{-1/2}\mathsf M_q(0)H_N^{-1/2}\bigr)\gg\log q?}
\]
This is the shifted main-term positivity audit. It is the next genuine operator-valued gap.

\end{document}
"""
(OUT / 'shifted_main_term_positivity_step129.tex').write_text(tex)

schema = {
    "step": 129,
    "name": "Shifted main-term positivity audit",
    "active_object": "pole-cancelled BPRZ shifted main-term matrix M_q(0)",
    "main_gate": "lambda_min(H^{-1/2} M_q(0) H^{-1/2}) >> log q",
    "imported_infrastructure": [
        "BPRZ q-aspect twisted second moment with arbitrary coefficients",
        "standard AFE/off-diagonal/mollifier-length machinery",
        "finite prime-conductor character orthogonality"
    ],
    "framework_native_outputs": [
        "matrix lower-frame form",
        "visibility coupling gamma*c_hyb",
        "nonclaim/no-overread boundary",
        "tail promotion requirement"
    ],
    "artifacts": [p.name for p in OUT.iterdir() if p.is_file()]
}
(OUT / 'step129_schema.json').write_text(json.dumps(schema, indent=2))

# LaTeX structure check
text = tex
env_pairs = []
for env in ["document", "enumerate", "definition", "proposition", "proof"]:
    env_pairs.append({
        "environment": env,
        "begin_count": text.count(f"\\begin{{{env}}}"),
        "end_count": text.count(f"\\end{{{env}}}"),
        "balanced": text.count(f"\\begin{{{env}}}") == text.count(f"\\end{{{env}}}")
    })
pd.DataFrame(env_pairs).to_csv(OUT / 'latex_structure_check_step129.csv', index=False)

# Zip all artifacts
zip_path = OUT / 'step129_shifted_main_term_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for p in OUT.iterdir():
        if p.is_file() and p.name != zip_path.name:
            zf.write(p, arcname=p.name)
print(f"Wrote artifacts to {OUT}")
