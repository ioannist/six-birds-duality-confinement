import os, json, csv, math, zipfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step134_actual_omega_tail')
OUT.mkdir(parents=True, exist_ok=True)

def write(path, text):
    path = OUT / path
    path.write_text(text, encoding='utf-8')
    return path

# ----------------------------
# Synthetic scenarios / sanity data
# ----------------------------
N = np.arange(4, 121, 4)
# K-like thresholds, in a proxy scale
K = 0.18 * N + 4
# Tail scenarios (not RH evidence)
exact_tail = np.zeros_like(N, dtype=float)
fast_tail = np.exp(-0.22 * K)
slow_tail = 1.0 / np.sqrt(K)
# Incidence amplification proxy; mild when weighted/conditioned, severe when raw boolean unweighted
amp_mild = np.exp(0.015 * N)
amp_raw = np.exp(0.08 * N)
blind_fast_mild = np.minimum(1.0, amp_mild * fast_tail)
blind_fast_raw = np.minimum(1.0, amp_raw * fast_tail)
blind_slow_mild = np.minimum(1.0, amp_mild * slow_tail)
# Effective lower frame gamma * (1-delta^2) with gamma ~ log q; choose log q proxy
logq = 0.25 * N + 5
c_floor_exact = 1 - exact_tail**2
c_floor_fast = np.maximum(0, 1 - blind_fast_mild**2)
c_floor_slow = np.maximum(0, 1 - blind_slow_mild**2)
eff_exact = logq * c_floor_exact
eff_fast = logq * c_floor_fast
eff_slow = logq * c_floor_slow

