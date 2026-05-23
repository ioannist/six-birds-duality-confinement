from pathlib import Path
import json, csv, math, zipfile
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step128_twisted_second_moment_import')
out.mkdir(parents=True, exist_ok=True)

step = 128

def write(path, text):
    (out/path).write_text(text, encoding='utf-8')

# Core notes
tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,booktabs,enumitem,geometry,hyperref}
\geometry{margin=1in}
\title{Step 128: Auditing the $q$-Aspect Twisted Second Moment as a Matrix Lower-Frame Theorem}
\author{Six Birds / Membrane RH Working Notes}
\date{}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{warning}{Warning}
\begin{document}
\maketitle

\section*{Purpose}
Step 127 identified the next import target: a source-weighted character Gram
\[
G_{q,w}(m,n)=\sum_{\chi\in\mathcal X_q} w_\chi\chi(n)\overline{\chi(m)}
\]
must dominate a coefficient metric $H_N$ uniformly over coefficient vectors. Step 128 audits the
most natural existing platform:
\[
\sum_{\chi\bmod q}^{+} |L(1/2,\chi)|^2\left|\sum_{n\le q^\kappa} a_n\chi(n)n^{-1/2}\right|^2,
\]
using the $q$-aspect twisted second moment with an arbitrary Dirichlet polynomial.

The goal is not to rederive the approximate functional equation, mollifier-length technology, or
large-sieve machinery. Those are imported analytic-number-theory infrastructure. The framework-native
question is whether the published asymptotic is strong enough in \emph{operator norm} to imply a lower frame.

\section{Imported theorem shape}
The Bui--Pratt--Robles--Zaharescu theorem has the form, for prime $q$, even primitive characters, shifts
$\alpha,\beta$, and arbitrary coefficients $\alpha_a\ll a^\varepsilon$,
\[
I_{\alpha,\beta}(a)=\frac1{\varphi^+(q)}\sum_{\chi\bmod q}^{+}
L(1/2+\alpha,\chi)L(1/2+\beta,\overline\chi)|A(\chi)|^2
=M_{\alpha,\beta,q}(a)+E_{\alpha,\beta,q}(a),
\]
where
\[
A(\chi)=\sum_{a\le q^\kappa}\alpha_a\chi(a)a^{-1/2},
\qquad \kappa<\frac{51}{101}.
\]
The project reads this as a candidate source-weighted quadratic form.

\section{Matrix lower-frame import criterion}
\begin{definition}[Matrix lower-frame import]
The twisted second moment imports as a membrane source record on a coefficient window $V_q$ if there are
positive constants $\gamma_q$ and $\varepsilon_q<1$ such that, for every coefficient vector $a\in V_q$,
\[
M_q(a)\ge \gamma_q\|a\|_{H_q}^2,
\qquad |E_q(a)|\le \varepsilon_q\gamma_q\|a\|_{H_q}^2.
\]
Then
\[
G_{q,w}\succeq (1-\varepsilon_q)\gamma_q H_q.
\]
\end{definition}

\begin{theorem}[Conditional matrix import]
Assume that the shifted second-moment asymptotic admits a homogeneous, coefficient-uniform formulation on
$V_q$, and that the shifted main term has a positive critical-line limit satisfying
\[
M_q(a)\ge c_0(\log q)\|a\|_{H_q}^2
\]
for all $a\in V_q$, with the error bounded by
\[
|E_q(a)|\le \varepsilon_q c_0(\log q)\|a\|_{H_q}^2,
\qquad \varepsilon_q<1.
\]
Then the normalized weighted Gram
\[
G_{q,|L|^2}^{\rm norm}(m,n)
=\frac1{\varphi^+(q)}\sum_{\chi\bmod q}^{+}|L(1/2,\chi)|^2\chi(m)\overline{\chi(n)}
\]
satisfies
\[
G_{q,|L|^2}^{\rm norm}\succeq (1-\varepsilon_q)c_0(\log q)H_q.
\]
Thus the source strength is $\gamma_q\asymp\log q$ in normalized currency.
\end{theorem}

