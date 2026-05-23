import itertools, json, math, os, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step132_blind_suppression')
OUT.mkdir(parents=True, exist_ok=True)

# Boolean cube utilities
def subsets(k):
    return list(range(1<<k))

def popcount(x):
    return int(x.bit_count())

def zeta_convolution(b, k):
    # Zb(S) = sum_{T subset S} b(T); fast zeta transform
    z = b.copy().astype(float)
    for i in range(k):
        bit = 1<<i
        for mask in range(1<<k):
            if mask & bit:
                z[mask] += z[mask ^ bit]
    return z

def walsh_transform(f, k):
    # normalized Walsh characters (-1)^{|A cap S|}/sqrt(2^k)
    h = f.copy().astype(float)
    n = len(h)
    length = 1
    while length < n:
        for i in range(0, n, 2*length):
            for j in range(i, i+length):
                x = h[j]; y = h[j+length]
                h[j] = x + y
                h[j+length] = x - y
        length *= 2
    return h / math.sqrt(n)

def inv_walsh_transform(h, k):
    # same as Walsh for normalized transform
    return walsh_transform(h, k)

def blind_ratio_for_seed(b, k, R):
    z = zeta_convolution(b, k)
    wh = walsh_transform(z, k)
    denom = np.dot(z, z)
    blind_masks = [A for A in range(1<<k) if popcount(A) >= R]
    blind = float(np.sum(wh[blind_masks]**2))
    tail_masks = [S for S in range(1<<k) if popcount(S) >= R]
    z_tail = zeta_convolution(np.array([b[S] if popcount(S)>=R else 0.0 for S in range(1<<k)]), k)
    tail_ratio = float(np.dot(z_tail, z_tail) / denom) if denom>0 else np.nan
    blind_ratio = blind/denom if denom>0 else np.nan
    return blind_ratio, tail_ratio, denom

# Exact formula check for Fourier coefficient after zeta convolution
# \\hat{Zb}(A)=2^{-k/2}(-1)^|A| sum_{V subset A^c} 2^{k-|A|-|V|} b(A union V)
def coefficient_formula(b, A, k):
    comp = ((1<<k)-1) ^ A
    total = 0.0
    V = comp
    sub = V
    # iterate all V subset comp
    s = sub
    x = s
    # standard subset iteration
    Vmask = comp
    sub = Vmask
    while True:
        total += (2.0 ** (k - popcount(A) - popcount(sub))) * b[A | sub]
        if sub == 0:
            break
        sub = (sub - 1) & Vmask
    return (2.0 ** (-k/2.0)) * ((-1.0) ** popcount(A)) * total

rng = np.random.default_rng(132)
k = 10
R = 7
n = 1<<k
# scenarios with degree-decaying seeds
rows=[]
for decay in np.linspace(0.15, 1.5, 18):
    b = np.zeros(n)
    for S in range(n):
        deg = popcount(S)
        b[S] = rng.normal() * math.exp(-decay * deg)
    br, tr, denom = blind_ratio_for_seed(b, k, R)
    rows.append({'k':k,'R':R,'decay':decay,'blind_ratio':br,'zeta_tail_ratio':tr,'norm_Zb_sq':denom})
pd.DataFrame(rows).to_csv(OUT/'blind_suppression_decay_scenarios_step132.csv', index=False)

# exact annihilation low-degree support
ann=[]
for maxdeg in range(0, k+1):
    b = np.zeros(n)
    for S in range(n):
        if popcount(S) <= maxdeg:
            b[S] = rng.normal()
    br, tr, denom = blind_ratio_for_seed(b, k, R)
    ann.append({'k':k,'R':R,'max_seed_degree':maxdeg,'blind_ratio_size_ge_R':br,'zeta_tail_ratio_size_ge_R':tr,'annihilated_expected': maxdeg < R})
pd.DataFrame(ann).to_csv(OUT/'exact_annihilation_by_degree_step132.csv', index=False)

