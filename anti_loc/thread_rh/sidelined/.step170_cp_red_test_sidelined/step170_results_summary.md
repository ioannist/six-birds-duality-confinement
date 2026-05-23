# Step 170 Results Summary

Verdict: `V_CPRED_STUCK`.

The explicit legal generator is `G170_1`, supported in [0.40,0.70] union [0.90,1.30] union [1.70,2.30] subset [1/4,4]. It is
constructed from three fixed smooth bumps
`beta_{r,R}(t)=exp(-(R-r)^2/((t-r)(R-t)))` on `r<t<R`, zero otherwise:

`g(t)=beta_{0.40,0.70}(t)-2.42572377955429 beta_{0.90,1.30}(t)+1.11714918636953 beta_{1.70,2.30}(t), beta_{r,R}(t)=exp(-(R-r)^2/((t-r)(R-t))) on r<t<R and 0 otherwise`.

The computed moment checks are

- `ghat(0) = 0.0000000000000000e+00`
- `ghat(1) = 8.6736173798840355e-19`

so the inherited Step 119 co-Poisson legality conditions hold to numerical
quadrature precision. The corresponding legal Burnol atom is
`u_G := Cg`, with
`Cg(t)=sum_{n>=1} g(t/n)/n - ghat(1)`.

For the first test generator and shift `ell=log(2)`, the inherited Step 169
subclass computation gives the transported packet

`For u_G=Cg and G(s)=ghat(s): M(J_a P_infty tau_log2 (I-P_infty) u_G)(s)=[T_{1/4} mathsf P_infty M_{2^{s-1/2}}(I-mathsf P_infty) M_zeta G](s). Expanded: [T_{1/4} mathsf P_infty M_zeta(2^{s-1/2}G)](s)-[T_{1/4} mathsf P_infty M_{2^{s-1/2}} mathsf P_infty M_zeta G](s).`

The co-Poisson target for the same generator has
`M(Cg)(s)=zeta(s)G(s)`. The numerical Mellin samples in
`mellin_samples_step170.csv` include the first nontrivial zeta-zero ordinate;
there the target `zeta(s)G(s)` is zero to quadrature precision.

The comparison halts before a POS/NEG/PART verdict: the inherited records do
not give the exact action of `mathsf P_infty` or `T_a` on the explicit profile
`M_zeta G`, nor a zeta-ideal covariance statement for those operators. Thus
the computation neither establishes a legal `h` with transported packet `C h`
nor proves that no such `h` exists.
