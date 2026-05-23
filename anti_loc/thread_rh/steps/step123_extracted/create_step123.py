import os, json, math, csv, zipfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step123_balanced_length')
out.mkdir(parents=True, exist_ok=True)

step = 123

tex = r'''
\documentclass[11pt]{article}
\usepackage[a4paper,margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue}

\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{remark}{Remark}

\newcommand{\eps}{\varepsilon}
\newcommand{\XiBD}{\Xi^{\rm reg}_{BD,N}}
\newcommand{\XiBC}{\Xi^{\rm BC}}
\newcommand{\cH}{c_{{\rm hyb},N}}
\newcommand{\gN}{\gamma_N}
\newcommand{\LamN}{\Lambda_{R,N}}

\title{Step 123: Balanced-Length Theorem for the Regularized Müntz/co-Poisson Shadow}
\author{Riemann membrane construction notes}
\date{}

\begin{document}
\maketitle

\section{Purpose}
Steps 119--122 made the Burnol-to-Dirichlet readability problem lawful.  The naive critical-line partial sum of \(\zeta\) was rejected.  The accepted shadow is a regularized Müntz/co-Poisson shadow
\[
Z_X^\omega(s)
=\sum_{n\ge 1}\omega(n/X)n^{-s}-X^{1-s}\Omega(1-s),
\]
with the pole/Müntz correction included.  The associated readability defect is
\[
\delta^{\rm reg}_{BD,N}
=\bigl\|(I-P^{\rm reg}_{D,N})B_NG_{B,N}^{-1/2}\bigr\|.
\]
Step 123 isolates the new quantitative compatibility gate:
\[
\text{the shadow length must be large enough for Müntz accuracy,}
\]
while
\[
\text{the same length must remain short enough for the source moment theorem.}
\]
This is the balanced-length problem.

\section{Abstract data}
Let \(Y_{R,N}\) be a finite window of the residual sector of \(\Xi^{\rm BC}\).  Let \(B_N\) be the Burnol/co-Poisson response synthesis and let \(D_N^{\rm reg}(X_N)\) be the regularized Dirichlet-readable synthesis at length \(X_N\).  The full source route has the form
\[
G_{\mathcal X,N}\succeq \gamma_N H_N,
\qquad
R_N^*H_NR_N\succeq c_{{\rm hyb},N}G_{R,N},
\]
so that
\[
R_N^*G_{\mathcal X,N}R_N\succeq \gamma_Nc_{{\rm hyb},N}G_{R,N}.
\]
The goal is
\[
\gamma_Nc_{{\rm hyb},N}\to\infty
\]
with fixed/exhaustive tail promotion.

\section{Müntz shadow error model}
\begin{definition}[Müntz shadow parameters]
For a Burnol window \(N\), let
\[
T_N = \text{vertical/spectral height},
\qquad
A_N = \text{uniform Burnol atom complexity},
\]
and suppose the contour residual obeys
\[
\tau_{M,N}(X_N)
\le C_M A_N(1+T_N)^\alpha X_N^{-\eta}
\]
for fixed \(C_M,\alpha,\eta>0\).  Let
\[
\epsilon_{B,N}=\text{Burnol geometric exhaustion defect},
\]
\[
\epsilon_{\rm Mell,N}=\text{Mellin/Dirichlet modeling defect},
\]
\[
\kappa_{\rm tail,N}=\text{coefficient/support/tail defect}.
\]
Define
\[
E_N(X_N):=
\epsilon_{B,N}+\epsilon_{\rm Mell,N}+C_MA_N(1+T_N)^\alpha X_N^{-\eta}+\kappa_{\rm tail,N}.
\]
\end{definition}

By Step 122,
\[
\delta^{\rm reg}_{BD,N}\le \epsilon_{\rm Mell,N}+\tau_{M,N}(X_N)+\kappa_{\rm tail,N},
\]
and hence
\[
c_{{\rm hyb},N}\ge 1-E_N(X_N)^2.
\]

\section{Source length cap}
The source moment theorem is not available at arbitrary Dirichlet length.  We encode its admissible range by a scale \(Q_N\) and exponent \(\theta>0\):
\[
X_N\le Q_N^\theta.
\]
For example, in the Heap--Soundararajan lower-bound method, the source polynomials are deliberately short.  In their zeta setup the constructed Dirichlet polynomial has length bounded by a small power of the ambient scale, schematically \(\le T^{k/9}\).  In this note the analogous input is the black-box length cap \(X_N\le Q_N^\theta\).

\section{Balanced-length theorem}
\begin{theorem}[Balanced-length theorem]
Assume:
\begin{enumerate}[label=(\roman*)]
\item the regularized Müntz/co-Poisson shadow satisfies
\[
\delta^{\rm reg}_{BD,N}
\le
\epsilon_{\rm Mell,N}+C_MA_N(1+T_N)^\alpha X_N^{-\eta}+\kappa_{\rm tail,N};
\]
\item the source theorem is valid for lengths \(X_N\le Q_N^\theta\), with
\[
G_{\mathcal X,N}\succeq \gamma_NH_N;
\]
\item the finite residual windows have fixed/exhaustive tail promotion.
\end{enumerate}
If there exists a choice \(X_N\le Q_N^\theta\) such that
\[
E_N(X_N)<1
\]
and
\[
\gamma_N\bigl(1-E_N(X_N)^2\bigr)\to\infty,
\]
then the residual sector is source-absorbed:
\[
\Xi^{\rm BC}\preceq F_N+E_N^{\rm abs}
\]
with vanishing completed defect after tail promotion.
\end{theorem}

\begin{proof}
By the Step 122 angular-gap estimate,
\[
c_{{\rm hyb},N}\ge 1-E_N(X_N)^2.
\]
The finite matrix lower-frame theorem gives
\[
R_N^*G_{\mathcal X,N}R_N
\succeq
\gamma_Nc_{{\rm hyb},N}G_{R,N}
\succeq
\gamma_N\bigl(1-E_N(X_N)^2\bigr)G_{R,N}.
\]
If the last coefficient diverges and the finite residual windows promote through a fixed/exhaustive tail record, then the residual anti-invariant currency collapses on the completed residual sector.  This is precisely the source-absorption record for \(\Xi^{\rm BC}\). \end{proof}

\begin{corollary}[Maximal admissible shadow]
The best available choice under the source cap is \(X_N=Q_N^\theta\).  Thus a sufficient condition is
\[
\epsilon_{B,N}+\epsilon_{\rm Mell,N}+\kappa_{\rm tail,N}\to0,
\]
\[
A_N(1+T_N)^\alpha Q_N^{-\theta\eta}\to0,
\]
and
\[
\gamma_N\to\infty.
\]
Then
\[
c_{{\rm hyb},N}\to1,
\qquad
\gamma_Nc_{{\rm hyb},N}\to\infty.
\]
\end{corollary}

\begin{corollary}[Polynomial-growth phase boundary]
Suppose
\[
A_N\asymp Q_N^a,
\qquad
T_N\asymp Q_N^t.
\]
Then the Müntz contour residual can vanish under the source length cap only if
\[
\boxed{a+\alpha t<\theta\eta.}
\]
The boundary case \(a+\alpha t=\theta\eta\) gives no vanishing without additional logarithmic savings; the supercritical case
\[
a+\alpha t>\theta\eta
\]
forces a persistent readability defect under the declared source cap.
\end{corollary}

\begin{corollary}[Positive visibility floor]
Even if the visibility defect does not vanish, the source route may still close if there is a quantitative floor
\[
E_N(X_N)\le 1-\sigma_N,
\]
with
\[
\gamma_N\sigma_N\to\infty.
\]
Indeed
\[
1-E_N^2\ge 1-(1-\sigma_N)^2\ge \sigma_N.
\]
If \(\sigma_N\) decays too quickly for \(\gamma_N\) to compensate, the route remains support-only.
\end{corollary}

\section{Interpretation}
Step 123 turns the route into a three-way quantitative obligation:
\[
\boxed{\text{Burnol side: }\epsilon_{B,N}\to0,}
\]
\[
\boxed{\text{shadow side: }A_N(1+T_N)^\alpha X_N^{-\eta}\text{ small,}}
\]
\[
\boxed{\text{source side: }X_N\le Q_N^\theta\text{ and }\gamma_N\text{ grows}.}
\]
The decisive inequality is
\[
\boxed{A_N(1+T_N)^\alpha\ll Q_N^{\theta\eta}.}
\]
It says that the Burnol/Müntz window cannot be allowed to grow faster than the admissible short-polynomial length supplied by the source theorem.

\section{Nonclaims}
This step does not prove RH.  It does not prove the Heap--Soundararajan matrix lift.  It does not prove Burnol atom exhaustion.  It does not prove the Müntz angular gap.  It proves the conditional quantitative compatibility theorem that these ingredients must satisfy.

\end{document}
'''
(out/'muntz_balanced_length_step123.tex').write_text(tex)

