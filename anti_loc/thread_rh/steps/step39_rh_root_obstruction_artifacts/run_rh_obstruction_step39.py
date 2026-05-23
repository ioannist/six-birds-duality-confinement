"""Small algebra checks for Step 39.
These checks are not Six Birds simulations. They only verify PSD/Loewner
facts used in the obstruction ledger.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path(__file__).resolve().parent

def lammax(M: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((M + M.T.conj()) / 2)[-1])

def lammin(M: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((M + M.T.conj()) / 2)[0])

cases = []
# EF domination failure: A not <= K.
A = np.diag([2.0, 0.2]); K = np.eye(2)
cases.append(dict(case="EF_domination_failure", gate="explicit_formula_domination",
                  violation=lammax(A-K), status="fails: zero displacement exceeds carrier currency"))
# Character frame hole: source frame misses e2.
F = np.diag([100.0, 0.0]); Theta_inv = np.eye(2)
cases.append(dict(case="character_frame_hole", gate="full_character_frame",
                  violation=max(0.0, -lammin(F-1.0*Theta_inv)), status="fails: uncovered anti-invariant direction"))
# Coercivity bounded: Lambda not growing.
Lambda = 5.0; bound = 1.0/Lambda
cases.append(dict(case="coercivity_growth_failure", gate="source_growth",
                  violation=bound, status="finite budget only; no exact collapse"))
# Null-mode legality false.
C = np.diag([0.0, 1.0]); L = np.array([[1.0, 0.0]])
K_pseudo = L @ np.linalg.pinv(C) @ L.T
cases.append(dict(case="null_mode_legality_failure", gate="null_mode_legality",
                  violation=float(K_pseudo[0,0]), status="pseudoinverse says zero but true variational capacity is infinite"))
# Visibility failure: off-fixed mass invisible.
cases.append(dict(case="visibility_exhaustivity_failure", gate="zero_visibility",
                  violation=1.0, status="off-fixed mass can be omitted or mapped to zero by nonseparating readout"))
# Trace shadow overread: traces equal but Loewner fails.
A = np.diag([2.0, 0.5]); K = np.diag([1.0, 1.5])
cases.append(dict(case="trace_shadow_overread", gate="loewner_not_trace",
                  violation=lammax(A-K), status="traces match but anti-invariant Loewner domination fails"))
# Public shadow invariant-only failure.
Kmat = np.diag([0.5, 2.0]); Theta = np.eye(2)
cases.append(dict(case="invariant_only_failure", gate="anti_invariant_sector",
                  violation=lammax(Kmat-Theta), status="invariant sector passes, anti-invariant sector fails"))
pd.DataFrame(cases).to_csv(OUT / "rh_obstruction_cases_step39.csv", index=False)

# Confinement ladder bound: good and bad examples.
rows = []
eps = 0.25
trTheta = 2.0
for n in [1,2,4,8,16,32,64,128,256,512,1024]:
    Lambda = float(n)
    trEsrc = n**-1.5
    trEEF = n**-2
    t = 1.0
    bound = (1/eps**2)*((1+t)*(trTheta/Lambda + trEsrc) + (1+1/t)*trEEF)
    rows.append(dict(model="good_ladder", n=n, Lambda=Lambda, trEsrc=trEsrc, trEEF=trEEF, eps=eps, mass_bound=bound))
    Lambda_bad = 10.0
    trEsrc_bad = 0.1
    trEEF_bad = n**-1
    bound_bad = (1/eps**2)*((1+t)*(trTheta/Lambda_bad + trEsrc_bad) + (1+1/t)*trEEF_bad)
    rows.append(dict(model="bad_ladder", n=n, Lambda=Lambda_bad, trEsrc=trEsrc_bad, trEEF=trEEF_bad, eps=eps, mass_bound=bound_bad))
pd.DataFrame(rows).to_csv(OUT / "rh_obstruction_ladder_bounds_step39.csv", index=False)

# Gate table.
gates = [
    ("O1", "explicit_formula_domination", "contractive factorization V_Z = T W_cmp or controlled EF defect", "off-fixed displacement not paid by carrier"),
    ("O2", "character_frame", "sources form lower frame over all of Y^-", "hidden anti-invariant character direction"),
    ("O3", "coercivity_growth", "Lambda -> infinity or sufficient finite budget", "finite allowance remains"),
    ("O4", "null_mode_legality", "L^- annihilates kernel of C on legal quotient", "fake zero budget or infinite true capacity"),
    ("O5", "zero_visibility_exhaustivity", "zero ledger visible and readout separates Fix(J)", "zeros hidden or off-fixed displacement invisible"),
    ("O6", "closure_promotion", "formed predictive closure and finite-to-continuum defects controlled", "finite/local statement overread globally"),
    ("O7", "scope_nonclaim", "excluded probes recorded as nonclaims", "gating mistaken for zero confinement"),
]
pd.DataFrame(gates, columns=["slot", "gate", "accepted_record", "failure_witness"]).to_csv(OUT / "rh_obstruction_gate_table_step39.csv", index=False)

# Theorem map.
theorems = [
    ("T39.1", "Defective confinement inequality", "EF domination + budget bound", "off-fixed mass bound"),
    ("T39.2", "Asymptotic confinement", "Lambda->infty, EF/src defects ->0", "visible off-fixed mass ->0"),
    ("T39.3", "Quantitative obstruction alternative", "observed mass exceeds bound", "at least one gate false"),
    ("T39.4", "Asymptotic obstruction alternative", "limsup off-fixed mass positive", "one of EF, frame, growth, null, visibility, promotion fails"),
    ("L39.1", "Incomplete character frame witness", "source readouts have common kernel", "unpriced anti-invariant witness"),
    ("L39.2", "Null-mode false collapse", "probe sees kernel of C", "pseudoinverse shadow invalid"),
]
pd.DataFrame(theorems, columns=["id", "result", "hypothesis", "conclusion"]).to_csv(OUT / "theorem_map_step39.csv", index=False)
print("Wrote Step 39 check artifacts to", OUT)
