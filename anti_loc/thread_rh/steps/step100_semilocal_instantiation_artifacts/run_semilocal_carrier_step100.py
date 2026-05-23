import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/rh_membrane_step100_semilocal_instantiation')
OUT.mkdir(parents=True, exist_ok=True)

# Model 1: trace-class versus non-trace-class zero ledger tails.
Nmax = 300
n = np.arange(1, Nmax+1)
Kmax = 200000
k = np.arange(1, Kmax+1)
trace_eigs = k**(-2.2)
nontrace_eigs = k**(-1.0)
# normalize first to sum ~1, nontrace to finite truncation for plotting only
trace_eigs = trace_eigs / trace_eigs.sum()
nontrace_eigs = nontrace_eigs / nontrace_eigs[:Kmax].sum()

def tail(eigs, nvals):
    cumsum = np.cumsum(eigs)
    return np.array([max(0.0, 1.0 - cumsum[min(int(i), len(eigs))-1]) for i in nvals])

trace_tail = tail(trace_eigs, n)
nontrace_tail = tail(nontrace_eigs, n)
Lambda = n**0.72
budget_collapse = 1.0/Lambda + trace_tail
moving_window_tail = 1.0/Lambda + nontrace_tail

pd.DataFrame({
    'N': n,
    'lambda_N': Lambda,
    'inverse_lambda': 1.0/Lambda,
    'trace_class_zero_tail': trace_tail,
    'nontrace_model_tail': nontrace_tail,
    'certified_budget_trace_class': budget_collapse,
    'support_only_budget_nontrace_model': moving_window_tail,
}).to_csv(OUT/'plancherel_tail_model_step100.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.loglog(n, trace_tail, label='trace-class ledger tail')
plt.loglog(n, nontrace_tail, label='moving-window / slow tail model')
plt.loglog(n, 1.0/Lambda, label='source budget 1/Lambda_N')
plt.xlabel('window size N')
plt.ylabel('tail / budget')
plt.title('Trace-class tail versus moving-window support-only tail')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'plancherel_tail_model_step100.png', dpi=200)
plt.close()

plt.figure(figsize=(7,4.5))
plt.loglog(n, budget_collapse, label='certified budget with trace-class tail')
plt.loglog(n, moving_window_tail, label='support-only budget with slow tail')
plt.xlabel('window size N')
plt.ylabel('1/Lambda_N + tail_N')
plt.title('Completed lower-frame budget collapse requires tail control')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'completed_budget_collapse_step100.png', dpi=200)
plt.close()

# Model 2: compact Delta absorption by finite windows.
delta_eigs = np.exp(-k/35.0)
delta_eigs = delta_eigs / delta_eigs.sum()
delta_tail = tail(delta_eigs, n)
source_abs = 1.0/Lambda + delta_tail
pd.DataFrame({'N': n, 'delta_compact_tail': delta_tail, 'inverse_lambda':1.0/Lambda, 'absorption_allowance':source_abs}).to_csv(OUT/'compact_delta_absorption_model_step100.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.loglog(n, delta_tail, label='compact Delta positive-tail')
plt.loglog(n, 1.0/Lambda, label='source budget 1/Lambda_N')
plt.loglog(n, source_abs, label='absorption allowance')
plt.xlabel('window size N')
plt.ylabel('tail / allowance')
plt.title('Compact Delta shortcut: finite window plus tail')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'compact_delta_absorption_model_step100.png', dpi=200)
plt.close()

# Model 3: semilocal measure deformation for finite S (toy with Euler factors). Avoid poles by sample range.
xi = np.linspace(-30,30,2001)
primes = [2,3,5,7]
rows=[]
base = np.ones_like(xi)
for m in range(0, len(primes)+1):
    S = primes[:m]
    weight = np.ones_like(xi)
    for p in S:
        z = 0.5 - 1j*xi
        Lp = 1.0/(1.0 - p**(-z))
        weight *= np.abs(Lp)**2
    rows.append({'num_primes':m, 'primes':' '.join(map(str,S)) if S else 'none', 'weight_min':float(weight.min()), 'weight_max':float(weight.max()), 'weight_mean':float(weight.mean()), 'weight_std':float(weight.std())})
    if m in [0,1,2,4]:
        plt.plot(xi, weight, label=f'|local factors|^2, m={m}')
plt.xlabel('spectral variable xi')
plt.ylabel('toy dm_S / dxi')
plt.title('Semilocal response measure deformation by finite Euler factors')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'semilocal_measure_deformation_step100.png', dpi=200)
plt.close()
pd.DataFrame(rows).to_csv(OUT/'semilocal_measure_deformation_summary_step100.csv', index=False)

