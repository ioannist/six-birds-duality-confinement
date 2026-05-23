import numpy as np
import csv, json, os, zipfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = '/mnt/data/rh_membrane_step101_delta_compactness'
os.makedirs(OUT, exist_ok=True)

def write_csv(path, rows, headers=None):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        if headers: w.writerow(headers)
        w.writerows(rows)

# ---------- Model A: compact kernel and bounded semilocal transport ----------
# A compact/Hilbert-Schmidt kernel K remains compact after bounded conjugation.
N = 220
x = np.linspace(-1, 1, N)
dx = x[1] - x[0]
X, Y = np.meshgrid(x, x)
K = np.exp(-5*np.abs(X-Y)) * dx
sK = np.linalg.svd(K, compute_uv=False)
B = 1.0 + 0.35*np.sin(3*x) + 0.15*np.cos(7*x)
Kt = (B[:, None]) * K * (B[None, :])
sKt = np.linalg.svd(Kt, compute_uv=False)
rows = [[i+1, float(sK[i]), float(sKt[i])] for i in range(len(sK))]
write_csv(os.path.join(OUT,'compact_after_quotient_spectrum_step101.csv'), rows, ['rank','compact_kernel_sv','bounded_transport_sv'])
plt.figure(figsize=(7,4.2))
plt.semilogy(range(1,len(sK)+1), sK, label='compact kernel')
plt.semilogy(range(1,len(sKt)+1), sKt, label='bounded semilocal transport')
plt.xlabel('rank')
plt.ylabel('singular value')
plt.title('Compact residual survives bounded transport')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT,'compact_after_quotient_spectrum_step101.png'), dpi=180)
plt.close()

# ---------- Model B: raw finite-place multiplier deformation ----------
# Multiplication by a nonzero bounded function is not compact on non-atomic L2.
primes = [2,3,5]
def local_factor_mod2(xi):
    z = np.ones_like(xi, dtype=complex)
    for p in primes:
        z *= 1.0/(1 - p**(-0.5)*np.exp(1j*xi*np.log(p)))
    return np.abs(z)**2
Ns = [128,256,512,1024,2048]
summary = []
for n in Ns:
    xi = np.linspace(-80,80,n,endpoint=False)
    m = local_factor_mod2(xi)
    # normalized deformation symbol; nonzero on a positive-measure set.
    phi = np.abs(m/np.mean(m)-1.0)
    sv = np.sort(phi)[::-1]
    summary.append([n, float(sv[0]), float(np.quantile(sv,0.75)), float(np.quantile(sv,0.5)), float(np.mean(sv>0.05)), float(np.mean(sv>0.01))])
write_csv(os.path.join(OUT,'multiplication_noncompact_proxy_step101.csv'), summary, ['grid_N','max_sv_proxy','q75_sv_proxy','median_sv_proxy','frac_gt_0p05','frac_gt_0p01'])
# Long profile for largest N
n=2048
xi = np.linspace(-80,80,n,endpoint=False)
phi = np.abs(local_factor_mod2(xi)/np.mean(local_factor_mod2(xi))-1.0)
sv_mult = np.sort(phi)[::-1]
write_csv(os.path.join(OUT,'noncompact_multiplier_residue_step101.csv'), [[i+1,float(sv_mult[i])] for i in range(n)], ['rank','sv_proxy'])
plt.figure(figsize=(7,4.2))
plt.semilogy(range(1,n+1), sv_mult)
plt.xlabel('rank')
plt.ylabel('singular value proxy')
plt.title('Raw finite-place multiplier: noncompact proxy')
plt.tight_layout()
plt.savefig(os.path.join(OUT,'multiplication_noncompact_proxy_step101.png'), dpi=180)
plt.close()

# ---------- Model C: compact vs noncompact residue profile ----------
ranks = np.arange(1,1001)
compact = 1/(ranks**1.8)
noncompact_floor = 0.18 + 0.12*np.abs(np.sin(0.11*ranks))
combined = compact + noncompact_floor
write_csv(os.path.join(OUT,'combined_compact_noncompact_residue_step101.csv'), [[int(r), float(compact[i]), float(noncompact_floor[i]), float(combined[i])] for i,r in enumerate(ranks)], ['rank','compact_tail','noncompact_floor','combined'])
plt.figure(figsize=(7,4.2))
plt.loglog(ranks, compact, label='compact tail')
plt.loglog(ranks, noncompact_floor, label='noncompact floor')
plt.loglog(ranks, combined, label='combined residual')
plt.xlabel('rank')
plt.ylabel('eigen/singular value proxy')
plt.title('Compactness test: tail decay vs residual floor')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT,'combined_compact_noncompact_residue_step101.png'), dpi=180)
plt.close()

