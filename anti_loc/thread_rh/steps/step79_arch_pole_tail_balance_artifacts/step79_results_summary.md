# Step 79: Archimedean, Pole, and Tail Balance Audit

## Purpose
This step audits the non-prime completion slots required to turn the signed Weil explicit formula into a positive completed feature package suitable for a Douglas bridge.

## Main identity
From the autocorrelation lift, the signed prime term

\[
P_{\mathrm{pr},L}(h_f)=-\sum_a w_{a,L}(h_f(a)+h_f(-a))
\]

is related to the positive shift-difference feature

\[
q_{\mathrm{pr},L}[f]=\sum_a w_{a,L}\|\tau_a f-f\|^2
\]

by

\[
q_{\mathrm{pr},L}[f]=P_{\mathrm{pr},L}(h_f)+d_{\mathrm{pr},L}\|f\|^2,
\qquad d_{\mathrm{pr},L}=2\sum_a w_{a,L}.
\]

Thus the prime slot is positive only after a diagonal repair.

## Completion-balance gate
Writing the signed non-prime terms as

\[
R_{\mathrm{sgn},L}=G_{\infty,L}+P_{\mathrm{pole},L}+T_{\mathrm{sgn},L},
\]

and the positive candidate carrier as

\[
q_{\mathrm{cmp},L}=q_{\mathrm{pr},L}+q^+_{\infty,L}+q^+_{\mathrm{pole},L}+q^+_{\mathrm{tail},L},
\]

the balance form is

\[
\mathcal B_L[f]
=d_{\mathrm{pr},L}\|f\|^2+q^+_{\infty,L}[f]+q^+_{\mathrm{pole},L}[f]+q^+_{\mathrm{tail},L}[f]-R_{\mathrm{sgn},L}(h_f).
\]

The completed feature package passes only if

\[
\mathcal B_L\ge0
\]

on the chosen core, or if its negative part is carried as an explicit defect.

## Slot statuses

- Prime-power: positive after diagonal repair.
- Archimedean/gamma: plausible positive shift-kernel feature, but exact gamma matching is unearned.
- Pole/completion: finite-rank positive feature template; null/pole audit required.
- Tail/support: positive omitted features or explicit defect; needs fixed/exhaustive ledger tail control.

## Sanity checks
For a toy cutoff \(L=6\), the prime weights gave

\[
\sum_a w_a\approx 4.5428017577,
\]

so

\[
d_{\mathrm{pr},L}\approx9.0856035154.
\]

The signed prime symbol had minimum \(-9.0856035154\), while the repaired symbol had minimum approximately zero and matched the positive shift-difference symbol up to roundoff.

## Nonclaim
This step does not prove RH. It does not prove exact gamma matching or the Weil--Douglas bridge. It only identifies the balance gate that gamma, pole/completion, and tail terms must satisfy to pay the prime diagonal repair.
