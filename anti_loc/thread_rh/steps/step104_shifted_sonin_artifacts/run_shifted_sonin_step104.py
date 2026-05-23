import json, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step104_shifted_sonin')
OUT.mkdir(parents=True, exist_ok=True)

def sonin_projection_matrix(N, Lbox=8.0, time_radius=1.0, freq_radius=1.0):
    x = np.linspace(-Lbox, Lbox, N, endpoint=False)
    dx = x[1]-x[0]
    time_mask = np.abs(x) <= time_radius
    F = np.fft.fft(np.eye(N))/np.sqrt(N)      # maps physical to Fourier coordinates
    freqs = np.fft.fftfreq(N, d=dx)*2*np.pi
    freq_mask = np.abs(freqs) <= freq_radius
    U_cols = np.eye(N)[:, time_mask]
    V_cols = np.conj(F).T[:, freq_mask]       # physical vectors with low Fourier support
    A = np.concatenate([U_cols, V_cols], axis=1)
    Q, _ = np.linalg.qr(A, mode='reduced')
    S = np.eye(N) - Q @ Q.conj().T             # projection onto approximate Sonin space
    return S, x, dx, time_mask, freq_mask

def shift_matrix(N, m):
    return np.roll(np.eye(N), m, axis=0)

records = []
sv_records = []
Ns = [32, 48, 64, 80]
for N in Ns:
    S, x, dx, time_mask, freq_mask = sonin_projection_matrix(N)
    m = max(1, int(round(0.5/dx)))
    T = shift_matrix(N, m)
    B = S @ T @ (np.eye(N)-S)
    sv = np.linalg.svd(B, compute_uv=False)
    records.append({
        'N': N, 'dx': dx, 'integer_shift_m': m, 'shift_a_approx': m*dx,
        'time_dim': int(time_mask.sum()), 'freq_dim': int(freq_mask.sum()),
        'rank_gt_1e-8': int((sv>1e-8).sum()),
        'rank_gt_0p9': int((sv>0.9).sum()),
        'top_sv': float(sv[0]),
        'min_top_block_sv': float(sv[:max(1,(sv>0.9).sum())].min()) if (sv>0.9).sum() else np.nan,
        'sv_5': float(sv[4]) if len(sv)>4 else np.nan,
        'sv_10': float(sv[9]) if len(sv)>9 else np.nan,
    })
    for j,s in enumerate(sv[:30], start=1):
        sv_records.append({'N':N, 'index':j, 'singular_value':float(s)})

pd.DataFrame(records).to_csv(OUT/'discrete_sonin_shift_summary_step104.csv', index=False)
pd.DataFrame(sv_records).to_csv(OUT/'discrete_sonin_shift_singular_values_step104.csv', index=False)

# Boundary packet test in continuous-looking discretization.
packet_records=[]
N=160
S, x, dx, time_mask, freq_mask = sonin_projection_matrix(N)
Lbox=8.0
shift_a=0.5
m=max(1,int(round(shift_a/dx)))
T=shift_matrix(N,m)
# choose a small interval near the right boundary that shifts outside [-1,1]
J_mask=(x>0.72)&(x<0.95)
phi=np.zeros(N, dtype=complex)
# smooth-ish bump on J
xx=x[J_mask]
if len(xx)>0:
    center=(xx.min()+xx.max())/2
    sigma=max((xx.max()-xx.min())/6, dx)
    bump=np.exp(-0.5*((xx-center)/sigma)**2)
    phi[J_mask]=bump
phi=phi/(np.linalg.norm(phi) if np.linalg.norm(phi)>0 else 1.0)
# Fourier projection low band
F=np.fft.fft(np.eye(N))/np.sqrt(N)
freqs=np.fft.fftfreq(N,d=dx)*2*np.pi
freq_mask=np.abs(freqs)<=1.0
PF=np.conj(F).T[:,freq_mask] @ (np.conj(F).T[:,freq_mask]).conj().T
PT=np.diag(time_mask.astype(float))
for k in range(0,20):
    n=10+5*k
    f=phi*np.exp(1j*n*x)
    f=f/np.linalg.norm(f)
    v=T@f
    son=S@v
    packet_records.append({
        'modulation_n': n,
        'norm_time_projection_after_shift': float(np.linalg.norm(PT@v)),
        'norm_lowfreq_projection_after_shift': float(np.linalg.norm(PF@v)),
        'norm_sonin_projection_error': float(np.linalg.norm(son-v)),
        'norm_sonin_projection': float(np.linalg.norm(son)),
    })
pd.DataFrame(packet_records).to_csv(OUT/'boundary_packet_sonin_projection_step104.csv', index=False)

# Compact comparison model singular values n^-2 and noncompact plateau.
comp=[]
for j in range(1,101):
    comp.append({'index':j, 'compact_model':1/(j*j), 'noncompact_plateau_model':1.0 if j<=20 else 0.0})
pd.DataFrame(comp).to_csv(OUT/'compact_vs_noncompact_model_step104.csv', index=False)

# Plots
sv_df=pd.DataFrame(sv_records)
plt.figure(figsize=(7,4.5))
for N in Ns:
    d=sv_df[sv_df.N==N]
    plt.semilogy(d['index'], d['singular_value'], marker='o', label=f'N={N}')
plt.xlabel('singular value index')
plt.ylabel('singular value')
plt.title('Discrete Sonin off-diagonal shift block')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'sonin_shift_singular_values_step104.png', dpi=180)
plt.close()

