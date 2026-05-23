import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step66_fixed_ledger')
OUT.mkdir(parents=True, exist_ok=True)

# 1. Fixed squeeze: a fixed positive ledger mass cannot be dominated by 1/n forever.
ns = np.arange(1, 501)
fixed_rows = []
for mass in [0.0, 0.01, 0.05, 0.1]:
    for n in ns:
        b = 1.0 / n
        fixed_rows.append({
            'model': 'fixed_ledger_squeeze',
            'n': int(n),
            'fixed_mass': mass,
            'budget_trace': b,
            'domination_holds': bool(mass <= b + 1e-15),
            'violation': max(mass - b, 0.0)
        })
fixed_df = pd.DataFrame(fixed_rows)
fixed_df.to_csv(OUT/'fixed_squeeze_checks_step66.csv', index=False)

plt.figure(figsize=(7,4.5))
for mass in [0.01, 0.05, 0.1]:
    sub = fixed_df[fixed_df.fixed_mass == mass]
    plt.plot(sub.n, sub.violation, label=f'fixed mass {mass}')
plt.xlabel('stage n')
plt.ylabel('domination violation max(mass - 1/n, 0)')
plt.title('A nonzero fixed ledger cannot be squeezed by 1/n forever')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'fixed_ledger_squeeze_violation_step66.png', dpi=160)
plt.close()

# 2. Monotone nontermination K_n = 1 + 1/n vs Theta=1.
mono_rows=[]
for n in ns:
    k=1+1/n
    defect=k-1
    mono_rows.append({'n': int(n), 'K_n': k, 'Theta': 1.0, 'defect': defect, 'finite_stage_accepted': bool(k <= 1.0)})