# CSVs
with open(OUT/'omega_tail_scenarios_step134.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['N','K_proxy','tail_exact','tail_fast_exp','tail_slow_poly','blind_fast_mild_amp','blind_fast_raw_amp','blind_slow_mild_amp'])
    for row in zip(N,K,exact_tail,fast_tail,slow_tail,blind_fast_mild,blind_fast_raw,blind_slow_mild):
        w.writerow([float(x) for x in row])

with open(OUT/'restricted_source_strength_step134.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['N','logq_proxy','effective_exact','effective_fast_tail','effective_slow_tail','c_floor_fast','c_floor_slow'])
    for row in zip(N,logq,eff_exact,eff_fast,eff_slow,c_floor_fast,c_floor_slow):
        w.writerow([float(x) for x in row])

# Boolean exact annihilation check: if seed degree < R, modes with |A| >= R vanish
ks = np.arange(4, 19)
R = np.ceil(0.55 * ks).astype(int)
# dimension of killed modes / total modes
from math import comb
killed_frac=[]
for k,r in zip(ks,R):
    killed = sum(comb(k,j) for j in range(r,k+1))
    killed_frac.append(killed/(2**k))
with open(OUT/'omega_exact_annihilation_table_step134.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['k_primes','degree_cutoff_R','fraction_modes_annihilated_if_seed_degree_less_than_R'])
    for row in zip(ks,R,killed_frac):
        w.writerow(row)

# Incidence conditioning proxy
kgrid = np.arange(1,41)
phi = (1+5**0.5)/2
raw_condition = phi**(2*kgrid)
weighted_good = np.exp(0.02*kgrid)
with open(OUT/'incidence_conditioning_step134.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['k_primes','raw_boolean_condition_proxy_phi_2k','weighted_condition_proxy'])
    for row in zip(kgrid, raw_condition, weighted_good):
        w.writerow([float(x) for x in row])

# Plots
plt.figure(figsize=(8,5))
plt.semilogy(N, fast_tail, label='fast imported Ω-tail proxy')
plt.semilogy(N, slow_tail, label='slow/generic tail proxy')
plt.semilogy(N, np.maximum(1e-16, exact_tail+1e-16), label='exact Ω-cutoff')
plt.xlabel('window index N')
plt.ylabel('seed high-Ω tail proxy')
plt.title('Step 134: Ω-tail regimes for actual seed audit')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'omega_tail_regimes_step134.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
plt.plot(N, blind_fast_mild, label='fast tail + mild incidence amplification')
plt.plot(N, blind_fast_raw, label='fast tail + raw Boolean amplification')
plt.plot(N, blind_slow_mild, label='slow tail + mild amplification')
plt.xlabel('window index N')
plt.ylabel('blind-sector overlap proxy δ_N')
plt.title('Blind-sector overlap depends on tail and incidence conditioning')
plt.legend()
plt.ylim(-0.02,1.05)
plt.tight_layout()
plt.savefig(OUT/'blind_overlap_from_tail_step134.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
plt.plot(N, eff_exact, label='exact Ω cutoff')
plt.plot(N, eff_fast, label='fast tail')
plt.plot(N, eff_slow, label='slow tail')
plt.xlabel('window index N')
plt.ylabel('effective source strength proxy γ(1-δ²)')
plt.title('Restricted BPRZ salvage needs a visibility floor')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'effective_restricted_source_step134.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
plt.semilogy(kgrid, raw_condition, label='raw Boolean incidence conditioning')
plt.semilogy(kgrid, weighted_good, label='weighted/declared conditioning target')
plt.xlabel('number of squarefree primes k')
plt.ylabel('conditioning proxy')
plt.title('Incidence convolution amplification is a separate gate')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'incidence_conditioning_step134.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
plt.plot(ks, killed_frac, marker='o')
plt.xlabel('number of primes in Boolean cube')
plt.ylabel('fraction of Walsh modes exactly annihilated')
plt.title('Exact annihilation of deep blind modes by Ω support')
plt.tight_layout()
plt.savefig(OUT/'exact_annihilation_fraction_step134.png', dpi=180)
plt.close()

# Tables
omega_tail_gate_rows = [
    ['G1', 'Seed declaration', 'Regularized Burnol/Müntz seed b_N and prime blocks declared upstream', 'needed', 'prevents target-selected Ω cutoff'],
    ['G2', 'Ω-block projection', 'P_{Ω≤K} defined by fixed prime blocks and thresholds K_j', 'accepted finite definition', 'standard HS architecture import'],
    ['G3', 'Exact blind annihilation', 'Blind modes whose negative-prime set violates a block cutoff vanish on P_{Ω≤K} b_N', 'proved finite Boolean theorem', 'algebraic, not RH evidence'],
    ['G4', 'Actual seed tail', '||Z(I-P_{Ω≤K})b_N|| / ||Zb_N|| is small or <1', 'open analytic gate', 'must be proven for actual Burnol/Müntz residual coefficients'],
    ['G5', 'Incidence conditioning', 'Z_y does not over-amplify the high-Ω tail beyond declared bound', 'open operator gate', 'raw Boolean ℓ² conditioning can be bad'],
    ['G6', 'Restricted BPRZ lower frame', 'BPRZ GCD-log main kernel lower-bounds nonblind residual class', 'conditional', 'requires Step 130 blind-sector exclusion'],
    ['G7', 'Completed promotion', 'finite residual windows exhaust completed residual ledger', 'open', 'fixed/exhaustive tail record required'],
]
with open(OUT/'omega_tail_gate_table_step134.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['gate','name','condition','status','note']); w.writerows(omega_tail_gate_rows)

theorem_rows = [
    ['T134.1', 'Ω-tail domination', 'Pi_blind Z b = Pi_blind Z P_upblind b', 'blind-sector mass is controlled by high-divisibility seed tail'],
    ['T134.2', 'Block cutoff annihilation', 'If seed satisfies Ω_j ≤ K_j and each blind mode violates some K_j, then Pi_blind Zb=0', 'exact finite annihilation'],
    ['T134.3', 'Tail residual bound', 'δ_N ≤ τ_{Ω,N}', 'where τ_{Ω,N}=||Z(I-P_{Ω≤K})b||/||Zb||'],
    ['T134.4', 'Restricted source salvage', '<Zb,K_qZb> ≥ γ_q(1-δ_N²)||Zb||²', 'BPRZ lower frame survives on nonblind residual class'],
    ['T134.5', 'Actual-seed verdict', 'HS-style seed passes by declaration; generic Burnol/Müntz seed remains open', 'avoid overreading scalar HS tail as operator tail'],
]
with open(OUT/'theorem_map_step134.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','name','statement','meaning']); w.writerows(theorem_rows)

arithmetic_rows = [
    ['HS Ω-block machinery', 'Imported architecture', 'Prime blocks, Ω(n_j)≤K_j truncations, exponential tail bounds in scalar mean estimates', 'supports seed-side tail control but not automatically operator worst-direction control'],
    ['Burnol co-Poisson/Müntz', 'Carrier/readability', 'Provides zeta/Müntz convolution and Sonine/co-Poisson carrier', 'defines the actual seed coefficient problem'],
    ['BPRZ twisted second moment', 'Weighted source platform', 'GCD-log kernel from arbitrary polynomial twist', 'usable only after blind-sector suppression'],
    ['Framework Ξ', 'Adequacy residual', 'Xi_GCD = R_N^* Pi_sf R_N', 'measures exact overlap of actual residual coefficient class with blind sector'],
]
with open(OUT/'arithmetic_input_table_step134.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['input','role','imported_content','framework_use']); w.writerows(arithmetic_rows)

route_rows = [
    ['Exact Ω cutoff', 'accepted finite mechanism', 'blind modes violating Ω thresholds annihilated', 'needs actual seed projection residual/tail'],
    ['HS-style declared seed', 'promising', 'tail controlled by imported Ω-block architecture', 'must lift scalar/mean tail to uniform residual operator tail'],
    ['Generic Burnol/Müntz seed', 'not certified', 'no automatic Ω-tail smallness', 'Xi_GCD remains possible'],
    ['Restricted BPRZ', 'conditional salvage', 'lower frame on nonblind residual class', 'requires δ_N<1 and error subordinate'],
]
with open(OUT/'route_status_step134.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['route','status','what_passes','remaining_gate']); w.writerows(route_rows)

# LaTeX note
tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,geometry,booktabs,hyperref}
\geometry{margin=1in}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{corollary}{Corollary}
\newcommand{\XiG}{\Xi_{\mathrm{GCD}}}
\newcommand{\Om}{\Omega}
\title{Step 134: Actual Burnol--M\"untz Seed $\Omega$-Tail Estimate}
\author{RATCHET / Six Birds RH membrane thread}
\date{}
\begin{document}
\maketitle

\section{Purpose}
Steps 130--133 identified a precise obstruction and a precise possible repair.  The BPRZ shifted second-moment main kernel has squarefree Boolean near-null modes, so it cannot be imported as a lower frame on the unrestricted coefficient space.  But the actual residual coefficient class is not arbitrary: it passes through the zeta/M\"untz incidence convolution.  Step 132 showed that deep Boolean blind modes only see high-divisibility seed coefficients.  Step 133 imported the Heap--Soundararajan $\Omega$-block architecture as the right external analytic-number-theory template.

Step 134 asks whether the \emph{actual} regularized Burnol/M\"untz residual seed coefficients satisfy the required high-$\Omega$ tail estimate.

\section{Finite squarefree model}
Let $P_y$ be a finite set of primes, and identify squarefree divisors of $\prod_{p\in P_y}p$ with subsets $S\subseteq P_y$.  Let $b(S)$ be the seed coefficient vector.  The finite zeta/incidence convolution is
\[
  (Z_y b)(T)=\sum_{S\subseteq T}b(S).
\]
For a Boolean blind family $\mathcal B$ with negative-prime supports $A\subseteq P_y$, define the upward closure
\[
  \uparrow\mathcal B=\{S\subseteq P_y:\exists A\in\mathcal B,\ A\subseteq S\}.
\]

\begin{lemma}[Upward-closure identity]
For every seed $b$,
\[
  \Pi_{\mathcal B}Z_yb=\Pi_{\mathcal B}Z_yP_{\uparrow\mathcal B}b.
\]
Thus blind-sector mass is controlled exactly by the high-divisibility seed tail.
\end{lemma}

\begin{corollary}[Block cutoff annihilation]
Let the prime set be decomposed into blocks $\mathcal P_j$, and let $K_j$ be declared thresholds.  If the seed satisfies
\[
  \Omega_j(S):=|S\cap\mathcal P_j|\le K_j\quad\text{for every }j,
\]
and every blind mode $A\in\mathcal B$ violates at least one threshold,
\[
  |A\cap\mathcal P_j|>K_j\quad\text{for some }j,
\]
then
\[
  \Pi_{\mathcal B}Z_yb=0.
\]
\end{corollary}

\section{Actual-seed tail gate}
Let $b_N$ denote the actual regularized Burnol/M\"untz residual seed coefficients in a finite window.  Let
\[
  P_{\Om\le K}=\prod_j P_{\Om_j\le K_j}
\]
be the upstream-declared $\Omega$-block projection.  Define
\[
  \tau_{\Om,N}=\frac{\|Z_y(I-P_{\Om\le K})b_N\|}{\|Z_yb_N\|}.
\]
Then
\[
  \frac{\|\Pi_{\mathcal B}Z_yb_N\|}{\|Z_yb_N\|}\le \tau_{\Om,N},
\]
provided $\mathcal B$ is covered by threshold-violating blind modes.

This is the deterministic form of the desired tail estimate.  Heap--Soundararajan-type arguments supply an imported architecture for $\Omega$-block truncation and scalar mean tail bounds, but the membrane route requires the uniform residual operator version
\[
  \left\|Z_y(I-P_{\Om\le K})B_NG_{B,N}^{-1/2}\right\|\le \tau_{\Om,N}.
\]
This is the true Step 134 analytic obligation.

\section{Incidence amplification gate}
The incidence map $Z_y$ can amplify coefficient tails.  In raw Boolean $\ell^2$, the one-prime incidence matrix has singular values $\varphi$ and $\varphi^{-1}$, where $\varphi=(1+\sqrt5)/2$.  For $k$ primes this gives condition number $\varphi^{2k}$.  Therefore seed tail smallness must be measured after the lawful response-space weighting, or accompanied by an incidence-conditioning record.

We record the gate as
\[
  \|Z_y(I-P_{\Om\le K})b_N\|\le \mathfrak C_{Z,N}\|(I-P_{\Om\le K})b_N\|_{\mathrm{seed}},
\]
with a declared bound on $\mathfrak C_{Z,N}$.

\section{Restricted BPRZ salvage}
Let $K_q$ be the BPRZ GCD--log main kernel.  Assume it satisfies a lower frame on the nonblind residual class:
\[
  K_q\succeq \gamma_q I\quad\text{on }(1-\Pi_{\mathcal B})H,
  \qquad \gamma_q\asymp \log q.
\]
If
\[
  \|\Pi_{\mathcal B}Z_yb_N\|\le \delta_N\|Z_yb_N\|,
\]
then
\[
  \langle Z_yb_N,K_qZ_yb_N\rangle
  \ge \gamma_q(1-\delta_N^2)\|Z_yb_N\|^2.
\]
Hence exact suppression $\delta_N\to0$ is sufficient, but a uniform floor $\delta_N\le\delta<1$ can also suffice when $\gamma_q\to\infty$.

\section{Verdict}
The actual Burnol/M\"untz seed $\Omega$-tail estimate is not closed in full generality.  The finite Boolean mechanism is proved, and the Heap--Soundararajan architecture supplies the right non-smuggled $\Omega$-block template.  But the generic Burnol/M\"untz residual seed is not automatically $\Omega$-truncated.  Therefore the accepted route is conditional on one of:
\begin{enumerate}
\item a declared HS-compatible seed/projection with vanishing projection residual;
\item a uniform positive floor $\tau_{\Om,N}\le\tau<1$ plus diverging source strength;
\item a separate source-frame record for the remaining $\Xi_{\mathrm{GCD}}$ residual.
\end{enumerate}

\section{Nonclaim}
This step does not prove RH, does not prove that the BPRZ theorem gives a full lower frame, and does not prove that generic Burnol/co-Poisson atoms have small high-$\Omega$ tail.  It identifies the exact deterministic tail theorem required to make the restricted BPRZ route lawful.

\end{document}
'''
write('muntz_actual_omega_tail_step134.tex', tex)

summary = r'''
# Step 134: Actual Burnol/Müntz seed Ω-tail estimate

## Main verdict

The unrestricted BPRZ lower-frame import remains blocked by the squarefree Boolean GCD-log blind sector.

Step 134 proves the finite deterministic suppression mechanism and identifies the exact missing analytic record:

\[
\boxed{
\tau_{\Omega,N}
=
\frac{\|Z_y(I-P_{\Omega\le K})b_N\|}{\|Z_yb_N\|}
\to0
}
\]

or at least

\[
\boxed{\tau_{\Omega,N}\le \tau<1.}
\]

Here \(b_N\) is the actual regularized Burnol/Müntz residual seed and \(Z_y\) is the finite zeta/incidence convolution.

## Main theorem

For a Boolean blind family \(\mathcal B\),

\[
\Pi_{\mathcal B}Z_yb
=
\Pi_{\mathcal B}Z_yP_{\uparrow\mathcal B}b.
\]

So blind-sector mass is controlled exactly by the upward-closure / high-divisibility tail of the seed.

If the seed satisfies declared block cutoffs

\[
\Omega_j(S)\le K_j
\]

and every blind mode violates some block cutoff, then

\[
\boxed{\Pi_{\mathcal B}Z_yb=0.}
\]

## What Heap--Soundararajan contributes

Heap--Soundararajan provide the right imported architecture: prime blocks, \(\Omega(n_j)\le K_j\) truncations, and exponentially small scalar tail terms in their mean-value proof. Their construction defines short Dirichlet polynomials designed to mimic powers of \(\zeta\), and their block thresholds are declared before the mean-value estimates.

What remains new here is the uniform residual operator tail:

\[
\boxed{
\left\|Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\right\|
\le \tau_{\Omega,N}.
}
\]

Scalar average tail control is not the same as this worst-direction residual tail bound.

## Incidence conditioning warning

The incidence convolution \(Z_y\) can amplify seed tails. In the raw Boolean \(\ell^2\) model, the one-prime incidence matrix has singular values \(\varphi\) and \(\varphi^{-1}\), so the condition number over \(k\) primes grows like \(\varphi^{2k}\).

Therefore the route needs either:

\[
\boxed{\text{lawful weighted response norm where incidence is controlled}}
\]

or

\[
\boxed{\text{an explicit incidence amplification budget}.}
}
\]

## Restricted BPRZ salvage

If the BPRZ GCD-log kernel has lower frame

\[
K_q\succeq \gamma_q I,
\qquad \gamma_q\asymp \log q,
\]

on the nonblind residual class, and

\[
\|\Pi_{\mathcal B}Z_yb_N\|\le\delta_N\|Z_yb_N\|,
\]

then

\[
\boxed{
\langle Z_yb_N,K_qZ_yb_N\rangle
\ge
\gamma_q(1-
\delta_N^2)\|Z_yb_N\|^2.
}
\]

So exact suppression is sufficient, but a uniform positive floor \(\delta_N<1\) can also be enough when \(\gamma_q\to\infty\).

## Route status

The HS-style declared seed route is viable if the residual seed can be made \(\Omega\)-compatible without smuggling.

The generic Burnol/Müntz seed route is not certified: no automatic high-\(\Omega\) tail bound has been proved.

The active residual is still

\[
\boxed{
\Xi_{\rm GCD,N}=R_N^*\Pi_{\rm sf}R_N.
}
\]

Step 134 shows how this residual is dominated by the high-divisibility seed tail, but does not prove that the actual seed tail vanishes.

## Bottom line

\[
\boxed{
\text{The next analytic obligation is a uniform }\Omega\text{-tail theorem for the actual residual seed.}
}
\]

If that theorem fails, \(\Xi_{\rm GCD}\) remains as a genuine residual requiring a separate source-frame record.
'''
write('step134_results_summary.md', summary)

nonclaim = '''# Step 134 nonclaim boundary

Step 134 does not prove RH.

It does not prove the unrestricted BPRZ shifted-second-moment main kernel is a lower frame. Step 130 already blocked that by the squarefree Boolean near-null sector.

It does not prove that a generic Burnol/co-Poisson atom has small high-Omega tail after the regularized Müntz shadow.

It does not replace scalar Heap--Soundararajan tail estimates by an operator-valued residual tail theorem. It identifies the exact operator tail theorem needed.

It does not license target-selected Omega thresholds. Prime blocks and thresholds must be declared upstream, as in the imported Heap--Soundararajan architecture.

It does not remove the need for completed fixed/exhaustive residual-tail promotion.
'''
write('nonclaim_boundary_step134.md', nonclaim)

schema = {
    'step': 134,
    'title': 'Actual Burnol/Müntz seed Ω-tail estimate',
    'status': 'conditional reduction; actual-seed operator tail remains open',
    'active_residual': 'Xi_GCD,N = R_N^* Pi_sf R_N',
    'main_gate': 'uniform high-Omega seed tail after zeta/Müntz incidence convolution',
    'key_quantities': {
        'tau_Omega_N': '||Z_y(I-P_{Omega<=K})b_N|| / ||Z_y b_N||',
        'delta_N': 'blind-sector overlap ||Pi_blind Z_y b_N|| / ||Z_y b_N||',
        'gamma_q': 'restricted BPRZ lower-frame strength on nonblind class',
        'Xi_GCD_N': 'GCD-log adequacy residual'
    },
    'verdict': {
        'HS_style_seed': 'promising if uniform operator tail lift is proved',
        'generic_Burnol_seed': 'not certified',
        'BPRZ_salvage': 'conditional on blind-sector suppression or positive floor'
    }
}
write('step134_schema.json', json.dumps(schema, indent=2))

# LaTeX structure check
checks=[]
text=tex
checks.append(['environment_balance_document', text.count('\\begin{document}') == text.count('\\end{document}')])
checks.append(['environment_balance_enumerate', text.count('\\begin{enumerate}') == text.count('\\end{enumerate}')])
checks.append(['no_pdf_generated', True])
with open(OUT/'latex_structure_check_step134.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['check','passed']); w.writerows(checks)

# Zip selected artifacts
zip_path = OUT/'step134_actual_omega_tail_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)

print('created', len(list(OUT.iterdir())), 'files in', OUT)
