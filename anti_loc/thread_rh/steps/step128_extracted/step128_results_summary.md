
# Step 128: q-aspect twisted second moment as a matrix lower-frame theorem

## Verdict
The Bui--Pratt--Robles--Zaharescu twisted second moment is the right first analytic-number-theory platform for the source-weighted matrix lower frame.

It studies

\[
\sum_{\chi\bmod q}^{+}
|L(1/2,\chi)|^2
\left|\sum_{n\le q^\kappa} a_n\chi(n)n^{-1/2}\right|^2
\]

for arbitrary Dirichlet-polynomial coefficients and reaches

\[
\kappa<51/101=1/2+1/202.
\]

But it does **not automatically** give the membrane source record. The project needs the theorem in matrix lower-frame form:

\[
G_{q,w}\succeq \gamma_{q,w}H_N
\]

uniformly over every residual coefficient vector.

## Conditional import theorem
If the published asymptotic can be rewritten as

\[
a^*G_{q,w}a=M_q(a)+E_q(a)
\]

with

\[
M_q(a)\ge c_0(\log q)\|a\|_{H_q}^2
\]

and

\[
|E_q(a)|\le \varepsilon_q c_0(\log q)\|a\|_{H_q}^2,
\qquad \varepsilon_q<1,
\]

then

\[
G_{q,w}\succeq (1-\varepsilon_q)c_0(\log q)H_q.
\]

So normalized source strength is of order \(\log q\). Unnormalized source strength is of order \(q\log q\), subject to the source-currency audit.

## What remains new
The existing analytic NT theorem supplies a scalar/bilinear asymptotic for arbitrary coefficients. The framework still needs:

1. homogeneous coefficient normalization;
2. positivity of the shifted main kernel after \(\alpha,\beta\to0\);
3. operator-norm error subordinate to the main term;
4. parity/primitive/principal-character defect records;
5. compatibility with the Burnol-to-Dirichlet shadow length;
6. fixed/exhaustive residual-tail promotion.

## Route status
This step imports the standard q-aspect twisted-second-moment platform and isolates the project-native gap:

\[
\text{arbitrary-coefficient moment asymptotic}
\quad\not\Rightarrow\quad
\text{matrix lower frame without a lower-eigenvalue audit.}
\]

## Next step
Step 129 should audit the main term itself: take the Bui--Pratt--Robles--Zaharescu shifted main term, pass to \(\alpha,\beta\to0\), and decide whether the resulting kernel has a uniform positive lower bound on the residual coefficient class.
