
# Step 102 summary: Semilocal projection residual derivation

## Main result

Let \(P_\infty\) be the archimedean Sonin/prolate projection and let \(P_S\) be the semilocal projection.  Transport \(P_S\) back to the archimedean response space.  The transported projection is not generally the same as \(P_\infty\), because the semilocal Hardy--Titchmarsh carrier changes the Hilbert metric.

Let the pulled-back semilocal metric be

\[
A_S=\theta_S^*\theta_S.
\]

With

\[
H_\infty=M\oplus M^\perp,
\qquad
M=\operatorname{Ran}P_\infty,
\]

write

\[
A_S=
\begin{pmatrix}
A_{MM}&A_{MN}\\
A_{NM}&A_{NN}
\end{pmatrix}.
\]

Then the transported semilocal projection is the \(A_S\)-orthogonal projection onto \(M\), and

\[
\boxed{
\mathcal R_S
=
U_SP_SU_S^{-1}-P_\infty
=
\begin{pmatrix}
0&A_{MM}^{-1}A_{MN}\\
0&0
\end{pmatrix}.
}
\]

So compactness of the projection residual is exactly the compactness of the off-diagonal metric-mixing block:

\[
\boxed{
\mathcal R_S\text{ compact}
\iff
P_\infty A_S(I-P_\infty)\text{ compact}.
}
\]

## Interpretation

The semilocal local-factor deformation does not itself prove compactness.  Bounded transport preserves compactness, but a raw nonzero multiplier on a non-atomic \(L^2\) space is not compact.

The actual compactness target is therefore:

\[
\boxed{
P_\infty A_S(I-P_\infty).
}
\]

This block measures how much the semilocal metric mixes the archimedean Sonin/prolate sector with its orthogonal complement.

If this block is compact, then \(\Delta_S\) is compact-after-quotient up to finite-rank pole/null records and declared tails.

If it is not compact, the noncompact sector is precisely what the Hecke/Dirichlet source ladder must cover.

## Numerical sanity checks

Finite-dimensional toy checks verify the block formula and show the qualitative distinction:

- finite-rank metric mixing gives finite-rank residual;
- decaying off-diagonal singular values give compact-like residual;
- nondecaying singular values give noncompact-like residual.

These are only algebra sanity checks, not RH evidence.