# ---------- Model D: compact Delta absorption budget ----------
stages = np.arange(1,501)
Lambda = np.sqrt(stages)
compact_tail = 1/(stages**1.4)
budget = 1/Lambda + compact_tail
write_csv(os.path.join(OUT,'compact_source_absorption_model_step101.csv'), [[int(stages[i]), float(Lambda[i]), float(compact_tail[i]), float(budget[i])] for i in range(len(stages))], ['stage','Lambda_n','compact_tail','total_budget'])
plt.figure(figsize=(7,4.2))
plt.loglog(stages, 1/Lambda, label='frame budget Lambda^-1')
plt.loglog(stages, compact_tail, label='compact tail')
plt.loglog(stages, budget, label='total budget')
plt.xlabel('stage')
plt.ylabel('budget proxy')
plt.title('If Delta_S^+ is compact, absorption reduces to frame + tail')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT,'compact_source_absorption_model_step101.png'), dpi=180)
plt.close()

# ---------- Model E: projection tail operator norm ----------
# essential norm proxy for compact vs noncompact residual under finite windows.
windows = np.arange(5,501)
compact_op_tail = 1/(windows**0.8)
noncompact_essential = 0.15*np.ones_like(windows,dtype=float)
write_csv(os.path.join(OUT,'projection_tail_models_step101.csv'), [[int(windows[i]), float(compact_op_tail[i]), float(noncompact_essential[i])] for i in range(len(windows))], ['window_N','compact_operator_tail','noncompact_essential_floor'])
plt.figure(figsize=(7,4.2))
plt.loglog(windows, compact_op_tail, label='compact operator tail')
plt.loglog(windows, noncompact_essential, label='noncompact essential floor')
plt.xlabel('window N')
plt.ylabel('tail norm proxy')
plt.title('Finite-window promotion distinguishes compact from noncompact residual')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT,'projection_tail_operator_norm_step101.png'), dpi=180)
plt.close()

# ---------- Tables ----------
gates = [
    ['G1','CC archimedean slot','Import compact-after-quotient/Sonin-prolate remainder','accepted as imported theorem slot','Compactness survives bounded semilocal transport'],
    ['G2','Semilocal measure deformation','Finite local factors define bounded invertible maps between L2(dm_S) and L2(dm_infty)','accepted for finite S','Measure change itself is compactness-neutral'],
    ['G3','Raw multiplier compactness','Check finite-place Euler-factor multiplier as compact correction on fixed non-atomic L2','fails in general','Nonzero multiplication is not compact'],
    ['G4','Projection residual','R_S = U_S P_S U_S^{-1} - P_infty compact/Hilbert-Schmidt after quotient','open','This is the real semilocal compactness target'],
    ['G5','Delta decomposition','Delta_S = bounded-conjugate compact + finite rank + compact/tail + noncompact residual','open','Needed before source absorption can be simplified'],
    ['G6','Compact absorption shortcut','If Delta_S^+ compact, finite-window absorption plus vanishing tail suffices','conditional','Short-circuits full source lower-frame requirement'],
    ['G7','Noncompact fallback','If essential norm of Delta_S^+ remains positive, cover it by Hecke/Dirichlet lower frame','open fallback','Noncompact sector becomes constructive source target'],
]
write_csv(os.path.join(OUT,'delta_compactness_gate_table_step101.csv'), gates, ['gate','record','test','status','meaning'])

status = [
    ['Delta_infty_CC','archimedean Sonin/prolate correction','compact-after-quotient','imported from Connes-Consani','Use as gamma-slot theorem'],
    ['U_S','semilocal local-factor measure map','bounded invertible/unitary between weighted L2 spaces','follows from finite local factors','compactness-neutral'],
    ['M_{m_S}-I','raw multiplier deformation on fixed L2','not compact unless zero a.e.','functional analysis no-go','cannot itself be the compact residual'],
    ['R_S','semilocal projection residual','unknown','requires semilocal prolate theorem','highest-leverage target'],
    ['Delta_fin_S','finite-place cross-term after exact decomposition','unknown/source-absorbable candidate','not compact-certified','decides Tier-1 route'],
    ['Delta_pole_S','pole/completion/null correction','finite-rank','framework record','cannot pay full infinite core'],
    ['Delta_tail_S','finite-to-completed tail','tail/defect','requires fixed/exhaustive ledger','must vanish for exact confinement'],
]
write_csv(os.path.join(OUT,'delta_compactness_status_table_step101.csv'), status, ['component','description','compactness_status','basis','implication'])

