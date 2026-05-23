import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT=Path('/mnt/data/anti_localization_step59_xi_repair')
OUT.mkdir(exist_ok=True)
rng=np.random.default_rng(59)

def psd_sqrt_inv(C, tol=1e-10):
    w,V=np.linalg.eigh((C+C.T)/2)
    pos=w>tol
    invsqrt=np.zeros_like(C)
    sqrt=np.zeros_like(C)
    pinv=np.zeros_like(C)
    if np.any(pos):
        invsqrt=V[:,pos]@np.diag(1/np.sqrt(w[pos]))@V[:,pos].T
        sqrt=V[:,pos]@np.diag(np.sqrt(w[pos]))@V[:,pos].T
        pinv=V[:,pos]@np.diag(1/w[pos])@V[:,pos].T
    return sqrt,invsqrt,pinv,pos

def rand_spd(n, gap=0.5):
    A=rng.normal(size=(n,n))
    return A.T@A + gap*np.eye(n)

def xi(C,L,D,tol=1e-10):
    Csqrt,Cinvsqrt,Cpinv,_=psd_sqrt_inv(C,tol)
    TL=L@Cinvsqrt
    TD=D@Cinvsqrt
    # projection onto row span of TL = Ran(TL.T)
    # P = TL.T (TL TL.T)^dag TL
    P=TL.T@np.linalg.pinv(TL@TL.T, rcond=tol)@TL
    Xi=TD@(np.eye(C.shape[0])-P)@TD.T
    # block formula
    KLL=L@Cpinv@L.T
    KDL=D@Cpinv@L.T
    KDD=D@Cpinv@D.T
    Xi2=KDD-KDL@np.linalg.pinv(KLL, rcond=tol)@KDL.T
    return (Xi+Xi.T)/2, (Xi2+Xi2.T)/2

def maxeig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2)[-1])

def mineig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2)[0])

# Random identity/native extension checks
rows=[]
for i in range(80):
    n=rng.integers(4,9); p=rng.integers(1, min(4,n)); q=rng.integers(1,min(4,n)); r=rng.integers(1,min(4,n))
    C=rand_spd(n, gap=0.2)
    L=rng.normal(size=(p,n)); D=rng.normal(size=(q,n)); M=rng.normal(size=(r,n))
    Xi1,Xi1b=xi(C,L,D)
    Xi_plus,_=xi(C,np.vstack([L,M]),D)
    # conditional subtraction via direct difference PSD
    decrease=Xi1-Xi_plus
    rows.append({
        'trial':i,'n':n,'p_native':p,'q_dissolving':q,'r_new':r,
        'projection_block_error':float(np.linalg.norm(Xi1-Xi1b,2)),
        'min_eig_decrease':mineig(decrease),
        'max_eig_xi_before':maxeig(Xi1),
        'max_eig_xi_after':maxeig(Xi_plus),
    })
pd.DataFrame(rows).to_csv(OUT/'xi_repair_random_identity_checks_step59.csv', index=False)

# Same family saturation
rows=[]
for i in range(40):
    n=6; p=3; q=2
    C=rand_spd(n)
    L=rng.normal(size=(p,n)); D=rng.normal(size=(q,n))
    B=rng.normal(size=(2,p))
    M=B@L
    Xi1,_=xi(C,L,D)
    Xi_plus,_=xi(C,np.vstack([L,M]),D)
    rows.append({'trial':i,'same_family_error':float(np.linalg.norm(Xi_plus-Xi1,2))})
pd.DataFrame(rows).to_csv(OUT/'same_family_saturation_step59.csv', index=False)

# Obstruction witness example: Xi budget violated, witness top eigenvector
rows=[]
for Mval in [1,2,5,10,50,100,1e3,1e4]:
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D=np.array([[0.0,Mval]])
    Xi1,_=xi(C,L,D)
    Omega=np.array([[1.0]])
    Delta=Xi1-Omega
    rows.append({'M':Mval,'xi':Xi1[0,0],'budget':1.0,'violation':Delta[0,0], 'witness_z':1.0})
