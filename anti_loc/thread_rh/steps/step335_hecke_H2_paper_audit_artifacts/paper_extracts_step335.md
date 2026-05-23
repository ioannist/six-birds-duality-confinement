# Step 335 Paper Extracts — Hecke H2

H2 cascade need:

> source lower-frame F_n >= Lambda_n (Theta_0^-)^{-1}, Lambda_n -> infinity, plus Plancherel tail/exhaustivity.

## Soundararajan 2000

Source: *Nonvanishing of quadratic Dirichlet L-functions at s=1/2*, arXiv:math/9902163.

Verbatim extract, Introduction/Theorem 1:

> "For at least 87.5% of the odd square-free integers"

Paper-grounded role: supplies strong nonvanishing/lower-bound machinery for quadratic primitive Dirichlet characters via mollified first/second moments. It also invokes a large sieve lemma for real primitive characters with conductor bounded by Q.

Audit conclusion: lower-bound machinery exists, but not in the H2 operator lower-frame form.

## Conrey-Soundararajan 2002

Source: *Real zeros of quadratic Dirichlet L-functions*, arXiv:math/0111013.

Verbatim extract, Introduction:

> "a positive proportion of quadratic Dirichlet L-functions"

Paper-grounded role: establishes positive-proportion zero-free/nonvanishing results and uses large-sieve inputs plus mollifier constraints.

Audit conclusion: supports source lower-bound diagnostics and conductor-uniform estimates in a specific family; not an H2 lower-frame theorem.

## Conrey-Iwaniec-Soundararajan 2011

Source: *Asymptotic Large Sieve*, arXiv:1105.1176.

Verbatim extract, Abstract:

> "linear forms in primitive Dirichlet characters"

Paper-grounded role: directly addresses primitive-character averaging and asymptotic large-sieve bilinear forms. It defines an averaging operator over primitive characters of conductor about Q.

Audit conclusion: supplies the closest Plancherel-tail/exhaustivity framework, but not the exact cascade tail ledger.

## Khan-Ngo 2015

Source: *Nonvanishing of Dirichlet L-functions*, arXiv:1512.04030.

Verbatim extract, Abstract:

> "at least 3/8 of the primitive Dirichlet characters"

Paper-grounded role: shows modern mollifier lower-bound/nonvanishing machinery for primitive characters of large prime modulus.

Audit conclusion: reinforces the lower-bound side of H2, while remaining family-specific.

## Iwaniec-Sarnak 2000

Source: IAS public page and fetched PDF, *Perspectives on the Analytic Theory of L-functions*.

Verbatim extract from IAS page:

> "Perspectives on the Analytic Theory of L-Functions"

Paper-grounded role: broad perspective source. The fetched PDF was public, but `pdftotext` produced only form-feed characters in this environment, so no section-level extracts were used.

## H2 Resolution Boundary

The literature contains:

- positive-proportion nonvanishing and mollifier lower-bound technology;
- large-sieve and asymptotic large-sieve averaging over primitive characters;
- conductor-bounded character-family estimates.

The literature audit did not find:

- an explicit source lower-frame `F_n >= Lambda_n (Theta_0^-)^{-1}`;
- a proof of `Lambda_n -> infinity` in the cascade's operator notation;
- a full Plancherel tail/exhaustivity ledger integrated with that lower-frame.
