import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json, zipfile

out = Path('/mnt/data/rh_membrane_step147_weight_schedule')
out.mkdir(exist_ok=True, parents=True)

# Gate table
gates = pd.DataFrame([
    ['W1', 'Positive separation', 'omega_{rho,k} > 0 for every visible residual zero direction', 'required', 'passed by all declared schedules'],
    ['W2', 'No q-dependence', 'weights may depend on height/envelope, not Re rho - 1/2', 'required', 'passed by envelope, polynomial, exp schedules'],
    ['W3', 'Trace class', 'sum omega q^2 ||Pi_R Y||^2 < infinity', 'required', 'proved for envelope schedule if shell envelopes finite'],
    ['W4', 'Tail promotion', 'P_N strongly exhausts H_R and K_R^omega trace class', 'required', 'inherits Step 145 strong exhaustion gate'],
    ['W5', 'Source compatibility', 'sup_N tr(F_N^Omega K_R^omega) < infinity', 'open', 'Step 148 target'],
    ['W6', 'Adequacy scope', 'weighted residual carrier covers all off-critical zero probes or residual is declared', 'open', 'not closed by weight schedule alone'],
], columns=['gate','name','condition','status','comment'])
gates.to_csv(out/'weight_schedule_gate_table_step147.csv', index=False)

# Schedules table
schedules = pd.DataFrame([
    ['envelope-normalized', '2^{-j}/((1+n_j)(1+E_j))', 'finite shell evaluator envelopes E_j', 'automatic trace-class, weakest but safest', 'height shell + envelope only'],
    ['polynomial', '(1+|gamma|)^{-B}(1+k)^{-2}', 'cumulative evaluator envelope O(T^A), choose B>A+2', 'less collapsed high zeros, needs analytic envelope', 'height only'],
    ['stretched-exponential', 'exp(-B(1+|gamma|)^nu)(1+k)^{-2}', 'envelope exp(C T^theta), choose nu>theta', 'robust if finite-order envelope is known', 'height only'],
    ['Gaussian', 'exp(-B(1+|gamma|)^2)(1+k)^{-2}', 'sub-Gaussian or finite-order envelope', 'very safe but may be source-currency weak', 'height only'],
], columns=['schedule','formula','needed_envelope','benefit','no_smuggling_status'])
schedules.to_csv(out/'weight_schedule_options_step147.csv', index=False)

# Theorem map
thm = pd.DataFrame([
    ['T147.1', 'Envelope-normalized trace-class theorem', 'Finite dyadic shell evaluator envelopes', 'K_R^omega is trace-class'],
    ['T147.2', 'Weighted separation theorem', 'All weights strictly positive', 'tr K_R^omega=0 implies q(rho)=0 for every visible residual zero direction'],
    ['T147.3', 'Analytic schedule criterion', 'Polynomial/stretched exponential evaluator envelope', 'Simpler height-only weights are trace-class'],
    ['T147.4', 'Completed squeeze with weighted ledger', 'Trace class + strong exhaustion + finite source budget', 'completed residual ledger collapses if Lambda_N^Omega -> infinity'],
    ['O147.1', 'Source compatibility', 'Need sup_N tr(F_N^Omega K_R^omega)<infty', 'left open for Step 148'],
], columns=['id','claim','hypotheses','conclusion'])
thm.to_csv(out/'theorem_map_step147.csv', index=False)

# Arithmetic input table
arith = pd.DataFrame([
    ['Burnol evaluators', 'Continuity and existence of Y^a_{rho,k}', 'imported from Burnol Sonine/co-Poisson theory', 'needed to define K_R^omega'],
    ['Evaluator shell envelope', 'E_j < infinity or analytic bound', 'open analytic/carrier envelope', 'needed for trace-class theorem'],
    ['Zero index ledger', 'dyadic height shells over nontrivial zeros with finite multiplicity', 'standard zeta analytic structure', 'used only for indexing, not RH'],
    ['Restricted source frame', 'F_N^Omega and Lambda_N^Omega from prior steps', 'conditional BPRZ/omega-compatible route', 'needed for source squeeze'],
    ['Source audit budget', 'sup_N tr(F_N^Omega K_R^omega)<infty', 'open', 'Step 148'],
], columns=['input','record','source_status','role'])
arith.to_csv(out/'arithmetic_input_table_step147.csv', index=False)