construct = [
    ['C1','Write exact semilocal projection P_S','Define P_S in Y_S^- rather than by public shadow','needed'],
    ['C2','Transport to archimedean geometry','Compute R_S=U_S P_S U_S^{-1}-P_infty','needed'],
    ['C3','Test compact/Hilbert-Schmidt kernel','Show R_S has square-integrable kernel or compact singular decay','open'],
    ['C4','Separate multiplier artifact','Prove multiplier deformation cancels/pairs or is not in Delta_S','open'],
    ['C5','If compact, build finite-window absorption','Use tail projections Pi_N Delta Pi_N + tail','conditional'],
    ['C6','If noncompact, identify mode','Compute essential-norm witness and route to source frame','fallback'],
]
write_csv(os.path.join(OUT,'construction_tasks_step101.csv'), construct, ['id','task','deliverable','status'])

theorems = [
    ['T1','Bounded transport compactness','K compact and A,B bounded imply AKB compact','imports CC compactness into semilocal finite-S setting'],
    ['T2','Multiplier noncompactness','On non-atomic L2, nonzero multiplication is not compact','rules out raw Euler-factor multiplier as compact correction'],
    ['T3','Projection residual criterion','If R_S compact and CC residual compact, Delta_S compact modulo finite-rank/tail','reduces compactness to semilocal prolate projection theorem'],
    ['T4','Compact absorption','If Delta_S^+ compact then finite windows approximate it up to vanishing tail','short-circuits full infinite lower-frame requirement'],
    ['T5','Essential obstruction','If essential norm of Delta_S^+ is positive, compact absorption cannot prove confinement','forces Hecke/source-coercivity route'],
]
write_csv(os.path.join(OUT,'theorem_map_step101.csv'), theorems, ['id','name','statement','use'])

arith = [
    ['A1','CC archimedean compact-after-quotient','already available as imported theorem slot','use'],
    ['A2','Semilocal Hardy-Titchmarsh finite local-factor insertion','available for finite S','use'],
    ['A3','Semilocal prolate projection compactness','not available in uploaded papers','prove or cite future work'],
    ['A4','Finite-window tail/exhaustivity','not automatic','must prove'],
    ['A5','Hecke/Dirichlet source lower frame','fallback if noncompact','major arithmetic input'],
]
write_csv(os.path.join(OUT,'arithmetic_input_table_step101.csv'), arith, ['id','input','status','role'])

schema = {
    'step': 101,
    'title': 'Semilocal Delta_S compactness test',
    'carrier': 'Y_S^- = L2(R, dm_S)^-',
    'active_obstruction': 'Delta_S = q_Weil,S - q_pos,S',
    'verdict': 'CC archimedean residual compactness transports across bounded semilocal maps, but Delta_S compactness is not certified because raw finite-place multiplier deformation is noncompact on a fixed non-atomic response space. The true target is the semilocal projection residual R_S.',
    'next_step': 'derive and audit R_S = U_S P_S U_S^{-1} - P_infty, and test compact/Hilbert-Schmidt status.'
}
with open(os.path.join(OUT,'step101_schema.json'),'w') as f:
    json.dump(schema,f,indent=2)

nonclaim = '''# Step 101 nonclaim boundary\n\nThis step does not prove RH.\n\nIt does not prove that \\(\\Delta_S\\) is compact.\n\nIt proves a compactness audit: imported archimedean compactness is stable under bounded semilocal transport, while raw finite-place multiplier deformation is not compact on a fixed non-atomic response space. Therefore compactness of \\(\\Delta_S\\) requires an exact semilocal projection/prolate decomposition, cancellation/pairing of multiplier artifacts, or a source-frame fallback.\n\nFinite-window checks remain support-only unless an exhaustive tail bridge is supplied.\n'''
with open(os.path.join(OUT,'nonclaim_boundary_step101.md'),'w') as f:
    f.write(nonclaim)

summary = r'''# Step 101: Semilocal \(\Delta_S\) Compactness Test

## Verdict

\[
\boxed{\Delta_S\text{ is not compact-certified yet.}}
\]

The imported Connes--Consani archimedean residual is compact-after-quotient, and finite semilocal local-factor transport is bounded/invertible. Therefore compact archimedean remainders remain compact after semilocal transport.

But the raw finite-place Euler-factor multiplier deformation is not compact on a fixed non-atomic \(L^2\) response space. Thus compactness of \(\Delta_S\) cannot be inferred from finite local factors alone.

## New load-bearing residual

The real compactness target is now

\[
\boxed{\mathcal R_S=U_SP_SU_S^{-1}-P_\infty.}
\]

Here \(P_\infty\) is the archimedean Sonin/prolate compression and \(P_S\) is the accepted semilocal compression/projection, if constructed.

The gate is:

\[
\boxed{\mathcal R_S\text{ compact or Hilbert--Schmidt after the legal quotient.}}
\]

If this passes, \(\Delta_S\) becomes compact-after-quotient modulo finite-rank pole/null records and vanishing tail records.

## Compactness shortcut

If \(\Delta_S^+\) is compact, finite-window source absorption becomes enough:

\[
\Delta_S^+\preceq F_n+E_{\mathrm{tail},n},
\qquad E_{\mathrm{tail},n}\to0.
\]

If \(\|\Delta_S^+\|_{\rm ess}>0\), compact absorption cannot close the bridge and the remaining noncompact sector must be covered by a full Hecke/Dirichlet source frame.

## Bottom line

\[
\boxed{\text{The next pressure point is the semilocal projection residual }\mathcal R_S.}
\]
'''
with open(os.path.join(OUT,'step101_results_summary.md'),'w') as f:
    f.write(summary)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\title{Step 101: Semilocal $\Delta_S$ Compactness Test}
