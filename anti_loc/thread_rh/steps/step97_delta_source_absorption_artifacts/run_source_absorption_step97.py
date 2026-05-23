import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step97_delta_source_absorption')
OUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(9701)

def psd_from_rank(d, r, scale=1.0):
    A = rng.normal(size=(r, d))
    return scale * (A.T @ A) / max(r, 1)

def lam_min(A):
    return float(np.linalg.eigvalsh((A + A.T)/2)[0])

def lam_max(A):
    return float(np.linalg.eigvalsh((A + A.T)/2)[-1])

def pos_part_trace(A):
    vals = np.linalg.eigvalsh((A + A.T)/2)
    return float(np.maximum(vals, 0).sum())

# Experiment 1: full random source absorption
d = 12
Delta = psd_from_rank(d, d, scale=1.0)
records = []
F = np.zeros((d, d))
for m in range(1, 81):
    q = rng.normal(size=(d, 1))
    q = q / np.linalg.norm(q)
    lam = 0.35 + 0.01*m
    F += lam * (q @ q.T)
    residual = Delta - F
    records.append({
        'm': m,
        'lambda_min_F': lam_min(F),
        'lambda_max_residual': lam_max(residual),
        'positive_residual_trace': pos_part_trace(residual),
        'absorbed': lam_max(residual) <= 1e-10
    })
full_df = pd.DataFrame(records)
full_df.to_csv(OUT/'full_source_absorption_ladder_step97.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.plot(full_df['m'], full_df['positive_residual_trace'], label='positive residual trace')
plt.plot(full_df['m'], full_df['lambda_min_F'], label='lambda_min(F)')
plt.xlabel('number of source records')
plt.ylabel('value')
plt.title('Full source absorption ladder')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'full_source_absorption_ladder_step97.png', dpi=180)
plt.close()

# Experiment 2: partial coverage failure
d=10
Delta = np.eye(d)
F = np.zeros((d,d))
records=[]
covered=5
for m in range(1,61):
    q = np.zeros((d,1))
    idx = rng.integers(0, covered)
    q[idx,0]=1.0
    lam=1.0
    F += lam*(q@q.T)
    residual=Delta-F
    # hidden dimension min source coverage on uncovered is 0; residual max remains at least 1
    records.append({
        'm':m,
        'covered_dimensions':covered,
        'lambda_min_F':lam_min(F),
        'lambda_max_residual':lam_max(residual),
        'positive_residual_trace':pos_part_trace(residual),
        'uncovered_residual_expected':1.0
    })
partial_df=pd.DataFrame(records)
partial_df.to_csv(OUT/'partial_coverage_failure_step97.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(partial_df['m'], partial_df['lambda_max_residual'], label='max residual eigenvalue')
plt.plot(partial_df['m'], partial_df['positive_residual_trace'], label='positive residual trace')
plt.xlabel('source records on first 5 dimensions')
plt.ylabel('residual')
plt.title('Partial source coverage cannot absorb hidden directions')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'partial_coverage_failure_step97.png', dpi=180)
plt.close()

# Experiment 3: lower-frame growth and currency collapse
records=[]
Theta_trace=d
for n in range(1,101):
    Lambda=n**0.75
    defect=1/(1+n)**1.3
    budget=Theta_trace/Lambda+defect
    records.append({'n':n,'Lambda_n':Lambda,'defect':defect,'trace_budget_bound':budget})
budget_df=pd.DataFrame(records)
budget_df.to_csv(OUT/'lower_frame_budget_collapse_step97.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(budget_df['n'], budget_df['trace_budget_bound'], label='trace budget bound')
plt.plot(budget_df['n'], 1/budget_df['Lambda_n'], label='1/Lambda_n')
plt.xlabel('stage n')
plt.ylabel('bound')
plt.title('Lower-frame source growth collapses budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'lower_frame_budget_collapse_step97.png', dpi=180)
plt.close()

# Experiment 4: moving-window tail requirement
records=[]
for n in range(1,101):
    window_bound=1/(n**1.2)
    good_tail=1/(n**1.1)
    bad_tail=0.25+1/(n+1)
    records.append({
        'n':n,
        'window_bound':window_bound,
        'good_tail':good_tail,
        'good_total':window_bound+good_tail,
        'bad_tail':bad_tail,
        'bad_total':window_bound+bad_tail
    })
tail_df=pd.DataFrame(records)
tail_df.to_csv(OUT/'moving_window_tail_requirement_step97.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(tail_df['n'], tail_df['good_total'], label='exhaustive: window + vanishing tail')
plt.plot(tail_df['n'], tail_df['bad_total'], label='support-only: nonvanishing tail')
plt.xlabel('finite conductor/window stage')
plt.ylabel('total obstruction')
plt.title('Moving-window source windows require tail/exhaustivity')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'moving_window_tail_requirement_step97.png', dpi=180)
plt.close()

# Experiment 5: upper-frame does not imply lower-frame
records=[]
for k in range(1,11):
    # all sources in first coordinate: upper norm grows, lower frame is zero
    F=np.zeros((10,10)); F[0,0]=k
    records.append({'num_sources':k,'upper_frame_norm':lam_max(F),'lower_frame_constant':lam_min(F)})
upper_df=pd.DataFrame(records)
upper_df.to_csv(OUT/'upper_not_lower_frame_step97.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(upper_df['num_sources'], upper_df['upper_frame_norm'], label='upper frame norm')
plt.plot(upper_df['num_sources'], upper_df['lower_frame_constant'], label='lower frame constant')
plt.xlabel('sources on one direction')
plt.ylabel('frame values')
plt.title('Upper/source mass alone does not imply lower frame')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'upper_not_lower_frame_step97.png', dpi=180)
plt.close()

print('Wrote Step 97 artifacts to', OUT)
