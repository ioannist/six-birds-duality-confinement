# Step 100: Semilocal Plancherel/Exhaustivity Instantiation

This step chooses the Tier-1 carrier:

\[
Y_S^- = L^2(\mathbb R, dm_S)^-,\qquad dm_S(\xi)=\left|\prod_{v\in S}L_v(1/2-i\xi)\right|^2d\xi.
\]

It turns the abstract Step 99 promotion theorem into concrete semilocal records:

- finite windows \(\Pi_{S,T,N}:Y_S^-\to Y_{S,T,N}^-\), built from spectral cutoffs and semilocal cyclic-pair/prolate/orthogonal-polynomial windows;
- inverse-budget tail forms \(\mathsf T_{S,T,N}\);
- finite-window source frames \(\mathsf F^{\rm win}_{S,T,N}\);
- the completed promotion inequality

\[
\mathsf F_{S,T,N}+\Lambda_{S,T,N}\mathsf T_{S,T,N}
\succeq
\Lambda_{S,T,N}(\Theta_{0,S}^-)^{-1}.
\]

The active analytic target remains:

\[
\Delta_S^+\preceq \mathsf F_{S,T,N}+E_{\rm abs,S,T,N}.
\]

## Most important theorem

If finite-window source frames satisfy a lower-frame inequality and the tail is exhaustive on the completed zero ledger, then the finite-window character/source evidence promotes to a completed anti-invariant source lower frame.

## Compactness shortcut

If \(\Delta_S^+\) is compact on \(Y_S^-\), absorption reduces to finite-window domination plus a vanishing compact tail. If compactness fails, the non-compact residual sector becomes the next source-frame target.

## Status

This step does not prove RH. It instantiates the concrete semilocal carrier and tells us exactly what has to be proved next.