\author{Six Birds / RH Membrane Program}
\date{}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{remark}{Remark}
\begin{document}
\maketitle

\section{Purpose}
The hybrid semilocal route has reduced the active obstruction to
\[
  \Delta_S=q_{\mathrm{Weil},S}-q_{\mathrm{pos},S}
\]
on the semilocal anti-invariant response space
\[
  Y_S^- = L^2(\mathbb R,dm_S)^-, \qquad
  dm_S(\xi)=\left|\prod_{v\in S}L_v\left(\frac12-i\xi\right)\right|^2d\xi .
\]
This note asks whether $\Delta_S^+$ is compact, compact-after-quotient, tail-defect-only, or a genuine infinite-dimensional obstruction.

\section{Elementary compactness gates}
\begin{lemma}[bounded transport preserves compactness]
If $K$ is compact and $A,B$ are bounded operators, then $AKB$ is compact.
\end{lemma}
\begin{proof}
The compact operators form a closed two-sided ideal in $\mathcal B(H)$.
\end{proof}

\begin{lemma}[multiplication no-go]
Let $(X,\mu)$ be non-atomic. If $M_m$ is compact on $L^2(X,\mu)$, then $m=0$ a.e.
\end{lemma}
\begin{proof}
If $|m|>\varepsilon$ on a set of positive measure, split that set into infinitely many disjoint positive-measure pieces $E_j$. The normalized indicators $e_j$ form an orthonormal sequence and $\|M_m e_j\|\ge\varepsilon$, so $M_m e_j$ has no norm-convergent subsequence.
\end{proof}

\section{Semilocal consequence}
For finite $S$, the local Euler-factor product
\[
  A_S(\xi)=\prod_{p\in S_f}L_p(1/2-i\xi)
\]
is bounded and bounded away from zero on the real line. Thus changing from $dm_\infty$ to $dm_S$ is a bounded invertible, indeed unitary after the correct weighting, transport between response geometries. Compactness of an already compact archimedean residual is preserved.

However, the raw multiplier deformation $M_{|A_S|^2-1}$ is not compact on a fixed non-atomic $L^2$ space unless it vanishes. Therefore compactness of $\Delta_S$ is not automatic.

\section{The real compactness target}
The load-bearing semilocal residual is
\[
  \mathcal R_S=U_S P_S U_S^{-1}-P_\infty,
\]
where $P_\infty$ is the archimedean Sonin/prolate compression and $P_S$ is the semilocal compression/projection. The compactness gate is
\[
  \mathcal R_S\in\mathcal K(Y^-_\infty)
\]
or stronger, Hilbert--Schmidt after quotient.

\begin{theorem}[Step 101 dichotomy]
The semilocal cross-term $\Delta_S^+$ is accepted as compact only if its finite-place multiplier sector cancels, is paired into a compact semilocal prolate/Sonin residual, is removed by a lawful quotient, or is absent from the exact decomposition. If a positive essential-norm sector remains, compact finite-window absorption cannot close the RH bridge; the surviving sector must be charged by a full Hecke/Dirichlet source lower frame.
\end{theorem}

\section{Strategic verdict}
The archimedean piece is compact-after-quotient by the imported Connes--Consani mechanism. The semilocal finite-place cross-term is not compact-certified. The next construction target is the exact operator formula for $\mathcal R_S$ and its compact/Hilbert--Schmidt status.

\end{document}
'''
with open(os.path.join(OUT,'semilocal_delta_compactness_step101.tex'),'w') as f:
    f.write(tex)
# structural check
check_rows = []
for env in ['document','theorem','lemma','definition','remark']:
    check_rows.append([env, tex.count('\\begin{'+env+'}'), tex.count('\\end{'+env+'}')])
write_csv(os.path.join(OUT,'latex_structure_check_step101.csv'), check_rows, ['environment','begin_count','end_count'])

# zip
zip_path = os.path.join(OUT,'step101_delta_compactness_artifacts.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for name in sorted(os.listdir(OUT)):
        if name == os.path.basename(zip_path):
            continue
        z.write(os.path.join(OUT,name), arcname=name)
print('done', OUT)
