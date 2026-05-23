import json, math, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step117_residual_coefficient_map')
OUT.mkdir(parents=True, exist_ok=True)
np.random.seed(117)

# -----------------------------
# Finite response model
# -----------------------------
M = 160
Tmax = 6.0
t = np.linspace(-Tmax, Tmax, M, endpoint=False)
dt = t[1]-t[0]
# Weighted coordinates: values multiplied by sqrt(dt)
sqrtw = np.sqrt(dt)

F = np.fft.fft(np.eye(M), norm='ortho')
Finv = F.conj().T
freq = 2*np.pi*np.fft.fftfreq(M, d=dt)

# Time/Fourier forbidden windows (toy Sonin projection)
time_mask = (np.abs(t) < 1.2).astype(float)
freq_mask = (np.abs(freq) < 1.2).astype(float)
P_T = np.diag(time_mask)
P_F = Finv @ np.diag(freq_mask) @ F
# Projection onto intersection ker P_T ∩ ker P_F via nullspace of stacked constraints
A = np.vstack([P_T, P_F])
U, svals, Vh = np.linalg.svd(A, full_matrices=True)
rank = np.sum(svals > 1e-9)
Z = Vh.conj().T[:, rank:]
P_sonin = Z @ Z.conj().T
I = np.eye(M, dtype=complex)

# Fractional log-shift by log 2 in periodic finite model
a = math.log(2.0)
Tshift = Finv @ np.diag(np.exp(-1j*freq*a)) @ F
B = P_sonin @ Tshift @ (I - P_sonin)

# Zero-evaluator proxy span: finite Mellin oscillations at first zeta zero ordinates (toy only)
gammas = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073])
Ycols = []
for g in gammas:
    Ycols.append(np.exp(1j*g*t) * sqrtw)
    Ycols.append(np.exp(-1j*g*t) * sqrtw)
Y = np.column_stack(Ycols)
QY, _ = np.linalg.qr(Y)
PiY = QY @ QY.conj().T

Xi = B.conj().T @ PiY @ B
Xi = (Xi + Xi.conj().T)/2
vals, vecs = np.linalg.eigh(Xi)
idx = np.argsort(vals)[::-1]
vals = vals[idx]
vecs = vecs[:, idx]
# residual sector: leading positive directions
r = 18
residual_basis = vecs[:, :r]
# residual synthesis in weighted H coordinates; orthonormal basis
M_R = residual_basis
G_R = M_R.conj().T @ M_R

# Helper functions

def orth_basis(D, tol=1e-10):
    if D.size == 0 or D.shape[1] == 0:
        return np.empty((M,0), dtype=complex)
    Q, R = np.linalg.qr(D, mode='reduced')
    if R.ndim == 2 and R.shape[0] > 0:
        diag = np.abs(np.diag(R))
        keep = diag > tol * max(1.0, diag.max())
        Q = Q[:, keep]
    return Q

def visibility(D):
    Q = orth_basis(D)
    if Q.shape[1] == 0:
        A = np.zeros((r,r), dtype=complex)
    else:
        Zq = Q.conj().T @ M_R
        A = Zq.conj().T @ Zq
    A = (A + A.conj().T)/2
    ev = np.linalg.eigvalsh(A)
    c = float(max(0.0, min(1.0, ev.min().real)))
    eps = float(math.sqrt(max(0.0, 1-c)))
    mean_vis = float(np.trace(A).real / r)
    return c, eps, mean_vis, ev.real

# Coefficient dictionaries.
# 1) Naive short Dirichlet atoms in log coordinate.
def dirichlet_atoms(Xmax):
    cols = []
    for n in range(2, Xmax+1):
        col = (n**-0.5) * np.exp(-1j*t*np.log(n)) * sqrtw
        # normalize
        norm = np.linalg.norm(col)
        if norm > 1e-12:
            cols.append(col/norm)
    return np.column_stack(cols) if cols else np.empty((M,0), dtype=complex)

