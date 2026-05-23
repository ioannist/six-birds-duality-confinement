import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

out=Path('/mnt/data/rh_membrane_step85_lowfreq_gate')
out.mkdir(exist_ok=True)

# Model CND symbol: prime-like finite shifts + gamma-like integral approximation near zero.
xi=np.linspace(1e-5,5,2000)
# Simple paired symbol with quadratic zero: Psi = xi^2/(1+xi^2) + 0.2*(1-cos(2xi))
Psi = xi**2/(1+xi**2) + 0.2*(1-np.cos(2*xi))
# small-x asymptotics coefficient roughly 1 + 0.4 = 1.4 times xi^2
ratio=Psi/xi**2
pd.DataFrame({'xi':xi,'Psi':Psi,'Psi_over_xi2':ratio}).to_csv(out/'paired_symbol_lowfreq_step85.csv',index=False)

plt.figure(figsize=(6,4))
plt.loglog(xi,Psi,label=r'$\Psi(\xi)$')
plt.loglog(xi,1.4*xi**2,'--',label=r'$1.4\xi^2$')
plt.xlabel(r'$\xi$')
plt.ylabel('symbol')
plt.title('Paired CND symbol has quadratic zero')
plt.legend()
plt.tight_layout()
plt.savefig(out/'paired_symbol_lowfreq_step85.png',dpi=160)
plt.close()

# Anti-invariant low-frequency wave packets: odd pair of gaussians centered at +/-eps in frequency.
# Energy quotient approximated by average Psi over packets.
eps_vals=np.logspace(-3,-0.3,60)
sigma_factor=0.2
rows=[]
for eps in eps_vals:
    sig=sigma_factor*eps
    grid=np.linspace(-4*eps,4*eps,4001)
    # odd/anti-invariant frequency packet: Gaussian near eps minus Gaussian near -eps, imaginary odd up to phase
    amp=np.exp(-0.5*((grid-eps)/sig)**2)-np.exp(-0.5*((grid+eps)/sig)**2)
    norm=np.trapz(np.abs(amp)**2,grid)
    # symbol model even
    psi_grid=grid**2/(1+grid**2)+0.2*(1-np.cos(2*grid))
    energy=np.trapz(psi_grid*np.abs(amp)**2,grid)/norm
    rows.append({'epsilon_center':eps,'packet_width':sig,'normalized_energy':energy})
pd.DataFrame(rows).to_csv(out/'anti_invariant_lowfreq_packets_step85.csv',index=False)
plt.figure(figsize=(6,4))
plt.loglog([r['epsilon_center'] for r in rows],[r['normalized_energy'] for r in rows],label='anti-invariant packet energy')
plt.loglog(eps_vals,1.4*eps_vals**2,'--',label=r'$\sim \epsilon^2$')
plt.xlabel('low-frequency center epsilon')
plt.ylabel('normalized carrier energy')
plt.title('Anti-invariance does not create a spectral gap')
plt.legend()
plt.tight_layout()
plt.savefig(out/'anti_invariant_no_gap_step85.png',dpi=160)
plt.close()

# Capacity integrals for ghat ~ |xi|^s and Psi~xi^2 near zero.
cutoffs=np.logspace(-6,-1,50)
orders=[0.0,0.25,0.5,0.75,1.0,1.5]
rows=[]
for s in orders:
    for delta in cutoffs:
        # integral from delta to 1 of xi^(2s)/xi^2 dxi = int xi^(2s-2)
        p=2*s-2
        if abs(p+1)<1e-12:
            val=np.log(1/delta)
        else:
            val=(1-delta**(p+1))/(p+1)
        rows.append({'s':s,'cutoff_delta':delta,'truncated_capacity':val})
pd.DataFrame(rows).to_csv(out/'lowfreq_cancellation_capacity_step85.csv',index=False)
plt.figure(figsize=(6,4))
for s in orders:
    sub=[r for r in rows if r['s']==s]
    plt.loglog([r['cutoff_delta'] for r in sub],[r['truncated_capacity'] for r in sub],label=f's={s}')
plt.gca().invert_xaxis()
plt.xlabel('low-frequency cutoff delta')
plt.ylabel(r'$\int_\delta^1 \xi^{2s-2}d\xi$')
plt.title('Capacity divergence unless cancellation order s>1/2')
plt.legend()
plt.tight_layout()
plt.savefig(out/'lowfreq_cancellation_capacity_step85.png',dpi=160)
plt.close()

# Gap after quotient |xi|>=delta.
deltas=np.logspace(-4,0,80)
gaps=[]
for d in deltas:
    xs=np.linspace(d,5,10000)
    ps=xs**2/(1+xs**2)+0.2*(1-np.cos(2*xs))
    gaps.append({'delta_gap_cutoff':d,'lower_frame_min_symbol':ps.min()})
pd.DataFrame(gaps).to_csv(out/'quotient_gap_step85.csv',index=False)
plt.figure(figsize=(6,4))
plt.loglog(deltas,[g['lower_frame_min_symbol'] for g in gaps])
plt.xlabel(r'quotient cutoff $|\xi|\geq\delta$')
plt.ylabel('lower frame / min symbol')
plt.title('Gap exists only after low-frequency quotient')
plt.tight_layout()
plt.savefig(out/'quotient_gap_step85.png',dpi=160)
plt.close()

print('created Step 85 artifacts in', out)