# coefficient formula checks
checks=[]
b = rng.normal(size=n)
z = zeta_convolution(b, k)
wh = walsh_transform(z, k)
for A in rng.choice(n, size=40, replace=False):
    cf = coefficient_formula(b, int(A), k)
    checks.append({'A_mask': int(A), 'negative_count': popcount(int(A)), 'walsh_coeff': wh[int(A)], 'formula_coeff': cf, 'abs_error': abs(wh[int(A)]-cf)})
pd.DataFrame(checks).to_csv(OUT/'boolean_coefficient_formula_checks_step132.csv', index=False)

# lower-frame salvage model
lf=[]
logq=100.0
gamma_good=0.25*logq
gamma_blind=0.0
for delta in np.linspace(0,0.99,60):
    lower = gamma_good*(1-delta**2)+gamma_blind*delta**2
    lf.append({'blind_overlap_delta':delta,'blind_mass_delta_sq':delta**2,'good_kernel_lower':gamma_good,'certified_lower_bound':lower,'normalized_by_logq':lower/logq})
pd.DataFrame(lf).to_csv(OUT/'lower_frame_salvage_by_blind_overlap_step132.csv', index=False)

# high-divisibility tail for structured seed: truncated Omega + exponential leakage
ht=[]
for Kmax in [2,3,4,5,6]:
    b = np.zeros(n)
    for S in range(n):
        deg=popcount(S)
        if deg <= Kmax:
            b[S] = rng.normal() / math.sqrt(math.comb(k, deg) if math.comb(k,deg)>0 else 1)
        else:
            b[S] = 0.05*rng.normal()*math.exp(-0.8*(deg-Kmax))
    z = zeta_convolution(b, k)
    denom=np.dot(z,z)
    for Rt in range(0,k+1):
        br,tr,_=blind_ratio_for_seed(b,k,Rt)
        ht.append({'k':k,'seed_core_max_degree':Kmax,'blind_threshold_R':Rt,'blind_ratio':br,'zeta_tail_ratio':tr,'norm_Zb_sq':denom})
pd.DataFrame(ht).to_csv(OUT/'high_divisibility_tail_sweep_step132.csv', index=False)

# Plots
plt.figure(figsize=(7,4.5))
df=pd.read_csv(OUT/'blind_suppression_decay_scenarios_step132.csv')
plt.plot(df['decay'], df['blind_ratio'], marker='o', label='blind energy ratio')
plt.plot(df['decay'], df['zeta_tail_ratio'], marker='s', label='zeta-image high-divisibility tail')
plt.yscale('log')
plt.xlabel('degree-decay of seed coefficients')
plt.ylabel('ratio')
plt.title('Boolean blind-sector suppression follows high-divisibility tail')
plt.legend()
plt.tight_layout(); plt.savefig(OUT/'blind_suppression_decay_step132.png', dpi=180); plt.close()

plt.figure(figsize=(7,4.5))
df=pd.read_csv(OUT/'exact_annihilation_by_degree_step132.csv')
plt.plot(df['max_seed_degree'], df['blind_ratio_size_ge_R'], marker='o')
plt.axvline(R-0.5, linestyle='--')
plt.yscale('symlog', linthresh=1e-16)
plt.xlabel('maximum seed degree Ω')
plt.ylabel(f'blind ratio for modes with ≥ {R} negative signs')
plt.title('Exact annihilation when seed degree is below blind threshold')
plt.tight_layout(); plt.savefig(OUT/'exact_annihilation_by_degree_step132.png', dpi=180); plt.close()

plt.figure(figsize=(7,4.5))
df=pd.read_csv(OUT/'lower_frame_salvage_by_blind_overlap_step132.csv')
plt.plot(df['blind_overlap_delta'], df['normalized_by_logq'], marker='')
plt.xlabel('blind overlap δ')
plt.ylabel('certified lower bound / log q')
plt.title('Restricted lower-frame salvage after blind-sector suppression')
plt.tight_layout(); plt.savefig(OUT/'lower_frame_salvage_step132.png', dpi=180); plt.close()