summary = r'''
# Step 123: Balanced-Length Theorem

This step formalizes the quantitative compatibility gate between the regularized Müntz/co-Poisson shadow and Heap--Soundararajan-style source estimates.

The source route now has the form

\[
G_{\mathcal X,N}\succeq \gamma_NH_N,
\qquad
R_N^*H_NR_N\succeq c_{{\rm hyb},N}G_{R,N},
\]

so

\[
R_N^*G_{\mathcal X,N}R_N\succeq \gamma_Nc_{{\rm hyb},N}G_{R,N}.
\]

The route needs

\[
\gamma_Nc_{{\rm hyb},N}\to\infty.
\]

## Main error model

The regularized shadow error is bounded by

\[
E_N(X_N)
=
\epsilon_{B,N}
+
\epsilon_{{\rm Mell},N}
+C_MA_N(1+T_N)^\alpha X_N^{-\eta}
+
\kappa_{{\rm tail},N}.
\]

Here:

- \(\epsilon_{B,N}\) is Burnol geometric exhaustion error;
- \(\epsilon_{{\rm Mell},N}\) is Mellin/Dirichlet modeling error;
- \(C_MA_N(1+T_N)^\alpha X_N^{-\eta}\) is the Müntz contour residual;
- \(\kappa_{{\rm tail},N}\) is coefficient/support/tail defect.

The visibility lower bound is

\[
c_{{\rm hyb},N}\ge 1-E_N(X_N)^2.
\]

## Source length cap

Heap--Soundararajan-style moment technology works with short Dirichlet polynomials.  We encode this by

\[
X_N\le Q_N^\theta.
\]

Thus the same length \(X_N\) must be:

- large enough to make the Müntz shadow accurate;
- short enough for the source moment theorem.

## Main theorem

If there exists \(X_N\le Q_N^\theta\) such that

\[
E_N(X_N)<1
\]

and

\[
\gamma_N(1-E_N(X_N)^2)\to\infty,
\]

then the residual sector is source-absorbed after fixed/exhaustive tail promotion.

## Maximal-length sufficient condition

Choosing the largest admissible length

\[
X_N=Q_N^\theta
\]

gives the sufficient condition

\[
\epsilon_{B,N}+\epsilon_{{\rm Mell},N}+\kappa_{{\rm tail},N}\to0,
\]

\[
A_N(1+T_N)^\alpha Q_N^{-\theta\eta}\to0,
\]

and

\[
\gamma_N\to\infty.
\]

Then

\[
c_{{\rm hyb},N}\to1,
\qquad
\gamma_Nc_{{\rm hyb},N}\to\infty.
\]

## Polynomial phase boundary

If

\[
A_N\asymp Q_N^a,
\qquad
T_N\asymp Q_N^t,
\]

then the visibility side can vanish under the source cap only if

\[
\boxed{a+\alpha t<\theta\eta.}
\]

This is the balanced-length inequality.

## Meaning

The Müntz/co-Poisson shadow wants a long Dirichlet shadow.  The Heap--Soundararajan source theorem wants the Dirichlet polynomial to remain short.  Step 123 identifies the exact growth window in which both can hold.

## Status

This is conditional.  It does not prove RH, the matrix moment lower-frame theorem, Burnol atom exhaustion, or the angular-gap estimate.  It proves the quantitative compatibility theorem those ingredients must satisfy.
'''
(out/'step123_results_summary.md').write_text(summary)

