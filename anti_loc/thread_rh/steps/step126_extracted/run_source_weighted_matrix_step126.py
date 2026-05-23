import json, math, csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step126_source_weighted_matrix')
out.mkdir(parents=True, exist_ok=True)

# ---------- finite weighted character Gram models ----------
def primitive_prime_gram(q, support, weights=None, include_principal=False):
    # multiplicative group modulo prime q. support: integers 1..L with L<q.
    # characters indexed by k=0..q-2 using primitive root.
    # Find primitive root brute force
    def is_primitive(g):
        phi=q-1
        factors=[]
        n=phi
        p=2
        while p*p<=n:
            if n%p==0:
                factors.append(p)
                while n%p==0: n//=p
            p+=1
        if n>1: factors.append(n)
        return all(pow(g, phi//p, q)!=1 for p in factors)
    g=next(x for x in range(2,q) if is_primitive(x))
    logmap={1:0}
    cur=1
    for e in range(0,q-1):
        logmap[cur]=e
        cur=(cur*g)%q
    ks=list(range(q-1))
    if not include_principal:
        ks=ks[1:]
    if weights is None:
        weights=np.ones(len(ks))
    support=np.array(support)
    V=np.zeros((len(ks), len(support)), dtype=complex)
    for i,k in enumerate(ks):
        for j,n in enumerate(support):
            e=logmap[n%q]
            V[i,j]=np.exp(2j*np.pi*k*e/(q-1))
    W=np.diag(weights)
    return V.conj().T@W@V

q=257
L=128
support=np.arange(1,L+1)
d=L
rng=np.random.default_rng(126)

scenarios=[]
weight_scenarios={
    'uniform_all': ('all', None, True),
    'uniform_primitive': ('primitive', None, False),
}
# explicit deterministic weights on primitive characters (q-2 weights)
nprim=q-2
idx=np.arange(1,q-1)
# mild positive variation
weight_scenarios['mild_variation_primitive'] = ('primitive', 1+0.15*np.cos(2*np.pi*idx/(q-1)), False)
# stronger variation with positive floor
weight_scenarios['strong_floor_primitive'] = ('primitive', 0.35+0.85*(np.sin(2*np.pi*idx/(q-1))**2), False)
# near-zero sector: not zero, but small weights on a block
w=np.ones(nprim)
w[25:65]=0.02
weight_scenarios['near_zero_block_primitive'] = ('primitive', w, False)
# actual zero block: demonstrates kernel/low eig risk
w2=np.ones(nprim)
w2[25:65]=0.0
weight_scenarios['zero_block_primitive'] = ('primitive', w2, False)

for name,(kind,w,include_principal) in weight_scenarios.items():
    G=primitive_prime_gram(q, support, weights=w, include_principal=include_principal)
    eig=np.linalg.eigvalsh((G+G.conj().T)/2).real
    scenarios.append({
        'scenario': name,
        'q': q,
        'support_size_d': d,
        'include_principal': include_principal,
        'min_eigenvalue': float(eig.min()),
        'median_eigenvalue': float(np.median(eig)),
        'max_eigenvalue': float(eig.max()),
        'condition_number_proxy': float(eig.max()/max(eig.min(),1e-12)),
        'positive': bool(eig.min()>1e-8),
    })

# Write scenario CSV
with open(out/'weighted_character_gram_scenarios_step126.csv','w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(scenarios[0].keys()))
    writer.writeheader(); writer.writerows(scenarios)

# eigenvalue plot
plt.figure(figsize=(9,5))
for name,(kind,w,include_principal) in weight_scenarios.items():
    G=primitive_prime_gram(q, support, weights=w, include_principal=include_principal)
    eig=np.linalg.eigvalsh((G+G.conj().T)/2).real
    plt.plot(np.sort(eig), label=name)
plt.yscale('symlog', linthresh=1e-2)
plt.xlabel('eigenvalue index')
plt.ylabel('weighted Gram eigenvalue')
plt.title('Step 126 weighted character Gram: lower-frame sensitivity')
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(out/'weighted_character_gram_eigenvalues_step126.png', dpi=180)
plt.close()

# fluctuation norm model: w = wbar + delta, lower bound from perturbation norm
rows=[]
floors=np.linspace(0,1.0,41)
for floor in floors:
    # weights with floor plus sinusoidal variation rescaled to mean 1
    w=floor + (1-floor)*(0.5+0.5*np.cos(2*np.pi*idx/(q-1)))
    w=w/np.mean(w)
    G=primitive_prime_gram(q, support, weights=w, include_principal=False)
    G0=primitive_prime_gram(q, support, weights=None, include_principal=False)
    E=G-np.mean(w)*G0
    eig=np.linalg.eigvalsh((G+G.conj().T)/2).real
    eig0=np.linalg.eigvalsh((G0+G0.conj().T)/2).real
    rows.append({
        'floor_parameter':float(floor),
        'mean_weight':float(np.mean(w)),
        'min_weight':float(np.min(w)),
        'lambda_min_actual':float(eig.min()),
        'uniform_base_lambda_min':float(eig0.min()),
        'fluctuation_operator_norm':float(np.linalg.norm(E,2)),
        'weyl_lower_bound':float(np.mean(w)*eig0.min()-np.linalg.norm(E,2)),
    })
with open(out/'weight_fluctuation_bound_step126.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)

plt.figure(figsize=(8,5))
plt.plot([r['floor_parameter'] for r in rows],[r['lambda_min_actual'] for r in rows], label='actual λ_min')
plt.plot([r['floor_parameter'] for r in rows],[r['weyl_lower_bound'] for r in rows], label='Weyl perturbation lower bound')
plt.axhline(0, linestyle='--')
plt.xlabel('declared weight floor parameter')
plt.ylabel('lower-frame strength')
plt.title('Step 126: fluctuation control versus actual lower frame')
plt.legend()
plt.tight_layout()
plt.savefig(out/'weight_fluctuation_lower_bound_step126.png', dpi=180)
plt.close()

# matrix moment import map: toy coefficient dimension d and q conductor ratio
Q_vals=np.array([257,509,1021,2039,4093])
rows2=[]
for Q in Q_vals:
    for theta in [0.45,0.5,0.55,0.6,0.75,0.9]:
        Lmax=int(Q**theta)
        # prime-conductor exact finite frame all chars if L<q; primitive min q-1-d
        gamma=max(Q-1-Lmax,0)
        rows2.append({'q':int(Q),'theta_len':theta,'support_size_floor_q_theta':Lmax,'primitive_lower_frame_gamma':gamma,'legal_no_alias':Lmax<Q})
with open(out/'prime_conductor_length_regimes_step126.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(rows2[0].keys()))
    writer.writeheader(); writer.writerows(rows2)

plt.figure(figsize=(8,5))
for theta in sorted(set(r['theta_len'] for r in rows2)):
    rr=[r for r in rows2 if r['theta_len']==theta]
    plt.plot([r['q'] for r in rr],[r['primitive_lower_frame_gamma'] for r in rr], marker='o', label=f'θ={theta}')
plt.xscale('log'); plt.yscale('symlog', linthresh=1)
plt.xlabel('prime conductor q')
plt.ylabel('primitive γ = q-1-|N|')
plt.title('Step 126 finite primitive lower-frame strength by length regime')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'prime_conductor_length_regimes_step126.png', dpi=180)
plt.close()

# literature import table
literature_rows=[
    {'source':'Finite character orthogonality','imported_statement':'Complete characters mod prime q give exact coefficient lower frame when support length < q.','framework_use':'Finite source block; not a completed proof without tail/exhaustivity.','remaining_gap':'Source weighting, normalization, completed promotion.'},
    {'source':'Conrey-Iwaniec-Soundararajan asymptotic large sieve','imported_statement':'Asymptotic large sieve for linear forms in primitive Dirichlet characters.','framework_use':'Candidate source-weighted/asymptotic coefficient Gram technology.','remaining_gap':'Need lower-frame form uniform over residual coefficient vectors with project-specific weights.'},
    {'source':'Heap-Soundararajan lower moments','imported_statement':'Short Dirichlet polynomials mimic zeta powers and yield scalar lower moment bounds.','framework_use':'Template for source strength gamma_N.','remaining_gap':'Scalar lower bound is not an operator-valued lower frame.'},
    {'source':'Pratt-Robles perturbed moments','imported_statement':'General Dirichlet polynomial A(s) in perturbed zeta moments and longer mollifier range.','framework_use':'Model for coefficient-uniform/polarizable moment estimates.','remaining_gap':'t-aspect scalar/weighted estimates still need residual matrix lower-frame import.'},
    {'source':'Tang-Wu mixed moments 2025','imported_statement':'Twisted mixed moments over primitive characters modulo q with power-saving error.','framework_use':'Candidate q/hybrid-aspect platform for source weights.','remaining_gap':'Need lower-frame positivity for arbitrary residual coefficient vectors, not only scalar asymptotics.'},
    {'source':'Gao-Wu-Zhao mollified fourth moment 2025','imported_statement':'Mollified fourth moment for Dirichlet L-functions to modulus q with polynomial length q^{1/22-eps}.','framework_use':'Concrete q-aspect source-weight length boundary.','remaining_gap':'Length may be too short unless conductor decoupling/visibility floors compensate.'},
    {'source':'Burnol Sonine/co-Poisson corpus','imported_statement':'Carrier/exhaustivity and co-Poisson/Müntz bridge.','framework_use':'Residual coefficient visibility and tail ledger.','remaining_gap':'Burnol-to-Dirichlet readability and boundary residual inclusion.'},
    {'source':'CCM semilocal Hardy-Titchmarsh/Sonin','imported_statement':'Semilocal response geometry and single-prime moment/Jacobi scaffolding.','framework_use':'Ambient Hilbert room for semilocal cross-term.','remaining_gap':'No completed lower-frame/source absorption theorem.'},
]
with open(out/'literature_import_table_step126.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(literature_rows[0].keys()))
    writer.writeheader(); writer.writerows(literature_rows)

# gate table
gate_rows=[
    {'gate':'W0 unweighted finite frame','statement':'For prime q and L<q, complete characters give G=(q-1)I; primitive gives (q-1)I-11*.','status':'settled finite algebra'},
    {'gate':'W1 source weighting','statement':'Replace uniform weights by source weights w_chi and prove G_w >= gamma H.','status':'active analytic import'},
    {'gate':'W2 fluctuation control','statement':'If G_w = wbar G0 + E and ||E|| < wbar lambda_min(G0), lower frame survives.','status':'functional-analytic sufficient criterion'},
    {'gate':'W3 positive floor','statement':'If w_chi >= w_min >0, then G_w >= w_min G0.','status':'usually unavailable for L-weights'},
    {'gate':'W4 matrix moment asymptotic','statement':'Uniform asymptotic for all coefficient vectors: a*G_w a = Main(a)+Err(a), Main>=gamma||a||_H^2, Err<=eps Main.','status':'desired operator-valued lift'},
    {'gate':'W5 visibility coupling','statement':'Combine G_w lower frame with c_hyb,N from Burnol-to-Dirichlet readability.','status':'framework-native Xi gate'},
    {'gate':'W6 tail promotion','statement':'Promote finite coefficient windows to completed residual ledger with vanishing tail.','status':'still open'},
    {'gate':'W7 no-smuggling','statement':'Characters, weights, supports, and normalizations declared upstream; no target-selected coefficients.','status':'mandatory discipline'},
]
with open(out/'source_weighted_gate_table_step126.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(gate_rows[0].keys()))
    writer.writeheader(); writer.writerows(gate_rows)

# theorem map
thm_rows=[
    {'name':'Weighted source Gram','formula':'G_{q,w}(m,n)=sum_{chi in X_q} w_chi chi(n) conjugate(chi(m))','role':'source currency on coefficient space'},
    {'name':'Perturbative lower-frame criterion','formula':'G_w >= wbar G_0 - ||E_w|| I','role':'sufficient criterion when weights are near uniform'},
    {'name':'Matrix moment lower-frame criterion','formula':'a^*G_w a >= gamma a^*H a for all a','role':'operator-valued import target'},
    {'name':'Residual absorption consequence','formula':'R_N^*G_w R_N >= gamma c_hyb,N G_R,N','role':'connects source frame to Xi^{BC} residual'},
    {'name':'Completed promotion condition','formula':'F_N + Lambda_N T_N >= Lambda_N G_R','role':'finite-to-completed ledger promotion'},
]
with open(out/'theorem_map_step126.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(thm_rows[0].keys()))
    writer.writeheader(); writer.writerows(thm_rows)

# route status
route_rows=[
    {'component':'unweighted finite prime conductor frame','status':'closed','next_action':'use as baseline not as RH proof'},
    {'component':'source-weighted character Gram','status':'open','next_action':'import/as-formalize matrix moment asymptotic'},
    {'component':'visibility c_hyb,N','status':'separate Xi gate','next_action':'feed Step 121-124 errors into lower-frame product'},
    {'component':'completed residual tail','status':'open','next_action':'Burnol/semilocal Plancherel-exhaustivity record'},
    {'component':'existing analytic NT machinery','status':'must import','next_action':'map each theorem to W1-W4 gates rather than rederive'},
]
with open(out/'route_status_step126.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(route_rows[0].keys()))
    writer.writeheader(); writer.writerows(route_rows)

# arithmetic input table
arith_rows=[
    {'input':'uniform complete character orthogonality','needed_for':'baseline gamma_N','available':'yes finite prime q'},
    {'input':'primitive character correction','needed_for':'nonprincipal source family','available':'yes finite rank-one defect for prime q'},
    {'input':'asymptotic large sieve / bilinear primitive-character asymptotic','needed_for':'weighted/asymptotic coefficient Gram','available':'literature platform, not yet imported as lower frame'},
    {'input':'mollified/mixed moment asymptotic with arbitrary coefficient vector','needed_for':'L-weighted G_w lower frame','available':'partial in literature; operator lower-frame formulation new'},
    {'input':'positive main term matrix','needed_for':'Main(a)>=gamma||a||^2','available':'must be identified from imported theorem'},
    {'input':'operator-norm error bound','needed_for':'Err<=epsilon Main uniformly','available':'hard gap'},
    {'input':'source currency normalization','needed_for':'meaning of gamma_N divergence','available':'framework record required'},
]
with open(out/'arithmetic_input_table_step126.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(arith_rows[0].keys()))
    writer.writeheader(); writer.writerows(arith_rows)

# nonclaim boundary
(out/'nonclaim_boundary_step126.md').write_text('''# Step 126 nonclaim boundary

This step does not prove RH and does not prove a completed Hecke/Dirichlet source ladder.

Accepted finite facts:
- Complete characters modulo a prime give an exact finite coefficient frame when the coefficient support does not alias modulo q.
- Removing the principal character for prime q creates a rank-one defect.

Not claimed:
- Existing scalar moment lower bounds imply an operator-valued lower frame.
- Large-sieve upper bounds imply source coercivity.
- Finite conductor windows promote to a completed residual ledger without tail/exhaustivity.
- L-weighted source weights have a positive pointwise floor.
- Any target-selected character family or mollifier is lawful.

The active missing object is a source-weighted matrix lower-frame theorem:

    G_{q,w} \succeq \gamma_{q,w} H_N

uniformly over residual coefficient vectors and compatible with the Burnol/semilocal tail records.
''')

# summary and tex
summary = r'''# Step 126: Source-weighted matrix lower-frame import

## Main output

The unweighted finite prime-conductor block is settled, but the RH-relevant source route needs a source-weighted matrix lower frame:

\[
G_{q,w}(m,n)=\sum_{\chi\in\mathcal X_q} w_\chi\chi(n)\overline{\chi(m)}
\succeq \gamma_{q,w} H_N.
\]

For prime \(q\), support \(\mathcal N_N\subset\{1,\dots,L_N\}\), and \(L_N<q\), complete character orthogonality gives

\[
G_q^{\rm all}=(q-1)I.
\]

Removing the principal character gives

\[
G_q^{\rm prim}=(q-1)I-\mathbf 1\mathbf 1^*,
\]

so

\[
\lambda_{\min}(G_q^{\rm prim})=q-1-d_N,
\qquad d_N=|\mathcal N_N|.
\]

This finite frame is not the hard part anymore.

## Active import target

The hard analytic import is the weighted lower-frame theorem:

\[
\sum_{\chi\in\mathcal X_q}w_\chi\left|\sum_{n\in\mathcal N_N}a_n\chi(n)\right|^2
\ge \gamma_{q,w}\|a\|_{H_N}^2
\quad\text{for every }a.
\]

Existing moment and asymptotic-large-sieve results are relevant platforms, but scalar moments do not automatically give this operator-valued inequality.

## Three sufficient routes

1. **Weight floor:** if \(w_\chi\ge w_{\min}>0\), then \(G_{q,w}\ge w_{\min}G_q\). This is usually unavailable for L-weighted sources.

2. **Fluctuation control:** if \(G_{q,w}=\bar wG_q+E_w\) and \(\|E_w\|<\bar w\lambda_{\min}(G_q)\), the lower frame survives.

3. **Matrix moment asymptotic:** prove uniformly in coefficient vectors

\[
a^*G_{q,w}a=\operatorname{Main}(a)+\operatorname{Err}(a),
\qquad
\operatorname{Main}(a)\ge\gamma\|a\|_{H_N}^2,
\qquad
|\operatorname{Err}(a)|\le\varepsilon\operatorname{Main}(a).
\]

This is the project-native operator-valued lift.

## Framework consequence

Combining the weighted lower frame with residual coefficient visibility gives

\[
R_N^*G_{q,w}R_N
\succeq
\gamma_{q,w}c_{\rm hyb,N}G_{R,N}.
\]

The completed residual source route still needs

\[
\gamma_{q,w}c_{\rm hyb,N}\to\infty
\]

plus fixed/exhaustive tail promotion.

## Status

Step 126 imports standard analytic-number-theory infrastructure and identifies the exact nonstandard demand:

\[
\boxed{\text{a source-weighted matrix lower frame on the residual coefficient space.}}
\]

The next step should not re-prove character orthogonality. It should map a specific existing theorem—CIS/asymptotic large sieve, Tang--Wu mixed moments, Pratt--Robles perturbed moments, or recent mollified fourth moments—onto the matrix lower-frame gates and mark exactly which hypotheses fail.
'''
(out/'step126_results_summary.md').write_text(summary)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,booktabs,geometry}
\geometry{margin=1in}
\title{Step 126: Source-Weighted Matrix Lower-Frame Import}
\author{Riemann Membrane / Six Birds Construction Log}
\date{May 14, 2026}
\begin{document}
\maketitle

\section{Purpose}
Step 125 closed the finite unweighted character frame.  Step 126 imports the analytic-number-theory landscape and isolates the genuinely new demand of the membrane route: a source-weighted matrix lower frame on the residual coefficient space.

\section{Finite baseline}
Let $q$ be prime, $\mathcal N_N\subset\{1,\ldots,L_N\}$, $L_N<q$, and $d_N=|\mathcal N_N|$.  For complete characters modulo $q$,
\[
\sum_{\chi\bmod q}\left|\sum_{n\in\mathcal N_N}a_n\chi(n)\right|^2=(q-1)\sum_{n\in\mathcal N_N}|a_n|^2.
\]
Thus
\[
G_q^{\rm all}=(q-1)I.
\]
For primitive characters modulo prime $q$, i.e. after removing the principal character,
\[
G_q^{\rm prim}=(q-1)I-\mathbf 1\mathbf 1^*,
\]
so
\[
\lambda_{\min}(G_q^{\rm prim})=q-1-d_N.
\]
This block is settled finite algebra.  It is not the completed RH source theorem.

\section{Weighted source Gram}
Let $w_\chi\ge0$ be the declared source weight/currency.  The active object is
\[
G_{q,w}(m,n)=\sum_{\chi\in\mathcal X_q}w_\chi\chi(n)\overline{\chi(m)}.
\]
The desired lower frame is
\[
G_{q,w}\succeq\gamma_{q,w}H_N.
\]
Equivalently,
\[
\sum_{\chi\in\mathcal X_q}w_\chi\left|\sum_{n\in\mathcal N_N}a_n\chi(n)\right|^2\ge\gamma_{q,w}\|a\|_{H_N}^2
\]
for all coefficient vectors $a$.

\section{Three sufficient criteria}
\subsection{Weight floor}
If $w_\chi\ge w_{\min}$ for all $\chi$, then
\[
G_{q,w}\succeq w_{\min}G_q.
\]
This is simple but usually unavailable for $L$-weighted sources.

\subsection{Fluctuation control}
Write
\[
G_{q,w}=\bar wG_q+E_w.
\]
Then
\[
G_{q,w}\succeq (\bar w\lambda_{\min}(G_q)-\|E_w\|)I.
\]
Thus the lower frame survives if
\[
\|E_w\|<\bar w\lambda_{\min}(G_q).
\]

\subsection{Matrix moment asymptotic}
The import target from analytic number theory is a uniform quadratic-form asymptotic:
\[
a^*G_{q,w}a=\operatorname{Main}(a)+\operatorname{Err}(a),
\]
with
\[
\operatorname{Main}(a)\ge\gamma\|a\|_{H_N}^2,
\qquad
|\operatorname{Err}(a)|\le\varepsilon\operatorname{Main}(a).
\]
This yields
\[
G_{q,w}\succeq (1-\varepsilon)\gamma H_N.
\]
Scalar moment lower bounds are insufficient unless they are uniform over all residual coefficient vectors.

\section{Residual source consequence}
Let $R_N$ be the residual coefficient map and suppose
\[
R_N^*H_NR_N\succeq c_{\rm hyb,N}G_{R,N}.
\]
Then
\[
R_N^*G_{q,w}R_N\succeq\gamma_{q,w}c_{\rm hyb,N}G_{R,N}.
\]
The completed route requires
\[
\gamma_{q,w}c_{\rm hyb,N}\to\infty,
\]
with residual tail/exhaustivity.

\section{Imported literature status}
The asymptotic-large-sieve and moment literature supplies candidate scalar and bilinear estimates.  The framework-native gap is the operator-valued lower-frame form on the residual coefficient space, with no target-selected sources and no finite-window overread.

\section{Nonclaim}
This step does not prove a completed source ladder.  It closes the finite unweighted block and identifies the exact weighted matrix import target.

\end{document}
'''
(out/'source_weighted_matrix_step126.tex').write_text(tex)

schema={
    'step':126,
    'title':'Source-weighted matrix lower-frame import',
    'main_object':'G_{q,w}(m,n)=sum_chi w_chi chi(n) conjugate(chi(m))',
    'finite_baseline':'For prime q and L<q, complete characters give (q-1)I; primitive gives (q-1)I-11*.',
    'active_gate':'G_{q,w} >= gamma_{q,w} H_N uniformly over residual coefficient vectors',
    'sufficient_routes':['weight_floor','fluctuation_control','matrix_moment_asymptotic'],
    'framework_output':'R_N^* G_{q,w} R_N >= gamma_{q,w} c_hyb,N G_R,N',
    'remaining_gaps':['source_weighted_matrix_moment','visibility_coupling','tail_exhaustivity','source_currency_normalization']
}
(out/'step126_schema.json').write_text(json.dumps(schema, indent=2))

# zip selected
import zipfile
zip_path=out/'step126_source_weighted_matrix_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)
print('created', out, 'files', len(list(out.iterdir())))
