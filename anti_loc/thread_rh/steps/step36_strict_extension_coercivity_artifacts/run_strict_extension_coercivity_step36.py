"""Step 36 sanity checks for strict-extension anti-invariant coercivity.
These are algebraic checks/illustrations, not Six Birds simulations.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step36_coercivity')
OUT.mkdir(parents=True, exist_ok=True)

# 1. Direct coercivity: C = I + lambda A, L=I, Theta=I => K=(I+lambda I)^-1
lams = np.logspace(-3, 4, 100)
rows=[]
for lam in lams:
    K = 1.0/(1.0+lam)
    bound = 1.0/lam
    rows.append({'lambda':lam, 'actual_budget':K, 'coercive_bound':bound, 'ratio_actual_over_bound':K/bound})
pd.DataFrame(rows).to_csv(OUT/'direct_coercivity_step36.csv', index=False)
plt.figure(figsize=(6,4))
plt.loglog(lams, [r['actual_budget'] for r in rows], label='actual K')
plt.loglog(lams, [r['coercive_bound'] for r in rows], label='lambda^{-1} bound')
plt.xlabel('coercivity lambda')
plt.ylabel('anti-invariant budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'direct_coercivity_collapse_step36.png', dpi=160)
plt.close()

# 2. Threshold accumulation: beta_j = 1/j^p
rows=[]
for p in [0.5, 1.0, 1.5, 2.0]:
    B=0.0
    for n in range(1,501):
        B += 1.0/(n**p)
        rows.append({'p':p, 'n':n, 'B_n':B, 'budget_bound':1.0/B})
pd.DataFrame(rows).to_csv(OUT/'threshold_accumulation_step36.csv', index=False)
plt.figure(figsize=(6,4))
for p in [0.5,1.0,1.5,2.0]:
    df=pd.DataFrame(rows)
    sub=df[df['p']==p]
    plt.loglog(sub['n'], sub['budget_bound'], label=f'p={p}')
plt.xlabel('threshold count n')
plt.ylabel('budget bound 1/sum beta')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'threshold_accumulation_step36.png', dpi=160)
plt.close()

# 3. Character block forcing: three anti-invariant characters with lambda growth exponents
rows=[]
for n in range(1,301):
    lambdas = np.array([n**0.5, n**1.0, n**1.5])
    budgets = 1.0/lambdas
    rows.append({
        'n':n,
        'lambda_min':lambdas.min(),
        'max_block_budget':budgets.max(),
        'chi1_budget':budgets[0],
        'chi2_budget':budgets[1],
        'chi3_budget':budgets[2],
    })
pd.DataFrame(rows).to_csv(OUT/'character_forcing_budget_step36.csv', index=False)
plt.figure(figsize=(6,4))
for key in ['chi1_budget','chi2_budget','chi3_budget','max_block_budget']:
    plt.loglog([r['n'] for r in rows], [r[key] for r in rows], label=key)
plt.xlabel('strict-extension level n')
plt.ylabel('character budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'character_forcing_budget_step36.png', dpi=160)
plt.close()

# 4. Partial hardening failure: C=diag(1+lambda,1), L=I => one coordinate remains budget 1.
rows=[]
for lam in lams:
    Kvals=np.array([1/(1+lam),1.0])
    rows.append({'lambda':lam, 'budget_1':Kvals[0], 'budget_2':Kvals[1], 'max_budget':Kvals.max()})
pd.DataFrame(rows).to_csv(OUT/'partial_hardening_failure_step36.csv', index=False)
plt.figure(figsize=(6,4))
plt.semilogx(lams, [r['budget_1'] for r in rows], label='hardened coordinate')
plt.semilogx(lams, [r['budget_2'] for r in rows], label='unhardened coordinate')
plt.semilogx(lams, [r['max_budget'] for r in rows], label='max budget')
plt.xlabel('lambda')
plt.ylabel('budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'partial_hardening_failure_step36.png', dpi=160)
plt.close()

# 5. Symmetry-only no-collapse and bounded addition lower bound summary
pd.DataFrame([
    {'case':'symmetry_only', 'C':'I', 'L_minus':'I', 'K_minus':'I', 'collapse':'no'},
    {'case':'bounded_addition', 'C_bound':'M I', 'L_L_star_min':'m', 'lower_bound':'m/M', 'collapse':'no if m,M fixed'},
]).to_csv(OUT/'symmetry_only_no_collapse_step36.csv', index=False)

# Gate table
pd.DataFrame([
    {'source':'completion/gamma-pole audit', 'math_form':'D_j >= beta_j L-*Theta^-1 L-', 'can_collapse':'yes if sum beta_j diverges', 'audit_status':'needs visible positive component and no missing completion terms'},
    {'source':'root-composite character forcing', 'math_form':'C_chi >= lambda_chi L_chi*Theta_chi^-1 L_chi', 'can_collapse':'yes if all anti-invariant lambda_chi -> infinity', 'audit_status':'needs equivariant block ledger'},
    {'source':'threshold/refinement growth', 'math_form':'threshold increments beta_j accumulate', 'can_collapse':'yes if sum beta_j diverges', 'audit_status':'needs S7/S8 confluence and tail control'},
    {'source':'parity/fixed-layer gating', 'math_form':'L^-_Gamma = 0', 'can_collapse':'exactly zero', 'audit_status':'lawful only with nonclaim/gating record'},
    {'source':'budget repair', 'math_form':'Theta^- increased', 'can_collapse':'no, weakens claim', 'audit_status':'claim weakening not zero-confinement'},
    {'source':'symmetry alone', 'math_form':'J-invariant split only', 'can_collapse':'no', 'audit_status':'insufficient'},
    {'source':'bounded positive additions', 'math_form':'C_n <= M I', 'can_collapse':'no if L is nondegenerate', 'audit_status':'insufficient for collapse'},
]).to_csv(OUT/'coercivity_source_gate_table_step36.csv', index=False)

# Theorem map
pd.DataFrame([
    {'theorem':'coercivity implies budget collapse','input':'C >= lambda L*Theta^-1 L','output':'K <= lambda^-1 Theta','role':'core budget theorem'},
    {'theorem':'cumulative strict audit','input':'D_j >= beta_j A, sum beta_j -> infinity','output':'K_n -> 0','role':'strict extension source'},
    {'theorem':'exact fixed-layer readout','input':'L^-_Gamma=0','output':'K^-=0','role':'parity/gating source'},
    {'theorem':'character-wise coercivity','input':'each anti-invariant character block coercive','output':'root-composite budget bound','role':'algebraic source'},
    {'theorem':'bounded addition no-collapse','input':'C_n <= M I and L L* >= m I','output':'K_n >= m/M I','role':'no-go'},
    {'theorem':'symmetry-only no-collapse','input':'J-invariant split only','output':'K^- may equal I','role':'no-go'},
]).to_csv(OUT/'theorem_map_step36.csv', index=False)

# Schema
schema={
    'step':'36',
    'name':'strict_extension_source_of_anti_invariant_coercivity',
    'objects':['formed_closure','C_Gamma','L_minus_Gamma','Theta_minus_0','strict_extension_record','lambda'],
    'target':'C_Gamma >= lambda L_minus^* Theta_minus_0^{-1} L_minus with lambda -> infinity',
    'accepted_sources':['completion_gamma_pole_audit','root_composite_character_forcing','threshold_refinement_accumulation','parity_fixed_layer_gating_with_nonclaim'],
    'not_sufficient':['symmetry_only','trace_only','bounded_addition','post_hoc_lambda','budget_repair_as_confinement'],
    'closure_scope':'formed closures/layers only; non-closed artifacts are outside scope',
    'rh_reading':'off-critical displacement is anti-invariant; confinement needs explicit-formula domination plus anti-invariant budget collapse'
}
(OUT/'strict_extension_coercivity_schema_step36.json').write_text(json.dumps(schema, indent=2))

# Key summary table
pd.DataFrame([
    {'model':'direct scalar coercivity','final_budget':rows[-1]['max_budget'] if False else 1/(1+lams[-1]), 'lesson':'coercivity collapses budget'},
    {'model':'threshold p=1/2','final_budget':1/sum(1/np.sqrt(np.arange(1,501))), 'lesson':'divergent increment sum collapses budget slowly'},
    {'model':'threshold p=2','final_budget':1/sum(1/(np.arange(1,501)**2)), 'lesson':'summable increments leave finite budget'},
    {'model':'partial hardening','final_budget':1.0, 'lesson':'unhardened anti-invariant direction prevents collapse'},
]).to_csv(OUT/'step36_key_table.csv', index=False)

print('Wrote Step 36 artifacts to', OUT)
