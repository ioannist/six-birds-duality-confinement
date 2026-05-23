# Step 170 Results Summary

Verdict: `V_subclass_proved`.

The inherited `P_infty` is not a projection onto a zeta-zero spectral region. The exact records identify it as the imported archimedean Sonin/prolate projection. In the raw archimedean model, Step 104 defines `H=L^2(R)` (or the even subspace), `P_lambda` as spatial cutoff onto `[-lambda,lambda]`,
`\widehat P_lambda=F^{-1}P_lambda F`, the Sonin space
`\mathcal S_lambda=ker P_lambda cap ker \widehat P_lambda`, and `S_lambda` as the orthogonal projection onto `\mathcal S_lambda`. Steps 102, 103, 153, 154, and 162 then use this imported projection as `P_infty`, with Mellin-side representative `mathsf P_infty=U_infty P_infty U_infty^{-1}`.

The direct full-carrier identity

```tex
\mathsf P_\infty M_\zeta G = M_\zeta A_\infty G
```

is therefore a zeta-ideal invariance property of the Sonin/prolate projection. It is not, from the inherited records alone, logically equivalent to absence of zeta zeros in a projection range.

The target-equivalence test gives `not_target_equivalent`: full ZI-COV would imply zero-jet cancellation

```tex
(\mathsf P_\infty M_\zeta G)^{(k)}(\rho)=0
```

for all legal `G` and zeta-zero labels in the evaluation region, but this is a property of `mathsf P_infty`. It does not imply that `zeta` has no zeros unless one adds a non-inherited jet-surjectivity assumption for the projected range.

The proved subclass is the zero-free-output subclass. Let `Omega` be a measurable region in the Mellin boundary/strip on which `1/zeta` is bounded, and restrict to legal profiles `G` such that

```tex
\mathsf P_\infty M_\zeta G
```

has support in `Omega` and remains in the legal Mellin carrier. Then

```tex
A_\infty^\Omega G
= M_{1/\zeta}\mathsf P_\infty M_\zeta G
```

is a bounded operator on this subclass and

```tex
\mathsf P_\infty M_\zeta G
= M_\zeta A_\infty^\Omega G.
```

This proves ZI-COV(i) on that subclass only. It does not close `Xi_BC` and does not prove the full ZI-COV lemma.
