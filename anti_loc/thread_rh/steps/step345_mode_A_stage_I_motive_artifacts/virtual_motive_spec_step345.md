# Step 345 Virtual Motive Spec: `M^b`

This is a finite operational signature for Mode A Stage I.  It is not a
category, topos, scheme, or measure-space construction.

## Finite Basis

Fix a finite kernel size `N`.  The Stage I consistency table uses `N=4`; the
Stage II preview also uses basis labels up to `k=10`.

For each `k in {1,...,N}` use the free rational vector basis

- `H_{chi,k}`: Hecke-realization carrier at character `chi` and derivative
  index `k`.
- `Z_{j,k}`: zeta-realization carrier at zeta zero `rho_j` and derivative
  index `k`.
- `Omega_{chi,j,k}`: non-descending obstruction symbol.

An element is a finite formal rational linear combination of those basis
symbols.  The canonical normal form is sorted by `(side, chi, j, k)` with like
terms combined.

## Lens and Realizations

The host lens is typed:

- `R_H(H_{chi,k}) = |(L(s,chi) M(G)(s))^(k)(rho_chi)|`.
- `R_H(Z_{j,k}) = 0`.
- `R_H(Omega_{chi,j,k}) = defect_H(chi,j,k)` as a ledger entry, not a number
  to be killed.
- `R_zeta(Z_{j,k}) = |(zeta(s) M(G)(s))^(k)(rho_j)|`.
- `R_zeta(H_{chi,k}) = 0`.
- `R_zeta(Omega_{chi,j,k}) = defect_zeta(chi,j,k)` as a ledger entry.

The lens therefore produces a pair `(host_value, defect_ledger)`.  The defect
ledger is part of the output and is not quotiented away.

## Equivalence

`u ~ v` iff their canonical normal forms are exactly equal, including all
`Omega` coefficients.  This is intentionally strict: it prevents smuggling the
H6 bridge by silently imposing `Omega=0`.

## Rewrite Rules

1. `combine`: `a B + b B -> (a+b) B`.
2. `zero`: `0 B -> 0`.
3. `sort`: normal form sorts basis symbols lexicographically.
4. `transfer`: for fixed `(chi,j,k)`,
   - `F(H_{chi,k}) = Z_{j,k} + Omega_{chi,j,k}`.
   - `F(Z_{j,k}) = H_{chi,k} + Omega_{chi,j,k}`.
   - `F(Omega_{chi,j,k}) = -Omega_{chi,j,k}`.

By linear extension, `F^2 = id` on every basis element:

- `F^2(H) = F(Z+Omega) = H+Omega-Omega = H`.
- `F^2(Z) = F(H+Omega) = Z+Omega-Omega = Z`.
- `F^2(Omega) = Omega`.

## Defect Ledger

The obstruction record is

`D_{chi,j,k} = F(H_{chi,k}) - Z_{j,k} = Omega_{chi,j,k}`.

The direct H6 bridge would require `D_{chi,j,k}=0`.  Stage I explicitly does
not impose this.  Steps 338, 340, 341, 342, and 344 are recorded as evidence
that elementary host-layer descents do not justify that quotient.

## Preserved Existing Cases

The algebra preserves existing framework computations as realization records:
Hecke evaluator values remain `R_H(H_{chi,k})`; zeta Branch C values remain
`R_zeta(Z_{j,k})`.  No previously retained no-go is weakened because the
non-descending symbol is retained in the normal form.
