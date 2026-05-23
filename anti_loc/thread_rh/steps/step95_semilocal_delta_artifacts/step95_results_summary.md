# Step 95 — Extracting the Semilocal Cross-Term Operator \(\Delta_S\)

## Purpose

This step executes the first construction move of the hybrid semilocal RH program. The archimedean/gamma slot is now treated as an imported Connes--Consani positivity record. The new task is to place the actual semilocal Weil form and the candidate positive feature package on the same response core and extract the remaining cross-term

\[
\Delta_S=q_{\mathrm{Weil},S}-q_{\mathrm{pos},S}.
\]

This is the analytic object that must be shown nonpositive, defect-paid, or absorbed by a Hecke/Dirichlet source frame.

## Semilocal core

For a finite set of places \(S\) with \(\infty\in S\), use the semilocal Hardy--Titchmarsh transform. On the Mellin side, the semilocal injection inserts local Euler factors:

\[
F_\mu w_S(\eta_S f)(\xi)
=
\prod_{p\in S\setminus\{\infty\}} L_p(1/2-i\xi)\,F_\mu w_\infty f(\xi).
\]

Thus the natural response space is

\[
Y_S=L^2(\mathbb R,dm_S),
\qquad
 dm_S(\xi)=\left|L_\infty(1/2-i\xi)\prod_{p\in S_f}L_p(1/2-i\xi)\right|^2d\xi.
\]

The core used in this step is

\[
\mathcal C_S^-=V_S\eta_S(\mathcal S_0(\mathbb R)^{\mathrm{ev}})\cap Y_S^-.
\]

## Extracted object

The signed semilocal Weil form is pulled to the response core:

\[
q_{\mathrm{Weil},S}[y]=QW_S(V_S^{-1}y,V_S^{-1}y).
\]

The candidate positive form is

\[
q_{\mathrm{pos},S}
=
q_\infty^{\mathrm{CC}}
+
q_{\mathrm{pr},S}^{\mathrm{pair}}
+
q_{\mathrm{pole},S}^{+}
+
q_{\mathrm{tail},S}^{+}.
\]

Then

\[
\boxed{\Delta_S=q_{\mathrm{Weil},S}-q_{\mathrm{pos},S}.}
\]

Its positive part is the cross-term obstruction.

## Main theorem

If

\[
q_Z\le q_{\mathrm{Weil},S}+e_{\mathrm{Weil},S}
\]

and

\[
\Delta_S\le e_{\Delta,S},
\]

then

\[
q_Z\le q_{\mathrm{pos},S}+e_{\mathrm{Weil},S}+e_{\Delta,S}.
\]

So the semilocal Weil--Douglas bridge reduces to controlling \(\Delta_S\).

## Source absorption route

The source route is:

\[
\Delta_S^+\preceq F_n+E_{\mathrm{abs},n},
\]

where

\[
F_n=
\sum_{s\in\mathcal S_n}\lambda_sQ_s^*\Theta_s^{-1}Q_s.
\]

If

\[
F_n\succeq\Lambda_n(\Theta_0^-)^{-1},
\qquad
\Lambda_n\to\infty,
\]

then the cross-term is absorbed into the anti-invariant source-coercivity ladder.

## What \(\Delta_S\) contains

\(\Delta_S\) contains five mismatch records:

1. semilocal measure deformation by finite local Euler factors;
2. nonunitary semilocal injection \(\eta_S\), so semilocal grading differs from archimedean grading;
3. prime--archimedean cross-term from multiplicative local-factor insertion versus additive positive features;
4. pole/completion/null-mode records;
5. tail and finite-to-completed promotion defects.

## Sanity checks

The toy matrix checks only verify the algebraic gate, not RH.

- The identity \(K_{\mathrm{Weil}}-K_{\mathrm{pos}}=\Delta\) held to numerical roundoff.
- A full-sector source frame absorbs \(\Delta^+\).
- A partial source frame can leave a hidden positive cross-term uncovered.
- Finite local factors visibly deform the semilocal response measure.

## Bottom line

Step 95 makes the hybrid semilocal target concrete:

\[
\boxed{\text{compute or bound }\Delta_S.}
\]

The next step should inspect this object against the Connes--Consani semilocal Hardy--Titchmarsh/prolate machinery and decide whether \(\Delta_S\) is naturally a compact/finite-rank defect, a source-absorbable form, or a genuine obstruction.