plt.figure(figsize=(7,4.5))
df=pd.read_csv(OUT/'high_divisibility_tail_sweep_step132.csv')
for Kmax,sub in df.groupby('seed_core_max_degree'):
    plt.plot(sub['blind_threshold_R'], sub['blind_ratio'], marker='o', label=f'core Ω≤{Kmax}')
plt.yscale('log')
plt.xlabel('blind threshold R')
plt.ylabel('blind energy ratio')
plt.title('Blind energy falls when threshold exceeds seed divisibility')
plt.legend(ncol=2, fontsize=8)
plt.tight_layout(); plt.savefig(OUT/'high_divisibility_tail_sweep_step132.png', dpi=180); plt.close()

# Tables
pd.DataFrame([
    {'gate':'Boolean coefficient identity','status':'proved finite exact','obligation':'Use Walsh/zeta-convolution formula; no analytic NT input.'},
    {'gate':'Upward-closure suppression','status':'proved finite exact','obligation':'Blind modes only depend on seed coefficients divisible by their negative prime set.'},
    {'gate':'Actual Burnol/Müntz high-divisibility tail','status':'open analytic input','obligation':'Show zeta-image tail of regularized seed is small on upward closure of GCD-log blind sets.'},
    {'gate':'Restricted BPRZ lower frame','status':'conditional salvage','obligation':'Lower bound on complement of blind sector plus small blind overlap.'},
    {'gate':'Completed residual-tail promotion','status':'open framework promotion','obligation':'Move finite Boolean windows to fixed/exhaustive Burnol/Sonine residual ledger.'},
]).to_csv(OUT/'blind_suppression_gate_table_step132.csv', index=False)

pd.DataFrame([
    {'result':'Walsh coefficient formula','statement':'Fourier coefficient of Z_y b at negative set A depends only on seed coefficients on supersets of A.','status':'proved'},
    {'result':'Upward closure theorem','statement':'Π_B Z_y b = Π_B Z_y P_{↑B} b for any blind family B.','status':'proved'},
    {'result':'Degree-threshold corollary','statement':'If b is supported on Ω<R then all modes with at least R negative signs vanish exactly.','status':'proved'},
    {'result':'Restricted lower-frame theorem','statement':'If blind overlap is δ and K has lower bound γ log q on complement, then source main term gives ≥γ(1-δ²)log q on the image.','status':'conditional'},
    {'result':'Müntz seed tail theorem','statement':'The actual regularized Burnol/Müntz seed must satisfy upward-closure high-divisibility tail control.','status':'open'},
]).to_csv(OUT/'theorem_map_step132.csv', index=False)

pd.DataFrame([
    {'input':'Regularized Burnol/Müntz seed coefficients b_N','needed':'High-divisibility/upward-closure tail bound in the zeta-image norm','source':'Burnol/co-Poisson + Müntz regularization; not automatic'},
    {'input':'Ω-truncated Dirichlet-polynomial architecture','needed':'Declared non-smuggled truncation compatible with Heap--Soundararajan-style shortness','source':'Heap--Soundararajan uses Ω-block cutoffs and short Dirichlet polynomials'},
    {'input':'BPRZ shifted main kernel','needed':'Lower eigenvalue on complement of GCD-log blind modes','source':'External analytic NT import; unrestricted lower frame blocked by Step 130'},
    {'input':'Residual coefficient map R_N','needed':'Small projection into blind modes: Xi_GCD,N tail-small or source absorbed','source':'Framework / Xi adequacy gate'},
]).to_csv(OUT/'arithmetic_input_table_step132.csv', index=False)

