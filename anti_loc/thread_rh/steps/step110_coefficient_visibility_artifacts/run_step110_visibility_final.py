import json, math, zipfile
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
OUT=Path('/mnt/data/rh_membrane_step110_visibility_final'); OUT.mkdir(exist_ok=True)
np.random.seed(110)
M=256; T=40.0; t=np.linspace(-T,T,M,endpoint=False); dt=t[1]-t[0]
# Boundary-packet toy dictionary: localized oscillatory packets near four boundary locations.
centers=[-7.5,-5.5,5.5,7.5]; widths=[0.55,0.8]; freqs=[1.0,1.6,2.3,3.2,4.7,6.5]
cols=[]; meta=[]
for c in centers:
  for w in widths:
    for om in freqs:
      for sgn in [1,-1]:
        v=np.exp(-0.5*((t-c)/w)**2)*np.exp(1j*sgn*om*t)
        cols.append(np.sqrt(dt)*v)
        meta.append({'center':c,'width':w,'frequency':om,'sign':sgn})
Braw=np.column_stack(cols)
Qb,_=np.linalg.qr(Braw, mode='reduced')
# keep legal finite quotient dimensions
DIMS=[4,8,12,16,24,32,40]

def atoms_integers(X):
  ns=np.arange(2,X+1)
  A=(ns[None,:]**-0.5)*np.exp(-1j*np.outer(t,np.log(ns)))
  A=np.sqrt(dt)*A
  norms=np.linalg.norm(A,axis=0); norms[norms==0]=1
  return ns,A/norms

def atoms_log_uniform(K, maxlog=math.log(384)):
  freqs=np.linspace(0.1,maxlog,K)
  A=np.exp(-1j*np.outer(t,freqs))*np.sqrt(dt)
  norms=np.linalg.norm(A,axis=0); norms[norms==0]=1
  return freqs,A/norms

def projection(A,tol=1e-10):
  U,s,Vh=np.linalg.svd(A,full_matrices=False)
  if len(s)==0: return np.zeros((M,M),complex),0,np.inf
  r=int(np.sum(s>max(tol,1e-10*s[0])))
  Q=U[:,:r]
  cond=float(s[0]/s[r-1]) if r>0 else np.inf
  return Q@Q.conj().T,r,cond

def vis(B,A):
  P,r,cond=projection(A)
  C=(B.conj().T@P@B); C=(C+C.conj().T)/2
  ev=np.linalg.eigvalsh(C).real
  Res=(np.eye(M)-P)@B
  sres=np.linalg.svd(Res,compute_uv=False)
  resop=float(sres[0]) if len(sres) else 0.0
  c=float(max(0.0,ev[0]))
  return {'rank_A':r,'cond_A':cond,'c_min':c,'c_mean':float(np.mean(np.maximum(ev,0))), 'c_max':float(max(ev)), 'residual_op_norm':resop,'residual_mean_energy':float(np.mean(np.linalg.norm(Res,axis=0)**2)), 'identity_error':float(abs(c-max(0.0,1-resop**2)))}
# support sweep, dim 12
rows=[]
for X in [8,12,16,24,32,48,64,96,128,192,256,384]:
  ns,A=atoms_integers(X); rows.append({'dictionary':'integers','X':X,'num_atoms':len(ns),'boundary_dim':12, **vis(Qb[:,:12],A)})
int_df=pd.DataFrame(rows); int_df.to_csv(OUT/'coefficient_visibility_integer_sweep_step110.csv',index=False)
# dimension sweep fixed X=192
rows=[]; ns,A=atoms_integers(192)
for d in DIMS:
  rows.append({'dictionary':'integers_X192','X':192,'num_atoms':len(ns),'boundary_dim':d, **vis(Qb[:,:d],A)})
dim_df=pd.DataFrame(rows); dim_df.to_csv(OUT/'coefficient_visibility_dimension_sweep_step110.csv',index=False)
# log uniform benchmark
rows=[]
for K in [8,12,16,24,32,48,64,96,128,192]:
  fs,A=atoms_log_uniform(K); rows.append({'dictionary':'log_uniform_benchmark','num_atoms':K,'boundary_dim':12, **vis(Qb[:,:12],A)})