mono_df=pd.DataFrame(mono_rows)
mono_df.to_csv(OUT/'monotone_nontermination_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(mono_df.n, mono_df.defect)
plt.xlabel('stage n')
plt.ylabel('defect K_n - Theta')
plt.title('Defect decreases to zero but never terminates finitely')
plt.tight_layout()
plt.savefig(OUT/'monotone_nontermination_step66.png', dpi=160)
plt.close()

# 3. Moving ledger support-only failure.
# Visible ledger vanishes, but hidden tail remains constant.
move_rows=[]
for n in ns:
    visible_A = 0.0
    visible_budget = 0.0
    hidden_tail = 0.2
    completed_mass = visible_A + hidden_tail
    move_rows.append({
        'n': int(n),
        'visible_A_n': visible_A,
        'visible_budget_B_n': visible_budget,
        'hidden_tail_not_audited': hidden_tail,
        'completed_A_mass': completed_mass,
        'visible_status': 'passes',
        'completed_status': 'fails_exhaustivity'
    })
move_df=pd.DataFrame(move_rows)
move_df.to_csv(OUT/'moving_ledger_support_only_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(move_df.n, move_df.visible_budget_B_n, label='visible budget')
plt.plot(move_df.n, move_df.hidden_tail_not_audited, label='hidden tail')
plt.xlabel('stage n')
plt.ylabel('mass / budget')
plt.title('Moving visible ledger can vanish while hidden tail remains')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'moving_ledger_hidden_tail_step66.png', dpi=160)
plt.close()

# 4. Exhaustive tail success/failure.
exh_rows=[]
for n in ns:
    Bn = 1/n**2
    Tn_success = 1/n**2
    Tn_failure = 0.05
    exh_rows.append({
        'n': int(n),
        'visible_budget_B_n': Bn,
        'tail_success_T_n': Tn_success,
        'total_success_bound': Bn+Tn_success,
        'tail_failure_T_n': Tn_failure,
        'total_failure_bound': Bn+Tn_failure
    })
exh_df=pd.DataFrame(exh_rows)
exh_df.to_csv(OUT/'exhaustive_tail_budget_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(exh_df.n, exh_df.total_success_bound, label='exhaustive: B_n + T_n -> 0')
plt.plot(exh_df.n, exh_df.total_failure_bound, label='non-exhaustive: tail persists')
plt.xlabel('stage n')
plt.ylabel('completed-ledger upper bound')
plt.title('Exhaustive tail budget versus hidden tail failure')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'exhaustive_tail_budget_step66.png', dpi=160)
plt.close()

# 5. Optimized RH obstruction budget.
opt_rows=[]
for n in ns:
    Lambda = n
    tr_theta0 = 1.0
    esrc = 1/n**2
    eef = 1/n**3
    a = tr_theta0/Lambda + esrc
    b = eef
    t_opt = np.sqrt(b/a) if a>0 else 1.0
    opt_bound = (np.sqrt(a)+np.sqrt(b))**2
    t1_bound = 2*a+2*b  # t=1
    opt_rows.append({
        'n': int(n),
        'Lambda_n': Lambda,
        'a_n': a,
        'b_n': b,
        't_opt': t_opt,
        'optimized_trace_bound': opt_bound,
        't_equals_1_trace_bound': t1_bound
    })
opt_df=pd.DataFrame(opt_rows)
opt_df.to_csv(OUT/'optimized_obstruction_budget_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(opt_df.n, opt_df.optimized_trace_bound, label='optimized t')
plt.plot(opt_df.n, opt_df.t_equals_1_trace_bound, label='t=1')
plt.xlabel('stage n')
plt.ylabel('trace obstruction budget')
plt.title('Optimized root-composite obstruction budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'optimized_obstruction_budget_step66.png', dpi=160)
plt.close()

# Status table.
status_rows = [
    {'status': 'finite_completion', 'criterion': 'some finite N has completed ledger AZ = 0 or zero budget on fixed ledger', 'licenses_exact_confinement': True, 'warning': 'strongest form but often unavailable'},
    {'status': 'fixed_ledger', 'criterion': 'same completed AZ dominated by B_n with tr B_n -> 0', 'licenses_exact_confinement': True, 'warning': 'requires same-object visibility'},
    {'status': 'exhaustive_ledger', 'criterion': 'P_n AZ P_n or visible AZ_n plus tail T_n, with tr(B_n+T_n)->0', 'licenses_exact_confinement': True, 'warning': 'tail/exhaustivity record is load-bearing'},
    {'status': 'moving_ledger_support_only', 'criterion': 'AZ_n dominated by B_n -> 0 but no fixed/exhaustive bridge', 'licenses_exact_confinement': False, 'warning': 'visible finite stages may miss hidden zero tail'},
    {'status': 'failed_budget_collapse', 'criterion': 'EF/source defects or Lambda^{-1} term do not tend to zero', 'licenses_exact_confinement': False, 'warning': 'only quantitative confinement with nonzero allowance'},
    {'status': 'failed_visibility', 'criterion': 'zero readout does not separate fixed locus or ledger incomplete', 'licenses_exact_confinement': False, 'warning': 'off-fixed mass may be invisible'},
]
pd.DataFrame(status_rows).to_csv(OUT/'ledger_status_table_step66.csv', index=False)

# Theorem map.
theorem_rows = [
    {'theorem': 'fixed-ledger squeeze', 'claim': 'AZ <= B_n for all n and tr B_n -> 0 implies AZ=0', 'hypothesis_type': 'fixed completed ledger'},
    {'theorem': 'exhaustive-ledger squeeze', 'claim': 'P_n AZ P_n <= B_n, P_n -> I, tr B_n -> 0 implies AZ=0', 'hypothesis_type': 'monotone exhaustive visibility'},
    {'theorem': 'tail-budget squeeze', 'claim': 'AZ <= AZ_n + T_n, AZ_n <= B_n, tr(B_n+T_n)->0 implies AZ=0', 'hypothesis_type': 'visible ledger plus tail record'},
    {'theorem': 'moving-ledger no-go', 'claim': 'AZ_n <= B_n -> 0 alone does not imply completed AZ=0', 'hypothesis_type': 'countermodel'},
    {'theorem': 'RH fixed-ledger criterion', 'claim': 'EF/source budget squeeze of fixed/exhaustive AZ gives critical-line confinement', 'hypothesis_type': 'root-composite obligation'},
]
pd.DataFrame(theorem_rows).to_csv(OUT/'theorem_map_step66.csv', index=False)

print('Step 66 checks written to', OUT)
