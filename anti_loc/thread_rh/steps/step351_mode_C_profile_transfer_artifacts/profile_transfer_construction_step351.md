# Step 351 Mode C Profile-Transfer Construction

## Matching Primitive Head Profiles

H6 matches two validated primitive head profiles:

1. **Invariant-descent (ID)**: H6 is a descent problem from Hecke-side
   evaluator conclusions to a zeta-side Burnol/Sonine residual.
2. **Obstruction-ledger (OL)**: Branch C records a nonzero residual
   obstruction, represented here as an explicit ledger entry.

## Finite Operational Signature

The recombined carrier is

`U_IDxOL = {(u_inv, lambda_obs)}`.

For this finite Stage I construction:

- `u_inv = (chi, k, H_chi_k)` is a Hecke evaluator state.
- `lambda_obs >= 0` is a ledger obstruction against zeta descent.
- `q(u_inv, lambda_obs)` descends only when `lambda_obs = 0`.
- If `lambda_obs != 0`, the zeta lens is blocked and reports the defect.

## Lens

For the Hecke substrate:

`q_H(chi,k,H_chi_k,lambda_obs) = H_chi_k`.

For the zeta descent target:

`q_zeta(chi,k,H_chi_k,lambda_obs) = blocked(lambda_obs)` when
`lambda_obs != 0`, and `H_chi_k` when `lambda_obs = 0`.

## Ledger

For the target `rho_1`, the finite obstruction ledger is

`lambda_obs(chi,k;rho_1) = |log(H_chi_k / Z_k(rho_1))|`.

This is not a bridge formula.  It is an obstruction record: nonzero values
mean the Hecke evaluator cannot be identified with the zeta residual by the
ID lens alone.

## Rewrite Rules

- `ID_compute`: preserves `lambda_obs` and emits the Hecke evaluator.
- `OL_compare`: computes and stores `lambda_obs`.
- `Descend`: allowed iff `lambda_obs = 0`.

Dropping OL sets `lambda_obs = 0` trivially and therefore forces descent;
this is expected to change the descent decision and expose false residuals.
