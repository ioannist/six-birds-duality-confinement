import os, json, math, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step136_response_metric_incidence')
out.mkdir(parents=True, exist_ok=True)

# --- helpers ---
def primes_upto(n):
    sieve = bytearray(b'\x01')*(n+1)
    if n>=0: sieve[0]=0
    if n>=1: sieve[1]=0
    for i in range(2,int(n**0.5)+1):
        if sieve[i]:
            step=i
            start=i*i
            sieve[start:n+1:step]=b'\x00'*(((n-start)//step)+1)
    return [i for i in range(2,n+1) if sieve[i]]

def sigma_plus(r):
    # Singular value of [[1,0],[r,1]] with r >= 0
    lam = 1 + 0.5*r*r + r*math.sqrt(1 + 0.25*r*r)
    return math.sqrt(lam)

def sigma_minus(r):
    return 1.0/sigma_plus(r)

ys = [10,20,30,50,75,100,150,200,300,500,750,1000,1500,2000,3000,5000,7500,10000]
phi = (1+math.sqrt(5))/2
rows=[]
for y in ys:
    ps = primes_upto(y)
    k = len(ps)
    log_raw = k*math.log(phi)
    log_weighted = sum(math.log(sigma_plus(p**-0.5)) for p in ps)
    sum_r = sum(p**-0.5 for p in ps)
    sum_inv = sum(1/p for p in ps)
    req_exact = math.exp(-log_weighted)
    req_floor_half = 0.5*math.exp(-log_weighted)
    rows.append(dict(y=y, prime_count=k, log_raw_boolean_norm=log_raw,
                     raw_boolean_norm=math.exp(log_raw) if log_raw<700 else np.inf,
                     log_response_weighted_norm=log_weighted,
                     response_weighted_norm=math.exp(log_weighted),
                     sum_p_minus_half=sum_r, sum_p_minus_one=sum_inv,
                     required_seed_tail_for_vanish=req_exact,
                     required_seed_tail_for_delta_half=req_floor_half,
                     log_norm_ratio=log_raw-log_weighted))
amp = pd.DataFrame(rows)
amp.to_csv(out/'incidence_amplification_table_step136.csv', index=False)

# Single prime singular values
ps = primes_upto(2000)
svp = pd.DataFrame([dict(p=p, r=p**-0.5, sigma_plus=sigma_plus(p**-0.5), sigma_minus=sigma_minus(p**-0.5), log_sigma_plus=math.log(sigma_plus(p**-0.5))) for p in ps])
svp.to_csv(out/'single_prime_singular_values_step136.csv', index=False)

# Tail scenarios: model e_omega = exp(-c sqrt(y)/log y) or y^{-A}
rows=[]
for y in ys[4:]:
    ps = primes_upto(y)
    logA = sum(math.log(sigma_plus(p**-0.5)) for p in ps)
    scale = math.sqrt(y)/max(1, math.log(y))
    for c in [0.25,0.5,1.0,1.5,2.0,3.0]:
        e = math.exp(-c*scale)
        tau = min(1e100, math.exp(logA)*e)
        c_floor = max(0.0, 1-tau*tau) if tau<1e50 else 0.0
        rows.append(dict(y=y, model='exp(-c sqrt(y)/log y)', parameter=c, log_incidence_norm=logA, seed_tail=e, incidence_conditioned_tail=tau, visibility_floor=c_floor))
    for A in [0.5,1,2,4,8]:
        e = y**(-A)
        tau = math.exp(logA)*e
        c_floor = max(0.0, 1-tau*tau)
        rows.append(dict(y=y, model='y^{-A}', parameter=A, log_incidence_norm=logA, seed_tail=e, incidence_conditioned_tail=tau, visibility_floor=c_floor))
tail = pd.DataFrame(rows)
tail.to_csv(out/'tail_requirement_scenarios_step136.csv', index=False)

# Effective source strength scenarios gamma = log q, q = exp(y/kappa?) Simple models
rows=[]
for y in ys[5:]:
    logA = amp[amp.y==y].log_response_weighted_norm.iloc[0]
    scale=math.sqrt(y)/math.log(y)
    for c in [1.0,2.0,3.0]:
        seed_tail = math.exp(-c*scale)
        delta = math.exp(logA)*seed_tail
        visibility = max(0, 1-delta**2) if delta < 1e40 else 0
        for logq_factor in [1,2,4,8,16]:
            # pretend log q = factor*y; gamma ~ log q
            gamma = logq_factor*y
            eff = gamma*visibility
            rows.append(dict(y=y, tail_c=c, logq_factor=logq_factor, seed_tail=seed_tail, delta=delta, visibility_floor=visibility, gamma_model=gamma, effective_source_strength=eff))
eff=pd.DataFrame(rows)
eff.to_csv(out/'effective_source_strength_scenarios_step136.csv', index=False)

# gate tables
gate_rows = [
    dict(gate='R1_response_metric_declared', status='accepted_formula', obligation='Declare whether coefficient space uses raw Boolean l2, Dirichlet H=sum |a_n|^2/n, or semilocal/Burnol response metric before measuring Z_y.'),
    dict(gate='R2_metric_normalized_incidence', status='proved_finite', obligation='Conjugate Z_y by the response weight; for H=sum |a_n|^2/n the local block is [[1,0],[p^{-1/2},1]].'),
    dict(gate='R3_amplification_bound', status='proved_finite', obligation='Use A_y=prod_{p<=y} sigma_+(p^{-1/2}) rather than raw phi^{pi(y)}.'),
    dict(gate='R4_tail_after_incidence', status='open_analytic', obligation='Prove ||Z_y(I-P_{Omega<=K})B_NG_B^{-1/2}|| <= tau_N for actual Burnol/Muntz windows.'),
    dict(gate='R5_positive_floor', status='conditional', obligation='If A_y e_{Omega,N} <= delta < 1, restricted BPRZ lower-frame survives with floor 1-delta^2.'),
    dict(gate='R6_completed_tail_promotion', status='not_yet_earned', obligation='Promote finite y/q windows to completed residual ledger with fixed/exhaustive tail control.'),
]
pd.DataFrame(gate_rows).to_csv(out/'response_metric_gate_table_step136.csv', index=False)

theorem_rows = [
    dict(name='Metric-normalized incidence factorization', statement='For H_y with squarefree weight w(S)=prod_{p in S}p^{-1}, W^{1/2}Z_yW^{-1/2}=tensor_{p<=y} [[1,0],[p^{-1/2},1]].', status='proved_finite'),
    dict(name='Weighted incidence norm', statement='||Z_y||_{H_y->H_y}=prod_{p<=y} sigma_+(p^{-1/2}), where sigma_+(r)^2=1+r^2/2+r sqrt(1+r^2/4).', status='proved_finite'),
    dict(name='Amplification asymptotic', statement='log ||Z_y||_{H_y->H_y} <= 1/2 sum_{p<=y}p^{-1/2}+O(sum p^{-1}) = (1+o(1)) sqrt(y)/log y.', status='standard_PNT_input'),
    dict(name='Incidence-conditioned tail transfer', statement='If e_{Omega,N}=||(I-P_{Omega<=K})B_NG_B^{-1/2}||_H, then tau^Z_{Omega,N} <= A_y e_{Omega,N}.', status='proved_finite'),
    dict(name='Restricted lower-frame salvage', statement='If blind overlap delta_N<=A_y e_{Omega,N}<1 and K_q has lower frame gamma_q on nonblind class, then restricted source strength is gamma_q(1-delta_N^2).', status='conditional'),
]
pd.DataFrame(theorem_rows).to_csv(out/'theorem_map_step136.csv', index=False)

route_rows = [
    dict(route='raw_boolean_metric', verdict='too_pessimistic_for_source_route', reason='Amplification phi^{pi(y)} is exponential in number of primes and ignores Dirichlet coefficient energy.'),
    dict(route='Dirichlet_H_metric', verdict='viable_but_conditional', reason='Amplification drops to exp((1+o(1))sqrt(y)/log y), but actual Omega-tail must beat this.'),
    dict(route='semilocal_response_metric', verdict='preferred', reason='Finite local factors are native to the semilocal response measure; same normalization principle applies carrier-natively.'),
    dict(route='assume_tail_small_before_Z', verdict='rejected', reason='High-Omega tail must be small after incidence response, not only before incidence.'),
]
pd.DataFrame(route_rows).to_csv(out/'route_status_step136.csv', index=False)

arith_rows = [
    dict(input='Prime number estimates', role='Estimate sum_{p<=y} p^{-1/2} and sum p^{-1}.', status='standard_import'),
    dict(input='Heap-Soundararajan Omega-block architecture', role='Provide non-smuggled block cutoffs and tail templates.', status='imported_template'),
    dict(input='Burnol/co-Poisson seed model', role='Define actual B_N whose high-Omega response tail must be bounded.', status='carrier_native_open'),
    dict(input='BPRZ restricted lower frame', role='Supply gamma_q on nonblind residual coefficient class.', status='conditional_after_blind_suppression'),
    dict(input='Completed residual ledger', role='Promote finite Boolean/source windows to completed membrane theorem.', status='open_framework_gate'),
]
pd.DataFrame(arith_rows).to_csv(out/'arithmetic_input_table_step136.csv', index=False)

# plots
plt.figure(figsize=(8,5))
plt.plot(amp['y'], amp['log_raw_boolean_norm'], marker='o', label='raw Boolean log norm')
plt.plot(amp['y'], amp['log_response_weighted_norm'], marker='o', label='response-weighted log norm')
plt.xlabel('prime cutoff y')
plt.ylabel('log amplification')
plt.title('Incidence amplification: raw Boolean vs response metric')
plt.legend()
plt.tight_layout()
plt.savefig(out/'incidence_amplification_comparison_step136.png', dpi=200)
plt.close()

plt.figure(figsize=(8,5))
plt.plot(svp['p'], svp['sigma_plus'])
plt.xlabel('prime p')
plt.ylabel(r'$\sigma_+(p^{-1/2})$')
plt.title('One-prime response-normalized incidence singular value')
plt.tight_layout()
plt.savefig(out/'single_prime_singular_values_step136.png', dpi=200)
plt.close()

# requirement plot
plt.figure(figsize=(8,5))
plt.plot(amp['y'], amp['required_seed_tail_for_vanish'], marker='o', label='tail needed for delta<=1')
plt.plot(amp['y'], amp['required_seed_tail_for_delta_half'], marker='o', label='tail needed for delta<=1/2')
plt.yscale('log')
plt.xlabel('prime cutoff y')
plt.ylabel('required pre-incidence tail')
plt.title('Seed-tail requirement after response-metric incidence amplification')
plt.legend()
plt.tight_layout()
plt.savefig(out/'tail_requirement_step136.png', dpi=200)
plt.close()

# effective source for c=2,3 across y with logq_factor=4 maybe
sel = eff[(eff['logq_factor']==4) & (eff['tail_c'].isin([1.0,2.0,3.0]))]
plt.figure(figsize=(8,5))
for c, grp in sel.groupby('tail_c'):
    plt.plot(grp['y'], grp['effective_source_strength'], marker='o', label=f'tail c={c}')
plt.xlabel('prime cutoff y')
plt.ylabel('gamma * visibility floor')
plt.title('Restricted source strength after incidence-conditioned visibility')
plt.legend()
plt.tight_layout()
plt.savefig(out/'restricted_source_strength_after_metric_step136.png', dpi=200)
plt.close()

# Write LaTeX
tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\usepackage{hyperref}
\title{Step 136: Response-Metric Normalization for the Incidence Operator}
\author{Six Birds / RH Membrane Working Thread}
\date{}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{corollary}{Corollary}
\begin{document}
\maketitle

\section{Purpose}
Step 135 identified the correct GCD-log blind-sector control as an incidence-conditioned tail
\[
\tau_{\Omega,N}^{Z}=\|Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|.
\]
The raw Boolean incidence operator has norm $\varphi^k$ on a $k$-prime cube, which is too pessimistic if the coefficient space is not raw Boolean $\ell^2$. Step 136 asks whether the natural Burnol/Muentz/Dirichlet response metric reduces this amplification.

\section{The squarefree incidence model}
Let $P_y$ be a finite set of primes and identify squarefree divisors with subsets $S\subseteq P_y$.  The zeta/Muentz incidence operator is
\[
(Z_yb)(T)=\sum_{S\subseteq T} b(S).
\]
On raw Boolean $\ell^2$, each prime contributes the local matrix
\[
Z_0=\begin{pmatrix}1&0\\1&1\end{pmatrix},
\]
and hence
\[
\|Z_y\|_{\ell^2\to\ell^2}=\varphi^{|P_y|},
\qquad \varphi=\frac{1+\sqrt5}{2}.
\]

\section{Response-weighted Dirichlet metric}
The residual source route uses the Dirichlet coefficient metric
\[
H_y(b)=\sum_{S\subseteq P_y}|b(S)|^2w(S),
\qquad w(S)=\prod_{p\in S}p^{-1}.
\]
Equivalently, after conjugation by $W^{1/2}$, the one-prime incidence block becomes
\[
L_p=\begin{pmatrix}1&0\\p^{-1/2}&1\end{pmatrix}.
\]

\begin{theorem}[Response-normalized incidence norm]
Let $r_p=p^{-1/2}$ and let
\[
\sigma_+(r)^2=1+\frac{r^2}{2}+r\sqrt{1+\frac{r^2}{4}}.
\]
Then
\[
\|Z_y\|_{H_y\to H_y}=\prod_{p\le y}\sigma_+(p^{-1/2}).
\]
Moreover
\[
\log\|Z_y\|_{H_y\to H_y}
\le \frac12\sum_{p\le y}p^{-1/2}+O\left(\sum_{p\le y}p^{-1}\right)
=(1+o(1))\frac{\sqrt y}{\log y}.
\]
\end{theorem}

\begin{proof}
The weighted conjugation is tensor-product local.  The singular values of
$L_p=\begin{psmallmatrix}1&0\\r&1\end{psmallmatrix}$ are the square roots of the eigenvalues of
\[
L_p^*L_p=\begin{pmatrix}1+r^2&r\\r&1\end{pmatrix},
\]
which are
\[
1+\frac{r^2}{2}\pm r\sqrt{1+\frac{r^2}{4}}.
\]
The tensor-product norm is the product of the local norms. The asymptotic bound follows from
$\log\sigma_+(r)=r/2+O(r^2)$ and the standard prime sums.
\end{proof}

\section{Incidence-conditioned tail transfer}
Let
\[
e_{\Omega,N}=\|(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|_{H_y}.
\]
Then
\[
\tau_{\Omega,N}^{Z}
\le
\mathcal A_y e_{\Omega,N},
\qquad
\mathcal A_y:=\prod_{p\le y}\sigma_+(p^{-1/2}).
\]
Consequently,
\[
\Xi_{\rm GCD,N}\preceq (\mathcal A_y e_{\Omega,N})^2G_{B,N}.
\]
Thus exact suppression requires $e_{\Omega,N}=o(\mathcal A_y^{-1})$, while a positive floor only requires
\[
\mathcal A_y e_{\Omega,N}\le \delta<1.
\]

\section{Verdict}
The response metric does reduce the raw Boolean amplification.  The amplification drops from
\[
\varphi^{\pi(y)}=\exp\{(\log\varphi+o(1))y/\log y\}
\]
to
\[
\mathcal A_y=\exp\{(1+o(1))\sqrt y/\log y\}.
\]
This is a major reduction, but not a disappearance. The actual Burnol/Muentz seed tail must still beat the response-normalized incidence amplification, or else $\Xi_{\rm GCD}$ remains a genuine residual.

\section{Next gate}
The next analytic obligation is not raw incidence control. It is a metric-native high-$\Omega$ tail theorem:
\[
\|(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|_{H_y}
\le
\varepsilon_N
\quad\text{with}\quad
\mathcal A_y\varepsilon_N<1
\]
preferably tending to zero. This is the Step 137 target.
\end{document}
'''
(out/'response_metric_incidence_step136.tex').write_text(tex)

summary = r'''
# Step 136: Response-Metric Normalization for the Incidence Operator

This step answers the question left by Step 135: does the Burnol/Müntz/semilocal response metric reduce the raw Boolean incidence amplification \(\|Z_y\|=\varphi^k\)?

## Main result

Yes, but only partially.

In the natural Dirichlet coefficient metric

\[
H_y(b)=\sum_{S\subseteq P_y}|b(S)|^2\prod_{p\in S}p^{-1},
\]

the incidence operator

\[
(Z_yb)(T)=\sum_{S\subseteq T}b(S)
\]

is conjugate to the tensor product of local blocks

\[
L_p=\begin{pmatrix}1&0\\p^{-1/2}&1\end{pmatrix}.
\]

Therefore

\[
\|Z_y\|_{H_y\to H_y}=\prod_{p\le y}\sigma_+(p^{-1/2}),
\]

where

\[
\sigma_+(r)^2=1+\frac{r^2}{2}+r\sqrt{1+\frac{r^2}{4}}.
\]

Thus

\[
\log\|Z_y\|_{H_y\to H_y}
=(1+o(1))\frac{\sqrt y}{\log y}.
\]

This is much smaller than the raw Boolean amplification

\[
\varphi^{\pi(y)}=\exp\{(\log\varphi+o(1))y/\log y\}.
\]

## Consequence

If

\[
e_{\Omega,N}=\|(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|_{H_y},
\]

then

\[
\tau_{\Omega,N}^{Z}
\le
\mathcal A_y e_{\Omega,N},
\qquad
\mathcal A_y=\prod_{p\le y}\sigma_+(p^{-1/2}).
\]

So

\[
\Xi_{{\rm GCD},N}\preceq(\mathcal A_ye_{\Omega,N})^2G_{B,N}.
\]

Exact suppression needs

\[
e_{\Omega,N}=o(\mathcal A_y^{-1}).
\]

A positive visibility floor only needs

\[
\mathcal A_ye_{\Omega,N}<1.
\]

## Verdict

The response metric saves the route from the raw \(\varphi^k\) amplification, but it does not make incidence harmless.

The actual Burnol/Müntz seed tail must beat the response-normalized amplification

\[
\mathcal A_y=\exp\{(1+o(1))\sqrt y/\log y\}.
\]

The next gate is a metric-native high-\(\Omega\) tail theorem for the actual seed windows.
'''
(out/'step136_results_summary.md').write_text(summary)

nonclaim = r'''
# Step 136 Nonclaim Boundary

Step 136 does not prove RH.

It does not prove that the actual Burnol/Müntz residual seed has a small high-\(\Omega\) tail.

It does not prove the restricted BPRZ lower frame on the completed residual class.

It does not prove completed finite-to-infinite source promotion.

It only proves the finite response-metric normalization of the zeta/Müntz incidence operator and identifies the correct amplification factor

\[
\mathcal A_y=\prod_{p\le y}\sigma_+(p^{-1/2}).
\]

Any later claim that \(\Xi_{\rm GCD}\) is small must still provide a metric-native estimate for

\[
\|Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|.
\]
'''
(out/'nonclaim_boundary_step136.md').write_text(nonclaim)

schema = {
    'step': 136,
    'title': 'Response-Metric Normalization for the Incidence Operator',
    'main_objects': ['Z_y', 'H_y', 'A_y', 'tau_Omega_N^Z', 'Xi_GCD_N'],
    'main_result': 'Raw Boolean incidence amplification phi^k is replaced by product_p sigma_+(p^{-1/2}) in the Dirichlet response metric.',
    'status': 'finite_operator_gate_proved; actual_seed_tail_open',
    'next_step': 'Step 137: metric-native high-Omega tail theorem for actual Burnol/Muntz seed windows'
}
(out/'step136_schema.json').write_text(json.dumps(schema, indent=2))

# copy script itself
script_src = Path('/tmp/create_step136.py')
(out/'run_response_metric_incidence_step136.py').write_text(script_src.read_text())

# Zip artifacts
zip_path = out/'step136_response_metric_incidence_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name == zip_path.name:
            continue
        z.write(p, arcname=p.name)
print(f'Created {zip_path} with {len(list(out.iterdir()))} files')