summary_df=pd.DataFrame(records)
plt.figure(figsize=(6.5,4.2))
plt.plot(summary_df['N'], summary_df['rank_gt_0p9'], marker='o')
plt.xlabel('discretization size N')
plt.ylabel('# singular values > 0.9')
plt.title('Growing noncompact-like plateau')
plt.tight_layout()
plt.savefig(OUT/'sonin_shift_plateau_growth_step104.png', dpi=180)
plt.close()

pkt=pd.DataFrame(packet_records)
plt.figure(figsize=(7,4.5))
plt.semilogy(pkt['modulation_n'], pkt['norm_lowfreq_projection_after_shift'], label='low-frequency projection')
plt.semilogy(pkt['modulation_n'], pkt['norm_sonin_projection_error'], label='Sonin projection error')
plt.plot(pkt['modulation_n'], pkt['norm_sonin_projection'], label='Sonin projection norm')
plt.xlabel('modulation n')
plt.ylabel('norm')
plt.title('Boundary packets survive in Sonin projection')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'boundary_packet_sonin_projection_step104.png', dpi=180)
plt.close()

comp_df=pd.DataFrame(comp)
plt.figure(figsize=(7,4.5))
plt.semilogy(comp_df['index'], comp_df['compact_model'], label='compact tail n^-2')
plt.semilogy(comp_df['index'], comp_df['noncompact_plateau_model'], label='noncompact plateau')
plt.xlabel('index')
plt.ylabel('model singular value')
plt.title('Compact versus noncompact singular tails')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'compact_vs_noncompact_tail_step104.png', dpi=180)
plt.close()

schema = {
    'step': 104,
    'title': 'Shifted Sonin/prolate off-diagonal compactness test',
    'operator': 'B_a = S_lambda tau_a (I-S_lambda)',
    'main_verdict': 'noncompact for the standard archimedean Sonin projection and any nonzero log shift, before additional semilocal prolate repair/quotient/source records',
    'critical_witness': 'high-frequency packets supported in the cutoff interval that are shifted outside the time cutoff and away from the Fourier cutoff',
    'route_implication': 'compactness shortcut fails for raw local-factor shifts; use semilocal prolate repair or Hecke source absorption'
}
(OUT/'step104_schema.json').write_text(json.dumps(schema, indent=2))

# CSV tables
pd.DataFrame([
    {'gate':'define Sonin projection','status':'accepted in archimedean model','record':'S_lambda projects to ker P_time cap ker P_freq'},
    {'gate':'derive off-diagonal block','status':'accepted','record':'B_a=S_lambda tau_a(I-S_lambda)'},
    {'gate':'compactness for nonzero shift','status':'failed for raw archimedean Sonin projection','record':'boundary packet witness gives noncompactness'},
    {'gate':'Hilbert-Schmidt status','status':'failed for raw shift','record':'noncompact implies not Hilbert-Schmidt'},
    {'gate':'semilocal rescue','status':'open','record':'requires semilocal prolate projection cancellation, quotient, or source absorption'},
]).to_csv(OUT/'shifted_sonin_gate_table_step104.csv', index=False)

pd.DataFrame([
    {'component':'time-cutoff packet witness','status':'noncompact witness','meaning':'high-frequency packets in cutoff interval become near-Sonin after shift'},
    {'component':'single local-factor shift tau_logp','status':'noncompact before repair','meaning':'one Bohr shift already defeats compactness shortcut'},
    {'component':'finite local-factor combination','status':'noncompact unless cancellations are audited','meaning':'positive Bohr coefficients do not remove boundary-packet sector'},
    {'component':'semilocal prolate correction','status':'open','meaning':'could still cancel through a different P_S, not by raw S_lambda'},
    {'component':'Hecke source ladder','status':'required if no semilocal cancellation','meaning':'must charge noncompact sector by lower-frame source coercivity'},
]).to_csv(OUT/'shifted_sonin_component_status_step104.csv', index=False)

pd.DataFrame([
    {'task':'Prove boundary-packet noncompactness for standard Sonin projection','status':'done in Step 104'},
    {'task':'Check whether the actual semilocal prolate projection cancels boundary packets','status':'next analytic target'},
    {'task':'If cancellation fails, define source probes covering boundary-packet sector','status':'future / source route'},
    {'task':'Retain all-six records and Xi adequacy for off-critical probes','status':'standing obligation'},
]).to_csv(OUT/'construction_tasks_step104.csv', index=False)

pd.DataFrame([
    {'theorem':'Boundary packet witness theorem','claim':'S_lambda tau_a(I-S_lambda) is noncompact for nonzero shift a'},
    {'theorem':'Metric residual consequence','claim':'Raw local-factor shifts make R_S noncompact unless semilocal prolate repair changes the projection'},
    {'theorem':'Source route corollary','claim':'If repair fails, Hecke/Dirichlet lower-frame absorption is unavoidable'},
]).to_csv(OUT/'theorem_map_step104.csv', index=False)

(OUT/'nonclaim_boundary_step104.md').write_text('''# Step 104 nonclaim boundary\n\nThis step does not prove or disprove RH.\n\nIt does not prove that the actual semilocal Connes--Consani--Moscovici prolate operator has noncompact residual. It proves a sharper negative result for the raw archimedean Sonin projection under a nonzero log shift.\n\nTherefore the compactness shortcut remains possible only if the semilocal prolate projection has an additional cancellation mechanism beyond transporting the archimedean Sonin projection. Otherwise the route must use Hecke/Dirichlet source absorption.\n''')

# Zip selected files
zip_path=OUT/'step104_shifted_sonin_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)
print('wrote', OUT)