log_df=pd.DataFrame(rows); log_df.to_csv(OUT/'coefficient_visibility_log_uniform_benchmark_step110.csv',index=False)
# residual spectra examples
spec=[]
for X,d in [(16,12),(64,12),(192,12),(192,32)]:
  ns,A=atoms_integers(X); P,r,cond=projection(A); B=Qb[:,:d]
  C=(B.conj().T@P@B); C=(C+C.conj().T)/2; ev=np.linalg.eigvalsh(C).real
  for j,e in enumerate(ev): spec.append({'X':X,'boundary_dim':d,'eig_index':j+1,'visibility_eigenvalue':float(max(e,0))})
pd.DataFrame(spec).to_csv(OUT/'visibility_eigenvalues_step110.csv',index=False)
# compensation scenarios
sc=[]
for _,row in int_df.iterrows():
  N=int(row.X); c=float(row.c_min)
  for gname,g in [('logN',math.log(max(N,2))),('sqrtN',math.sqrt(N)),('N^0.75',N**0.75),('N',N)]:
    sc.append({'N':N,'c_N_empirical':c,'gamma_model':gname,'gamma_N':g,'Lambda_N':c*g})
pd.DataFrame(sc).to_csv(OUT/'source_visibility_compensation_scenarios_step110.csv',index=False)
# kernel/adversarial examples
adv=[]
for X in [16,32,64,128]:
  ns,A=atoms_integers(X); P,r,cond=projection(A); U,s,Vh=np.linalg.svd(np.eye(M)-P,full_matrices=False); v=U[:,:1]
  adv.append({'X':X,'num_atoms':len(ns),'rank_A':r, **{('adversarial_'+k):v2 for k,v2 in vis(v,A).items() if k in ['c_min','residual_op_norm']}})
