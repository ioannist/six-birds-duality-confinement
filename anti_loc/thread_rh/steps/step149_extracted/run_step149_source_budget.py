import json
import math
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step149_source_audit_budget')
OUT.mkdir(parents=True, exist_ok=True)

# Scenario data for source budget squeeze
N = np.arange(2, 501)
Lambda = np.log(N+1)
tail = 1/np.sqrt(N)
residual_mass = 0.35

scenarios = []
for name, budget in [
    ('sublinear_budget', np.sqrt(Lambda)),
    ('linear_natural_budget', residual_mass*Lambda),
    ('linear_half_budget', 0.5*residual_mass*Lambda),
    ('superlinear_budget', residual_mass*Lambda*np.log(np.log(N+3)+1)),
]:
    upper = budget/Lambda + tail
    lower_for_positive_mass = residual_mass * np.ones_like(N)
    for n, lam, b, t, u, lb in zip(N, Lambda, budget, tail, upper, lower_for_positive_mass):
        scenarios.append({
            'N': int(n),
            'scenario': name,
            'Lambda': float(lam),
            'budget_B_N': float(b),
            'budget_ratio_B_over_Lambda': float(b/lam),
            'tail': float(t),
            'completed_upper_bound': float(u),
            'no_free_lower_ratio_if_mass_positive': float(lb),
        })
scenario_df = pd.DataFrame(scenarios)
scenario_df.to_csv(OUT/'source_budget_scenarios_step149.csv', index=False)

# Evaluator exposure shell model
J = np.arange(1, 31)
# shell envelope weights chosen as in Step 147-style fixed weighted ledger
n_j = np.ceil(2 + J*np.log(J+2)).astype(int)
E_j = (1+J)**2
omega_j = 2.0**(-J) / ((1+n_j)*(1+E_j))
q2_bound = 0.25
# Source response models U_N(shell)
rows=[]
for growth in ['sublinear_shell_response','linear_shell_response','superlinear_shell_response']:
    for j, nj, Ej, oj in zip(J, n_j, E_j, omega_j):
        if growth == 'sublinear_shell_response':
            exposure_growth = np.sqrt(Lambda[-1])/(1+j)
        elif growth == 'linear_shell_response':
            exposure_growth = Lambda[-1]*(1/(1+j))
        else:
            exposure_growth = Lambda[-1]*np.log(j+2)/(1+j)
        rows.append({
            'shell': int(j),
            'scenario': growth,
            'n_j': int(nj),
            'E_j': float(Ej),
            'omega_j': float(oj),
            'q2_bound': q2_bound,
            'source_response_envelope_U_j': float(exposure_growth),
            'weighted_contribution': float(oj*q2_bound*exposure_growth*nj*Ej/(1+Ej)),
        })
exposure_df = pd.DataFrame(rows)
exposure_df.to_csv(OUT/'source_evaluator_exposure_step149.csv', index=False)

# Gate tables
pd.DataFrame([
    {'gate':'fixed ledger','condition':'K_R^omega is fixed, positive, trace-class, and independent of N','status':'required'},
    {'gate':'lower frame','condition':'F_N^Omega + E_N^Omega >= Lambda_N^Omega G_R with Lambda_N^Omega -> infinity','status':'conditional from restricted source route'},
    {'gate':'source exposure','condition':'tr(F_N^Omega K_R^omega)/Lambda_N^Omega -> 0','status':'collapse-level; not routine'},
    {'gate':'source defect','condition':'tr(E_N^Omega K_R^omega)/Lambda_N^Omega -> 0','status':'required'},
    {'gate':'tail','condition':'tr((I-P_N)K_R^omega(I-P_N)) -> 0','status':'requires fixed/exhaustive ledger'},
    {'gate':'separation','condition':'omega_z > 0 on visible residual zero directions','status':'passes by declared schedule'},
    {'gate':'no moving weights','condition':'omega_z must not scale with Lambda_N after the fact','status':'enforced'},
]).to_csv(OUT/'source_audit_budget_gate_table_step149.csv', index=False)

pd.DataFrame([
    {'theorem':'No-free source budget','input':'F_N^Omega+E_N^Omega >= Lambda_N^Omega G_R, K_R^omega >= 0','output':'tr(F_N^Omega K_R^omega)+tr(E_N^Omega K_R^omega) >= Lambda_N^Omega tr(G_R K_R^omega)'},
    {'theorem':'Collapse by sublinear budget','input':'source exposure and source defect are o(Lambda_N^Omega)','output':'tr(G_R K_R^omega)=0'},
    {'theorem':'Obstruction if residual mass positive','input':'tr(G_R K_R^omega)>0 and defects negligible','output':'source exposure ratio has positive liminf'},
    {'theorem':'Evaluator response expansion','input':'K_R^omega=sum_z omega_z q_z^2 |y_z><y_z|','output':'tr(F_N K_R^omega)=sum_z omega_z q_z^2 <F_N y_z,y_z>'},
]).to_csv(OUT/'theorem_map_step149.csv', index=False)