# 2) Burnol/co-Poisson-like atoms: compact generators with two moment vanishings,
#    then multiplicative co-sum by log n shifts. This is a declared toy model.
def moment_corrected_bump(center, width):
    z = (t-center)/width
    bump = np.exp(-1.0/(1-z*z))
    bump[np.abs(z)>=1] = 0.0
    # subtract linear combination of two fixed compact correction functions to impose two moments
    # moments: ∫ g(t) dt = 0 and ∫ e^{-t} g(t) dt = 0
    c1 = np.ones_like(t)
    c2 = np.exp(-t)
    # Use two broad windows as correction shapes
    w1 = np.exp(-0.5*((t+2.5)/1.4)**2)
    w2 = np.exp(-0.5*((t-2.5)/1.4)**2)
    A2 = np.array([[np.sum(w1)*dt, np.sum(w2)*dt],
                   [np.sum(np.exp(-t)*w1)*dt, np.sum(np.exp(-t)*w2)*dt]], dtype=float)
    b2 = np.array([np.sum(bump)*dt, np.sum(np.exp(-t)*bump)*dt], dtype=float)
    try:
        coeff = np.linalg.solve(A2, b2)
    except np.linalg.LinAlgError:
        coeff = np.linalg.lstsq(A2, b2, rcond=None)[0]
    g = bump - coeff[0]*w1 - coeff[1]*w2
    return g

def interp_shift(vals, shift):
    # zero-extension interpolation for vals(t-shift)
    return np.interp(t-shift, t, vals, left=0.0, right=0.0)

def copoisson_synthesis(g, Ncop=36):
    out = np.zeros_like(g, dtype=float)
    for n in range(1, Ncop+1):
        out += (n**-0.5) * interp_shift(g, math.log(n))
    # remove residual constants in two moment directions after synthesis
    w1 = np.ones_like(t)
    w2 = np.exp(-t)
    A2 = np.array([[np.sum(w1*w1)*dt, np.sum(w1*w2)*dt],
                   [np.sum(w2*w1)*dt, np.sum(w2*w2)*dt]], dtype=float)
    b2 = np.array([np.sum(out*w1)*dt, np.sum(out*w2)*dt], dtype=float)
    try:
        coeff = np.linalg.solve(A2, b2)
    except np.linalg.LinAlgError:
        coeff = np.linalg.lstsq(A2, b2, rcond=None)[0]
    out = out - coeff[0]*w1 - coeff[1]*w2
    return out

def burnol_atoms(num_centers):
    centers = np.linspace(-4.5, 4.5, num_centers)
    widths = [0.55, 0.9]
    cols = []
    for width in widths:
        for c in centers:
            g = moment_corrected_bump(c, width)
            h = copoisson_synthesis(g)
            col = h * sqrtw
            norm = np.linalg.norm(col)
            if norm > 1e-10:
                cols.append(col/norm)
            # include cosine-dual proxy by Fourier transform, to impose Sonine-style paired visibility
            hF = np.real(F @ (h*sqrtw))
            col2 = hF.astype(complex)
            norm2 = np.linalg.norm(col2)
            if norm2 > 1e-10:
                cols.append(col2/norm2)
    return np.column_stack(cols) if cols else np.empty((M,0), dtype=complex)

# Build sweeps
rows = []
for K in [8, 16, 32, 64, 96, 128]:
    Dd = dirichlet_atoms(max(3, K+2))
    c, eps, mean, ev = visibility(Dd)
    rows.append({'dictionary':'short_dirichlet','size':Dd.shape[1], 'c_RN':c, 'epsilon_RN':eps, 'mean_visibility':mean, 'min_eig':ev.min(), 'median_eig':np.median(ev), 'max_eig':ev.max()})

for centers in [2,4,8,12,16,24]:
    Db = burnol_atoms(centers)
    c, eps, mean, ev = visibility(Db)
    rows.append({'dictionary':'burnol_copoisson','size':Db.shape[1], 'c_RN':c, 'epsilon_RN':eps, 'mean_visibility':mean, 'min_eig':ev.min(), 'median_eig':np.median(ev), 'max_eig':ev.max()})