# CSV tables
import pandas as pd

gate_rows = [
    {"gate":"regularized shadow", "condition":"delta_BD_reg <= eps_Mell + C_M A_N (1+T_N)^alpha X_N^{-eta} + kappa_tail", "status":"formalized", "failure":"unreadable Burnol-to-Dirichlet residual Xi_BD_reg"},
    {"gate":"source length cap", "condition":"X_N <= Q_N^theta", "status":"declared", "failure":"shadow needs a polynomial longer than source moment machinery allows"},
    {"gate":"visibility floor", "condition":"E_N(X_N)<1", "status":"required", "failure":"c_hyb lower bound collapses to zero"},
    {"gate":"effective source growth", "condition":"gamma_N (1-E_N(X_N)^2) -> infinity", "status":"required", "failure":"finite evidence only / no completed budget collapse"},
    {"gate":"tail promotion", "condition":"fixed/exhaustive residual tail", "status":"required", "failure":"moving-window support-only"},
    {"gate":"polynomial phase boundary", "condition":"a + alpha t < theta eta", "status":"sufficient in polynomial regime", "failure":"persistent Muntz readability defect under source cap"},
]
pd.DataFrame(gate_rows).to_csv(out/'balanced_length_gate_table_step123.csv', index=False)

criterion_rows = [
    {"regime":"vanishing shadow", "condition":"eps_B+eps_Mell+kappa_tail -> 0 and A_N(1+T_N)^alpha Q_N^{-theta eta}->0", "consequence":"c_hyb -> 1"},
    {"regime":"positive floor", "condition":"E_N <= 1 - sigma_N and gamma_N sigma_N -> infinity", "consequence":"source route can still close"},
    {"regime":"critical", "condition":"a+alpha t = theta eta", "consequence":"requires logarithmic savings or better regularization"},
    {"regime":"supercritical", "condition":"a+alpha t > theta eta", "consequence":"Muntz shadow too long for source method"},
    {"regime":"visibility collapse", "condition":"E_N >= 1 eventually", "consequence":"Xi_BD_reg must be separately absorbed or scoped out"},
]
pd.DataFrame(criterion_rows).to_csv(out/'balanced_length_criterion_table_step123.csv', index=False)

