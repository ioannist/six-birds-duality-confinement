# Step 388 Large-Sieve H6 Attack

## External Anchor

Conrey-Iwaniec-Soundararajan 2011, arXiv:1105.1176, "Asymptotic Large Sieve", gives asymptotics for bilinear / quadratic averages over primitive Dirichlet characters of Dirichlet-polynomial linear forms.  The usable schematic form is

`sum_chi |sum_n alpha_n chi(n)|^2 = diagonal main term + controlled off-diagonal/asymptotic terms`

provided the coefficient sequences and family parameters satisfy the paper's support and averaging hypotheses.

## Cascade Hecke Linear Form

For `h_chi(s)=L(s,chi) M(G_star)(s)`,

`h_chi^(k)(rho_chi) = sum_{n>=1} alpha_n^{(chi,k)} chi(n)`,

formally with

`alpha_n^{(chi,k)} = n^{-rho_chi} sum_{j=0}^k binom(k,j) M(G_star)^{(k-j)}(rho_chi)(-log n)^j`.

This is the requested linear-form structure, but it is not a CIS-ready family because `alpha_n` depends on `chi` through `rho_chi`.

## Applicability Result

The asymptotic large sieve needs a common coefficient sequence over the character family.  The cascade data evaluates each character at its own first zero, so the coefficient sequence changes with the character.  The available seven-character set is also finite, low-conductor, and far outside the asymptotic conductor family needed by the theorem.

## Verdict

The large-sieve route is technically meaningful only after a new cascade implementation fixes a common spectral parameter or rewrites the evaluator by an approximate functional equation with common coefficients.  With the present Step 320-322 data, it does not construct an averaged H6 bridge.
