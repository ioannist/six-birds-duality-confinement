# Step 112 summary

Step 112 defines a non-smuggled Burnol/co-Poisson atom family for the coefficient-visibility side of the RH source route.

The key correction to the previous framing is:

c_N is not a column-norm condition on a fixed map. It is a spanning residual for a constructible family.

Main finite identity:

R_N^* H_N R_N = M_N^* P_N M_N = G_{B,N} - E_{coef,N}^* E_{coef,N}.

Thus

c_N = 1 - || E_{coef,N} G_{B,N}^(-1/2) ||^2.

The declared Burnol atom family uses compactly supported generators g_{nu,N} on [a,A], A=1/a, with right-Mellin vanishings at 0 and 1. Its co-Poisson image is

C_a(g)(x)=sum_{n>=1} g(x/n)/n - \hat g(1).

With both vanishings, the image is a legal Sonine/co-Poisson atom.

Toy audit:
- best c_N in sweep: 0.2175
- final epsilon_N at 96 atoms: 0.8854
- final c_N at 96 atoms: 0.216

The toy audit is not RH evidence. It only tests the spanning-residual gate.

Next step:
Step 113 should attempt the actual Burnol density/visibility theorem: prove that declared co-Poisson atoms are dense in the relevant boundary-packet sector, or isolate the residual subspace.