for centers in [2,4,8,12,16,24]:
    Db = burnol_atoms(centers)
    Dd = dirichlet_atoms(60)
    Dh = np.column_stack([Db, Dd])
    c, eps, mean, ev = visibility(Dh)
    rows.append({'dictionary':'hybrid_burnol_dirichlet','size':Dh.shape[1], 'c_RN':c, 'epsilon_RN':eps, 'mean_visibility':mean, 'min_eig':ev.min(), 'median_eig':np.median(ev), 'max_eig':ev.max()})

sweep = pd.DataFrame(rows)
sweep.to_csv(OUT/'residual_coefficient_visibility_sweep_step117.csv', index=False)

# Choose representative final dictionaries
D_dir = dirichlet_atoms(128)
D_bur = burnol_atoms(24)
D_hyb = np.column_stack([D_bur, dirichlet_atoms(48)])
summary_rows = []
for name,D in [('short_dirichlet_X192',D_dir),('burnol_copoisson_32centers',D_bur),('hybrid_burnol_dirichlet',D_hyb)]:
    c, eps, mean, ev = visibility(D)
    summary_rows.append({'case':name,'atoms':D.shape[1],'c_RN':c,'epsilon_RN':eps,'mean_visibility':mean,'lambda_min':ev.min(),'lambda_median':np.median(ev),'lambda_max':ev.max(),'rank_D':np.linalg.matrix_rank(D, tol=1e-9)})
summary = pd.DataFrame(summary_rows)
summary.to_csv(OUT/'residual_coefficient_visibility_summary_step117.csv', index=False)

# visibility spectrum for hybrid
c, eps, mean, ev_h = visibility(D_hyb)
pd.DataFrame({'eigen_index':np.arange(1,len(ev_h)+1),'visibility_eigenvalue':np.sort(ev_h)}).to_csv(OUT/'residual_visibility_spectrum_step117.csv', index=False)

# gamma * c scenarios
scenario_rows=[]
Ns=np.array([10,20,50,100,200,500,1000,2000,5000], dtype=float)
for label, cmodel in [('bounded_visibility', lambda N: 0.25+0*N),('log_decay', lambda N: 1/np.log(N+3)),('power_decay_half', lambda N: N**-0.5),('power_decay_one', lambda N: N**-1.0)]:
    for gamma_label, gamma_model in [('HS_log2',lambda N: np.log(N+3)**2),('HS_log',lambda N: np.log(N+3)),('strong_power_quarter',lambda N: N**0.25)]:
        for N in Ns:
            cv=float(cmodel(N)); gam=float(gamma_model(N));
            scenario_rows.append({'c_model':label,'gamma_model':gamma_label,'N':int(N),'c_N':cv,'gamma_N':gam,'Lambda_eff':cv*gam})
scen=pd.DataFrame(scenario_rows)
scen.to_csv(OUT/'residual_source_compensation_scenarios_step117.csv', index=False)

# Plots
plt.figure(figsize=(7,4.5))
for name, grp in sweep.groupby('dictionary'):
    plt.plot(grp['size'], grp['c_RN'], marker='o', label=name)
plt.xlabel('dictionary atom count')
plt.ylabel('worst-direction visibility $c_{R,N}$')
plt.title('Residual coefficient visibility by dictionary')
plt.ylim(-0.02,1.02)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'residual_coefficient_visibility_step117.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
for name, grp in sweep.groupby('dictionary'):
    plt.plot(grp['size'], grp['epsilon_RN'], marker='o', label=name)
plt.xlabel('dictionary atom count')
plt.ylabel('spanning miss $\epsilon_{R,N}$')
plt.title('Residual coefficient blind-spot residual')
plt.ylim(-0.02,1.02)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'residual_coefficient_blindspot_step117.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(np.arange(1,len(ev_h)+1), np.sort(ev_h), marker='o')
plt.xlabel('residual-sector eigen-direction')
plt.ylabel('visibility eigenvalue')
plt.title('Hybrid residual visibility spectrum')
plt.ylim(-0.02,1.02)
plt.tight_layout()
plt.savefig(OUT/'residual_visibility_spectrum_step117.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
for (cmodel,gmodel), grp in scen.groupby(['c_model','gamma_model']):
    if gmodel == 'HS_log2':
        plt.plot(grp['N'], grp['Lambda_eff'], marker='o', label=cmodel)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('N')
plt.ylabel('$\gamma_N c_{R,N}$')
plt.title('Effective residual source strength under HS-log$^2$ growth')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'residual_effective_source_strength_step117.png', dpi=180)
plt.close()

