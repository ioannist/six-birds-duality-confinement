# Conrey--Li survival test for the RH membrane construction

Conrey--Li show that natural de Branges-type positivity conditions associated with `xi(s)` and `1/xi(s)` fail for zeta and Dirichlet L-functions. Therefore any RH membrane positivity ansatz must pass this test:

1. It must not imply the de Branges `H(E)` positivity condition that Conrey--Li disprove.
2. It must not imply the `F(W)` positivity condition that Sarnak's argument refutes.
3. If it uses an RKHS, the RKHS must be carrier-native and quotient/completion aware, not the naive `E(z)=xi(1-iz)` or `W(z)=1/xi(1-iz)` construction.
4. If it uses a positivity form, it must be semilocal/adelic, paired-feature, source-coercive, or explicitly scoped.
5. Trace equality, finite tests, and public signatures are insufficient.

Pass condition for our Tier-1 route: importing Connes--Consani's archimedean positivity and working semilocally should not entail the false de Branges conditions, because the carrier is a Sonin/prolate compression / semilocal trace record rather than the naive zeta RKHS.