# Route status table
route = pd.DataFrame([
    ['unweighted ledger trace class', 'not certified', 'zero/evaluator norm sum may diverge'],
    ['weighted ledger trace class', 'conditionally passed', 'envelope-normalized weights close it if shell envelopes finite'],
    ['separation after weighting', 'passed', 'strictly positive weights preserve zero separation'],
    ['source compatibility', 'open', 'needs C_src^omega finite'],
    ['completed residual-tail promotion', 'conditional', 'requires P_N exhaustion plus trace-class ledger'],
    ['full RH claim', 'not claimed', 'still needs adequacy and all remaining source gates'],
], columns=['route_component','status','reason'])
route.to_csv(out/'route_status_step147.csv', index=False)

# Construction tasks
tasks = pd.DataFrame([
    ['147-A', 'Define dyadic height shells and evaluator envelope E_j', 'done', 'height/envelope schedule'],
    ['147-B', 'Prove envelope-normalized trace-class theorem', 'done', 'dyadic 2^{-j} summability'],
    ['147-C', 'Verify strict positive weights preserve separation', 'done', 'nonnegative sum of positive-weighted terms'],
    ['147-D', 'Identify analytic envelope schedules', 'done', 'polynomial/exponential alternatives'],
    ['148-A', 'Audit source budget C_src^omega', 'next', 'source-compatible normalization'],
], columns=['task','description','status','output'])
tasks.to_csv(out/'construction_tasks_step147.csv', index=False)

# Nonclaim boundary
nonclaim = """# Step 147 nonclaim boundary

Step 147 does not prove RH.

It does not prove that the unweighted residual zero ledger is trace class.

It does not prove an analytic evaluator-norm envelope for Burnol zero evaluators.

It does not prove source compatibility of the chosen weights; this is Step 148.

It does not prove that the residual carrier H_R covers every off-critical zero probe. That remains an adequacy gate.

What Step 147 proves is narrower: given finite dyadic evaluator envelopes, there is a lawful strictly positive weight schedule that makes the residual ledger trace class while preserving separation on visible residual zero directions.
"""
(out/'nonclaim_boundary_step147.md').write_text(nonclaim)

schema = {
    'step': 147,
    'name': 'Zero-evaluator norm envelope and weight schedule',
    'main_objects': ['K_R^omega', 'omega_{rho,k}', 'E_j', 'C_src^omega'],
    'closed_gates': ['trace-class by envelope-normalized weights', 'separation after weighting'],
    'open_gates': ['source compatibility', 'analytic evaluator envelope', 'full adequacy'],
    'next_step': 148
}
(out/'step147_schema.json').write_text(json.dumps(schema, indent=2))

# Generate toy plots and CSVs
J = np.arange(0, 24)
# toy shell counts and envelopes
twoJ = 2.0**J
n_j = np.maximum(1, (twoJ * np.log2(2+twoJ)/12).astype(int))
E_poly = (1+twoJ)**2
E_exp = np.exp(0.18*np.sqrt(twoJ))
# envelope normalized trace contribution upper bound is 1/4 * 2^-j
trace_env = 0.25 * 2.0**(-J)
trace_poly_B6 = 0.25 * n_j * E_poly * (1+twoJ)**(-6)
trace_poly_B3 = 0.25 * n_j * E_poly * (1+twoJ)**(-3)

