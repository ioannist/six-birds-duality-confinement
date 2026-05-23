import csv, json, math, os, zipfile
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step53_navier_xi')
OUT.mkdir(parents=True, exist_ok=True)

def cap_scaling_exponent(d, s, m):
    # For cell-average derivative order m under H^s audit:
    # Cap_r ~ r^{2(s-m)-d} if s < d/2+m; log if equality; bounded if above.
    critical = d/2 + m
    if abs(s-critical) < 1e-12:
        return None
    if s < critical:
        return 2*(s-m)-d
    return 0.0

rows=[]
d=3
cases=[
    ('energy L2 controls velocity cell average',0.0,0),
    ('enstrophy H1 controls velocity cell average',1.0,0),
    ('H2 controls velocity cell average',2.0,0),
    ('enstrophy H1 controls gradient/vorticity cell average',1.0,1),
    ('H2 controls gradient/vorticity cell average',2.0,1),
    ('critical H5/2 controls gradient/vorticity cell average',2.5,1),
    ('H3 controls gradient/vorticity cell average',3.0,1),
]
for name,s,m in cases:
    critical=d/2+m
    exp=cap_scaling_exponent(d,s,m)
    if exp is None:
        behavior='log divergence'
        display='log(1/r)'
    elif s < critical:
        behavior='power divergence as r -> 0'
        display=f'r^{exp:.1f}'
    else:
        behavior='bounded as r -> 0'
        display='O(1)'
    rows.append(dict(case=name,d=d,s=s,derivative_order=m,critical_s=critical,scaling=display,behavior=behavior))

with open(OUT/'sobolev_capacity_scaling_step53.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# Plot normalized asymptotic curves for cases.
rs=np.logspace(-4,0,400)
plt.figure(figsize=(7,4.5))
for name,s,m in cases:
    crit=d/2+m
    exp=cap_scaling_exponent(d,s,m)
    if exp is None:
        vals=np.log(1/rs+math.e)
    elif s < crit:
        vals=rs**exp
    else:
        vals=np.ones_like(rs)
    vals=vals/vals[-1]
    plt.loglog(rs, vals, label=f's={s:g}, m={m}')
plt.gca().invert_xaxis()
plt.xlabel('cell scale r (decreasing to the right)')
plt.ylabel('relative capacity scale')
plt.title('Sobolev-audit capacity scaling for localized probes in d=3')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'sobolev_capacity_scaling_step53.png', dpi=180)
plt.close()

# Additional obligation table
obligations=[
    {'slot':'Carrier','symbol':'H_j or E_j','NS_reading':'scale-localized divergence-free velocity/vorticity carrier','must_prove':'formed closure with lawful quotient and boundary/support conditions'},
    {'slot':'Audit','symbol':'C_j','NS_reading':'energy, enstrophy, dissipation, or stronger parabolic audit','must_prove':'positive audit with null-mode legality and predictive transport'},
    {'slot':'Native probes','symbol':'L_j','NS_reading':'declared shell/cell energy, enstrophy, filtered velocity/vorticity probes','must_prove':'admissible predictive probe family with recombination closure'},
    {'slot':'Dissolving probes','symbol':'D_j','NS_reading':'pointwise or scale-local blow-up probes: velocity, vorticity, gradient, strain','must_prove':'these are the probes required for the regularity/continuation claim'},
    {'slot':'Adequacy residual','symbol':'Xi_{C_j}(D_j | L_j)','NS_reading':'blind spot between native energy ledger and blow-up probes','must_prove':'uniform bound, summable residual, or collapse under strict extension'},
    {'slot':'Predictive membrane','symbol':'K_j <= Theta','NS_reading':'no native predictive recombination needles across shells/time','must_prove':'summable defects and route/protocol honesty'},
    {'slot':'Layer-dissolving promotion','symbol':'K^D_j <= A_j Theta_j A_j^* + Xi_j','NS_reading':'native membrane implies no blow-up needles only if Xi is controlled','must_prove':'adequacy, not merely energy inequality'},
]
with open(OUT/'navier_adequacy_obligations_step53.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(obligations[0].keys()))
    w.writeheader(); w.writerows(obligations)

schema={
  'name':'NavierAdequacyDemonstration',
  'purpose':'Symbolic mapping of formed-layer membrane/adequacy residual theory to Navier-Stokes-style regularity probes.',
  'objects':{
    'C_s':'Sobolev/energy audit operator, modelled as (I-Delta)^s or scale-local variant.',
    'L_j':'native energy/enstrophy/shell probe family declared by the closure.',
    'D_j':'layer-dissolving localized point/cell/gradient/vorticity blow-up probe family.',
    'Xi':'conditional adequacy residual Xi_C(D|L), the blind-spot currency.'
  },
  'main_scaling':'Localized derivative order m probe under H^s audit has capacity finite at point scale iff s > d/2 + m; below that it diverges like r^{2(s-m)-d} or logarithmically at equality.',
  'claim_status':'symbolic proof-level demonstration, not an NS regularity proof and not a Six Birds simulation.',
  'nonclaims':['does not prove Navier-Stokes regularity','does not instantiate a native Six Birds NS substrate','does not claim energy/enstrophy adequacy for blow-up probes']
}
with open(OUT/'navier_xi_schema_step53.json','w') as f:
    json.dump(schema,f,indent=2)

# theorem map
thm=[
    {'id':'T53.1','name':'Localized Sobolev capacity scaling','input':'H^s audit, derivative order m localized probe at scale r','output':'capacity finite iff s>d/2+m; scaling otherwise'},
    {'id':'T53.2','name':'Energy/enstrophy blind spot','input':'d=3, s=0 or s=1 native audit','output':'pointwise velocity/gradient/vorticity probes have divergent capacity'},
    {'id':'T53.3','name':'Xi promotion for NS probes','input':'native membrane K_L<=Theta and Xi_C(D|L)<=Xi','output':'dissolving probe membrane K_D<=A Theta A^*+Xi'},
    {'id':'T53.4','name':'Strict extension alternatives','input':'added probes or stronger audit source','output':'Xi can contract only when the extension sees the blow-up blind spot'},
]
with open(OUT/'theorem_map_step53.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(thm[0].keys()))
    w.writeheader(); w.writerows(thm)

print('wrote step53 scaling artifacts')