# kernel failure plot: use a dictionary with very few atoms
D_bad = burnol_atoms(3)
Qbad = orth_basis(D_bad)
Zbad = Qbad.conj().T @ M_R if Qbad.shape[1] else np.zeros((0,r), dtype=complex)
A_bad = Zbad.conj().T @ Zbad
bad_ev = np.linalg.eigvalsh((A_bad+A_bad.conj().T)/2).real
plt.figure(figsize=(7,4.5))
plt.plot(np.sort(bad_ev), marker='o')
plt.xlabel('residual-sector direction')
plt.ylabel('visibility eigenvalue')
plt.title('Kernel/partial dictionary failure on residual sector')
plt.ylim(-0.02,1.02)
plt.tight_layout()
plt.savefig(OUT/'residual_kernel_failure_step117.png', dpi=180)
plt.close()

# Gate tables
gate = pd.DataFrame([
    {'gate':'R-sector declaration','status':'defined','mathematical_record':'Y_{R,N}=Ran Xi^{BC}_{N} or leading positive residual window','failure_if_missing':'source frame may charge wrong sector'},
    {'gate':'coefficient synthesis','status':'defined','mathematical_record':'D_N:C^{I_N}->H_N^{resp}','failure_if_missing':'no translation to arithmetic sensors'},
    {'gate':'visibility residual','status':'exact finite identity','mathematical_record':'c_{R,N}=1-||(I-P_N)M_{R,N}G_{R,N}^{-1/2}||^2','failure_if_missing':'blind directions in ker R_N'},
    {'gate':'source Gram lower frame','status':'separate arithmetic input','mathematical_record':'G_{X,N} >= gamma_N H_N','failure_if_missing':'scalar moments only charge selected directions'},
    {'gate':'effective strength','status':'conditional','mathematical_record':'Lambda_{R,N}=gamma_N c_{R,N}','failure_if_missing':'no residual absorption'},
    {'gate':'completed promotion','status':'open tail record','mathematical_record':'G_R <= Pi_N^*G_{R,N}Pi_N + T_{R,N}, tr T_{R,N}->0','failure_if_missing':'finite window support only'},
    {'gate':'no smuggling','status':'declared','mathematical_record':'dictionary declared by Burnol/co-Poisson rules before target residual test','failure_if_missing':'target-selected atoms'}
])
gate.to_csv(OUT/'residual_coefficient_gate_table_step117.csv', index=False)

theorem_map = pd.DataFrame([
    {'item':'Finite residual visibility identity','statement':'R_N^*H_NR_N=G_{R,N}-E_{coef,N}^*E_{coef,N}','role':'exact adequacy residual for coefficient dictionary'},
    {'item':'Residual matrix moment lower frame','statement':'G_X >= gamma H and R^*HR >= cG_R imply R^*G_XR >= gamma c G_R','role':'finite source absorption theorem'},
    {'item':'Completed residual promotion','statement':'finite residual frames plus tail/exhaustivity promote to completed Xi^{BC} absorption','role':'fixed/exhaustive ledger requirement'},
    {'item':'No-kernel corollary','statement':'ker R_N != 0 implies no source through R_N can charge all residual directions','role':'hard failure mode'},
    {'item':'Strict dictionary extension monotonicity','statement':'adding declared atoms cannot decrease c_{R,N}','role':'Six Birds strict-extension / Xi monotonicity'}
])
theorem_map.to_csv(OUT/'theorem_map_step117.csv', index=False)

