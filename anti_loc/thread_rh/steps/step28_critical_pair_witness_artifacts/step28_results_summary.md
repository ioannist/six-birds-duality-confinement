# Step 28: Critical-Pair and Recombination Witnesses

## Result

This step proves that the accepted probe-family anti-localization gate

\[
\mathsf K_{C,\Gamma}(L)\preceq \Theta
\]

is equivalent to the absence of native recombination witnesses.

Given

\[
\mathsf D=\mathsf K-\Theta,
\]

the family gate fails iff there exists a recombination vector \(y\) such that

\[
y^*\mathsf D y>0.
\]

The maximum additive violation is

\[
\lambda_{\max}(\mathsf K-\Theta),
\]

and, when \(\Theta\succ0\), the maximum relative violation is

\[
\lambda_{\max}(\Theta^{-1/2}\mathsf K\Theta^{-1/2})-1.
\]

## Minimal critical pairs

If the declared response family has coordinates, every failure has a support-minimal witness support \(S\). For such a minimal support,

\[
\lambda_{\max}(\mathsf D_S)>0,
\]

while all proper principal submatrices are nonpositive. By eigenvalue interlacing, \(\mathsf D_S\) has exactly one positive eigenvalue.

## Two-anchor criterion

For

\[
\mathsf D_S=\begin{pmatrix}a&c\\ \bar c&b\end{pmatrix},
\qquad a\le0,
\qquad b\le0,
\]

the scalar probes pass, but the two-anchor recombination fails iff

\[
|c|^2>ab.
\]

This is the exact matrix criterion for the cancellation needle.

## Cyclic witnesses

For

\[
\mathsf D_k=-I_k+c(J_k-I_k),
\]

if

\[
\frac1{k-1}<c\le \frac1{k-2},
\]

then the full \(k\)-anchor recombination is a minimal critical pair: every proper support passes, but the full all-ones recombination fails.

## Protocol and predictive witnesses

If protocol-local blocks pass but the stacked block fails, every support-minimal witness must cross protocol blocks. Therefore route-local budgets do not certify route-union anti-localization.

For predictive families, the gate

\[
\widehat K_j\preceq\Theta\quad\forall j
\]

fails iff there is a future witness \((j,y)\) with

\[
y^*(\widehat K_j-\Theta)y>0.
\]

## Completion obligation

A critical-pair witness is not merely a counterexample. It is a closure obligation. If a formed closure claims accepted anti-localization and a witness exists, then one must:

1. exclude the recombination from the native family with a nonclaim record;
2. rewrite the package/audit carrier;
3. raise the budget and weaken the claim; or
4. downgrade the status.

Ignoring the witness is an overread.

## Interpretation

Family anti-localization is a completion statement. The layer membrane is intact exactly when all native recombination critical pairs have been resolved, priced, or lawfully excluded.
