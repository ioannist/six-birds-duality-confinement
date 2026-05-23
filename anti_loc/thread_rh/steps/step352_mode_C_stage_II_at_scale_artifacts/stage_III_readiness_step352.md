# Step 352 Stage III Readiness

Mode C Stage II at scale confirms that the ID x OL carrier is operational:

- The Hecke lens reproduces known H5 evaluator values exactly.
- The OL ledger blocks zeta descent wherever the finite defect
  `lambda_obs(chi,k,j) = |log(H_chi,k / Z_rho_j,k)|` is nonzero.
- Dropping OL causes false descent at every zeta target cell.

## Translation Condition For H6

Within this OL framework, H6 would translate only if there exists a transfer
operator `T` and normalization data `N` such that

`T(H_chi,k; N_chi,j,k) = Z_rho_j,k`

for all characters, target zeta zeros, and tested `k`, with

`lambda_obs^T(chi,k,j) = |log(T(H_chi,k;N_chi,j,k) / Z_rho_j,k)| = 0`.

The current carrier does not supply such a transfer.  It supplies a reliable
ledger showing where descent is blocked.

## Candidate Transfer Forms For Stage III

1. **Scalar-per-target normalizer**
   `T(H_chi,k) = c_chi,j H_chi,k`.
   This would require `H_chi,k/Z_rho_j,k` to be k-independent.  Prior bridge
   fits indicate this is unlikely.

2. **Affine log-normalizer**
   `log T(H_chi,k) = a_chi,j + b_chi,j k + log H_chi,k`.
   This is the smallest plausible Stage III test because it can absorb a
   single exponential-rate mismatch without arbitrary per-k lookup.

3. **Kernel-preserving transfer**
   `T` acts before taking evaluator magnitudes, preserving a reproducing
   kernel or Sonine projection structure.  This is the strongest candidate
   compatible with H6, but no paper-grounded theorem was found in step 336.

4. **OL-minimizing transfer family**
   Choose a constrained family `T_theta`, minimize the aggregate
   `sum lambda_obs^T`, and test hold-out in `rho` and `G`.  This is a
   diagnostic Stage III route, not a proof.

## Readiness Verdict

Stage III is ready as a translation search over explicit transfer families.
The acceptance gate is strict: a candidate must reduce all tested
`lambda_obs` values to zero or near-zero on training and hold-out cells
without per-cell lookup.