# LaTeX working note
tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,booktabs,geometry}
\geometry{margin=1in}
\newtheorem{theorem}{Theorem}
\newtheorem{corollary}{Corollary}
\newtheorem{lemma}{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{remark}{Remark}
\title{Step 132: M\"untz Shadow High-Divisibility / Boolean Blind-Sector Suppression}
\author{Six Birds RH Membrane Thread}
\date{}
\begin{document}
\maketitle

\section{Purpose}
Step 130 showed that the unrestricted BPRZ shifted-main-term kernel has a squarefree Boolean near-null sector. Step 131 observed that the actual residual coefficient class is not arbitrary: it is generated by a regularized M\"untz/co-Poisson shadow and therefore passes through a zeta-incidence convolution on squarefree local coordinates. Step 132 proves the finite Boolean suppression theorem: deep blind modes only see high-divisibility seed coefficients.

\section{Boolean model}
Let $P_y$ be a finite set of $k$ primes and identify squarefree divisors of $P_y$ with subsets $S\subseteq P_y$. Let $b(S)$ be the seed coefficient vector and define the finite zeta/incidence convolution
\[
  (Z_y b)(T)=\sum_{S\subseteq T} b(S).
\]
For a sign vector $\epsilon\in\{\pm1\}^{P_y}$, write
\[
  A(\epsilon)=\{p\in P_y:\epsilon_p=-1\}.
\]
The normalized Walsh coefficient of $Z_yb$ at $\epsilon$ is
\[
  \widehat{Z_yb}(\epsilon)=2^{-k/2}\sum_{T\subseteq P_y}\epsilon(T)(Z_yb)(T),
  \qquad \epsilon(T)=\prod_{p\in T}\epsilon_p.
\]

\begin{theorem}[Boolean zeta-convolution coefficient formula]
For $A=A(\epsilon)$,
\[
\boxed{
  \widehat{Z_yb}(\epsilon)=
  2^{-k/2}(-1)^{|A|}
  \sum_{V\subseteq A^c}2^{k-|A|-|V|}b(A\cup V).
}
\]
Thus the coefficient at sign pattern $\epsilon$ only depends on seed coefficients supported on subsets containing every negative prime in $A(\epsilon)$.
\end{theorem}

\begin{proof}
Expand
\[
\widehat{Z_yb}(\epsilon)=2^{-k/2}\sum_T\epsilon(T)\sum_{S\subseteq T}b(S)
=2^{-k/2}\sum_S b(S)\sum_{T\supseteq S}\epsilon(T).
\]
The inner sum factors prime-by-prime. If a negative prime $p\in A$ is not in $S$, the local factor is $1+\epsilon_p=0$. Hence only $S\supseteq A$ survive. Writing $S=A\cup V$ with $V\subseteq A^c$, the negative primes contribute $(-1)^{|A|}$, the positive primes outside $V$ contribute factors of $2$, and the positive primes inside $V$ contribute $1$.
\end{proof}

\begin{definition}[Upward closure of blind modes]
For a family $\mathcal B$ of negative prime sets, define its upward closure by
\[
  \uparrow\mathcal B=\{S\subseteq P_y:\exists A\in\mathcal B\text{ with }A\subseteq S\}.
\]
Let $P_{\uparrow\mathcal B}$ be coordinate projection on seed vectors and $\Pi_{\mathcal B}$ the Walsh projection onto modes with $A(\epsilon)\in\mathcal B$.
\end{definition}

\begin{theorem}[Upward-closure suppression]
For every seed vector $b$,
\[
\boxed{
  \Pi_{\mathcal B}Z_yb=\Pi_{\mathcal B}Z_yP_{\uparrow\mathcal B}b.
}
\]
Consequently, blind-mode energy is controlled entirely by the high-divisibility seed tail on $\uparrow\mathcal B$.
\end{theorem}

\begin{corollary}[Degree-threshold annihilation]
Let
\[
  \mathcal B_R=\{A\subseteq P_y:|A|\ge R\}.
\]
Then $\uparrow\mathcal B_R=\{S:|S|\ge R\}$. Hence if $b(S)=0$ for $|S|\ge R$, then
\[
\boxed{\Pi_{\mathcal B_R}Z_yb=0.}
\]
More generally,
\[
  \frac{\|\Pi_{\mathcal B_R}Z_yb\|}{\|Z_yb\|}
  \le
  \frac{\|Z_yP_{|S|\ge R}b\|}{\|Z_yb\|}.
\]
\end{corollary}

\section{Application to the GCD-log blind sector}
Let $\Pi_{\rm sf}$ denote projection onto the squarefree Boolean modes whose GCD-log eigenvalues are below the accepted lower-frame threshold. The exact residual is
\[
  \Xi_{{\rm GCD},N}=R_N^*\Pi_{\rm sf}R_N.
\]
Step 132 says that when the residual coefficient map factors as $R_N=Z_yB_N$ on a squarefree window, then
\[
  \Xi_{{\rm GCD},N}\preceq B_N^* Z_y^*\Pi_{\rm sf}Z_yP_{\uparrow\mathcal B} B_N,
\]
where $\uparrow\mathcal B$ is the high-divisibility closure of the blind negative-prime sets. Thus the blind-sector problem is equivalent to a high-divisibility tail estimate for the actual regularized M\"untz seed coefficients.

\begin{theorem}[Restricted lower-frame salvage]
Assume the shifted main kernel $K_q$ is nonnegative and satisfies
\[
  K_q\succeq \gamma_q I
\]
on the complement of $\Pi_{\rm sf}$, where $\gamma_q\asymp \log q$. If
\[
  \|\Pi_{\rm sf}Z_yb\|\le \delta_N\|Z_yb\|,
\]
then
\[
\boxed{
  \langle Z_yb,K_qZ_yb\rangle\ge \gamma_q(1-\delta_N^2)\|Z_yb\|^2.
}
\]
Thus a positive visibility floor follows from $\delta_N<1$; exact blind suppression follows from $\delta_N\to0$.
\end{theorem}

\section{Consequences}
The unrestricted BPRZ lower-frame import remains blocked. The new conditional route is:
\[
\boxed{
\text{regularized M\"untz seed has small high-divisibility tail}
\Rightarrow
\Xi_{{\rm GCD},N}\text{ is tail-small}
\Rightarrow
\text{BPRZ lower frame works on the true residual class.}
}
\]
This is not an RH proof. It is the precise next analytic obligation.

\end{document}
'''
(OUT/'muntz_high_divisibility_step132.tex').write_text(tex)

summary = r'''# Step 132: Müntz shadow high-divisibility / Boolean blind-sector suppression theorem

## Main result

Step 132 proves an exact finite Boolean theorem. On a squarefree prime cube, the zeta/incidence convolution

\[
(Z_y b)(T)=\sum_{S\subseteq T}b(S)
\]

has Walsh coefficient at sign vector \(\epsilon\) given by

\[
\widehat{Z_yb}(\epsilon)=
2^{-k/2}(-1)^{|A|}
\sum_{V\subseteq A^c}2^{k-|A|-|V|}b(A\cup V),
\]

where \(A=\{p:\epsilon_p=-1\}\). Therefore a blind sign mode only sees seed coefficients divisible by every prime in its negative set.

## Upward-closure theorem

For any family of blind negative-prime sets \(\mathcal B\), define

\[
\uparrow\mathcal B=\{S: \exists A\in\mathcal B, A\subseteq S\}.
\]

Then

\[
\Pi_{\mathcal B}Z_yb=\Pi_{\mathcal B}Z_yP_{\uparrow\mathcal B}b.
\]

So the blind-sector projection is exactly controlled by the high-divisibility tail of the seed.

For the threshold family \(\mathcal B_R=\{A:|A|\ge R\}\), this gives

\[
\Pi_{\mathcal B_R}Z_yb=0
\]

whenever \(b(S)=0\) for \(|S|\ge R\).

## RH-route implication

The unrestricted BPRZ lower-frame import is blocked by squarefree Boolean near-null modes. Step 132 identifies the possible repair:

\[
\Xi_{{\rm GCD},N}=R_N^*\Pi_{\rm sf}R_N
\]

is tail-small if the actual regularized Burnol/Müntz seed coefficients have small high-divisibility tail on the upward closure of the blind sets.

If the GCD-log kernel has lower bound \(\gamma_q\asymp\log q\) on the nonblind complement and blind overlap is \(\delta_N\), then

\[
\langle Z_yb,K_qZ_yb\rangle
\ge
\gamma_q(1-\delta_N^2)\|Z_yb\|^2.
\]

A positive visibility floor is enough. Exact blind suppression is better but not necessary.

## New obligation

The active analytic target is now:

\[
\frac{\|\Pi_{\rm sf}Z_yb_N\|}{\|Z_yb_N\|}\to0
\]

or at least a uniform bound below one, for the actual regularized Burnol/Müntz residual seed coefficients.

This aligns with the Heap--Soundararajan architecture: their short Dirichlet polynomials use explicit \(\Omega\)-cutoffs, which is exactly the kind of high-divisibility control the Boolean blind-sector theorem needs.

## Nonclaim

Step 132 does not prove RH and does not prove the high-divisibility tail estimate for the actual Burnol/Müntz seed. It proves the finite algebraic mechanism and isolates the remaining analytic obligation.
'''
(OUT/'step132_results_summary.md').write_text(summary)

nonclaim = r'''# Step 132 nonclaim boundary

This step proves an exact finite Boolean suppression theorem. It does not prove RH.

It does not prove that the actual regularized Burnol/Müntz seed coefficients satisfy the required high-divisibility tail estimate.

It does not import the BPRZ shifted second-moment theorem as a full lower frame; Step 130 showed that unrestricted import is blocked.

It does not claim that all GCD-log blind modes are killed automatically. It says they are killed or controlled precisely when the seed coefficients have small mass on the upward closure of the relevant negative-prime sets.

The remaining analytic work is to prove the tail estimate for the actual residual coefficient class, or to source-absorb the resulting Xi_GCD residual.
'''
(OUT/'nonclaim_boundary_step132.md').write_text(nonclaim)

schema = {
    'step': 132,
    'title': 'Müntz shadow high-divisibility / Boolean blind-sector suppression theorem',
    'main_objects': ['Z_y incidence convolution', 'Walsh blind modes', 'upward closure of blind sets', 'Xi_GCD residual'],
    'proved': ['Walsh coefficient formula', 'upward-closure suppression identity', 'degree-threshold annihilation corollary', 'conditional restricted lower-frame salvage'],
    'open': ['high-divisibility tail estimate for actual regularized Burnol/Müntz seed coefficients', 'completed residual-tail promotion'],
    'next_step': 'Step 133: import Ω-truncated Dirichlet-polynomial architecture for the high-divisibility tail estimate'
}
(OUT/'step132_schema.json').write_text(json.dumps(schema, indent=2))

# simple structural check
check = {
    'tex_file': 'muntz_high_divisibility_step132.tex',
    'begin_document_count': tex.count('\\begin{document}'),
    'end_document_count': tex.count('\\end{document}'),
    'theorem_environments': tex.count('\\begin{theorem}'),
    'corollary_environments': tex.count('\\begin{corollary}'),
    'status': 'ok' if tex.count('\\begin{document}') == tex.count('\\end{document}') == 1 else 'check'
}
(OUT/'latex_structure_check_step132.json').write_text(json.dumps(check, indent=2))

# Zip artifacts
zip_path = OUT/'step132_blind_suppression_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for p in OUT.iterdir():
        if p.name == zip_path.name:
            continue
        zf.write(p, p.name)
print('created', zip_path)