pd.DataFrame(adv).to_csv(OUT/'coefficient_kernel_collapse_step110.csv',index=False)
# finite character frame toy
chars=[]
for q in [16,32,64,128]:
  x=np.arange(q); A=np.exp(2j*np.pi*np.outer(np.arange(q),x)/q)/np.sqrt(q); F=A.conj().T@A; ev=np.linalg.eigvalsh(F).real
  chars.append({'q':q,'family':'full','rank':int(np.linalg.matrix_rank(F)),'lambda_min':float(ev.min()),'lambda_max':float(ev.max())})
  A=A[:q//2,:]; F=A.conj().T@A; ev=np.linalg.eigvalsh((F+F.conj().T)/2).real
  chars.append({'q':q,'family':'half','rank':int(np.linalg.matrix_rank(F)),'lambda_min':float(max(ev.min(),0)),'lambda_max':float(ev.max())})
pd.DataFrame(chars).to_csv(OUT/'finite_character_frame_toy_step110.csv',index=False)
# tables
pd.DataFrame(meta).to_csv(OUT/'boundary_dictionary_metadata_step110.csv',index=False)
pd.DataFrame([
 {'gate':'CV1','criterion':'legal finite boundary Gram after null quotient','status':'defined in finite model'},
 {'gate':'CV2','criterion':'short Dirichlet coefficient atoms declared upstream','status':'candidate'},
 {'gate':'CV3','criterion':'R_N^*H_NR_N >= c_N G_BN','status':'central diagnostic'},
 {'gate':'CV4','criterion':'gamma_N c_N -> infinity','status':'open'},
 {'gate':'CV5','criterion':'finite boundary dictionaries exhaust completed Burnol/Sonine sector','status':'open'},
 {'gate':'CV6','criterion':'no target-selected coefficient supports','status':'required'}]).to_csv(OUT/'coefficient_visibility_gate_table_step110.csv',index=False)
pd.DataFrame([
 {'item':'visibility identity','statement':'R_N^*H_NR_N = G_BN - E_coef^*E_coef'},
 {'item':'visibility constant','statement':'c_N = 1 - ||E_coef G_B^{-1/2}||^2'},
 {'item':'source product','statement':'G_X>=gamma H and R^*HR>=cG_B imply R^*G_XR>=gamma cG_B'},
 {'item':'Xi link','statement':'E_coef^*E_coef is the coefficient blind spot'},
 {'item':'growth obligation','statement':'need gamma_N c_N -> infinity plus exhaustivity'}]).to_csv(OUT/'theorem_map_step110.csv',index=False)
pd.DataFrame([
 {'input':'Burnol Sonine/co-Poisson','role':'Y^- carrier and completed zero-ledger/exhaustivity backbone'},
 {'input':'Heap-Soundararajan dual mollifier','role':'source-strength template for gamma_N'},
 {'input':'finite character orthogonality','role':'local exact frame for finite coefficient spaces'},
 {'input':'CCM semilocal Hardy-Titchmarsh','role':'ambient response space for local-factor geometry'},
 {'input':'Six Birds Xi','role':'identifies coefficient misses as adequacy residuals'}]).to_csv(OUT/'arithmetic_input_table_step110.csv',index=False)
# plots
plt.figure(figsize=(7,4.6)); plt.plot(int_df.num_atoms,int_df.c_min,marker='o',label='integer atoms'); plt.plot(log_df.num_atoms,log_df.c_min,marker='s',label='log-uniform benchmark'); plt.xlabel('coefficient atoms'); plt.ylabel('c_N'); plt.title('Coefficient visibility constant'); plt.legend(); plt.tight_layout(); plt.savefig(OUT/'visibility_constant_vs_support_step110.png',dpi=180); plt.close()
plt.figure(figsize=(7,4.6)); plt.plot(int_df.num_atoms,int_df.residual_op_norm,marker='o'); plt.xlabel('coefficient atoms'); plt.ylabel('residual operator norm'); plt.title('Worst coefficient blind spot'); plt.tight_layout(); plt.savefig(OUT/'coefficient_residual_vs_support_step110.png',dpi=180); plt.close()
plt.figure(figsize=(7,4.6)); plt.plot(dim_df.boundary_dim,dim_df.c_min,marker='o'); plt.xlabel('boundary dimension'); plt.ylabel('c_N'); plt.title('Visibility versus boundary dimension'); plt.tight_layout(); plt.savefig(OUT/'visibility_dimension_sweep_step110.png',dpi=180); plt.close()
plt.figure(figsize=(7,4.6));
for X,d in [(16,12),(64,12),(192,12),(192,32)]:
  sub=pd.read_csv(OUT/'visibility_eigenvalues_step110.csv'); ss=sub[(sub.X==X)&(sub.boundary_dim==d)]; plt.semilogy(ss.eig_index,np.maximum(ss.visibility_eigenvalue,1e-14),marker='o',label=f'X={X},d={d}')
plt.xlabel('visibility eigenvalue index'); plt.ylabel('visibility eigenvalue'); plt.title('Visibility spectrum'); plt.legend(fontsize=8); plt.tight_layout(); plt.savefig(OUT/'visibility_spectrum_step110.png',dpi=180); plt.close()
plt.figure(figsize=(7,4.6)); scdf=pd.read_csv(OUT/'source_visibility_compensation_scenarios_step110.csv')
for g in ['logN','sqrtN','N^0.75','N']:
  ss=scdf[scdf.gamma_model==g]; plt.plot(ss.N,ss.Lambda_N,marker='o',label=g)
plt.xlabel('support cutoff X'); plt.ylabel('Lambda_N = gamma_N c_N'); plt.title('Effective source strength'); plt.legend(); plt.tight_layout(); plt.savefig(OUT/'gamma_c_compensation_step110.png',dpi=180); plt.close()
plt.figure(figsize=(7,4.6)); adf=pd.read_csv(OUT/'coefficient_kernel_collapse_step110.csv'); plt.plot(adf.X,adf.adversarial_c_min,marker='o'); plt.xlabel('X'); plt.ylabel('adversarial c_N'); plt.title('Undercomplete dictionaries have invisible directions'); plt.tight_layout(); plt.savefig(OUT/'coefficient_kernel_collapse_step110.png',dpi=180); plt.close()
# summary and tex
best=int_df.loc[int_df.c_min.idxmax()].to_dict(); bestlog=log_df.loc[log_df.c_min.idxmax()].to_dict(); maxerr=float(max(int_df.identity_error.max(),dim_df.identity_error.max(),log_df.identity_error.max()))
summary=f'''# Step 110 results summary\n\nStep 110 isolates coefficient visibility for the boundary source route.\n\nMain identity:\n\nR_N^* H_N R_N = M_N^* P_D M_N = G_B,N - E_coef,N^* E_coef,N.\n\nThus c_N is one minus the squared worst coefficient residual on the legal boundary quotient.\n\nFinite theorem: if G_X,N >= gamma_N H_N and R_N^*H_NR_N >= c_N G_B,N, then R_N^*G_X,N R_N >= gamma_N c_N G_B,N.\n\nFinite toy audit:\n- boundary dimension tested in main sweep: 12\n- best integer support: X={int(best['X'])}, atoms={int(best['num_atoms'])}, c_N={best['c_min']:.6g}\n- best engineered log-uniform benchmark: atoms={int(bestlog['num_atoms'])}, c_N={bestlog['c_min']:.6g}\n- max identity check error: {maxerr:.3e}\n\nInterpretation: Heap--Soundararajan-style estimates target gamma_N, while this step shows that the boundary-to-coefficient visibility c_N is a separate gate. If c_N=0, the missed boundary direction is a coefficient-level Xi blind spot.\n'''
(OUT/'step110_results_summary.md').write_text(summary)
nonclaim='''# Nonclaim boundary\n\nThis step does not prove RH and does not prove the Hecke/Dirichlet source ladder. It defines a finite coefficient-visibility gate. The numerical model is an algebraic sanity check only, not a Six Birds simulation and not RH evidence.\n'''
(OUT/'nonclaim_boundary_step110.md').write_text(nonclaim)
tex=r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,geometry}
\geometry{margin=1in}
\newtheorem{theorem}{Theorem}
\title{Step 110: Coefficient Visibility Audit for $R_N$}
\date{May 13, 2026}
\begin{document}
\maketitle
\section{Purpose}
The boundary source route factors into source strength $\gamma_N$ and coefficient visibility $c_N$. This note isolates $c_N$.
\section{Objects}
Let $M_N:Y_{\mathcal B,N}\to H_N^{\rm resp}$ synthesize a finite boundary-packet dictionary, with $G_{\mathcal B,N}=M_N^*M_N$. Let $\mathcal D_N:\mathbb C^{\mathcal N_N}\to H_N^{\rm resp}$ be the short Dirichlet synthesis map and $H_N=\mathcal D_N^*\mathcal D_N$. Define $R_N=\mathcal D_N^\dagger M_N$ and $E_{{\rm coef},N}=(I-P_N)M_N$, where $P_N$ projects onto $\operatorname{Ran}\mathcal D_N$.
\begin{theorem}[Coefficient visibility identity]
\[
R_N^*H_NR_N=M_N^*P_NM_N=G_{\mathcal B,N}-E_{{\rm coef},N}^*E_{{\rm coef},N}.
\]
Therefore
\[
c_N=\lambda_{\min}\left(G_{\mathcal B,N}^{-1/2}R_N^*H_NR_NG_{\mathcal B,N}^{-1/2}\right)=1-\|E_{{\rm coef},N}G_{\mathcal B,N}^{-1/2}\|^2.
\]
\end{theorem}
\begin{proof}
Insert $R_N=\mathcal D_N^\dagger M_N$ and $H_N=\mathcal D_N^*\mathcal D_N$. The middle factor $(\mathcal D_N^\dagger)^*\mathcal D_N^*\mathcal D_N\mathcal D_N^\dagger$ is $P_N$.
\end{proof}
\begin{theorem}[Finite matrix moment composition]
If $G_{\mathcal X,N}\succeq\gamma_NH_N$ and $R_N^*H_NR_N\succeq c_NG_{\mathcal B,N}$, then
\[
R_N^*G_{\mathcal X,N}R_N\succeq\gamma_Nc_NG_{\mathcal B,N}.
\]
\end{theorem}
\section{Membrane meaning}
The residual $E_{{\rm coef},N}^*E_{{\rm coef},N}$ is a coefficient-level adequacy residual. If it has a legal unit direction, then the source route has a $\Xi$ blind spot.
\section{Conclusion}
The completed route needs $\gamma_Nc_N\to\infty$ plus fixed/exhaustive tail promotion. Heap--Soundararajan moment technology is relevant to $\gamma_N$; the Burnol/Sonine coefficient visibility problem is the separate $c_N$ gate.
\end{document}
'''
(OUT/'coefficient_visibility_step110.tex').write_text(tex)
checks=[]
for env in ['document','theorem','proof']:
 checks.append({'environment':env,'begin':tex.count('\\begin{'+env+'}'),'end':tex.count('\\end{'+env+'}'),'balanced':tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}')})
pd.DataFrame(checks).to_csv(OUT/'latex_structure_check_step110.csv',index=False)
schema={'step':110,'title':'Coefficient visibility audit for R_N','main_identity':'R^* H R = G_B - E^*E','best_integer_c':float(best.c_min),'best_log_uniform_c':float(bestlog.c_min),'max_identity_error':maxerr}
(OUT/'step110_schema.json').write_text(json.dumps(schema,indent=2))
zip_path=OUT/'step110_coefficient_visibility_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in OUT.iterdir():
  if p.is_file() and p.name!=zip_path.name: z.write(p,p.name)
print(json.dumps(schema,indent=2))