\section{Audit verdict}
The existing theorem is structurally adjacent, but it is not yet a finished framework import. The remaining
records are:
\begin{enumerate}[label=\textbf{R\arabic*.}]
\item \textbf{Homogeneous coefficient norm.} Convert the arbitrary coefficient hypothesis into a normalized operator domain $V_q$.
\item \textbf{Main-term positivity.} Prove the $\alpha,\beta\to0$ main kernel is positive with a uniform lower eigenvalue.
\item \textbf{Uniform error.} Replace scalar/asymptotic error notation by an operator-norm bound subordinate to the main form.
\item \textbf{Parity and primitive records.} Even-character restriction and principal removal must be tracked as finite-rank or sector records.
\item \textbf{Length compatibility.} The length $q^\kappa$ must be compatible with the regularized Müntz shadow and the residual coefficient window.
\item \textbf{Source normalization.} Decide whether the source currency is normalized by $\varphi^+(q)$ or accumulated unnormalized.
\end{enumerate}

\section{Framework coupling}
The source lower frame couples to the residual visibility gate by
\[
R_N^*H_NR_N\succeq c_{{\rm hyb},N}G_{R,N}.
\]
If
\[
G_{q,w}\succeq\gamma_{q,w}H_N,
\]
then
\[
R_N^*G_{q,w}R_N\succeq \gamma_{q,w}c_{{\rm hyb},N}G_{R,N}.
\]
The completed membrane route requires
\[
\gamma_{q,w}c_{{\rm hyb},N}\to\infty
\]
with fixed/exhaustive residual-tail promotion.

\section{Conclusion}
The $q$-aspect twisted second moment with arbitrary Dirichlet polynomial is the right first external theorem platform. It already supplies the closest scalar/bilinear object to our source-weighted Gram. What remains genuinely new is converting that theorem into a lower-eigenvalue statement on the residual coefficient class, i.e. the matrix-lift / $\Xi$-adequacy import.
\end{document}
'''
write('twisted_second_moment_matrix_import_step128.tex', tex)

summary = r'''
# Step 128: q-aspect twisted second moment as a matrix lower-frame theorem

## Verdict
The Bui--Pratt--Robles--Zaharescu twisted second moment is the right first analytic-number-theory platform for the source-weighted matrix lower frame.

It studies

\[
\sum_{\chi\bmod q}^{+}
|L(1/2,\chi)|^2
\left|\sum_{n\le q^\kappa} a_n\chi(n)n^{-1/2}\right|^2
\]

for arbitrary Dirichlet-polynomial coefficients and reaches

\[
\kappa<51/101=1/2+1/202.
\]

But it does **not automatically** give the membrane source record. The project needs the theorem in matrix lower-frame form:

\[
G_{q,w}\succeq \gamma_{q,w}H_N
\]

uniformly over every residual coefficient vector.

## Conditional import theorem
If the published asymptotic can be rewritten as

\[
a^*G_{q,w}a=M_q(a)+E_q(a)
\]

with

\[
M_q(a)\ge c_0(\log q)\|a\|_{H_q}^2
\]

and

\[
|E_q(a)|\le \varepsilon_q c_0(\log q)\|a\|_{H_q}^2,
\qquad \varepsilon_q<1,
\]

then

\[
G_{q,w}\succeq (1-\varepsilon_q)c_0(\log q)H_q.
\]

So normalized source strength is of order \(\log q\). Unnormalized source strength is of order \(q\log q\), subject to the source-currency audit.

## What remains new
The existing analytic NT theorem supplies a scalar/bilinear asymptotic for arbitrary coefficients. The framework still needs:

1. homogeneous coefficient normalization;
2. positivity of the shifted main kernel after \(\alpha,\beta\to0\);
3. operator-norm error subordinate to the main term;
4. parity/primitive/principal-character defect records;
5. compatibility with the Burnol-to-Dirichlet shadow length;
6. fixed/exhaustive residual-tail promotion.

## Route status
This step imports the standard q-aspect twisted-second-moment platform and isolates the project-native gap:

\[
\text{arbitrary-coefficient moment asymptotic}
\quad\not\Rightarrow\quad
\text{matrix lower frame without a lower-eigenvalue audit.}
\]

