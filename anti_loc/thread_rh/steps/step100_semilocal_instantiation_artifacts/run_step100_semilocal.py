import os, json, csv, math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step100_semilocal_instantiation')
OUT.mkdir(parents=True, exist_ok=True)

# ---------- Helper models ----------
# Semilocal measure density proxy: actual finite local factors times a rapidly decaying archimedean proxy.
# We avoid claiming this is the exact normalized CCM measure in numerical checks; it is a carrier-shaped tail model.
def local_factor_abs2(t, p):
    # |(1 - p^{-1/2 + i t})^{-1}|^2
    z_abs = p ** (-0.5)
    theta = t * math.log(p)
    return 1.0 / (1 - 2*z_abs*np.cos(theta) + z_abs*z_abs)

def dm_density(t, primes=(2,3,5)):
    # A smooth finite mass proxy with local factor modulation.
    dens = np.exp(-(t/12.0)**2)  # proxy for archimedean decay; actual |Gamma|^2 decays exponentially.
    for p in primes:
        dens *= local_factor_abs2(t, p)
    return dens

def ledger_density(t):
    # synthetic trace-class zero-ledger density in response variable
    return (t**2/(1+t**2)) * np.exp(-(t/9.0)**2)  # anti-invariant-ish: vanishes at t=0

# Grid and measure
Tmax = 80.0
Ngrid = 20001
t = np.linspace(-Tmax, Tmax, Ngrid)
dt = t[1]-t[0]
mu = dm_density(t)
Aden = ledger_density(t)
weighted = mu * Aden
full_trace = np.trapz(weighted, t)

Ts = np.linspace(2, 60, 30)
tail_rows = []
for T in Ts:
    mask = np.abs(t) > T
    tail = np.trapz(weighted[mask], t[mask]) if np.any(mask) else 0.0
    tail_rows.append({
        'T': float(T),
        'trace_tail_proxy': float(tail),
        'relative_tail_proxy': float(tail/full_trace if full_trace else np.nan)
    })

with open(OUT/'semilocal_tail_model_step100.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=tail_rows[0].keys()); w.writeheader(); w.writerows(tail_rows)

plt.figure(figsize=(6,4))
plt.plot([r['T'] for r in tail_rows],[r['relative_tail_proxy'] for r in tail_rows], marker='o')
plt.yscale('log')
plt.xlabel('spectral window T')
plt.ylabel('relative tail trace proxy')
plt.title('Semilocal spectral tail model')
plt.tight_layout()
plt.savefig(OUT/'semilocal_tail_model_step100.png', dpi=180)
plt.close()

# Completed lower-frame promotion model: F_T = Lambda P_T w P_T, tail R_T = (I-P_T) w (I-P_T)
# Report certified full-frame bound with and without tail.
frame_rows=[]
for T in [5,10,15,20,30,40,60]:
    Lambda = T/5.0
    # discrete diagonal model on 100 modes, first floor(T) charged
    M=120
    modes=np.arange(1,M+1)
    inv_budget = 1.0/(1+modes/40.0)  # positive diagonal theta^{-1}
    charged = modes <= int(T)
    F = Lambda * inv_budget * charged
    tail = Lambda * inv_budget * (~charged)
    # without tail, minimum ratio F/(Lambda inv_budget) is zero; with tail it is one.
    ratio_without = np.min(F/(Lambda*inv_budget))
    ratio_with = np.min((F+tail)/(Lambda*inv_budget))
    uncharged_dim = int(np.sum(~charged))
    frame_rows.append({'T':T,'Lambda':Lambda,'min_ratio_without_tail':float(ratio_without),'min_ratio_with_tail':float(ratio_with),'uncharged_modes':uncharged_dim})
with open(OUT/'completed_lower_frame_promotion_step100.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=frame_rows[0].keys()); w.writeheader(); w.writerows(frame_rows)

plt.figure(figsize=(6,4))
plt.plot([r['T'] for r in frame_rows],[r['min_ratio_without_tail'] for r in frame_rows], marker='o', label='without tail')
plt.plot([r['T'] for r in frame_rows],[r['min_ratio_with_tail'] for r in frame_rows], marker='s', label='with tail')
plt.xlabel('window T')
plt.ylabel('min lower-frame ratio')
plt.title('Completed lower-frame promotion needs tail')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'completed_lower_frame_promotion_step100.png', dpi=180)
plt.close()

# Semilocal measure deformation plot for different S
plt.figure(figsize=(6,4))
ts = np.linspace(-20,20,4000)
for primes in [(), (2,), (2,3), (2,3,5)]:
    label = 'S={∞}' if len(primes)==0 else 'S={∞,'+','.join(map(str,primes))+'}'
    dens = dm_density(ts, primes=primes)
    dens = dens/np.max(dens)
    plt.plot(ts, dens, label=label)
plt.xlabel('s')
plt.ylabel('normalized density proxy')
plt.title('Finite local factors deform semilocal response measure')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'semilocal_measure_deformation_step100.png', dpi=180)
plt.close()

