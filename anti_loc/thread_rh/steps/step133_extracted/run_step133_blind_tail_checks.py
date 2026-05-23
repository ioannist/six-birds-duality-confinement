import json, csv, zipfile, math, os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step133_omega_tail_import')
out.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Toy / audit computations
# -----------------------------
# Scenario A: exact annihilation of blind modes by Omega truncation.
# Let blind threshold R and seed support Omega <= K. If K < R then deep blind modes vanish exactly.
exact_rows = []
for R in [4, 6, 8, 10, 12, 16, 20]:
    for K in range(0, R+3):
        exact = 1 if K < R else 0
        exact_rows.append({"blind_threshold_R": R, "seed_omega_cutoff_K": K, "exact_annihilation": exact, "tail_status": "zero" if exact else "requires_tail_bound"})
with open(out/'omega_exact_annihilation_step133.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=exact_rows[0].keys()); w.writeheader(); w.writerows(exact_rows)

# Scenario B: exponential high-Omega tail suppression.
# tau_Omega ~ exp(-c K/2); delta <= tau. Vary c and K.
tail_rows = []
for c in [0.05, 0.10, 0.20, 0.35, 0.50]:
    for K in range(5, 105, 5):
        tau = math.exp(-0.5*c*K)
        c_floor = max(0.0, 1 - tau*tau)
        tail_rows.append({"tail_decay_c": c, "omega_cutoff_K": K, "delta_bound": tau, "visibility_floor_lower_bound": c_floor})
with open(out/'omega_tail_suppression_scenarios_step133.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=tail_rows[0].keys()); w.writeheader(); w.writerows(tail_rows)

# Scenario C: Heap-Soundararajan-style block thresholds Kj = A*Pj; tail = exp(-sigma A Pj), product blocks.
# Use Pj values loosely modeled as descending large-to-small log intervals.
P_vals = np.array([2.0, 3.0, 5.0, 8.0, 13.0])
block_rows=[]
for A in [20,50,100,200,500]:
    # HS uses 500 P_j; include it as A=500.
    block_tails = np.exp(-0.75*A*P_vals)
    total_tail = float(block_tails.sum())
    delta = min(1.0, math.sqrt(total_tail))
    c_floor = max(0.0, 1-delta*delta)
    block_rows.append({"threshold_factor_A":A, "num_blocks":len(P_vals), "max_block_tail":float(block_tails.max()), "sum_block_tail":total_tail, "delta_bound":delta, "visibility_floor_lower_bound":c_floor})
with open(out/'hs_block_threshold_tail_model_step133.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=block_rows[0].keys()); w.writeheader(); w.writerows(block_rows)

# Scenario D: coupling to BPRZ restricted lower frame gamma ~ log q, with visibility floor = 1-delta^2.
source_rows=[]
for logq in np.linspace(20, 500, 25):
    for delta in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]:
        gamma = logq
        c_floor = max(0.0, 1-delta*delta)
        source_rows.append({"log_q":float(logq), "delta_blind_bound":delta, "visibility_floor":c_floor, "effective_strength":float(gamma*c_floor)})
with open(out/'restricted_bprz_source_strength_step133.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=source_rows[0].keys()); w.writeheader(); w.writerows(source_rows)

# Plots
plt.figure(figsize=(8,5))
for c in [0.05,0.1,0.2,0.35,0.5]:
    xs=[r['omega_cutoff_K'] for r in tail_rows if r['tail_decay_c']==c]
    ys=[r['delta_bound'] for r in tail_rows if r['tail_decay_c']==c]
    plt.plot(xs, ys, marker='o', label=f'c={c}')
plt.yscale('log')
plt.xlabel('Omega cutoff K')
plt.ylabel('blind-sector delta bound')
plt.title('High-divisibility tail suppression under Omega cutoff')
plt.legend()
plt.tight_layout()
plt.savefig(out/'omega_tail_suppression_step133.png', dpi=200)
plt.close()

plt.figure(figsize=(8,5))
for R in [4,8,12,16,20]:
    xs=[r['seed_omega_cutoff_K'] for r in exact_rows if r['blind_threshold_R']==R]
    ys=[r['exact_annihilation'] for r in exact_rows if r['blind_threshold_R']==R]
    plt.step(xs, ys, where='post', label=f'R={R}')
plt.xlabel('seed Omega cutoff K')
plt.ylabel('exact blind-mode annihilation indicator')
plt.title('Exact annihilation when K < blind threshold R')
plt.legend()
plt.tight_layout()
plt.savefig(out/'omega_exact_annihilation_step133.png', dpi=200)
plt.close()

plt.figure(figsize=(8,5))
xs=[r['threshold_factor_A'] for r in block_rows]
ys=[r['delta_bound'] for r in block_rows]
plt.plot(xs, ys, marker='o')
plt.yscale('log')
plt.xlabel('block threshold factor A in K_j=A P_j')
plt.ylabel('aggregate delta bound')
plt.title('Heap-Soundararajan block cutoff tail model')
plt.tight_layout()
plt.savefig(out/'hs_block_threshold_tail_step133.png', dpi=200)
plt.close()

plt.figure(figsize=(8,5))
for delta in [0.0,0.25,0.5,0.75,0.9,0.99]:
    xs=[r['log_q'] for r in source_rows if abs(r['delta_blind_bound']-delta)<1e-9]
    ys=[r['effective_strength'] for r in source_rows if abs(r['delta_blind_bound']-delta)<1e-9]
    plt.plot(xs, ys, label=f'delta={delta}')
plt.xlabel('log q')
plt.ylabel('effective strength ~ (1-delta^2) log q')
plt.title('Restricted BPRZ lower frame after blind-sector suppression')
plt.legend()
plt.tight_layout()
plt.savefig(out/'restricted_bprz_effective_strength_step133.png', dpi=200)
plt.close()

# CSV tables
literature_rows = [
    {"source":"Heap--Soundararajan 2020", "imported_object":"Omega-block truncated short Dirichlet polynomials N(s,alpha)", "used_for":"architecture for high-divisibility tail control; source-strength template", "not_used_for":"automatic operator lower frame"},
    {"source":"Burnol co-Poisson/Sonine", "imported_object":"co-Poisson/Muntz zeta multiplier and Sonine carrier", "used_for":"residual coefficient class and Burnol-native visibility", "not_used_for":"arbitrary Dirichlet readability without angular-gap proof"},
    {"source":"BPRZ twisted second moment", "imported_object":"L-weighted arbitrary-polynomial second moment", "used_for":"candidate source-weighted Gram", "not_used_for":"unrestricted lower frame after Step 130 obstruction"},
    {"source":"CCM semilocal Hardy--Titchmarsh", "imported_object":"semilocal response geometry with local factors", "used_for":"ambient carrier", "not_used_for":"Calkin-level compact repair"},
]
with open(out/'literature_import_table_step133.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=literature_rows[0].keys()); w.writeheader(); w.writerows(literature_rows)

gate_rows = [
    {"gate":"Omega-block declaration", "statement":"Prime blocks P_j and cutoffs K_j are chosen upstream, not from the residual target.", "status":"formulated"},
    {"gate":"Exact blind annihilation", "statement":"If seed support has Omega below every blind threshold, the corresponding blind Walsh modes vanish exactly.", "status":"proved finite Boolean theorem"},
    {"gate":"High-divisibility tail", "statement":"If the seed is not exactly truncated, the blind residual is bounded by the zeta-convolved high-Omega tail.", "status":"reduced to tail estimate"},
    {"gate":"Restricted BPRZ salvage", "statement":"If blind overlap delta<1 on the residual class, the BPRZ lower frame survives with floor (1-delta^2).", "status":"conditional"},
    {"gate":"Source matrix lift", "statement":"The source-weighted Gram must have a uniform lower eigenvalue on the nonblind residual class.", "status":"unearned analytic import"},
    {"gate":"Completed tail promotion", "statement":"Finite Omega-window suppression must promote through fixed/exhaustive residual ledger.", "status":"open"},
]
with open(out/'omega_tail_gate_table_step133.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=gate_rows[0].keys()); w.writeheader(); w.writerows(gate_rows)

theorem_rows = [
    {"label":"T133.1", "name":"Boolean upward-closure suppression", "claim":"Blind modes of zeta incidence convolution read only seed coefficients on the upward closure of their negative-prime sets.", "dependency":"Step 132 finite Boolean theorem"},
    {"label":"T133.2", "name":"Omega-tail bound", "claim":"For blind family B, ||Pi_B Zb||/||Zb|| is bounded by the normalized zeta-convolved tail of b on upward(B).", "dependency":"finite projection identity"},
    {"label":"T133.3", "name":"HS block import", "claim":"Heap--Soundararajan Omega-block architecture supplies a non-smuggled template for declaring prime-block cutoffs K_j and high-Omega truncations.", "dependency":"external analytic NT import"},
    {"label":"T133.4", "name":"Restricted BPRZ salvage", "claim":"If blind overlap is at most delta<1 and K_q has lower bound gamma on nonblind class, then the restricted lower frame has strength gamma(1-delta^2).", "dependency":"Step 130/132 plus residual-class restriction"},
]
with open(out/'theorem_map_step133.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=theorem_rows[0].keys()); w.writeheader(); w.writerows(theorem_rows)

route_rows = [
    {"route_component":"Burnol geometric exhaustion epsilon_B", "status":"open; handled by Burnol/Sonine density"},
    {"route_component":"Dirichlet readability delta_BD_reg", "status":"regularized via Muntz/co-Poisson shadow; angular gap still open"},
    {"route_component":"GCD blind overlap delta_GCD", "status":"reduced to Omega/high-divisibility tail"},
    {"route_component":"BPRZ weighted lower frame", "status":"unrestricted import blocked; restricted class may work"},
    {"route_component":"HS Omega architecture", "status":"imported as tail-control template, not as full proof"},
    {"route_component":"completed membrane claim", "status":"not proved"},
]
with open(out/'route_status_step133.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=route_rows[0].keys()); w.writeheader(); w.writerows(route_rows)

arithmetic_rows = [
    {"input":"Prime-block partition", "needed_form":"blocks P_j with declared cutoff K_j=A P_j", "current_status":"HS imported template"},
    {"input":"Seed Omega-tail", "needed_form":"||Z P_up b_N|| <= delta_N ||Z b_N||", "current_status":"new analytic obligation for actual Burnol/Muntz residual seed"},
    {"input":"Restricted main-kernel lower frame", "needed_form":"K_q >= gamma_q I on complement of blind sector", "current_status":"conditional after Step 130"},
    {"input":"Source-weighted matrix asymptotic", "needed_form":"operator-norm subordinate error for every coefficient vector in residual class", "current_status":"not supplied by scalar lower moments"},
    {"input":"Tail promotion", "needed_form":"finite Omega windows exhaust completed residual ledger", "current_status":"open"},
]
with open(out/'arithmetic_input_table_step133.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=arithmetic_rows[0].keys()); w.writeheader(); w.writerows(arithmetic_rows)

# Markdown summary
summary = r"""
# Step 133: Omega-truncated Dirichlet-polynomial architecture for GCD-log blind-sector suppression

## Purpose
Step 130 showed that the unrestricted BPRZ shifted-main-term kernel has squarefree Boolean near-null directions. Step 131 showed that the actual zeta/Müntz residual class may avoid those directions because zeta incidence convolution makes deep blind modes read only high-divisibility seed coefficients. Step 132 proved the finite Boolean mechanism.

Step 133 imports the Heap--Soundararajan Omega-block architecture as the standard analytic-number-theory template for controlling those high-divisibility seed tails.

## Main result
For a blind Walsh family B with upward closure up(B),

    Pi_B Z_y b = Pi_B Z_y P_up(B) b.

Therefore the GCD-log blind overlap is bounded by the zeta-convolved high-divisibility tail of the seed. If the seed is exactly supported below the blind threshold, the blind modes vanish exactly. If not, the residual is a declared Omega-tail defect.

## Heap--Soundararajan import
HS use prime blocks, truncated Omega counts, and short Dirichlet polynomials N(s, alpha) that mimic zeta powers while keeping length under control. In the framework, this supplies a non-smuggled architecture for declaring cutoffs K_j and controlling high-Omega tails. It does not by itself prove the operator lower frame.

## Conditional salvage of BPRZ
If the GCD-log kernel has lower bound gamma_q on the nonblind class and the actual residual coefficient image has blind overlap delta_N, then

    <Zb, K_q Zb> >= gamma_q (1 - delta_N^2) ||Zb||^2.

A positive floor delta_N < 1 is enough when gamma_q diverges; exact delta_N -> 0 is sufficient but stronger than needed.

## Remaining hard input
The new analytic obligation is to prove, for the actual regularized Burnol/Müntz residual seed b_N,

    ||Pi_blind Z_y b_N|| / ||Z_y b_N|| -> 0

or at least a uniform bound < 1.

This is a high-divisibility/Omega-tail estimate, not an AFE re-derivation.
""".strip()
(out/'step133_results_summary.md').write_text(summary)

nonclaim = r"""
# Step 133 nonclaim boundary

Step 133 does not prove RH.

It does not prove that Heap--Soundararajan moment lower bounds imply an operator-valued source frame.

It does not prove that the actual Burnol/Müntz residual seed has small high-Omega tail.

It does not remove the Step 130 unrestricted GCD-log lower-frame obstruction.

It proves a conditional reduction: if the actual residual seed obeys an Omega/high-divisibility tail estimate, then the GCD-log blind-sector residual is controlled and the BPRZ lower-frame import can be salvaged on the residual coefficient class.
""".strip()
(out/'nonclaim_boundary_step133.md').write_text(nonclaim)

tex = r"""
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\title{Step 133: $\Omega$-Truncated Dirichlet-Polynomial Architecture for GCD--Log Blind-Sector Suppression}
\author{Six Birds / RH Membrane Working Notes}
\date{May 2026}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{remark}{Remark}
\begin{document}
\maketitle

\section{Purpose}
Step 130 showed that the unrestricted BPRZ shifted-main-term kernel has squarefree Boolean near-null modes. Step 131 showed that these modes are not automatically fatal because the actual residual coefficient class is not arbitrary: it is produced by a zeta/Müntz incidence convolution. Step 132 proved that deep blind Walsh modes read only high-divisibility seed coefficients.

Step 133 imports the Heap--Soundararajan $\Omega$-block architecture as an external analytic-number-theory template for controlling this high-divisibility tail. We do not rederive their moment method. We translate the relevant architecture into the membrane/adequacy language.

\section{Boolean setup}
Let $P_y$ be a finite set of primes and identify squarefree divisors with subsets $S\subseteq P_y$. For a seed vector $b$, define the finite zeta incidence convolution
\[
  (Z_y b)(T)=\sum_{S\subseteq T} b(S).
\]
For a Boolean sign vector $\epsilon\in\{\pm1\}^{P_y}$, let $A(\epsilon)=\{p:\epsilon_p=-1\}$. Step 132 proved
\[
  \widehat{Z_y b}(\epsilon)
  =2^{-|P_y|/2}(-1)^{|A|}\sum_{V\subseteq A^c}2^{|P_y|-|A|-|V|}b(A\cup V).
\]
Hence the mode $\epsilon$ only reads seed coefficients supported on supersets of $A$.

\begin{definition}[Upward closure]
For a blind family $\mathcal B$ of negative-prime sets, define
\[
  \uparrow\mathcal B=
  \{S\subseteq P_y:\exists A\in\mathcal B,\ A\subseteq S\}.
\]
\end{definition}

\begin{theorem}[Blind-sector tail reduction]
Let $\Pi_{\mathcal B}$ project onto the blind Walsh modes corresponding to $\mathcal B$. Then
\[
  \Pi_{\mathcal B}Z_yb
  =\Pi_{\mathcal B}Z_yP_{\uparrow\mathcal B}b.
\]
Consequently,
\[
  \frac{\|\Pi_{\mathcal B}Z_yb\|}{\|Z_yb\|}
  \le
  \frac{\|Z_yP_{\uparrow\mathcal B}b\|}{\|Z_yb\|}.
\]
\end{theorem}

\section{Heap--Soundararajan block import}
The imported architecture consists of prime blocks $\mathcal P_j$, block sums $P_j$, and truncation thresholds
\[
  K_j=A P_j,
\]
with HS using a large constant threshold in their model. The corresponding seed class enforces
\[
  \Omega(n_j)\le K_j
\]
inside each block. In the membrane route, this is not a proof of a lower frame; it is a non-smuggled declaration of a high-divisibility cutoff.

\begin{definition}[$\Omega$-tail defect]
Let $P_{\Omega\le K}$ project onto seed coefficients obeying all declared block thresholds, and define
\[
  \tau_{\Omega,N}
  =\frac{\|Z_y(I-P_{\Omega\le K})b_N\|}{\|Z_yb_N\|}.
\]
\end{definition}

\begin{proposition}[Exact suppression under block threshold]
If every blind set $A\in\mathcal B$ violates at least one block threshold, i.e. $|A\cap\mathcal P_j|>K_j$ for some $j$, and $b=P_{\Omega\le K}b$, then
\[
  \Pi_{\mathcal B}Z_yb=0.
\]
If the seed is not exactly truncated, then
\[
  \|\Pi_{\mathcal B}Z_yb\|\le \|Z_y(I-P_{\Omega\le K})b\|.
\]
\end{proposition}

\section{Restricted BPRZ salvage}
Let $K_q$ be the GCD--log main kernel from Step 130. Suppose $K_q\succeq \gamma_q I$ on the complement of the blind sector. If
\[
  \|\Pi_{\mathcal B}Z_yb\|\le \delta_N\|Z_yb\|,
\]
then
\[
  \langle Z_yb,K_qZ_yb\rangle
  \ge \gamma_q(1-\delta_N^2)\|Z_yb\|^2.
\]
Thus $\delta_N\to0$ is sufficient, but a uniform $\delta_N<1$ is already enough if $\gamma_q\to\infty$.

\section{Open analytic obligation}
For the actual regularized Burnol/Müntz residual seed, one must prove
\[
  \frac{\|\Pi_{\rm blind}Z_yb_N\|}{\|Z_yb_N\|}\to0,
\]
or at least a uniform bound $<1$. This is the high-divisibility/Omega-tail gate.

\section{Nonclaim}
This note does not prove RH and does not claim that HS scalar moment machinery gives an operator-valued source frame. It imports the HS block architecture and identifies the exact additional tail and matrix-lower-frame records required by the membrane proof route.

\end{document}
""".strip()
(out/'muntz_omega_tail_import_step133.tex').write_text(tex)

schema = {
    "step": 133,
    "title": "Omega-truncated Dirichlet-polynomial architecture for GCD-log blind-sector suppression",
    "main_objects": ["Xi_GCD", "Pi_blind", "Z_y incidence convolution", "Omega-block cutoffs K_j", "tau_Omega,N"],
    "imported_literature": ["Heap--Soundararajan 2020", "Burnol co-Poisson/Sonine", "BPRZ twisted second moment", "CCM semilocal Hardy--Titchmarsh"],
    "main_result": "Blind-sector overlap is controlled by zeta-convolved high-divisibility seed tail; HS Omega truncation gives the imported architecture for declaring and estimating that tail.",
    "status": "conditional reduction, not RH proof",
    "next_step": "Step 134: actual Burnol/Muntz seed Omega-tail estimate"
}
(out/'step133_schema.json').write_text(json.dumps(schema, indent=2))

# Create a standalone check script copy
check_code = Path(__file__).read_text()
(out/'run_step133_blind_tail_checks.py').write_text(check_code)

# Zip artifacts
zip_path = out/'step133_omega_tail_import_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name == zip_path.name:
            continue
        z.write(p, arcname=p.name)
print('Created', zip_path)
print('Files:', len(list(out.iterdir())))