## Next step
Step 129 should audit the main term itself: take the Bui--Pratt--Robles--Zaharescu shifted main term, pass to \(\alpha,\beta\to0\), and decide whether the resulting kernel has a uniform positive lower bound on the residual coefficient class.
'''
summary = summary.replace('\u007f','')
write('step128_results_summary.md', summary)

literature_rows = [
    ['platform','what it supplies','length/aspect','framework status'],
    ['Bui-Pratt-Robles-Zaharescu 2018','q-aspect twisted second moment by square of arbitrary Dirichlet polynomial','prime q, length q^{51/101}','best first matrix-import candidate'],
    ['CIS asymptotic large sieve 2011','coefficient-uniform bilinear forms over primitive characters','q-aspect with modulus averaging','baseline bilinear infrastructure, likely upper/asymptotic not lower by itself'],
    ['Pratt-Robles 2018','perturbed moments with a general Dirichlet polynomial','t-aspect, longer mollifier','polarization/uniformity model, not directly q-source carrier'],
    ['Tang-Wu 2025','power-saving mixed moments of twisted L-functions over primitive characters','hybrid/general q','future platform for richer weights'],
    ['Gao-Wu-Zhao 2025','mollified fourth moment for Dirichlet L-functions','q-aspect, short mollifier length','length constraint platform'],
    ['Burnol co-Poisson/Sonine','carrier, zero-evaluator completeness/minimality, Müntz bridge','Sonine/co-Poisson carrier','visibility side, not source-strength side'],
]
with open(out/'literature_import_table_step128.csv','w',newline='',encoding='utf-8') as f:
    csv.writer(f).writerows(literature_rows)

gate_rows = [
    ['gate','mathematical statement','status after Step 128','failure mode'],
    ['T1 source-weighted Gram','G_{q,w}(m,n)=sum w_chi chi(n)conj(chi(m))','defined','not enough without lower eigenvalue'],
    ['T2 finite unweighted frame','G_q=(q-1)I for complete chars and L<q','settled in Step 125','aliasing if L>=q'],
    ['T3 BPRZ asymptotic','I_{alpha,beta}=Main+Err for arbitrary coefficients length q^{kappa}, kappa<51/101','import candidate','not yet operator lower frame'],
    ['T4 main positivity','Main_0(a)>=c log(q)||a||^2_H uniformly','open','main kernel could have soft directions'],
    ['T5 subordinate error','|Err(a)|<=epsilon Main(a) uniformly in a','open','asymptotic not in operator norm'],
    ['T6 parity/primitive record','even/primitive restriction tracked','partially standard','sector loss or rank defect'],
    ['T7 source normalization','normalized vs unnormalized source currency declared','open','fake divergence if normalization chosen after target'],
    ['T8 residual-tail promotion','finite source frame promotes to completed residual sector','open','moving-window support-only'],
]
with open(out/'twisted_second_moment_gate_table_step128.csv','w',newline='',encoding='utf-8') as f:
    csv.writer(f).writerows(gate_rows)

arithmetic_rows = [
    ['input','needed form','existing source','project use'],
    ['arbitrary coefficient asymptotic','uniform for all coefficient vectors in window','BPRZ Theorem 1.1','candidate matrix moment'],
    ['critical shift limit','alpha,beta -> 0 with pole cancellation audited','standard shifted moment calculus','construct main kernel M_q'],
    ['main kernel lower bound','lambda_min(M_q/H_q) >= c log q','not directly named in literature','new matrix/eigenvalue audit'],
    ['operator norm error','||H^{-1/2}Err H^{-1/2}|| <= eps log q','not automatic','new matrix import requirement'],
    ['length constraint','kappa<51/101 for arbitrary coefficients','BPRZ','must satisfy Step 123 balance'],
    ['special coefficients','longer range under convolution/smooth hypotheses','BPRZ Theorems 1.2/1.3','maybe useful if Burnol shadows have structure'],
    ['completed carrier tail','finite q windows exhaust residual sector','none automatic','framework fixed/exhaustive ledger'],
]
with open(out/'arithmetic_input_table_step128.csv','w',newline='',encoding='utf-8') as f:
    csv.writer(f).writerows(arithmetic_rows)

theorem_rows = [
    ['item','statement','role'],
    ['Definition','source-weighted Gram G_{q,w}','operator object to dominate H_N'],
    ['Theorem 128.1','Main + error + uniform positivity implies lower frame','conditional import theorem'],
    ['Proposition','BPRZ is adjacent but not sufficient without T4/T5','no-overread result'],
    ['Corollary','if gamma_q ~ log q and c_hyb >= c0>0 then residual source strength diverges','route payoff'],
]
with open(out/'theorem_map_step128.csv','w',newline='',encoding='utf-8') as f:
    csv.writer(f).writerows(theorem_rows)

route_rows = [
    ['route piece','status','next action'],
    ['finite unweighted prime frame','closed','keep as exact algebra block'],
    ['source-weighted |L|^2 frame','candidate','audit main kernel lower bound'],
    ['BPRZ arbitrary polynomial theorem','imported platform','translate into homogeneous matrix form'],
    ['Heap-Sound scalar source strength','template only','do not overread scalar direction'],
    ['Burnol/co-Poisson visibility','separate c_hyb side','continue angular-gap/tail audits'],
    ['completed RH membrane','not proved','requires lower frame + visibility + tail promotion'],
]
with open(out/'route_status_step128.csv','w',newline='',encoding='utf-8') as f:
    csv.writer(f).writerows(route_rows)

nonclaim = r'''
# Step 128 nonclaim boundary