pd.DataFrame({'j':J,'n_j_model':n_j,'E_poly_model':E_poly,'trace_env_upper':trace_env,
              'trace_poly_B6_model':trace_poly_B6,'trace_poly_B3_model':trace_poly_B3}).to_csv(out/'trace_class_weight_scenarios_step147.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.semilogy(J, trace_env, marker='o', label='envelope-normalized upper bound')
plt.semilogy(J, trace_poly_B6, marker='s', label='polynomial B=6 toy')
plt.semilogy(J, trace_poly_B3, marker='^', label='polynomial B=3 toy')
plt.xlabel('dyadic shell j')
plt.ylabel('shell trace contribution (toy / upper bound)')
plt.title('Trace-class shell contributions under weight schedules')
plt.legend()
plt.tight_layout()
plt.savefig(out/'trace_class_weight_schedules_step147.png', dpi=180)
plt.close()

# tail decay plot cumulative tail
cum_tail_env = np.array([trace_env[j:].sum() for j in range(len(J))])
cum_tail_b6 = np.array([trace_poly_B6[j:].sum() for j in range(len(J))])
cum_tail_b3 = np.array([trace_poly_B3[j:].sum() for j in range(len(J))])
pd.DataFrame({'j':J,'tail_env':cum_tail_env,'tail_poly_B6':cum_tail_b6,'tail_poly_B3':cum_tail_b3}).to_csv(out/'trace_tail_decay_step147.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.semilogy(J, cum_tail_env, marker='o', label='envelope-normalized tail')
plt.semilogy(J, cum_tail_b6, marker='s', label='polynomial B=6 tail')
plt.semilogy(J, cum_tail_b3, marker='^', label='polynomial B=3 tail')
plt.xlabel('tail begins at shell j')
plt.ylabel('remaining trace tail')
plt.title('Weighted residual ledger tail decay')
plt.legend()
plt.tight_layout()
plt.savefig(out/'weighted_ledger_tail_decay_step147.png', dpi=180)
plt.close()

# source compatibility conceptual scenarios
N = np.arange(1, 101)
Lambda = np.log(N+2)
vis_good = 0.8
vis_weak = 0.25
C_const = np.ones_like(N)*3
C_growth = (N+1)**0.5
squeeze_good = C_const/(Lambda*vis_good)
squeeze_bad = C_growth/(Lambda*vis_weak)
pd.DataFrame({'N':N,'Lambda_log':Lambda,'squeeze_const_budget':squeeze_good,'squeeze_growth_budget':squeeze_bad}).to_csv(out/'source_compatibility_scenarios_step147.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(N, squeeze_good, label='finite source budget / positive visibility')
plt.plot(N, squeeze_bad, label='growing source budget / weak visibility')
plt.xlabel('window index N')
plt.ylabel('C_src / Lambda_eff')
plt.title('Why source compatibility is a separate gate')
plt.legend()
plt.tight_layout()
plt.savefig(out/'source_compatibility_gate_step147.png', dpi=180)
plt.close()

# separation weights schedule plot
T = np.linspace(0, 100, 400)
w_poly = (1+T)**-4
w_exp = np.exp(-0.08*T)
w_gauss = np.exp(-0.006*T**2)
pd.DataFrame({'T':T,'poly_B4':w_poly,'exp_0p08':w_exp,'gauss_0p006':w_gauss}).to_csv(out/'positive_weight_schedules_step147.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.semilogy(T, w_poly, label='polynomial')
plt.semilogy(T, w_exp, label='exponential')
plt.semilogy(T, w_gauss, label='Gaussian')
plt.xlabel('height |Im rho|')
plt.ylabel('positive weight')
plt.title('Positive weights preserve separation despite decay')
plt.legend()
plt.tight_layout()
plt.savefig(out/'positive_weight_schedules_step147.png', dpi=180)
plt.close()

# zip everything selected
zip_path = out/'step147_weight_schedule_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for p in out.iterdir():
        if p.name != zip_path.name:
            zf.write(p, arcname=p.name)

print('Created Step 147 artifacts in', out)
