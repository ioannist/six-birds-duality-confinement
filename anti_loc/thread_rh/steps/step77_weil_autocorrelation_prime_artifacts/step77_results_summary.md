# Step 77: Weil autocorrelation lift and prime-slot matching

## Purpose
This step studies the first concrete matching problem for the RH Weil--Douglas bridge: how the classical Weil autocorrelation substitution turns the zero side into squares, and how the prime-power signed autocorrelation term relates to a positive shift-difference feature.

## Main conclusion
Let

\[
 h_f(a)=(f*\tilde f)(a)=\langle \tau_a f,f\rangle.
\]

For positive weights \(w_a\), define the signed prime autocorrelation term

\[
P_L(h_f)=-\sum_a w_a(h_f(a)+h_f(-a)).
\]

The positive shift-difference prime feature is

\[
q_{\mathrm{pr},L}[f]=\sum_a w_a\|\tau_a f-f\|_2^2.
\]

Then

\[
q_{\mathrm{pr},L}[f]
=2\left(\sum_a w_a\right)h_f(0)+P_L(h_f).
\]

So the positive prime feature equals the signed prime autocorrelation term plus a diagonal completion term.

## Minimal diagonal repair
For

\[
Q_c[f]=c\|f\|_2^2-\sum_a w_a(h_f(a)+h_f(-a)),
\]

one has \(Q_c\ge0\) for all \(f\) iff

\[
c\ge 2\sum_a w_a.
\]

At the sharp value,

\[
Q_c[f]=\sum_a w_a\|\tau_a f-f\|^2.
\]

Thus the diagonal completion is not optional.

## RH implication
The explicit formula's prime side is signed. The framework needs a positive feature package. Therefore the active matching problem is:

\[
\text{signed Weil formula}
\longrightarrow
\text{positive prime/gamma/pole/tail feature package}
\longrightarrow
\text{Douglas contraction}.
\]

The prime slot is naturally positive after adding the sharp diagonal repair. Gamma, pole/completion, and tail terms must supply or account for the remaining diagonal, null-mode, and support defects.

## Sanity-check result
For a toy prime-power cutoff \(L=6\), using weights

\[
w_{n,L}=\Lambda(n)n^{-1/2}(1-\log n/L)_+^2,
\]

there were 98 prime-power shifts, with

\[
\sum w_a\approx 4.5428017577,
\]

so the sharp diagonal repair is

\[
2\sum w_a\approx 9.0856035154.
\]

The signed prime symbol has minimum \(-9.0856035154\), while the repaired symbol has minimum \(0\), matching the positive shift-difference symbol to numerical roundoff.

## Nonclaim
This step does not prove RH, Weil positivity, or the Douglas bridge. It proves the algebraic matching relation between the autocorrelation lift, signed prime autocorrelation, and the positive shift-difference feature.
