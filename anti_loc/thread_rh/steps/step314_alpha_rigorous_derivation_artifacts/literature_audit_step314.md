# Step 314 Literature Audit: zeta-derivative ratios at zeros

Target needed for Branch C:

`arg(zeta^(j+1)(rho_1)/zeta^(j)(rho_1))` must admit a uniform phase
bound or asymptotic near `j ~= k/2`.  The needed statement is pointwise
in a fixed zero `rho_1` and high derivative order `j`.

## Sources checked

1. Conrey--Snaith, "Applications of L-functions Ratios Conjectures"
   PDF: https://web.williams.edu/Mathematics/sjmiller/public_html/ntandrmt/handouts/conrey/ConreySnaith_AppLFnsRatiosConj.pdf

   Relevant extract: Section 7 is "Discrete moments of the Riemann zeta
   function and its derivatives"; the paper says that "another kind of
   average" is "a discrete moment summing the zeta function, or its
   derivatives, at or near the zeros" and treats moments such as
   `|zeta'(rho)|`.  This gives averaged moment context, not a pointwise
   phase-ratio bound for `zeta^(j+1)(rho_1)/zeta^(j)(rho_1)`.

2. Conrey--Rubinstein--Snaith, "Moments of the derivative of the Riemann
   zeta-function and of characteristic polynomials"
   arXiv: https://arxiv.org/abs/math/0508378
   PDF: https://people.maths.bris.ac.uk/~mancs/papers/deriv.pdf

   Relevant extract: the abstract says the authors investigate "moments
   of the derivative" and formulate a conjecture for moments of the
   derivative of the Riemann zeta-function on the critical line.  The
   paper models derivative moments and zeros of zeta-prime, not high-order
   derivative-ratio phases at a fixed zero.

3. Hughes--Keating--O'Connell, "Random matrix theory and the derivative
   of the Riemann zeta function"
   PDF: https://maths.ucd.ie/~noconnell/pubs/hko00.pdf

   Relevant extract: the paper states that random matrix theory is used
   to model "discrete moments of the derivative of the Riemann zeta
   function" evaluated at the zeros.  Again this concerns distribution
   and moment models, not a deterministic phase-ratio bound.

4. Hughes--Pearce-Crump, "Complex moments of the derivative of the
   Riemann zeta function"
   arXiv: https://arxiv.org/abs/2509.07788

   Relevant extract: the abstract says it conjectures complex moments of
   `zeta'` evaluated at non-trivial zeros, via random-matrix and hybrid
   approaches.  This is closer to phase-sensitive information, but still
   moment-level and conjectural; it does not provide a pointwise bound for
   `arg(zeta^(j+1)/zeta^(j))` at a fixed zero.

5. Hughes--Pearce-Crump, "Integer moments of the derivatives of the
   Riemann zeta function"
   arXiv: https://arxiv.org/abs/2509.07792

   Relevant extract: the abstract says it conjectures a full asymptotic
   expansion for products of zeta functions at non-trivial zeros, then
   differentiates shifts to obtain integer moments of mixed derivatives.
   This is relevant background for mixed derivative moments, but it is
   conjectural and averaged, not the uniform fixed-zero phase control
   needed here.

## Audit conclusion

The literature contains substantial moment and ratios-conjecture evidence
for zeta derivatives at or near zeros, but I did not find a classical
theorem giving a pointwise, high-order derivative-ratio phase bound of the
form needed for Step 314:

`arg(zeta^(j+1)(rho_1)/zeta^(j)(rho_1)) = theta_zeta(j) + O(error)`

uniformly in `j` near `k/2`.

Therefore the alpha formula is numerically verified, but the rigorous
phase-control component remains open.

