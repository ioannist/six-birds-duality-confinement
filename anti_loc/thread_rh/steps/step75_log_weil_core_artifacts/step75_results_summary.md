# Step 75: Candidate Log-Side Weil Core and Completion Gate

This step proposes a concrete log-side candidate for the completed anti-invariant response core needed by the RH Weil--Douglas bridge.

The candidate core is

\[
\mathcal C^-_{\log}=\{f\in C_c^\infty(\mathbb R): Jf=-f\},\qquad (Jf)(t)=\overline{f(-t)}.
\]

The completed carrier-side feature map is organized as

\[
W_{\rm cmp}=\begin{bmatrix}W_{\rm pr}\\ W_\infty\\ W_{\rm pole}\\ W_{\rm tail}\end{bmatrix},
\qquad
K_{\rm cmp}=W_{\rm cmp}^*W_{\rm cmp}.
\]

Main slots:

- `prime-power`: positive finite shift-difference features at cutoff.
- `archimedean/gamma`: positive renormalized shift-difference feature with kernel shaped like \((2\sinh(|a|/2))^{-1}\).
- `pole/completion`: finite-dimensional moment/null-mode feature.
- `tail/support`: positive or defect feature tracking omitted shifts, support leakage, and finite-to-completed promotion.

Main theorem:

If the core inequality

\[
q_Z[f]\le q_{\rm cmp}[f]
\]

holds on a dense anti-invariant core and the completed carrier form is closable with this core as a form core, then

\[
V_Z^*V_Z\preceq W_{\rm cmp}^*W_{\rm cmp},
\]

and hence, by Douglas factorization,

\[
V_Z=T W_{\rm cmp},\qquad \|T\|\le1.
\]

Status: this is a candidate core and gate structure, not an RH proof. The positive feature template is credible; the missing work is exact matching to the completed zeta explicit formula and proving the Douglas domination.
