import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json, zipfile

out=Path('/mnt/data/rh_membrane_step148_source_weight_audit')
out.mkdir(exist_ok=True)

# Scenario 1: no-go divergence of raw cumulative source trace
N=np.arange(1,101)
Lambda=np.log1p(N)**1.2
masses=[1.0,0.2,0.05,0.0]
rows=[]
for m in masses:
    for n,lam in zip(N,Lambda):
        rows.append({'N':int(n),'Lambda':lam,'weighted_residual_mass':m,'lower_bound_trace':lam*m})
df=pd.DataFrame(rows)
df.to_csv(out/'raw_cumulative_trace_divergence_step148.csv',index=False)
plt.figure(figsize=(7,4.5))
for m in masses:
    sub=df[df['weighted_residual_mass']==m]
    plt.plot(sub['N'], sub['lower_bound_trace'], label=f'm={m:g}')
plt.xlabel('N')
plt.ylabel('lower bound: Lambda_N * tr(G_R K)')
plt.title('Raw cumulative source trace diverges unless residual mass is zero')
plt.legend()
plt.tight_layout()
plt.savefig(out/'raw_cumulative_trace_divergence_step148.png', dpi=180)
plt.close()

# Scenario 2: normalized frame bounded but no squeeze
mass=0.2
norm_trace=(Lambda/(1+Lambda))*mass
raw_trace=Lambda*mass
pd.DataFrame({'N':N,'Lambda':Lambda,'raw_trace_lb':raw_trace,'normalized_trace_lb':norm_trace}).to_csv(out/'normalized_vs_raw_source_trace_step148.csv',index=False)
plt.figure(figsize=(7,4.5))
plt.plot(N, raw_trace, label='raw cumulative lower bound')
plt.plot(N, norm_trace, label='normalized audit lower bound')
plt.xlabel('N')
plt.ylabel('trace lower bound')
plt.title('Normalization restores boundedness but removes divergence squeeze')
plt.legend()
plt.tight_layout()
plt.savefig(out/'normalized_vs_raw_source_trace_step148.png', dpi=180)
plt.close()

# Scenario 3: source-compatible shell weights for bounded audit families
j=np.arange(0,30)
nj=np.maximum(1,(2**(0.15*j)).astype(int))
Ej=(1+j)**2
Sj_bounded=(1+j)**1.5
omega=2.0**(-j)/((1+nj)*(1+Ej)*(1+Sj_bounded))
trace_shell=nj*omega*0.25*Ej
source_shell=nj*omega*0.25*Sj_bounded
pd.DataFrame({'shell_j':j,'n_j':nj,'E_j':Ej,'S_j_bounded':Sj_bounded,'omega':omega,'trace_shell_bound':trace_shell,'source_shell_bound':source_shell,'trace_cumulative':np.cumsum(trace_shell),'source_cumulative':np.cumsum(source_shell)}).to_csv(out/'bounded_audit_shell_weights_step148.csv',index=False)
plt.figure(figsize=(7,4.5))
plt.plot(j, np.cumsum(trace_shell), label='trace bound cumulative')
plt.plot(j, np.cumsum(source_shell), label='source audit bound cumulative')
plt.xlabel('dyadic shell j')
plt.ylabel('cumulative bound')
plt.title('Shell weights work for bounded audit families')
plt.legend()
plt.tight_layout()
plt.savefig(out/'bounded_audit_shell_weights_step148.png', dpi=180)
plt.close()

# Scenario 4: if cumulative source envelope grows with N, sup source envelope diverges
N2=np.arange(1,200)
Lambda2=np.log1p(N2)
y_norm2=1.0
source_envelope=Lambda2*y_norm2
pd.DataFrame({'N':N2,'Lambda_N':Lambda2,'source_envelope_on_fixed_nonzero_evaluator':source_envelope}).to_csv(out/'cumulative_source_envelope_diverges_step148.csv',index=False)
plt.figure(figsize=(7,4.5))
plt.plot(N2, source_envelope)
plt.xlabel('N')
plt.ylabel('<F_N y, y> lower bound')
plt.title('Cumulative lower frame makes fixed evaluator source envelope infinite')
plt.tight_layout()
plt.savefig(out/'cumulative_source_envelope_diverges_step148.png', dpi=180)
plt.close()

# Scenario 5: residual squeeze with bounded source work and trace tail
Lambda3=np.log1p(N)**1.1
tail=np.exp(-N/18)
C=1.0
squeeze=C/Lambda3 + tail
pd.DataFrame({'N':N,'Lambda':Lambda3,'tail':tail,'squeeze_bound':squeeze}).to_csv(out/'source_work_squeeze_step148.csv',index=False)
plt.figure(figsize=(7,4.5))
plt.plot(N, C/Lambda3, label='C_src/Lambda_N')
plt.plot(N, tail, label='trace tail')
plt.plot(N, squeeze, label='total squeeze bound')
plt.xlabel('N')
plt.ylabel('bound')
plt.title('If source-work is bounded, residual mass is squeezed')
plt.legend()
plt.tight_layout()
plt.savefig(out/'source_work_squeeze_step148.png', dpi=180)
plt.close()

# Gate status JSON/CSV check
tex=(out/'source_weight_audit_step148.tex').read_text()
checks={
    'brace_balance': tex.count('{')-tex.count('}'),
    'has_document': '\\begin{document}' in tex and '\\end{document}' in tex,
    'contains_no_go': 'Raw cumulative source-budget no-go' in tex,
    'files_created': sorted([p.name for p in out.iterdir()])
}
(out/'latex_structure_check_step148.json').write_text(json.dumps(checks, indent=2))

# Zip selected artifacts
zip_path=out/'step148_source_weight_audit_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name == zip_path.name:
            continue
        z.write(p, arcname=p.name)
print(f'Wrote {zip_path}')
