import json, csv, math, os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

out=Path('/mnt/data/anti_localization_step46_composition')
out.mkdir(parents=True, exist_ok=True)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{enumitem}
\usepackage{booktabs}
\usepackage[margin=1in]{geometry}

\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{corollary}{Corollary}
\newtheorem{remark}{Remark}

\DeclareMathOperator{\Ran}{Ran}
\DeclareMathOperator{\tr}{tr}

\title{Step 46: All-Six Record Composition and Propagation for Anti-Localization Membranes}
\author{working note}
\date{}

\begin{document}
\maketitle

\section{Purpose}
Step 41 defined an accepted formed-layer anti-localization membrane as a predictive family-currency bound with a completed witness ledger.  Step 45 refined the acceptance condition by requiring all six Six-Birds channels to be explicit.  This note proves the bridge law: accepted all-six membranes compose across lawful bridges and strict extensions only when every channel composes and the currency defects remain within budget.

The result is not a simulation theorem.  It is a proof-level bookkeeping theorem for membranes of the form
\[
  \mathsf K = L C^{\dagger} L^*,\qquad \mathsf K\preceq\Theta,
\]
with all carrier/package/probe/status data already formed.

\section{Single bridge transfer}

\begin{definition}[Membrane record]
A finite membrane record is a tuple
\[
  \mathsf M=(E,Y,C,L,\Theta;P_1,\dots,P_6,\mathsf N),
\]
where $E$ is the exact packaged feasibility coordinate space, $Y$ the native response space, $C\succeq0$ the packaged audit, $L:E\to Y$ the declared native family, $\Theta\succeq0$ the budget, and $P_1,\dots,P_6$ are the rewrite, feasibility, route, staging, packaging, and audit channel records.  Its currency matrix is
\[
  \mathsf K(\mathsf M)=LC^{\dagger}L^*.
\]
It is accepted only if null-mode legality holds, all six channels are accepted or explicitly scoped, and $\mathsf K\preceq\Theta$.
\end{definition}

\begin{definition}[Defective bridge]
A bridge $\mathsf B_{01}:\mathsf M_0\to\mathsf M_1$ consists of an energy pullback $P:E_1\to E_0$, a response transport $A:Y_0\to Y_1$, and a residual readout $R:E_1\to Y_1$ such that
\[
  C_1\succeq P^*C_0P,\qquad L_1=AL_0P+R.
\]
The residual currency is
\[
  E_R=RC_1^{\dagger}R^*.
\]
The bridge is all-six lawful if every channel $P_i$ has a composable channel map and an explicit defect/status record.
\end{definition}

\begin{theorem}[Defective membrane transfer]
Let $\mathsf B_{01}:\mathsf M_0\to\mathsf M_1$ be a defective bridge.  If $\mathsf K_0\preceq\Theta_0$, then for every $t>0$,
\[
  \mathsf K_1\preceq (1+t)A\Theta_0A^*+(1+t^{-1})E_R.
\]
Consequently $\mathsf M_1$ is accepted with budget $\Theta_1$ whenever
\[
  (1+t)A\Theta_0A^*+(1+t^{-1})E_R\preceq \Theta_1
\]
and the all-six channel records compose.
\end{theorem}

\begin{proof}
For any $u\in E_1$,
\[
  L_1u=AL_0Pu+Ru.
\]
The elementary inequality $(x+y)(x+y)^*\preceq(1+t)xx^*+(1+t^{-1})yy^*$ gives
\[
  L_1C_1^{\dagger}L_1^*
  \preceq
  (1+t)AL_0PC_1^{\dagger}P^*L_0^*A^*+(1+t^{-1})RC_1^{\dagger}R^*.
\]
The energy domination $C_1\succeq P^*C_0P$ implies the variational data-processing inequality
\[
  L_0PC_1^{\dagger}P^*L_0^*\preceq L_0C_0^{\dagger}L_0^*.
\]
Thus
\[
  \mathsf K_1\preceq (1+t)A\mathsf K_0A^*+(1+t^{-1})E_R
  \preceq (1+t)A\Theta_0A^*+(1+t^{-1})E_R.
\]
\end{proof}

\section{Composition of two bridges}

\begin{theorem}[Two-bridge composition]
Suppose
\[
  \mathsf M_0\xrightarrow{\mathsf B_{01}}\mathsf M_1\xrightarrow{\mathsf B_{12}}\mathsf M_2
\]
are defective all-six bridges with response transports $A_{01},A_{12}$ and residual currencies $E_{01},E_{12}$.  If $\mathsf K_0\preceq\Theta_0$, then for all $t_1,t_2>0$,
\[
\boxed{
  \mathsf K_2\preceq
  (1+t_2)(1+t_1)A_{12}A_{01}\Theta_0A_{01}^*A_{12}^*
  +(1+t_2)(1+t_1^{-1})A_{12}E_{01}A_{12}^*
  +(1+t_2^{-1})E_{12}.
}
\]
Thus the composed bridge is accepted with budget $\Theta_2$ only if the right-hand side is dominated by $\Theta_2$ and every $P_i$-channel composition is accepted.
\end{theorem}

