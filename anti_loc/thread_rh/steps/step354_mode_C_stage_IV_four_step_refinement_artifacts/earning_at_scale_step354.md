# Step 354 Earning-Its-Keep At Scale

The prior typed-condition catalog gives H6 the degenerate verdict
`V-NC bridge-failure`: it says no inherited Hecke-to-Burnol/Sonine bridge is
available, but it does not provide a finite residual calculus to measure
partial bridge attempts.

Mode C OL provides intermediate content not present in that catalog:

1. A computable residual:
   `lambda_obs(chi,k,j) = |log(H_chi,k/Z_rho_j,k)|`.
2. A load-bearing descent gate: nonzero `lambda_obs` blocks descent.
3. A transfer-search objective:
   minimize `sum lambda_obs(T_theta)^2`.
4. A failure diagnosis:
   step 353 showed weighted geometric transfer closes in-sample magnitude
   residuals but fails target hold-out.
5. A refinement path:
   step 354 decomposes the residual into magnitude, phase, and
   operator-compatibility components.

This is intermediate structural content: it does not solve H6, but it turns a
catalog-level bridge failure into a measurable residual program with
converse probes and ablation tests.
