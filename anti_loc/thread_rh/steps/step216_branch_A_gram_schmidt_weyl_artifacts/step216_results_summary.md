# Step 216 Results Summary

## Target

Test the Step 214/215 Weyl diagnostic after Gram-Schmidt orthonormalization of the sampled `kappa_{rho_n}` vectors.

## Setup

- CAND1: Burnol-boundary `K_{1/2}^Gamma(1/2+i tau,rho_n)` model, `n=1..20`.
- CAND2: zeta-form comparison model, `n=1..10`.
- Operator: `C_l = (I - P_infty) M_{m_l} P_infty`, `l = log 2`.
- Grid/model: Step 215 finite PSWF/sinc model, 140 Gauss-Legendre nodes on `[-100,100]`.
- Precision: mpmath input precision tested at 50, 80, and 100 dps; finite operator arrays are the inherited Step 214/215 sampled model.

## Gram-Schmidt Findings

CAND1 becomes numerically fragile after the first few orthogonal directions:

- Relative residuals start `1.0, 0.3637, 0.0520, 0.00656, 0.000552, ...`.
- Effective CAND1 dimension by residual threshold:
  - `rel > 1e-2`: 3 directions.
  - `rel > 1e-4`: 6 directions.
  - `rel > 1e-6`: 9 directions.
- The raw CAND1 norms collapse from `4.16e-7` to below `1e-29`, so later normalized directions are low-absolute-signal directions.

CAND1 `||C_l v_n||`:

- High-confidence directions: `1.7554`, `0.5312`.
- Low-absolute-signal directions include mixed values `1.0164, 0.1123, 0.1591, 0.5015, ...`.
- The Step 214 strong `~1.4+` lower bound does **not** persist across high-confidence orthogonal directions.

CAND2 remains well-conditioned:

- Relative residuals remain `0.833..1.0`.
- `||C_l v_n||` for `n=1..10`: `0.2389, 0.4161, 0.4238, 0.6355, 0.6068, 0.6163, 0.6257, 0.6654, 0.4720, 0.6142`.
- CAND2 is only a comparison model, not the verified `a=1/2` transport formula.

## Verdict

`V_weyl_gram_schmidt_inconclusive`.

The original Step 214 large lower-bound diagnostic is not certified as a multi-direction CAND1 essential-norm obstruction. It does not cleanly decay to zero either; instead the CAND1 orthogonalized directions rapidly become low-absolute-signal and precision-limited. CAND2 gives stable multi-direction nonzero behavior, but it is not the proven Burnol `a=1/2` model.