arith_rows = [
    {"input":"Burnol atom exhaustion", "symbol":"epsilon_B,N", "needed":"epsilon_B,N -> 0 or positive-floor budget", "source":"Burnol Sonine/co-Poisson completeness"},
    {"input":"Mellin/Dirichlet modeling", "symbol":"epsilon_Mell,N", "needed":"uniform angular-gap control on growing windows", "source":"regularized co-Poisson/Muntz construction"},
    {"input":"Muntz contour residual", "symbol":"C_M A_N(1+T_N)^alpha X_N^{-eta}", "needed":"small under source length cap", "source":"Muntz contour shift estimate"},
    {"input":"source length cap", "symbol":"X_N <= Q_N^theta", "needed":"black-box matrix moment theorem valid to this length", "source":"Heap-Soundararajan-style short polynomial technology"},
    {"input":"source lower frame", "symbol":"gamma_N", "needed":"gamma_N grows enough to overcome visibility floor", "source":"operator-valued lift of moment lower bounds"},
    {"input":"completed tail promotion", "symbol":"T_R,N", "needed":"fixed/exhaustive ledger tail vanishes", "source":"membrane Step 65-67 discipline"},
]
pd.DataFrame(arith_rows).to_csv(out/'arithmetic_input_table_step123.csv', index=False)

theorem_rows = [
    {"label":"BLT", "name":"Balanced-length theorem", "statement":"If X_N <= Q_N^theta, E_N(X_N)<1, and gamma_N(1-E_N^2)->infinity, then residual source absorption closes after tail promotion."},
    {"label":"ML", "name":"Maximal admissible length corollary", "statement":"With X_N=Q_N^theta, vanishing base errors and A_N(1+T_N)^alpha Q_N^{-theta eta}->0 imply c_hyb->1."},
    {"label":"PB", "name":"Polynomial boundary corollary", "statement":"If A_N~Q^a and T_N~Q^t, then vanishing Muntz error under source cap requires a+alpha t < theta eta."},
    {"label":"PF", "name":"Positive floor corollary", "statement":"If E_N <= 1-sigma_N and gamma_N sigma_N->infinity, source absorption can still close."},
]
pd.DataFrame(theorem_rows).to_csv(out/'theorem_map_step123.csv', index=False)

route_rows = [
    {"route":"Muntz shadow complete", "status":"conditional", "next_obligation":"prove angular-gap errors vanish within length cap"},
    {"route":"positive visibility floor", "status":"possible", "next_obligation":"prove gamma_N compensates floor decay"},
    {"route":"shadow supercritical", "status":"blocked for current source theorem", "next_obligation":"improve regularization or use longer moment technology"},
    {"route":"missed shadow residual", "status":"fallback", "next_obligation":"separate source absorption for Xi_BD_reg"},
]
pd.DataFrame(route_rows).to_csv(out/'route_status_step123.csv', index=False)

