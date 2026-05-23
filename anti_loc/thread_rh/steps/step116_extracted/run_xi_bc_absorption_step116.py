import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/rh_membrane_step116_xi_bc_source_absorption')
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(116)

# --- finite residual sector model ---
def orth(n):
    q, _ = np.linalg.qr(rng.normal(size=(n,n)))
    return q

n = 36
r = 10
Q = orth(n)
# residual Xi lives on first r directions with decaying eigenvalues
xi_eigs = np.concatenate([np.geomspace(3.0, 0.15, r), np.zeros(n-r)])
Xi = Q @ np.diag(xi_eigs) @ Q.T
Pi_R = Q[:, :r] @ Q[:, :r].T
Theta_inv = np.eye(n)

# full residual source coverage: all residual directions covered with growing Lambda
rows = []
for k, Lam in enumerate(np.linspace(1, 60, 40), start=1):
    # full coverage plus small noise/tail defects decreasing
    F_full = Lam * Pi_R + 0.05 * rng.normal(size=(n,n))
    F_full = (F_full + F_full.T)/2
    # force PSD-ish on residual by rebuilding
    F_full = Lam * Pi_R + 0.01*np.eye(n)
    # absorption allowance for Xi after source strength; compact/tail defect
    tail = 0.35/(k**1.2)
    allowance = np.linalg.norm(Xi, 2)/Lam + tail
    rows.append({'stage':k, 'Lambda':Lam, 'tail_defect':tail, 'residual_allowance_norm':allowance, 'status':'full_residual_frame'})
full_df = pd.DataFrame(rows)
full_df.to_csv(OUT/'xi_bc_full_residual_absorption_step116.csv', index=False)

# partial coverage: one residual eigen-direction is always missed
P_partial = Q[:, :r-1] @ Q[:, :r-1].T
rows = []
miss = xi_eigs[r-1]
for k, Lam in enumerate(np.linspace(1, 60, 40), start=1):
    tail = 0.35/(k**1.2)
    allowance = max(miss, np.linalg.norm(Xi,2)/Lam) + tail
    rows.append({'stage':k, 'Lambda':Lam, 'tail_defect':tail, 'uncovered_xi_eigenvalue':miss, 'residual_allowance_norm':allowance, 'status':'partial_frame_missing_one_direction'})
partial_df = pd.DataFrame(rows)
partial_df.to_csv(OUT/'xi_bc_partial_residual_failure_step116.csv', index=False)

# coefficient visibility scenarios on residual sector
Nvals = np.arange(8, 121, 4)
# plausible non-smuggled visibility gradually increasing
c_native = 1 - np.exp(-Nvals/35)
# bad dictionary saturates below 1
c_bad = 0.18*(1-np.exp(-Nvals/25))
# target-selected source is high but flagged
c_smuggled = 1 - np.exp(-Nvals/8)
# source strength inspired by log-growth lower moments (toy)
gamma = np.log(Nvals+3)**2
vis_df = pd.DataFrame({
    'N': Nvals,
    'c_native_declared': c_native,
    'c_bad_dictionary': c_bad,
    'c_target_selected_flagged': c_smuggled,
    'gamma_source_strength': gamma,
    'Lambda_native': gamma*c_native,
    'Lambda_bad': gamma*c_bad,
    'Lambda_target_selected_flagged': gamma*c_smuggled
})
vis_df.to_csv(OUT/'xi_bc_visibility_source_strength_step116.csv', index=False)