Step 128 does not prove RH.

It does not prove that the Bui--Pratt--Robles--Zaharescu theorem already yields a matrix lower frame.

It does not prove that the shifted main term is uniformly positive on the residual coefficient class.

It does not prove that the published error term is subordinate in operator norm.

It does not license replacing scalar lower moments or one chosen mollifier direction by a lower eigenvalue statement.

It does not resolve Burnol-to-Dirichlet visibility, Müntz regularization tails, semilocal descent, or fixed/exhaustive promotion.

The accepted output is only a theorem-import audit and a precise list of remaining gates.
'''
write('nonclaim_boundary_step128.md', nonclaim)

schema = {
    'step': 128,
    'title': 'q-aspect twisted second moment as source-weighted matrix lower-frame theorem',
    'active_object': 'G_{q,w}(m,n)=sum_chi w_chi chi(n)conj(chi(m))',
    'primary_external_platform': 'Bui-Pratt-Robles-Zaharescu arXiv:1808.10803',
    'length_range_arbitrary_coefficients': 'kappa < 51/101',
    'framework_target': 'G_{q,w} >= gamma_{q,w} H_N uniformly over residual coefficient vectors',
    'conditional_source_strength_normalized': 'gamma_q ~ log q if main positivity and subordinate error pass',
    'new_gaps': ['main-term lower eigenvalue', 'operator-norm error', 'homogeneous coefficient normalization', 'parity/primitive records', 'tail promotion'],
    'next_step': 'Audit shifted main-term positivity at alpha,beta -> 0'
}
write('step128_schema.json', json.dumps(schema, indent=2))

# Plots and data
# 1 length range regimes and import status.
kappas = np.linspace(0.1,0.8,400)
threshold_bprz = 51/101
threshold_half = 0.5
# modeled margin positive if below threshold_bprz
margin = threshold_bprz - kappas
with open(out/'length_regime_table_step128.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['kappa','below_1_2','below_BPRZ_51_101','margin_to_BPRZ'])
    for k,m in zip(kappas[::5],margin[::5]):
        w.writerow([f'{k:.5f}', int(k<threshold_half), int(k<threshold_bprz), f'{m:.5f}'])
plt.figure(figsize=(7,4))
plt.axvline(threshold_half, linestyle='--', label='1/2 barrier')
plt.axvline(threshold_bprz, linestyle='-', label='BPRZ 51/101')
plt.plot(kappas, margin)
plt.axhline(0)
plt.xlabel('Dirichlet polynomial length exponent kappa')
plt.ylabel('margin to BPRZ arbitrary-coefficient range')
plt.title('Step 128 length import window')
plt.legend()
plt.tight_layout()
plt.savefig(out/'length_import_window_step128.png', dpi=180)
plt.close()

# 2 main/error lower frame model.
q_exp = np.linspace(3,9,100)
logq = q_exp * math.log(10)
scenarios=[]
for eps0,label in [(0.15,'strong subordinate error'),(0.55,'weak but usable'),(0.95,'near failure'),(1.05,'fails')]:
    gamma = np.maximum(0,(1-eps0)*logq)
    scenarios.append((label, eps0, gamma))
    
plt.figure(figsize=(7,4))
for label,eps0,gamma in scenarios:
    plt.plot(q_exp, gamma, label=f'{label} eps={eps0}')
plt.xlabel('log10 q')
plt.ylabel('certified normalized gamma_q proxy')
plt.title('Matrix lower frame from main/error subordination')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'main_error_lower_frame_model_step128.png', dpi=180)
plt.close()
with open(out/'main_error_lower_frame_model_step128.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['log10_q','scenario','epsilon','gamma_proxy'])
    for i,x in enumerate(q_exp):
        for label,eps0,gamma in scenarios:
            w.writerow([f'{x:.4f}',label,eps0,f'{gamma[i]:.6f}'])

# 3 visibility floor coupling.
q_exp2=np.linspace(3,12,160)
logq2=q_exp2*math.log(10)
visibility=[1.0,0.5,0.1,0.02,0.0]
plt.figure(figsize=(7,4))
for c in visibility:
    eff=c*logq2
    plt.plot(q_exp2,eff,label=f'c_hyb={c}')
plt.xlabel('log10 q')
plt.ylabel('effective normalized source strength c_hyb log q')
plt.title('Visibility floor coupling after BPRZ import')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'visibility_floor_coupling_step128.png', dpi=180)
plt.close()
with open(out/'visibility_floor_coupling_step128.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['log10_q','c_hyb','effective_strength'])
    for i,x in enumerate(q_exp2):
        for c in visibility:
            w.writerow([f'{x:.4f}',c,f'{(c*logq2[i]):.6f}'])

# 4 random weighted Gram checks illustrative.
rng=np.random.default_rng(128)
rows=[]
for d in [8,16,32,64]:
    # base complete frame I; weights fluctuations around 1; eigenvalues of Fourier sample diagonal representation approximated random circulant? Create random diagonal characters matrix unitary-ish.
    # Just model G = U* diag(w) U for square unitary U, with w variations.
    X=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    Q,_=np.linalg.qr(X)
    for sigma in [0.0,0.1,0.3,0.6,1.0]:
        weights=np.exp(sigma*rng.normal(size=d))
        G=Q.conj().T@np.diag(weights)@Q
        eig=np.linalg.eigvalsh((G+G.conj().T)/2)
        rows.append([d,sigma,float(weights.mean()),float(weights.min()),float(eig.min()),float(eig.max())])
with open(out/'weighted_gram_toy_checks_step128.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['dimension','lognormal_sigma','mean_weight','min_weight','min_eigenvalue','max_eigenvalue']); w.writerows(rows)
plt.figure(figsize=(7,4))
for d in [8,16,32,64]:
    xs=[r[1] for r in rows if r[0]==d]
    ys=[r[4] for r in rows if r[0]==d]
    plt.plot(xs,ys,marker='o',label=f'd={d}')
plt.xlabel('weight fluctuation sigma')
plt.ylabel('toy min eigenvalue')
plt.title('Weighted Gram lower eigenvalue sensitivity')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'weighted_gram_lower_eigenvalue_toy_step128.png', dpi=180)
plt.close()

# Check script
script = r'''#!/usr/bin/env python3
"""Step 128 sanity checks: theorem algebra only, not RH evidence."""
import numpy as np
rng = np.random.default_rng(128)
for d in [8, 16, 32]:
    X = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    Q, _ = np.linalg.qr(X)
    weights = np.exp(0.3*rng.normal(size=d))
    G = Q.conj().T @ np.diag(weights) @ Q
    lam_min = np.linalg.eigvalsh((G+G.conj().T)/2).min()
    assert lam_min > 0
print('Step 128 weighted-Gram PSD sanity checks passed.')
'''
write('run_step128_matrix_import.py', script)
(out/'run_step128_matrix_import.py').chmod(0o755)

# Zip selected artifacts
zip_path=out/'step128_twisted_second_moment_import_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)

print('generated', len(list(out.iterdir())), 'files')