nonclaim = r'''
# Step 123 nonclaim boundary

Step 123 does not prove the Riemann Hypothesis.

It does not prove the Heap--Soundararajan matrix lower-frame lift.

It does not prove Burnol/co-Poisson atom exhaustion.

It does not prove the Müntz/co-Poisson angular-gap estimate.

It does not prove that the regularized Burnol-to-Dirichlet shadow defect vanishes.

It proves a conditional compatibility theorem: if the Müntz shadow can be made accurate at a length still allowed by the source moment theorem, and if the effective source strength diverges after visibility losses, then residual source absorption is formally available.

Any finite-window calculation remains support-only without fixed/exhaustive tail promotion.
'''
(out/'nonclaim_boundary_step123.md').write_text(nonclaim)

schema = {
    "step": 123,
    "title": "Balanced-Length Theorem for the Regularized Müntz/co-Poisson Shadow",
    "objects": {
        "E_N": "epsilon_B,N + epsilon_Mell,N + C_M A_N (1+T_N)^alpha X_N^{-eta} + kappa_tail,N",
        "source_cap": "X_N <= Q_N^theta",
        "visibility": "c_hyb,N >= 1 - E_N^2",
        "effective_strength": "Lambda_R,N = gamma_N c_hyb,N",
        "polynomial_boundary": "a + alpha t < theta eta"
    },
    "accepted_if": [
        "there exists X_N <= Q_N^theta with E_N(X_N)<1",
        "gamma_N*(1-E_N(X_N)^2) -> infinity",
        "fixed/exhaustive residual tail promotion passes"
    ],
    "fallbacks": [
        "positive visibility floor compensated by gamma_N",
        "improve regularization to reduce alpha or increase eta",
        "longer source moment technology to increase theta",
        "separate source absorption of missed Xi_BD_reg"
    ]
}
(out/'step123_schema.json').write_text(json.dumps(schema, indent=2))

# numerical models
Q = np.logspace(2, 10, 300)
alpha = 2.0
eta = 1.0
theta = 0.22
CM = 1.0
# scenarios: (name, a, t, base_error, gamma_power)
scenarios = [
    ("feasible", 0.02, 0.06, 0.08, 1.0),
    ("near_boundary", 0.08, 0.07, 0.12, 1.0),
    ("supercritical", 0.12, 0.08, 0.12, 1.0),
    ("positive_floor", 0.10, 0.055, 0.40, 1.0),
]
rows=[]
for name,a,t,base,gpow in scenarios:
    muntz = CM*(Q**a)*(1+Q**t)**alpha*(Q**(-theta*eta))
    E = np.minimum(1.5, base + muntz)
    c = np.maximum(0, 1-E**2)
    gamma = np.log(Q)**gpow
    Lam = gamma*c
    for i in [0, 75, 150, 225, 299]:
        rows.append({"scenario":name,"Q":Q[i],"a":a,"t":t,"E":E[i],"c_hyb_lower":c[i],"gamma":gamma[i],"effective_strength":Lam[i],"phase_value":a+alpha*t,"boundary":theta*eta})
pd.DataFrame(rows).to_csv(out/'balanced_length_scenario_values_step123.csv', index=False)

# Plot 1: phase diagram
A_vals = np.linspace(0, 0.35, 200)
T_vals = np.linspace(0, 0.20, 200)
AA, TT = np.meshgrid(A_vals, T_vals)
phase = AA + alpha*TT - theta*eta
plt.figure(figsize=(7,5))
plt.contourf(AA, TT, phase<0, levels=[-0.5,0.5,1.5], alpha=0.6)
plt.contour(AA, TT, phase, levels=[0], linewidths=2)
plt.xlabel('atom complexity exponent a')
plt.ylabel('vertical window exponent t')
plt.title('Balanced-length feasible region: a + alpha t < theta eta')
plt.tight_layout()
plt.savefig(out/'balanced_length_phase_region_step123.png', dpi=200)
plt.close()

# Plot 2: total defect
plt.figure(figsize=(7,5))
for name,a,t,base,gpow in scenarios:
    E = base + CM*(Q**a)*(1+Q**t)**alpha*(Q**(-theta*eta))
    plt.loglog(Q, E, label=name)
plt.axhline(1, linestyle='--')
plt.xlabel('source scale Q_N')
plt.ylabel('total shadow defect E_N at X_N=Q_N^theta')
plt.title('Regularized shadow defect under source length cap')
plt.legend()
plt.tight_layout()
plt.savefig(out/'shadow_defect_under_length_cap_step123.png', dpi=200)
plt.close()