pd.DataFrame(rows).to_csv(OUT/'xi_obstruction_witness_sweep_step59.csv', index=False)

# Public shadow overread: F forgets hidden Z coordinate
rows=[]
for Mval in np.logspace(0,5,30):
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D=np.array([[1.0,0.0],[0.0,Mval]])
    Xi_full,_=xi(C,L,D)
    F=np.array([[1.0,0.0]])
    Xi_pub=F@Xi_full@F.T
    rows.append({'M':Mval,'xi_intrinsic_maxeig':maxeig(Xi_full),'xi_public':Xi_pub[0,0]})
pd.DataFrame(rows).to_csv(OUT/'public_shadow_kernel_overread_step59.csv', index=False)

# Predictive repair: summable vs non-summable residuals
rows=[]
Xi_s=1.0; Xi_n=1.0
for j in range(1,201):
    # strict contraction with summable residual
    alpha=0.08
    E_s=1/(j+1)**2
    Xi_s=(1-alpha)*Xi_s+E_s
    # non-summable residual/harmonic input
    E_n=1/(j+1)
    Xi_n=Xi_n+E_n
    rows.append({'j':j,'summable_contracting_xi':Xi_s,'nonsummable_xi':Xi_n,'summable_residual':E_s,'nonsummable_residual':E_n})
pd.DataFrame(rows).to_csv(OUT/'predictive_repair_ladder_step59.csv', index=False)

# Defective bridge bound numerical checks: Xi' <= (1+t)B Xi B^T + (1+1/t)Xi_R
rows=[]
for i in range(50):
    n=6;p=3;q=2;r=2
    C=rand_spd(n)
    L=rng.normal(size=(p,n)); D=rng.normal(size=(q,n)); R=rng.normal(size=(q,n))*0.15
    Bmat=rng.normal(size=(q,q))
    Dp=Bmat@D+R
    XiD,_=xi(C,L,D)
    XiR,_=xi(C,L,R)
    XiP,_=xi(C,L,Dp)
    t=1.0
    Bound=(1+t)*Bmat@XiD@Bmat.T+(1+1/t)*XiR
    rows.append({'trial':i,'min_eig_bound_minus_actual':mineig(Bound-XiP),'actual_maxeig':maxeig(XiP),'bound_maxeig':maxeig(Bound)})
pd.DataFrame(rows).to_csv(OUT/'defective_bridge_xi_bound_step59.csv', index=False)

# Generate plots
plt.figure()
df=pd.read_csv(OUT/'xi_obstruction_witness_sweep_step59.csv')
plt.loglog(df['M'], df['xi'])
plt.xlabel('hidden blind-spot scale M')
plt.ylabel('Xi(D | L)')
plt.title('Xi obstruction witness grows as hidden blind spot grows')
plt.tight_layout()
plt.savefig(OUT/'xi_obstruction_witness_step59.png', dpi=160)
plt.close()

plt.figure()
df=pd.read_csv(OUT/'public_shadow_kernel_overread_step59.csv')
plt.loglog(df['M'], df['xi_intrinsic_maxeig'], label='intrinsic Xi')
plt.loglog(df['M'], df['xi_public']+1e-18, label='public shadow Xi')
plt.xlabel('hidden scale M')
plt.ylabel('blind-spot currency')
plt.title('Public shadow can hide intrinsic Xi')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'public_shadow_kernel_overread_step59.png', dpi=160)
plt.close()

plt.figure()
df=pd.read_csv(OUT/'predictive_repair_ladder_step59.csv')
plt.plot(df['j'], df['summable_contracting_xi'], label='contracting + summable residual')
plt.plot(df['j'], df['nonsummable_xi'], label='non-summable residual')
plt.xlabel('stage')
plt.ylabel('Xi budget')
plt.title('Predictive Xi repair: summable vs non-summable')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'predictive_xi_repair_ladder_step59.png', dpi=160)
plt.close()

print('done')