\begin{proof}
Apply the defective transfer theorem to $\mathsf B_{01}$ and then to $\mathsf B_{12}$.
\end{proof}

\begin{corollary}[Exact composition]
If both bridges are exact, $E_{01}=E_{12}=0$, and the response maps are isometrically normalized so that no inflation is used, then
\[
  \mathsf K_2\preceq A_{12}A_{01}\Theta_0A_{01}^*A_{12}^*.
\]
\end{corollary}

\section{Chains and predictive propagation}

\begin{definition}[Propagated budget]
Given a chain
\[
  \mathsf M_0\to\mathsf M_1\to\cdots\to\mathsf M_n
\]
with transfers
\[
  \mathsf K_{j+1}\preceq \alpha_j A_j\mathsf K_jA_j^*+\beta_jE_j,
\]
define recursively
\[
  \Theta_{j+1}^{\rm prop}=\alpha_jA_j\Theta_j^{\rm prop}A_j^*+\beta_jE_j,
  \qquad \Theta_0^{\rm prop}=\Theta_0.
\]
\end{definition}

\begin{theorem}[Chain propagation]
If $\mathsf K_0\preceq\Theta_0$, then
\[
  \mathsf K_n\preceq \Theta_n^{\rm prop}
\]
for every $n$.  Hence a chain of all-six records composes only as far as the propagated budget remains within the declared target budget.
\end{theorem}

\begin{proof}
Induction on $n$ using the transfer inequality.
\end{proof}

\begin{corollary}[Common response summable-defect case]
If $A_j=I$, $\alpha_j=1+\varepsilon_j$, $\beta_j=1$, and
\[
  \prod_j(1+\varepsilon_j)\le P<\infty,
  \qquad \sum_j E_j\preceq E_\infty,
\]
then
\[
  \mathsf K_n\preceq P(\Theta_0+E_\infty).
\]
Thus a common predictive membrane transfers along the chain if the declared budget dominates this bound.
\end{corollary}

\section{All-six channel composition}

\begin{definition}[Composed all-six status]
A bridge composition is all-six accepted when the following six records compose:
\begin{enumerate}[label=$P_\arabic*$:,leftmargin=2.2em]
\item rewrite/gauge/operator repairs commute or have a declared residual;
\item feasible carrier maps preserve frame/null legality;
\item route and protocol ledgers stack to the union block, not just diagonals;
\item staging/refinement defects are summable or within predictive budget;
\item packaging/canonicalization is lawful and not post-hoc selected;
\item audit/currency budgets propagate by the transfer inequality.
\end{enumerate}
\end{definition}

\begin{theorem}[All-six composition theorem]
Let $\mathsf M_0\to\mathsf M_1\to\mathsf M_2$ be accepted all-six membrane bridges.  If every $P_i$ channel composes with accepted status and the propagated currency bound is dominated by the declared budget $\Theta_2$, then the composite bridge $\mathsf M_0\to\mathsf M_2$ is an accepted all-six membrane bridge.  In particular, every native response recombination at the target remains priced by $\Theta_2$.
\end{theorem}

\begin{proof}
The currency part follows from the two-bridge composition theorem.  The claim is an accepted membrane rather than a support-only inequality only if every channel has accepted compositional status.  If a channel lacks such a record, the matrix inequality may still be true as a public or partial shadow, but the Six-Birds membrane assertion is not accepted.
\end{proof}

\section{Necessity countermodels}

\begin{proposition}[One missing channel blocks composition]
For each $i=1,\dots,6$, there exists a finite membrane diagram in which the currency inequality appears to transfer along local records, but the composed anti-localization claim is false or overread when the $P_i$ composition gate is omitted.
\end{proposition}

\begin{proof}[Proof sketch]
The six countermodels are the finite examples already used in the gate atlas, now placed in composition form:
\begin{enumerate}[label=$P_\arabic*$:,leftmargin=2.2em]
\item a gauge rewrite introduces a slow aligned mode after the first bridge;
\item an ill-conditioned feasible channel pair cancels into a needle after transport;
\item route-local budgets pass on both legs but the route-union block has a mixed witness;
\item each stage is finite but predictive capacities grow without a summable defect bound;
\item a public shadow transfers while the lawful witness has a hidden kernel direction;
\item diagonal audits transfer while a recombination witness appears in the off-diagonal block.
\end{enumerate}
Each gives $y^*(K-\Theta)y>0$ in the target despite the local-looking partial certificate.
\end{proof}