# Moving-window failure model: each finite window exact; tail can remain if adversarial ledger lives outside.
move_rows=[]
for T in range(5,65,5):
    hidden_position = T + 10
    finite_window_claim = 0.0
    hidden_tail_mass = 1.0
    move_rows.append({'T':T,'finite_window_obstruction':finite_window_claim,'hidden_tail_mass_without_exhaustivity':hidden_tail_mass,'hidden_position':hidden_position})
with open(OUT/'moving_window_failure_step100.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=move_rows[0].keys()); w.writeheader(); w.writerows(move_rows)

plt.figure(figsize=(6,4))
plt.plot([r['T'] for r in move_rows],[r['finite_window_obstruction'] for r in move_rows], marker='o', label='visible window')
plt.plot([r['T'] for r in move_rows],[r['hidden_tail_mass_without_exhaustivity'] for r in move_rows], marker='s', label='hidden tail')
plt.xlabel('window T')
plt.ylabel('mass / obstruction')
plt.title('Moving-window support-only failure')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'moving_window_failure_step100.png', dpi=180)
plt.close()

# Tables
window_maps = [
    {'object':'carrier','symbol':'Y^-_S','definition':'anti-invariant subspace of L^2(R,dm_S) under s -> -s','status':'chosen for Step 100'},
    {'object':'semilocal measure','symbol':'dm_S(s)','definition':'|prod_{v in S} L_v(1/2-is)|^2 ds','status':'from CCM Hardy--Titchmarsh canonical form'},
    {'object':'spectral window','symbol':'Pi_T','definition':'multiplication by 1_{|s|<=T} on Y^-_S','status':'lawful fixed-S window'},
    {'object':'finite-mode window','symbol':'Pi_{T,N}','definition':'optional projection onto first N orthogonal-polynomial/prolate modes inside |s|<=T','status':'support-only unless N-tail controlled'},
    {'object':'tail form','symbol':'T_T','definition':'(I-Pi_T)^* Theta^{-1} (I-Pi_T), or trace tail against A_Z','status':'must vanish for exact confinement'},
    {'object':'source frame','symbol':'F_{T,n}','definition':'sum lambda_omega Q_omega^* Theta_omega^{-1} Q_omega transported to Y^-_S','status':'not supplied by fixed K_S-invariant semilocal space alone'},
]
with open(OUT/'semilocal_window_maps_step100.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=window_maps[0].keys()); w.writeheader(); w.writerows(window_maps)

gate_rows = [
    {'gate':'G1 carrier choice','requirement':'Use Y^-_S = L^2(R,dm_S)^- with CCM unitary V_S','status':'accepted as concrete semilocal carrier'},
    {'gate':'G2 window maps','requirement':'Define Pi_T and optional Pi_{T,N} on the same fixed-S response space','status':'accepted'},
    {'gate':'G3 Plancherel tail','requirement':'Prove Theta^{-1} <= Pi_T^*B_TPi_T + T_T and tr(T_T A_Z)->0','status':'formal theorem; analytic tail input unearned'},
    {'gate':'G4 lower frame','requirement':'F_n >= Lambda_n(Theta_0^-)^{-1} on completed Y^-_S','status':'not supplied by finite character orthogonality alone'},
    {'gate':'G5 cross-term absorption','requirement':'Delta_S^+ <= F_n + E_abs,n','status':'active hard target'},
    {'gate':'G6 fixed/exhaustive zero ledger','requirement':'A_Z fixed or windowed with vanishing tail','status':'still required'},
    {'gate':'G7 all-six records','requirement':'rewrite, feasibility, route, staging, packaging, audit records','status':'must be populated for final RH claim'},
]
with open(OUT/'step100_gate_table.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=gate_rows[0].keys()); w.writeheader(); w.writerows(gate_rows)

theorem_rows = [
    {'theorem':'Concrete semilocal carrier','statement':'Y^-_S=L^2(R,dm_S)^- with dm_S=|prod_{v in S}L_v(1/2-is)|^2 ds; Fourier involution becomes s->-s','role':'puts Step 99 on CCM carrier'},
    {'theorem':'Spectral window exhaustivity','statement':'Pi_T -> I strongly and tr((I-Pi_T)A_Z(I-Pi_T))->0 for trace-class A_Z','role':'fixed-S tail bridge'},
    {'theorem':'Lower-frame promotion with tail','statement':'If F_T^win >= Lambda_T B_T and Theta^{-1} <= Pi_T^*B_TPi_T+T_T then F_T+Lambda_T T_T >= Lambda_T Theta^{-1}','role':'finite window to completed lower frame'},
    {'theorem':'Support-only warning','statement':'Finite windows without T_T do not imply completed lower frame','role':'prevents overreading finite spectral triples/finite characters'},
    {'theorem':'Character-source limitation on K-invariant semilocal carrier','statement':'K_S-invariant Y_S sees local factors in the measure; it does not itself provide all character modes','role':'points toward enlarged Hecke source carrier for full source ladder'},
]
with open(OUT/'theorem_map_step100.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=theorem_rows[0].keys()); w.writeheader(); w.writerows(theorem_rows)

status_rows = [
    {'route':'fixed semilocal CCM response space','verdict':'use now','reason':'gives concrete Y^-_S, measure, involution, window maps, and tail theorem'},
    {'route':'finite character orthogonality inside fixed finite quotient','verdict':'support-only','reason':'exact on finite quotient but not completed Y^- without tail'},
    {'route':'Hecke/idèle enlarged carrier','verdict':'backup / likely needed for full source frame','reason':'character Plancherel lives naturally there'},
    {'route':'spectral triples finite windows','verdict':'evidence, not proof','reason':'need determinant/ledger convergence'},
    {'route':'chiral adelic Dirac finite-prime truncations','verdict':'Tier-2 support','reason':'controlled finite-prime approximants but descent/tail remain'},
]
with open(OUT/'route_status_step100.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=status_rows[0].keys()); w.writeheader(); w.writerows(status_rows)

# Nonclaim boundary
(OUT/'nonclaim_boundary_step100.md').write_text('''# Step 100 nonclaim boundary\n\nThis step does not prove RH. It does not prove the source lower-frame inequality, and it does not prove absorption of Delta_S^+. It instantiates the Plancherel/tail theorem on the semilocal Connes--Consani--Moscovici response carrier and shows what the window maps and tail forms must be.\n\nFinite spectral windows, finite conductor windows, and finite character orthogonality remain support-only unless they carry a tail/exhaustivity bridge.\n\nThe fixed K_S-invariant semilocal carrier records finite local Euler factors in the measure dm_S. It does not by itself supply all Hecke character source modes; full character-source coercivity likely requires an enlarged Hecke/idèle carrier or a descent theorem.\n''')

# Schema JSON
schema = {
  'step': 100,
  'title': 'Semilocal Plancherel/tail instantiation on the CCM response carrier',
  'carrier': 'Y_S^- = L^2(R,dm_S)^-',
  'measure': 'dm_S(s)=|prod_{v in S} L_v(1/2-is)|^2 ds',
  'window_maps': ['Pi_T=M_{1_{|s|<=T}}', 'optional Pi_{T,N}=finite prolate/orthogonal-polynomial projection'],
  'tail_forms': ['T_T=(I-Pi_T)^*Theta^{-1}(I-Pi_T)', 'trace tail tr((I-Pi_T)A_Z(I-Pi_T))'],
  'main_status': 'spectral exhaustivity instantiated; source lower-frame remains open',
  'next_step': 'attempt semilocal Delta_S compactness/prolate tail theorem or formulate enlarged Hecke Plancherel lower frame'
}
(OUT/'step100_schema.json').write_text(json.dumps(schema, indent=2))

# LaTeX note
tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{remark}{Remark}
\newcommand{\R}{\mathbb R}
\newcommand{\C}{\mathbb C}
\newcommand{\one}{\mathbf 1}
\newcommand{\pre}{\preceq}
\title{Step 100: Semilocal Plancherel/Exhaustivity Instantiation}
\author{Six Birds / RH Membrane Program}
\date{}
\begin{document}
\maketitle

\section{Purpose}
Step 99 gave an abstract promotion theorem: finite character or finite-window source frames become completed lower frames only through a Plancherel/exhaustivity record plus a tail form.  Step 100 instantiates that theorem on one concrete carrier, namely the semilocal Connes--Consani--Moscovici response space.

This is not a proof of RH.  It fixes the response room, the window maps, and the exact tail objects that must be controlled before finite-window evidence can be promoted.

\section{Carrier choice}
Let $S$ be a finite set of rational places with $\infty\in S$.  Let
\[
  X_S=A_S/\Gamma,
  \qquad
  \Gamma=\{\pm p_1^{n_1}\cdots p_k^{n_k}:p_j\in S\setminus\{\infty\},\ n_j\in\mathbb Z\}.
\]
The semilocal Hardy--Titchmarsh construction gives a canonical response space
\[
  Y_S=L^2(\R,dm_S),
  \qquad
  dm_S(s)=\left|\prod_{v\in S}L_v\!\left(\frac12-is\right)\right|^2ds.
\]
The Fourier involution on the semilocal side becomes the symmetry $s\mapsto -s$ in this model.  We therefore set
\[
  Y_S^-:=\{y\in L^2(\R,dm_S):\mathcal J y=-y\},
  \qquad (\mathcal J y)(s)=y(-s),
\]
with the usual conjugate-linear variant when the carrier is complex and real structures are retained.

\section{Window maps}
For $T>0$, define the spectral window
\[
  \Pi_T:Y_S^-\to Y_{S,T}^-:=L^2([-T,T],dm_S)^-,
  \qquad
  \Pi_Ty=\one_{|s|\le T}y.
\]
The adjoint is extension by zero, and
\[
  \Pi_T^*\Pi_T=M_{\one_{|s|\le T}}.
\]
Optionally one may refine this by a finite-mode/prolate/orthogonal-polynomial projection $P_N^{(S)}$ and use
\[
  \Pi_{T,N}=P_N^{(S)}\Pi_T.
\]
This second truncation is support-only unless its $N$-tail is also audited.

\section{Tail/exhaustivity theorem on the fixed semilocal carrier}
\begin{theorem}[Trace-tail exhaustivity]
Let $A_Z\ge0$ be a trace-class completed zero ledger on $Y_S^-$. Then
\[
 \operatorname{tr}\big((I-\Pi_T^*\Pi_T)A_Z(I-\Pi_T^*\Pi_T)\big)\to0
 \qquad (T\to\infty).
\]
Consequently, finite spectral windows exhaust the zero ledger if the same completed ledger $A_Z$ is being squeezed.
\end{theorem}
\begin{proof}
The projections $P_T=\Pi_T^*\Pi_T$ increase strongly to $I$ on $Y_S^-$.  If $A_Z$ is positive trace-class, approximate it in trace norm by a finite-rank positive operator.  Strong convergence is uniform on finite-dimensional ranges, and the trace-norm approximation supplies the remaining $\varepsilon$.
\end{proof}

\section{Lower-frame promotion with explicit tail}
Let $\Theta_0^-$ be the native anti-invariant budget on $Y_S^-$.  Let $B_T$ be a positive window budget on $Y_{S,T}^-$.  A Plancherel/exhaustivity record is an inequality
\[
  (\Theta_0^-)^{-1}\preceq \Pi_T^*B_T\Pi_T+T_T,
  \qquad T_T\ge0.
\]
If a finite-window source frame satisfies
\[
  F_T^{\rm win}\succeq \Lambda_T B_T,
\]
then its lift
\[
  F_T=\Pi_T^*F_T^{\rm win}\Pi_T
\]
obeys
\[
  F_T+\Lambda_TT_T\succeq \Lambda_T(\Theta_0^-)^{-1}.
\]
Thus finite-window source coercivity promotes exactly to the extent that $T_T$ is small on the completed zero ledger.

\section{Concrete tail form}
In the simplest multiplication-budget case, if $(\Theta_0^-)^{-1}=M_w$ for a positive measurable weight $w$, then
\[
  T_T=M_{w\one_{|s|>T}}.
\]
The zero-ledger tail is
\[
  \operatorname{tr}(T_T^{1/2}A_ZT_T^{1/2}).
\]
The exact-confinement route requires this quantity to vanish along the same fixed or exhaustive ledger used in the zero-side squeeze.

\section{Important limitation}
The fixed $K_S$-invariant semilocal response space records the finite places through the measure $dm_S$.  It does not by itself provide all character-source modes.  Therefore, Step 100 instantiates the spectral Plancherel/tail gate, but it does not discharge the Hecke/Dirichlet lower-frame source gate
\[
  F_n\succeq \Lambda_n(\Theta_0^-)^{-1},\qquad \Lambda_n\to\infty.
\]
For that, one needs either a source readout family $Q_\omega$ descending lawfully to $Y_S^-$, or an enlarged Hecke/id\`ele carrier with a Plancherel theorem and a descent bridge back to the zeta zero ledger.

\section{Status}
Step 100 accepts the semilocal CCM response space as the first concrete carrier for window/tail bookkeeping:
\[
  Y_S^-=L^2(\R,dm_S)^-,\quad \Pi_T=M_{\one_{|s|\le T}},\quad T_T=(I-\Pi_T)^*(\Theta_0^-)^{-1}(I-\Pi_T).
\]
The remaining open tasks are source lower-frame construction and absorption of $\Delta_S^+$.
\end{document}
'''
(OUT/'semilocal_plancherel_instantiation_step100.tex').write_text(tex)

# Summary MD
summary = f'''# Step 100 summary\n\nThis step instantiates the Step 99 Plancherel/exhaustivity theorem on the semilocal Connes--Consani--Moscovici response carrier.\n\n## Chosen carrier\n\nFor a finite set of places `S` with infinity included, use\n\n```tex\nY_S^- = L^2(R, dm_S)^-,\n\\qquad dm_S(s)=|\\prod_{{v\\in S}} L_v(1/2-is)|^2 ds.\n```\n\nThe anti-invariant involution is the symmetry `s -> -s` on the Hardy--Titchmarsh side.\n\n## Window maps\n\n```tex\n\\Pi_T y = 1_{{|s|<=T}}y.\n```\n\nOptional finite-mode/prolate windows `Pi_{T,N}` are allowed but remain support-only unless their mode tail is controlled.\n\n## Main theorem\n\nFor a positive trace-class completed zero ledger `A_Z`,\n\n```tex\ntr((I-Pi_T^*Pi_T) A_Z (I-Pi_T^*Pi_T)) -> 0.\n```\n\nSo spectral windows are exhaustive only when they squeeze the same completed ledger, not merely moving finite slices.\n\n## Lower-frame promotion\n\nIf\n\n```tex\nF_T^win >= Lambda_T B_T,\n(Theta_0^-)^{-1} <= Pi_T^* B_T Pi_T + T_T,\n```\n\nthen\n\n```tex\nF_T + Lambda_T T_T >= Lambda_T (Theta_0^-)^{-1}.\n```\n\nThis is the exact finite-window-to-completed lower-frame promotion rule.\n\n## Verdict\n\nThe semilocal CCM carrier gives a concrete response space, window maps, and tail form. It does not by itself supply the Hecke/Dirichlet character lower frame. Full source coercivity still needs either source readouts descending to this carrier or an enlarged Hecke/idèle carrier.\n'''
(OUT/'step100_results_summary.md').write_text(summary)

# structural latex check
text = tex
checks = []
for env in ['document','theorem','proof','section']:
    checks.append({'env':env,'begin_count':text.count('\\begin{'+env+'}'),'end_count':text.count('\\end{'+env+'}')})
with open(OUT/'latex_structure_check_step100.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=['env','begin_count','end_count']); w.writeheader(); w.writerows(checks)

# Zip
import zipfile
zip_path = OUT/'step100_semilocal_plancherel_instantiation_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.name != zip_path.name:
            z.write(p, p.name)

print('wrote', OUT)