# Simple theorem/gate tables.
gate_rows = [
    ['G1', 'Carrier choice', 'Use fixed finite semilocal response space Y_S^- = L^2(R,dm_S)^-', 'accepted-as-instantiation', 'Requires fixed S; full RH still needs S/tail ladder'],
    ['G2', 'Window maps', 'P_{T,N}^{S,-}: anti-invariant spectral/prolate/cyclic-pair finite window', 'defined', 'Orthogonal-polynomial coefficients for general S are deferred in CCM; any directed finite-rank core may be used provisionally'],
    ['G3', 'Tail form', '(Theta_0^-)^{-1} <= Pi^*B Pi + T_{T,N}', 'defined-as-gate', 'Vanishing is ledger-trace/exhaustivity, not operator-norm tail'],
    ['G4', 'Finite lower frame', 'F_win >= Lambda B_win on window', 'finite-window-only', 'Needs character/source records on window'],
    ['G5', 'Completed promotion', 'F + Lambda T >= Lambda (Theta_0^-)^{-1}', 'conditional theorem', 'Only useful if tail vanishes in fixed/exhaustive ledger sense'],
    ['G6', 'Delta absorption', 'Delta_S^+ <= F + E_abs', 'active analytic target', 'Compact Delta would simplify; otherwise needs arithmetic lower-frame input'],
    ['G7', 'Adequacy', 'Xi_C(D_off | L^-) controlled', 'retained framework gate', 'Not discharged here'],
    ['G8', 'Conrey-Li survival', 'Do not collapse into de Branges/RKHS shift positivity', 'warning', 'Keep semilocal/Sonin/Hecke carrier distinct']
]
pd.DataFrame(gate_rows, columns=['gate','record','formula_or_content','status','defect_or_warning']).to_csv(OUT/'semilocal_carrier_gate_table_step100.csv', index=False)

theorem_rows = [
    ['T100.1', 'Semilocal carrier instantiation', 'Define Y_S^-, J_S, dm_S, P_{T,N}^{S,-}', 'Turns abstract Step 99 theorem into a concrete semilocal record'],
    ['T100.2', 'Finite-window promotion theorem', 'F_win >= Lambda B_win and inverse-budget tail imply completed lower frame up to Lambda T', 'Makes finite characters useful only with tail'],
    ['T100.3', 'Ledger-tail squeeze theorem', 'trace((I-P_n) A_Z (I-P_n)) -> 0 promotes finite windows to exact ledger control', 'Prevents moving-ledger overread'],
    ['T100.4', 'Compact Delta shortcut', 'If Delta_S^+ compact, finite windows capture it up to small tail', 'High-leverage analytic test suggested by user'],
    ['T100.5', 'No finite-window RH theorem', 'Without Plancherel/exhaustivity, finite windows remain support-only', 'Nonclaim boundary']
]
pd.DataFrame(theorem_rows, columns=['id','name','statement','role']).to_csv(OUT/'theorem_map_step100.csv', index=False)

construct_rows = [
    ['C1', 'Fix finite semilocal S', 'S={infty} union finite primes; define dm_S from local factors', 'done in theorem statement'],
    ['C2', 'Build anti-invariant core', 'Y_S^- = {y: y(s) = -conj(y(-s))}', 'done'],
    ['C3', 'Choose windows', 'P_T spectral cutoff plus P_N cyclic-pair/prolate/orthogonal polynomial projection', 'defined but coefficients for general S need CCM continuation'],
    ['C4', 'Define tail form', 'T_{T,N} in inverse-budget inequality and ledger trace tail tau_Z(T,N)', 'done as gate'],
    ['C5', 'Prove finite character/source frame on window', 'F_win >= Lambda B_win', 'open arithmetic / finite linear algebra'],
    ['C6', 'Prove Plancherel/exhaustivity', 'tau_Z(T,N)->0 and source/tail defects vanish', 'open analytic promotion'],
    ['C7', 'Absorb Delta_S^+', 'compact shortcut or Hecke source absorption', 'active target'],
    ['C8', 'Run Xi adequacy', 'Xi(D_off|L^-) controlled on same carrier', 'later step']
]
pd.DataFrame(construct_rows, columns=['task','object','requirement','status']).to_csv(OUT/'construction_tasks_step100.csv', index=False)

arith_rows = [
    ['Semilocal Hardy-Titchmarsh', 'V_S=M_S U_S unitary, dm_S=|prod L_v(1/2-is)|^2 ds', 'anchors the chosen carrier'],
    ['Cyclic-pair / prolate basis', 'orthogonal polynomial/prolate windows', 'native finite-rank projections'],
    ['Character finite frame', 'complete characters on finite quotient', 'window lower frame only'],
    ['Plancherel/exhaustivity', 'direct integral or strong projection convergence with trace-class ledger tail', 'completed promotion'],
    ['Delta compactness', 'Delta_S^+ compact or compact-after-quotient', 'shortcuts source absorption'],
    ['Source absorption', 'Delta_S^+ <= F_n + E_abs,n', 'main open inequality'],
]
pd.DataFrame(arith_rows, columns=['input','operator_content','role']).to_csv(OUT/'arithmetic_input_table_step100.csv', index=False)

# structural LaTeX check placeholder after tex generated separately
