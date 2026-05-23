# Step 76 — Weil Matching Equations for the Log-Side Feature Core

This step states the exact matching problem between the candidate positive log-side feature maps and the classical completed Weil explicit formula.

The key algebraic identity is

\[
\|\tau_a f-f\|_2^2=2\|f\|_2^2-2\operatorname{Re}\langle f,\tau_a f\rangle.
\]

Therefore positive shift features contain both a correlation term and a diagonal mass term. Matching a signed prime-power correlation from the explicit formula to a positive shift feature requires accounting for the diagonal mass through completion, pole, archimedean renormalization, or tail/support records.

The candidate prime feature is

\[
q_{{\rm pr},L}[f]
=\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}\alpha_L(\log n)^2\|\tau_{\log n}f-f\|_2^2.
\]

The completed matching residual is defined as

\[
\mathsf R_{{\rm match},L}[f]
= q_{{\rm cmp},L}[f]-Q_{{\rm Weil},L}[f].
\]

The Douglas gate can be attempted only after this residual is either zero or explicitly paid by a positive defect budget.

The core implication is:

\[
Q_{{\rm Weil},L}[f]
=q_{{\rm cmp},L}[f]-q_Z[f]-E_{{\rm match},L}[f]\ge0
\]

on a dense form core, together with closability/form-core records, implies

\[
V_Z^*V_Z\preceq W_{{\rm cmp},L}^*W_{{\rm cmp},L}+E_{{\rm match},L}.
\]

This is the precise bridge from Weil positivity to Douglas domination.