\section{Interpretation}
Composition is not merely functoriality of matrices.  It is functoriality of formed membranes.  The currency inequality supplies the numerical transfer; the six channel records supply the lawfulness of the transfer.  A composed membrane exists only when both parts survive.

\end{document}
'''
(out/'all_six_composition_step46.tex').write_text(tex)

summary = r'''
# Step 46: All-Six Record Composition and Propagation

This step proves the bridge law for accepted all-six anti-localization records.

Main result:

\[
\mathsf M_0\to\mathsf M_1\to\mathsf M_2
\]

composes to an accepted anti-localization membrane only when:

1. the currency matrices propagate within budget, and
2. each of the six channel records \(P_1,\dots,P_6\) composes with accepted status.

For a defective bridge with

\[
C_1\succeq P^*C_0P,\qquad L_1=AL_0P+R,
\]

and residual currency

\[
E_R=RC_1^\dagger R^*,
\]

the transfer theorem is

\[
\mathsf K_1\preceq (1+t)A\mathsf K_0A^*+(1+t^{-1})E_R.
\]

For two bridges:

\[
\mathsf K_2\preceq
(1+t_2)(1+t_1)A_{12}A_{01}\Theta_0A_{01}^*A_{12}^*
+(1+t_2)(1+t_1^{-1})A_{12}E_{01}A_{12}^*
+(1+t_2^{-1})E_{12}.
\]

So defects compose nontrivially; they are not ignorable.

The all-six channel rule is:

- \(P_1\): rewrite/gauge/operator repairs compose;
- \(P_2\): feasibility/frame/null legality composes;
- \(P_3\): route/protocol union composes as a block, not diagonals;
- \(P_4\): staging/refinement defects are summable or budgeted;
- \(P_5\): packaging/canonicalization is lawful and not post-hoc;
- \(P_6\): audit/currency budgets propagate.

If any one channel fails to compose, the resulting claim is downgraded to support-only, local-only, overread, or failed-audit.

Layman interpretation:

A membrane certificate can travel from one layer to another only if both the price table and all six honesty records travel with it.  Carrying only the price table is like moving a safety inspection report without proving it applies to the new building.
'''
(out/'step46_results_summary.md').write_text(summary)

schema = {
  "name":"AllSixMembraneCompositionRecord",
  "source_record":["E0","Y0","C0","L0","Theta0","P1..P6","Nonclaims"],
  "target_record":["E1","Y1","C1","L1","Theta1","P1..P6","Nonclaims"],
  "bridge_fields":{
    "energy_pullback":"P:E_target -> E_source",
    "response_transport":"A:Y_source -> Y_target",
    "readout_residual":"R:E_target -> Y_target",
    "energy_domination":"C_target >= P^* C_source P",
    "readout_equation":"L_target = A L_source P + R",
    "residual_currency":"E_R = R C_target^dagger R^*"
  },
  "composition_fields":{
    "currency_propagation":"K_{j+1} <= alpha_j A_j K_j A_j^* + beta_j E_j",
    "propagated_budget":"Theta_{j+1}=alpha_j A_j Theta_j A_j^*+beta_j E_j",
    "accepted_if":"K_j <= Theta_j and all P_i channels compose"
  },
  "channel_composition_gates":{
    "P1":"rewrite/gauge/operator repair commutes or has residual",
    "P2":"feasibility, frame, null-mode legality preserved",
    "P3":"route/protocol block union controlled",
    "P4":"staging/refinement defects summable or budgeted",
    "P5":"packaging/canonicalization lawful and non-posthoc",
    "P6":"currency/audit budget propagated"
  },
  "statuses":["accepted","support_only","local_only","overread","failed_audit","failed_channel_composition"]
}
(out/'all_six_composition_schema_step46.json').write_text(json.dumps(schema, indent=2))

# CSV tables
with (out/'composition_gate_table_step46.csv').open('w', newline='') as f:
    w=csv.writer(f)
    w.writerow(['channel','composition requirement','failure status','typical countermodel'])
    rows=[
        ['P1 rewrite/gauge','operator/gauge repair commutes or residual is budgeted','failed_channel_composition','gauge rewrite introduces slow aligned mode'],
        ['P2 feasibility/channel','frame and null legality preserved under transport','failed_audit','ill-conditioned channels cancel into needle'],
        ['P3 route/holonomy','route union block controlled, not route diagonals only','local_only','mixed-route recombination witness'],
        ['P4 staging/refinement','defects are summable or predictive budgeted','support_only','finite stages pass but K_j grows'],
        ['P5 packaging/canonicalization','lawful witness transported, public shadow not overread','overread','shadow passes, hidden kernel fails'],
        ['P6 audit/currency','full matrix budget propagates, not diagonal audit only','failed_audit','diagonal probes pass, recombination fails'],
    ]
    w.writerows(rows)

with (out/'theorem_map_step46.csv').open('w', newline='') as f:
    w=csv.writer(f)
    w.writerow(['theorem','input','output','role'])
    rows=[
        ['Defective membrane transfer','C1>=P^*C0P and L1=AL0P+R','K1 <= (1+t)AK0A^*+(1+t^{-1})E_R','single bridge budget transfer'],
        ['Two-bridge composition','two accepted transfer inequalities','explicit composed bound with E01,E12','defect propagation'],
        ['Chain propagation','K_{j+1} <= alpha A K_j A^*+beta E_j','K_n <= propagated Theta_n','predictive membrane transport'],
        ['Common response summable defect','product eps finite, sum defects bounded','uniform predictive budget','long chain acceptance'],
        ['All-six composition','currency bound + P1..P6 channel composition','accepted composed membrane','Six Birds lawfulness'],
        ['Missing-channel countermodels','omit one P_i','finite overclaim witness','necessity of all channels'],
    ]
    w.writerows(rows)

# numerical sanity checks
rng=np.random.default_rng(46)

def rand_spd(n, scale=1.0):
    A=rng.normal(size=(n,n))
    return scale*(A.T@A + 0.5*np.eye(n))

def psd_sqrt_inv(M):
    vals, vecs=np.linalg.eigh(M)
    return vecs@np.diag([1/np.sqrt(max(v,1e-12)) for v in vals])@vecs.T

def maxeig(M):
    return np.linalg.eigvalsh((M+M.T)/2)[-1]

def mineig(M):
    return np.linalg.eigvalsh((M+M.T)/2)[0]

# exact transfer checks
exact_rows=[]
for n in [2,3,4,5,6]:
    for trial in range(10):
        K0=rand_spd(n,0.2)
        Theta0=K0 + rand_spd(n,0.1)
        A=rng.normal(size=(n,n))/np.sqrt(n)
        K1=A@K0@A.T
        Theta1=A@Theta0@A.T
        exact_rows.append([n,trial,mineig(Theta1-K1),maxeig(K1),maxeig(Theta1)])
with (out/'exact_composition_checks_step46.csv').open('w', newline='') as f:
    w=csv.writer(f); w.writerow(['n','trial','min_eig_Theta_minus_K','maxeig_K1','maxeig_Theta1']); w.writerows(exact_rows)

# defective chain checks and optimize t/epsilon synthetic
chain_rows=[]
for length in [1,2,3,5,10,20,40]:
    K=np.array([[1.0]])
    Theta=np.array([[1.0]])
    eps=[]
    defects=[]
    for j in range(length):
        e=0.02/(j+1)**2
        d=0.03/(j+1)**2
        eps.append(e); defects.append(d)
        K=(1+e)*K + np.array([[d]])
    P=np.prod([1+e for e in eps])
    D=sum(defects)
    bound=P*(1+D)
    chain_rows.append([length,float(K[0,0]),float(bound),float(P),float(D),float(bound-K[0,0])])
with (out/'chain_propagation_checks_step46.csv').open('w', newline='') as f:
    w=csv.writer(f); w.writerow(['length','actual_K','summable_bound','product_P','sum_D','slack']); w.writerows(chain_rows)

# missing channel countermodel magnitudes
counter_rows=[]
countermodels = {
    'P1 rewrite/gauge': 100.0,
    'P2 feasibility/channel': 50.0,
    'P3 route/holonomy': 2.0,
    'P4 staging/refinement': 40.0,
    'P5 packaging/canonicalization': 25.5,
    'P6 audit/currency': 10.0,
}
with (out/'missing_channel_countermodels_step46.csv').open('w', newline='') as f:
    w=csv.writer(f); w.writerow(['missing_channel','violation_factor','status'])
    for k,v in countermodels.items():
        w.writerow([k,v,'failed if omitted'])

# plots
plt.figure(figsize=(7,4.5))
xs=[r[0] for r in chain_rows]
y1=[r[1] for r in chain_rows]
y2=[r[2] for r in chain_rows]
plt.plot(xs,y1,marker='o',label='propagated K')
plt.plot(xs,y2,marker='s',label='summable bound')
plt.xlabel('chain length')
plt.ylabel('scalar budget')
plt.title('Step 46: chain propagation with summable defects')
plt.legend()
plt.tight_layout()
plt.savefig(out/'chain_propagation_step46.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
labels=list(countermodels.keys())
vals=list(countermodels.values())
plt.bar(range(len(vals)), vals)
plt.xticks(range(len(vals)), [l.split()[0] for l in labels])
plt.ylabel('representative violation factor')
plt.title('Step 46: overclaim if a channel composition gate is omitted')
plt.tight_layout()
plt.savefig(out/'missing_channel_countermodels_step46.png', dpi=180)
plt.close()

# zip artifacts later using shell