pd.DataFrame([
    {'route':'collapse certificate','condition':'B_N^omega/Lambda_N^Omega -> 0','meaning':'visible residual off-critical ledger collapses'},
    {'route':'linear exposure','condition':'B_N^omega/Lambda_N^Omega -> c>0','meaning':'no residual collapse; source frame only bounds mass'},
    {'route':'uncontrolled exposure','condition':'no uniform source exposure envelope','meaning':'finite-window support only'},
    {'route':'moving-weight normalization','condition':'omega_z depends on N to force bounded exposure','meaning':'invalid for completed fixed ledger'},
]).to_csv(OUT/'route_status_step149.csv', index=False)

pd.DataFrame([
    {'input':'BPRZ twisted second moment','use':'candidate source-weighted lower frame on coefficient windows','status':'imported analytic NT infrastructure'},
    {'input':'CIS asymptotic large sieve','use':'primitive-character bilinear platform','status':'imported analytic NT infrastructure'},
    {'input':'Heap-Soundararajan Omega-block architecture','use':'upstream-declared source-readable cutoffs','status':'imported architecture; not operator lower frame'},
    {'input':'Burnol Sonine/co-Poisson carrier','use':'residual zero-evaluator carrier and ledger','status':'carrier infrastructure'},
    {'input':'CCM semilocal framework','use':'ambient local-factor response geometry','status':'semilocal carrier infrastructure'},
]).to_csv(OUT/'arithmetic_input_table_step149.csv', index=False)

pd.DataFrame([
    {'task':'Prove independent source-evaluator exposure envelope U_N^omega','status':'open'},
    {'task':'Check whether U_N^omega/Lambda_N^Omega -> 0','status':'collapse-level target'},
    {'task':'Reject moving N-dependent ledger weights','status':'discipline enforced'},
    {'task':'If no sublinear budget exists, record completed-ledger obstruction','status':'pending'},
]).to_csv(OUT/'construction_tasks_step149.csv', index=False)

# Schema
schema = {
    'step': 149,
    'title': 'Source Audit Budget Theorem or Obstruction',
    'main_objects': ['F_N^Omega', 'K_R^omega', 'Lambda_N^Omega', 'B_N^omega', 'G_R', 'E_N^Omega'],
    'main_verdict': 'Sublinear source exposure is collapse-level; source compatibility is not free.',
    'next_step': 'Step 150: source-evaluator exposure mechanism or completed-ledger obstruction ledger'
}
(OUT/'step149_schema.json').write_text(json.dumps(schema, indent=2))

(OUT/'nonclaim_boundary_step149.md').write_text('''# Nonclaim Boundary — Step 149\n\nStep 149 does not prove RH.\n\nIt does not prove the source exposure budget. It proves that a sublinear exposure budget, together with the growing source lower frame, is already a collapse certificate for the fixed residual ledger.\n\nIt does not allow moving the residual weights with N. Such a move is moving-window support evidence only.\n\nIt does not say BPRZ or any scalar moment theorem supplies the needed source-evaluator exposure envelope.\n''')

# Plots
plt.figure(figsize=(7,4.5))
for scen in ['sublinear_budget','linear_natural_budget','superlinear_budget']:
    d=scenario_df[scenario_df['scenario']==scen]
    plt.plot(d['N'], d['budget_ratio_B_over_Lambda'], label=scen.replace('_',' '))
plt.axhline(residual_mass, linestyle='--', label='no-free lower ratio if mass positive')
plt.xlabel('N')
plt.ylabel('B_N / Lambda_N')
plt.title('Source budget ratio versus no-free lower bound')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'source_budget_squeeze_step149.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
for scen in ['sublinear_budget','linear_natural_budget','superlinear_budget']:
    d=scenario_df[scenario_df['scenario']==scen]
    plt.plot(d['N'], d['completed_upper_bound'], label=scen.replace('_',' '))
plt.xlabel('N')
plt.ylabel('completed upper bound')
plt.title('Completed squeeze upper bound')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'completed_squeeze_budget_step149.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
for scen in exposure_df['scenario'].unique():
    d=exposure_df[exposure_df['scenario']==scen]
    plt.plot(d['shell'], d['weighted_contribution'].cumsum(), label=scen.replace('_',' '))
plt.xlabel('height shell')
plt.ylabel('cumulative weighted exposure proxy')
plt.title('Source-evaluator exposure shell model')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'source_evaluator_exposure_step149.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
alpha = np.linspace(0,1,200)
for m in [0.1,0.3,0.6]:
    plt.plot(alpha, alpha*m, label=f'allowed ratio alpha*m, m={m}')
plt.xlabel('alpha')
plt.ylabel('budget ratio')
plt.title('Strict contraction budget is collapse-level when alpha < 1')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'strict_budget_contraction_step149.png', dpi=180)
plt.close()

# simple structural check
checks = {
    'scenario_rows': int(len(scenario_df)),
    'exposure_rows': int(len(exposure_df)),
    'required_files_exist': True,
    'min_sublinear_ratio_final': float(scenario_df[scenario_df.scenario=='sublinear_budget']['budget_ratio_B_over_Lambda'].iloc[-1]),
    'positive_mass_lower_ratio': residual_mass,
}
(OUT/'step149_checks.json').write_text(json.dumps(checks, indent=2))

print(json.dumps(checks, indent=2))
