#!/usr/bin/env python3
"""Step 53: symbolic Navier adequacy scalings for Xi theory.
These are not Six Birds simulations. They are formula checks/plots for shell capacity exponents.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step53_navier_xi')
OUT.mkdir(parents=True, exist_ok=True)

def capacity_exponent(d: int, s: float, derivative_order: int) -> float:
    # Fourier shell dimension ~ 2^{d j}; audit weight ~ 2^{2s j}; derivative adds 2^{2q j}
    return d + 2*derivative_order - 2*s

rows = []
for d in [2,3,4]:
    for s in [0, 1, 1.5, 2, 2.5, 3, 3.5]:
        for q, label in [(0, 'velocity/value'), (1, 'gradient/vorticity')]:
            exp = capacity_exponent(d, s, q)
            rows.append({
                'dimension_d': d,
                'audit_sobolev_order_s': s,
                'probe_order_q': q,
                'probe_label': label,
                'shell_capacity_scaling_exponent': exp,
                'capacity_behavior': 'decays' if exp < 0 else ('constant' if abs(exp) < 1e-12 else 'grows'),
                'threshold_s_for_decay': d/2 + q,
            })
scaling = pd.DataFrame(rows)
scaling.to_csv(OUT/'navier_shell_capacity_scaling_step53.csv', index=False)

# A small finite Fourier shell model on T^d: capacity ~ number of modes / shell weight.
# We use asymptotic formula for dimensions; exact integer shells are unnecessary for this symbolic demo.
js = np.arange(0, 17)
model_rows = []
for d in [3]:
    for s in [0, 1, 2, 3]:
        for q, label in [(0, 'velocity/value'), (1, 'gradient/vorticity')]:
            exp = capacity_exponent(d, s, q)
            caps = 2.0 ** (exp * js)
            for j, cap in zip(js, caps):
                model_rows.append({
                    'j': int(j), 'dimension_d': d, 's': float(s), 'q': q,
                    'probe_label': label, 'exponent': exp, 'model_capacity': float(cap)
                })
model = pd.DataFrame(model_rows)
model.to_csv(OUT/'navier_shell_capacity_model_step53.csv', index=False)

# Plot velocity point capacity in d=3 for different audits.
plt.figure(figsize=(7, 4.5))
for s in [0, 1, 2, 3]:
    subset = model[(model.dimension_d==3)&(model.s==s)&(model.q==0)]
    plt.semilogy(subset['j'], subset['model_capacity'], marker='o', label=f's={s}')
plt.xlabel('shell depth j')
plt.ylabel('model capacity for value probe')
plt.title('d=3 shell capacity: value probe, H^s audit')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'navier_value_probe_capacity_scaling_step53.png', dpi=180)
plt.close()

# Plot gradient/vorticity capacity in d=3.
plt.figure(figsize=(7, 4.5))
for s in [0, 1, 2, 3]:
    subset = model[(model.dimension_d==3)&(model.s==s)&(model.q==1)]
    plt.semilogy(subset['j'], subset['model_capacity'], marker='o', label=f's={s}')
plt.xlabel('shell depth j')
plt.ylabel('model capacity for gradient/vorticity probe')
plt.title('d=3 shell capacity: gradient/vorticity probe, H^s audit')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'navier_gradient_probe_capacity_scaling_step53.png', dpi=180)
plt.close()

# Illustrative Xi residual: D point/gradient representer, L captures a fraction c of the C-dual representer.
coverage_rows = []
coverages = np.linspace(0, 1, 21)
base_cap = 100.0
for cov in coverages:
    xi = (1 - cov**2) * base_cap
    explained = cov**2 * base_cap
    coverage_rows.append({'coverage_norm_fraction': cov, 'explained_currency': explained, 'xi_residual': xi})
coverage_df = pd.DataFrame(coverage_rows)
coverage_df.to_csv(OUT/'navier_xi_coverage_model_step53.csv', index=False)

plt.figure(figsize=(7, 4.5))
plt.plot(coverage_df['coverage_norm_fraction'], coverage_df['xi_residual'], marker='o')
plt.xlabel('native coverage of dissolving representer')
plt.ylabel('Xi residual currency')
plt.title('Adequacy residual decreases only when native probes see the blind spot')
plt.tight_layout()
plt.savefig(OUT/'navier_xi_coverage_step53.png', dpi=180)
plt.close()

schema = {
  'step': 53,
  'name': 'Navier adequacy demonstration',
  'status': 'symbolic obligation map; not NS proof; not Six Birds simulation',
  'objects': {
    'H_j': 'dyadic shell / divergence-free velocity or vorticity carrier',
    'C_j': 'audit energy, e.g. H^s shell form, dissipation/enstrophy/Sobolev ledger',
    'L_j': 'native probes: shell energy/enstrophy/channel readouts declared by formed NS layer',
    'D_j': 'layer-dissolving probes: localized velocity, gradient, vorticity, strain, blow-up-rate readouts',
    'Xi_j': 'conditional adequacy residual Xi_{C_j}(D_j | L_j) measuring blind spot of native probes against blow-up probes'
  },
  'core_formula': 'Xi_C(D|L)=D C^dag D^* - D C^dag L^*(L C^dag L^*)^dag L C^dag D^*',
  'shell_scaling': 'Cap(point derivative order q; H^s audit on d-dimensional shell j) ~ 2^{(d+2q-2s)j}',
  'threshold': 'decay requires s > d/2 + q',
  'navier_3d_implication': {
    'velocity_value_probe': 'requires s>3/2 for decay',
    'gradient_vorticity_probe': 'requires s>5/2 for decay',
    'energy_enstrophy': 's=0 or s=1 are not adequate for gradient/vorticity point probes by this linear shell criterion'
  }
}
(OUT/'navier_xi_schema_step53.json').write_text(json.dumps(schema, indent=2))
print('wrote step 53 artifacts')
