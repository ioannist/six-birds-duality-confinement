# Step 437 Proof Attempt and Diagnosis

## 1. Counting asymptotics

Margulis gives, for compact negatively curved `X`,

```text
pi_X(T) = #{gamma primitive : ell(gamma) <= T} ~ exp(hT)/(hT).
```

The prime number theorem gives

```text
pi(exp T) ~ exp(T)/T.
```

Thus the leading term is compatible after metric rescaling to entropy `h=1`. Leading asymptotics alone do not prove mismatch.

## 2. Error-structure mismatch

For arithmetic-independent Anosov/geodesic systems, the refined orbit-counting error comes from spectral data of the transfer operator: topological pressure, mixing rates, and Pollicott-Ruelle resonances. These are substrate-specific dynamical invariants.

For rational primes, the refined explicit formula error is governed by zeros of the Riemann zeta function. Under RH it has square-root cancellation shape in `x`, and in `T=log x` it is controlled by oscillations `exp((1/2+i gamma)T)`.

A generic geodesic-flow resonance spectrum is not the zeta-zero spectrum. Therefore even when `h=1`, the second-order trace data are structurally different.

## 3. Pointwise length mismatch

In analytic families of hyperbolic surfaces, each closed geodesic length is a real-analytic function of Fenchel-Nielsen or equivalent geometric parameters. Requiring `ell(gamma_n)=log p_n` for all `n` imposes infinitely many analytic equations. Without an arithmetic mechanism, finite truncation matches are nongeneric and full equality is a measure-zero / meagre condition, not a structurally natural output.

This proves a generic no-go, not an absolute no-go over all conceivable synthetic systems.

## 4. Lafont-McReynolds dichotomy

Lafont-McReynolds show that every noncompact arithmetic hyperbolic 2- or 3-manifold has arbitrarily long arithmetic progressions in its primitive length spectrum. The result is not a direct proof that `{log p}` cannot occur, but it anchors the relevant dichotomy: arithmeticity leaves rigid length-spectrum fingerprints. Non-arithmetic systems do not inherit those fingerprints generically.

## 5. Sunada cross-check

Sunada isospectral non-isometric examples show length spectra do not uniquely determine geometry. This weakens any attempt to infer substrate from lengths alone, but it does not rescue the Route 2 construction: the problem is not uniqueness of substrate; it is deriving the specific prime-log length set without arithmetic primitives.

## Diagnosis

The full universal theorem candidate resists because `arithmetic-independent` is a design-prohibition notion rather than a formal invariant of all possible dynamical systems. The theorem-grade conclusion is instead a generic no-go plus a sharpened active constraint.