# matrix lower frame identity check on residual sector
checks = []
for trial in range(50):
    d = 12
    m = 25
    A = rng.normal(size=(m,m))
    H = A.T@A + 0.5*np.eye(m)
    gamma0 = 0.7 + 0.05*trial
    B = rng.normal(size=(m,m))
    Gx = gamma0*H + B.T@B
    R = rng.normal(size=(m,d))
    Gb = rng.normal(size=(d,d)); Gb = Gb.T@Gb + np.eye(d)
    # scale R so R^T H R >= c Gb
    RtHR = R.T@H@R
    vals = np.linalg.eigvalsh(np.linalg.solve(np.linalg.cholesky(Gb), RtHR) @ np.linalg.inv(np.linalg.cholesky(Gb)).T)
    # safer compute generalized via symmetric normalization
    Gbinv2 = np.linalg.inv(np.linalg.cholesky(Gb)).T
    c0 = np.min(np.linalg.eigvalsh(Gbinv2.T@RtHR@Gbinv2))
    F = R.T@Gx@R
    slack = F - gamma0*c0*Gb
    min_slack = np.min(np.linalg.eigvalsh((slack+slack.T)/2))
    checks.append({'trial':trial, 'gamma':gamma0, 'c_visibility':c0, 'min_certified_slack_eig':min_slack})
checks_df = pd.DataFrame(checks)
checks_df.to_csv(OUT/'matrix_lower_frame_checks_step116.csv', index=False)

# source candidate gate table data
candidates = pd.DataFrame([
    {'candidate':'residual-specific full character frame','upstream_visible':'yes','covers_residual_sector':'yes','tail_record':'required','no_smuggling':'passes if declared by conductor/order','status':'accepted theorem-shape, analytic input unearned'},
    {'candidate':'partial character subset','upstream_visible':'yes','covers_residual_sector':'no','tail_record':'not enough','no_smuggling':'can pass but incomplete','status':'fails residual lower-frame'},
    {'candidate':'single dual mollifier','upstream_visible':'yes','covers_residual_sector':'rank-one only','tail_record':'not enough','no_smuggling':'passes but scalar-only','status':'support evidence, not source frame'},
    {'candidate':'target-selected residual eigenvectors','upstream_visible':'no','covers_residual_sector':'yes by construction','tail_record':'irrelevant','no_smuggling':'fails','status':'rejected as smuggled'},
    {'candidate':'Burnol/co-Poisson atom visibility plus character frame','upstream_visible':'yes','covers_residual_sector':'conditional on c_N^R','tail_record':'required','no_smuggling':'passes if atom family declared before zeros/probes','status':'primary active route'}
])
candidates.to_csv(OUT/'xi_bc_source_candidate_gate_step116.csv', index=False)

# plots
plt.figure(figsize=(7,4.5))
plt.plot(full_df['Lambda'], full_df['residual_allowance_norm'], label='full residual frame')
plt.plot(partial_df['Lambda'], partial_df['residual_allowance_norm'], label='partial frame')
plt.xlabel('source lower-frame strength $\\Lambda_n$')
plt.ylabel('residual allowance norm')
plt.title('Residual-specific source absorption')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'xi_bc_residual_absorption_step116.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(vis_df['N'], vis_df['c_native_declared'], label='declared Burnol-native')
plt.plot(vis_df['N'], vis_df['c_bad_dictionary'], label='bad dictionary')
plt.plot(vis_df['N'], vis_df['c_target_selected_flagged'], label='target-selected flagged')
plt.xlabel('dictionary/source window size $N$')
plt.ylabel('residual visibility $c_N^R$')
plt.title('Residual-sector coefficient visibility scenarios')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'xi_bc_visibility_scenarios_step116.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(vis_df['N'], vis_df['Lambda_native'], label='native $\\gamma_N c_N^R$')
plt.plot(vis_df['N'], vis_df['Lambda_bad'], label='bad dictionary')
plt.plot(vis_df['N'], vis_df['Lambda_target_selected_flagged'], label='target-selected flagged')
plt.xlabel('window size $N$')
plt.ylabel('effective source strength')
plt.title('Effective residual source strength')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'xi_bc_effective_source_strength_step116.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(checks_df['trial'], checks_df['min_certified_slack_eig'])
plt.xlabel('random theorem check')
plt.ylabel('minimum certified slack eigenvalue')
plt.title('Finite matrix lower-frame theorem checks')
plt.tight_layout()
plt.savefig(OUT/'matrix_lower_frame_checks_step116.png', dpi=180)
plt.close()

print('created step 116 data and plots in', OUT)