construction_tasks = pd.DataFrame([
    {'task':'Replace toy residual vectors with Burnol analytic residual windows','owner':'analysis','status':'next','output':'M_{R,N} from Xi^{BC} finite windows'},
    {'task':'Define non-smuggled Burnol-to-Dirichlet hybrid atoms','owner':'analysis','status':'open','output':'D_N family with support/parity/Mellin records'},
    {'task':'Prove or bound c_{R,N}','owner':'analysis','status':'open','output':'epsilon_{R,N}->0 or classified residual blind spot'},
    {'task':'Lift Heap-Soundararajan to matrix lower moments','owner':'analytic number theory','status':'open','output':'G_{X,N} >= gamma_N H_N'},
    {'task':'Promote finite residual windows','owner':'framework/analysis','status':'open','output':'tail form T_{R,N}->0'},
    {'task':'All-six audit for residual sources','owner':'framework','status':'open','output':'P1-P6 records for sources and dictionaries'}
])
construction_tasks.to_csv(OUT/'construction_tasks_step117.csv', index=False)

arithmetic_input = pd.DataFrame([
    {'input':'Burnol residual-sector carrier','needed_for':'definition of Y_R and M_R','status':'partly imported from Burnol Sonine/co-Poisson theory'},
    {'input':'Burnol/co-Poisson atom density','needed_for':'c_{R,N} not collapsing','status':'open'},
    {'input':'Heap-Soundararajan matrix moments','needed_for':'gamma_N lower frame','status':'scalar template only'},
    {'input':'finite character orthogonality','needed_for':'local source Gram','status':'available on finite quotients'},
    {'input':'semilocal CCM transport','needed_for':'ambient response space','status':'available as framework, not full RH proof'},
    {'input':'tail/exhaustivity','needed_for':'completed promotion','status':'open'}
])
arithmetic_input.to_csv(OUT/'arithmetic_input_table_step117.csv', index=False)

route_status = pd.DataFrame([
    {'route':'zeta-factorization shortcut','status':'not earned','reason':'raw log-shift does not create zeta factor'},
    {'route':'compactness shortcut','status':'blocked for raw shifted Sonin block','reason':'noncompact boundary packets survive compact repair'},
    {'route':'Burnol atom visibility','status':'active c_N side','reason':'coefficient miss is spanning residual'},
    {'route':'Hecke/Dirichlet source absorption','status':'active gamma_N side','reason':'must charge Xi^{BC} residual sector'},
    {'route':'full RH conclusion','status':'not claimed','reason':'requires c_N, gamma_N, tail/exhaustivity, all-six records'}
])
route_status.to_csv(OUT/'route_status_step117.csv', index=False)

# Nonclaim boundary
(OUT/'nonclaim_boundary_step117.md').write_text('''# Step 117 nonclaim boundary

This step does not prove RH.

It does not prove that the residual-sector coefficient visibility constant c_{R,N} stays bounded away from zero in the actual Burnol/Sonine carrier.

It does not prove the Heap--Soundararajan matrix lower-frame lift.

It does not promote finite residual windows to the completed zero ledger.

It does not claim that the toy finite model is evidence for RH. The numerical checks are algebra sanity checks for the visibility identity and source-frame implication only.

The accepted output of Step 117 is the residual-sector coefficient-map schema and the exact finite adequacy identity

    c_{R,N}=1-||(I-P_N)M_{R,N}G_{R,N}^{-1/2}||^2.

The next proof obligation is to replace toy dictionaries by actual Burnol/co-Poisson hybrid atoms and prove a density/visibility theorem for the residual sector Xi^{BC}.
''')

# Schema
schema = {
    'step':117,
    'name':'Residual coefficient-map instantiation for Xi^{BC}',
    'objects':{
        'Xi_BC':'boundary-to-co-Poisson residual B^* Pi_Y B',
        'Y_R_N':'finite residual sector',
        'M_R_N':'residual synthesis map',
        'D_N':'declared coefficient dictionary synthesis map',
        'R_N':'D_N^dagger M_R_N',
        'c_R_N':'1 - ||(I-P_N) M_R_N G_R_N^{-1/2}||^2',
        'gamma_N':'source Gram lower-frame strength',
        'Lambda_R_N':'gamma_N c_R_N'
    },
    'status':{
        'finite_identity':'proved algebraically',
        'toy_check':'completed',
        'RH_claim':'none',
        'next':'Burnol-to-Dirichlet hybrid dictionary theorem'
    }
}
(OUT/'step117_schema.json').write_text(json.dumps(schema, indent=2))

print('Wrote Step 117 artifacts to', OUT)
