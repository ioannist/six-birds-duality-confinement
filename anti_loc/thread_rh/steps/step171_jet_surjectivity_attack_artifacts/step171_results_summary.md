# Step 171: Projected Zero-Jet Surjectivity Attack

Verdict:

`jet_surjectivity_verdict = V_surj_genuinely_kernel_required`.

The upgraded audit attempted the structural refutation paths U1a-d and the
non-kernel constructive path U2.  None decides a zero/order case from inherited
records.  All paths reduce to the same missing datum:

`Step102/Step104/Step105/Step153/Step162 Mellin-side Sonin/prolate projection
kernel or range-evaluator matrix record for mathsf P_infty`.

Equivalently, one needs an exact `K_infty(s,s')` formula or an equivalent
theorem deciding

```tex
<M_zeta G, mathsf P_infty y_{rho,k}>
```

for legal Step119 Burnol profiles `G`.

## Structural Pairing

For a zeta zero `rho` and `0 <= k < m_rho`, define

```tex
L_{rho,k}(G)
  := partial_s^k (mathsf P_infty M_zeta G)(rho).
```

Using the zero-evaluator vector and the fact that `mathsf P_infty` is a
transported orthogonal projection,

```tex
L_{rho,k}(G)
  = <mathsf P_infty M_zeta G, y_{rho,k}>
  = <M_zeta G, mathsf P_infty y_{rho,k}>.
```

Surjectivity requires this functional to be nonzero for some legal `G`.
Refutation requires `mathsf P_infty y_{rho0,k0}` to lie in
`(M_zeta B)^perp` for some specific `(rho0,k0)`.

## Attempted Structural Refutations

U1a pairing/duality:
The inherited range statement is only
`Ran mathsf P_infty = U_infty(S_lambda)`, with
`S_lambda = ker P_lambda cap ker Phat_lambda`.  This is support-Fourier Sonin
geometry, not an orthogonality theorem against `M_zeta` times legal Burnol
profiles.

U1b zero-evaluator structure:
Step153 gives the unprojected evaluator
`y_{rho,k}=T_a^* partial^k K_a^Gamma(.,rho)`.  It does not say
`mathsf P_infty y_{rho,k}` remains a zero-evaluator atom or a
zero-annihilating span.

U1c idempotency:
`P=P^*P` only rewrites the same pairing:
`<P M_zeta G,y>=<M_zeta G,P y>`.  It gives no commutation with `M_zeta`, no
zeta-ideal invariance, and no cancellation.

U1d specific zero:
At `rho1 = 1/2 + 14.134725...i`, `k=0`, Steps102/104/105 give prolate and
Calkin/compactness records, while Steps142/143/144 give Omega-density and tail
records.  None contains a rho-labelled matrix element or cancellation identity.

## Non-Kernel Constructive Attempt

`G=Y_{rho0,k0}` is not legal input; it is an evaluator-side vector.  Even if
tested formally, it requires `<M_zeta Y, P y>`.

`G=1` is not a Step119 legal Burnol profile with endpoint vanishings.  Its
unprojected zero jet vanishes below multiplicity, and the projected test
requires `<zeta, P y>`.

## Consequence

`target_equivalence_consequence = kernel_required_not_decided`.

Step 171 does not prove target-equivalence to RH and does not produce a
specific sharper-than-RH obstruction.  The Step 170 zero-free-output subclass
remains the retained conditional result.  Retained no-gos remain unchanged:
public-shadow non-promotion, finite-window Calkin blindness, auxiliary-GRH
smuggling, incomplete character spectrum support-only, scalar identity not
carrier identity, and ledger-relative Hecke non-comparability.
