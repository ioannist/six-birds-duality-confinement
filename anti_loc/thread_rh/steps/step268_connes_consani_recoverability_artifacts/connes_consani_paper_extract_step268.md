# Connes-Consani Paper Extracts for Step 268

Sources fetched:

- Connes-Consani 2014, `arXiv:1405.4527`, "The Arithmetic Site".
- Connes-Consani 2018, `arXiv:1805.10501`, "The Riemann-Roch strategy, Complex lift of the Scaling Site".

Only constructions relevant to the Branch A recoverability attempt are recorded.

## Connes-Consani 2014: Arithmetic Site

Definition of the arithmetic site:

```tex
\arith = \widehat{\N^\times}
\quad\text{with structure sheaf}\quad
\bar\N=(\N\cup\infty,\inf,+).
```

Points over \(\coo\):

```tex
\text{points over }\coo \text{ form }
\Q^\times\backslash\A_\Q/\hat\Z^*.
```

The Frobenius automorphisms correspond to the idèle-class action on this quotient.

Trace formula used in the Hasse-Weil count:

```tex
\mathrm{Tr}_{\rm distr}\left(\int_G h(u)U_u\,d^*u\right)
=\sum_{v\in\Sigma_\Q}\int_{\Q_v^*}
\frac{h(u^{-1})}{|1-u|}\,d^*u.
```

Main zeta theorem:

```tex
\frac{\partial_s\zeta_N(s)}{\zeta_N(s)}
=-\int_1^\infty N(u)u^{-s}d^*u,
\qquad
\zeta_N(s)=\zeta_\Q(s)=\pi^{-s/2}\Gamma(s/2)\zeta(s).
```

## Connes-Consani 2018: Map \(E\)

The zeta-side summation map:

```tex
E(f)(v):=\sum_{n\in\N^\times} f(nv).
```

The paper explains that after Fourier transform in the logarithmic variable,
this becomes multiplication by

```tex
\sum e^{-is\log n}=\zeta(is).
```

This gives a spectral realization route for zeta zeros through the cokernel of
the map \(E\).

## Connes-Consani 2018: Scaling Site

The Scaling Site is recorded as:

```tex
\scal2=(\rnt,\mathcal O).
```

The sections of \(\mathcal O\) are:

```tex
convex, piecewise affine functions with integral slopes.
```

The point theorem:

```tex
\text{points of }\rnt
\simeq \Q^\times\backslash\A_\Q/\hat\Z^*.
```

## Connes-Consani 2018: Riemann-Roch Strategy

The RH criterion is:

```tex
{\rm RH} \iff \langle f,f\rangle \leq 0
\quad\text{for}\quad
\int f(u)d^*u=\int f(u)du=0.
```

The divisor expression:

```tex
\langle f,f\rangle=D\bullet D,
\qquad
D:=\int f(\lambda)\Psi_\lambda\,d^*\lambda.
```

## Connes-Consani 2018: Complex Lift

The complex lift uses:

```tex
C(G):=\Q^*\backslash(\A_\Q\times G)/(\hat\Z\times{\rm id}).
```

## Extract Assessment

The papers provide adelic/scaling-site geometry, the map \(E\), a distributional
trace formula, a Hasse-Weil-style complete-zeta count, an RH quadratic-form
criterion, and a complex lift of the scaling site.

They do not provide:

- an embedding of the Burnol/Sonine carrier into the scaling-site framework;
- a formula for the Burnol projection \(P_\lambda\) in the Connes-Consani data;
- an operator identity for \([M_\zeta,P_\lambda]\);
- a Hochschild or cyclic trace identity computing the cascade value
  \(\Phi_{\max}=0.4904766190\).

Thus the cascade-needed recoverability claim is not a direct Connes-Consani
theorem.