# Plot 3: visibility lower bound
plt.figure(figsize=(7,5))
for name,a,t,base,gpow in scenarios:
    E = base + CM*(Q**a)*(1+Q**t)**alpha*(Q**(-theta*eta))
    c = np.maximum(0, 1-E**2)
    plt.semilogx(Q, c, label=name)
plt.xlabel('source scale Q_N')
plt.ylabel('lower bound for c_hyb,N')
plt.title('Hybrid visibility lower bound')
plt.legend()
plt.tight_layout()
plt.savefig(out/'visibility_lower_bound_step123.png', dpi=200)
plt.close()

# Plot 4: effective source strength
plt.figure(figsize=(7,5))
for name,a,t,base,gpow in scenarios:
    E = base + CM*(Q**a)*(1+Q**t)**alpha*(Q**(-theta*eta))
    c = np.maximum(0, 1-E**2)
    gamma = np.log(Q)**gpow
    Lam = gamma*c
    plt.semilogx(Q, Lam, label=name)
plt.xlabel('source scale Q_N')
plt.ylabel('gamma_N c_hyb,N')
plt.title('Effective source strength after visibility loss')
plt.legend()
plt.tight_layout()
plt.savefig(out/'effective_source_strength_step123.png', dpi=200)
plt.close()

# Plot 5: length tradeoff
Q2 = np.logspace(3,10,200)
base = 0.05
err_target = 0.1
trade_rows=[]
plt.figure(figsize=(7,5))
for name,a,t,_,_ in scenarios[:3]:
    Acomp = Q2**a
    Tcomp = Q2**t
    X_req = (CM*Acomp*(1+Tcomp)**alpha/err_target)**(1/eta)
    X_max = Q2**theta
    ratio = X_req / X_max
    plt.loglog(Q2, ratio, label=name)
    for i in [0, 80, 160, 199]:
        trade_rows.append({"scenario":name,"Q":Q2[i],"X_required_for_target_error":X_req[i],"X_max_source_cap":X_max[i],"ratio":ratio[i]})
plt.axhline(1, linestyle='--')
plt.xlabel('source scale Q_N')
plt.ylabel('X_required / X_max')
plt.title('Length tradeoff: Müntz accuracy vs source cap')
plt.legend()
plt.tight_layout()
plt.savefig(out/'length_tradeoff_step123.png', dpi=200)
plt.close()
pd.DataFrame(trade_rows).to_csv(out/'length_tradeoff_step123.csv', index=False)

# Plot 6: source cap with positive floor threshold
sigma = np.array([1/np.log(q)**r for r in [0.5, 1.0, 2.0] for q in []])
plt.figure(figsize=(7,5))
for r in [0.5, 1.0, 2.0]:
    sig = 1/np.log(Q)**r
    gamma = np.log(Q)
    plt.semilogx(Q, gamma*sig, label=f'sigma=(log Q)^-{r}')
plt.xlabel('source scale Q_N')
plt.ylabel('gamma_N sigma_N with gamma_N=log Q')
plt.title('Positive visibility floor compensation')
plt.legend()
plt.tight_layout()
plt.savefig(out/'positive_floor_compensation_step123.png', dpi=200)
plt.close()

# Check script
check_script = r'''#!/usr/bin/env python3
"""Sanity checks for Step 123 balanced-length formulas."""
import numpy as np

alpha=2.0
eta=1.0
theta=0.22
Q=np.logspace(2,10,50)

def total_error(Q,a,t,base=0.1):
    return base + (Q**a)*(1+Q**t)**alpha*(Q**(-theta*eta))

# Feasible polynomial regime should have decreasing Muntz component.
a,t=0.02,0.06
assert a+alpha*t < theta*eta
E=total_error(Q,a,t,base=0.05)
assert E[-1] < E[0]

# Supercritical polynomial regime should eventually grow.
a,t=0.12,0.08
assert a+alpha*t > theta*eta
E=total_error(Q,a,t,base=0.05)
assert E[-1] > E[0]

# Positive floor: if E <= 1-sigma then c >= sigma for sigma in (0,1).
for sigma in [0.1,0.3,0.7]:
    E=1-sigma
    c=1-E*E
    assert c >= sigma

print('Step 123 balanced-length checks passed.')
'''
(out/'run_balanced_length_step123.py').write_text(check_script)
os.chmod(out/'run_balanced_length_step123.py',0o755)

# zip artifacts
zip_path = out/'step123_balanced_length_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name == zip_path.name: continue
        z.write(p, p.name)

print('created', out)
