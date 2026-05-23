# Step 78: Completion Balance for Positive Weil Feature Matching

## Main result

Step 78 isolates the next RH analytic obstruction after the prime autocorrelation lift.

The signed prime autocorrelation term is

\[
P_{\mathrm{pr},L}(h_f)=-\sum_a w_a(h_f(a)+h_f(-a)).
\]

The positive prime shift feature is

\[
q_{\mathrm{pr},L}[f]=\sum_a w_a\|\tau_a f-f\|^2.
\]

They are related by

\[
q_{\mathrm{pr},L}[f]
=
P_{\mathrm{pr},L}(h_f)+d_{\mathrm{pr},L}\|f\|^2,
\qquad
 d_{\mathrm{pr},L}=2\sum_a w_a.
\]

So the positive prime feature requires a diagonal repair.

## Completion-balance form

Write the signed completed explicit-formula carrier as

\[
q_{\mathrm{sgn},L}=P_{\mathrm{pr},L}+R_{\mathrm{sgn},L}.
\]

The positive feature package is

\[
q_{\mathrm{cmp},L}=q_{\mathrm{pr},L}+q^+_{\infty,L}+q^+_{\mathrm{pole},L}+q^+_{\mathrm{tail},L}.
\]

Then

\[
q_{\mathrm{cmp},L}-q_{\mathrm{sgn},L}
=
\mathcal B_L,
\]

where

\[
\mathcal B_L[f]
=
d_{\mathrm{pr},L}\|f\|^2
+q^+_{\infty,L}[f]
+q^+_{\mathrm{pole},L}[f]
+q^+_{\mathrm{tail},L}[f]
-R_{\mathrm{sgn},L}[f].
\]

The matching gate is

\[
\mathcal B_L\ge0.
\]

If this fails, the negative part is an explicit-formula matching defect.

## Theorem

If

\[
q_Z\le q_{\mathrm{sgn},L}+e_{\mathrm{Weil},L}
\]

and

\[
\mathcal B_L\ge -e_{\mathrm{bal},L},
\]

then

\[
q_Z\le q_{\mathrm{cmp},L}+e_{\mathrm{Weil},L}+e_{\mathrm{bal},L}.
\]

If both defects vanish and the core-to-full gate passes, then

\[
V_Z^*V_Z\preceq W_{\mathrm{cmp},L}^*W_{\mathrm{cmp},L},
\]

hence

\[
V_Z=T W_{\mathrm{cmp},L},\qquad \|T\|\le1.
\]

## Sanity check

For a toy prime cutoff with \(L=6\), the prime weights gave

\[
\sum_a w_a\approx4.5428017577,
\]

so

\[
d_{\mathrm{pr},L}=2\sum_a w_a\approx9.0856035154.
\]

The signed prime symbol had minimum

\[
-9.0856035154,
\]

while the diagonal-repaired positive prime symbol had minimum approximately zero.

A toy gamma/pole/tail balance model required a pole/completion diagonal of about

\[
p_{\min}\approx4.9970819335
\]

for the completion-balance form to become nonnegative.

## Interpretation

The prime feature can be made positive, but not for free. It demands a diagonal payment.

That payment must be located in the completed carrier: gamma, pole/completion, tail, or a lawful quotient/defect record.

The explicit formula cannot merely balance signed terms. It must produce a positive payment ledger.

## Next active obstruction

Identify whether the actual gamma/pole/tail terms of the completed zeta package supply the needed completion-balance form:

\[
\mathcal B_L\ge0
\]

on the completed anti-invariant Weil core.
