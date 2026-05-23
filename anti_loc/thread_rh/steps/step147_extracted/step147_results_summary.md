# Step 147: Zero-evaluator norm envelope and weight schedule

## Purpose

Step 146 reduced the completed residual ledger to the trace-class condition

\[
\sum_{(\rho,k)} \omega_{\rho,k} q(\rho)^2\|\Pi_RY^a_{\rho,k}\|^2<\infty,
\qquad q(\rho)=\Re\rho-\frac12.
\]

Step 147 defines lawful positive weights, proves trace-class under an evaluator-norm envelope, and records the remaining source-compatibility gate.

---

## Main verdict

\[
\boxed{\text{The unweighted residual ledger is not trace-class-certified, but a positive weighted ledger is lawful.}}
\]

The cleanest universally safe schedule is an **envelope-normalized dyadic height schedule**. It is weak, but it preserves separation and makes the trace-class condition explicit rather than hidden.

---

## Canonical envelope-normalized schedule

Partition zero-evaluator indices into dyadic height shells

\[
\mathcal Z_j=\{(\rho,k):2^j\le 1+|\Im\rho|<2^{j+1},\;0\le k<m_\rho\}.
\]

Set

\[
n_j=\#\mathcal Z_j,
\qquad
E_j=\sup_{(\rho,k)\in\mathcal Z_j}\|\Pi_RY^a_{\rho,k}\|_{H_R}^2.
\]

If \(E_j<\infty\), define

\[
\boxed{
\omega_{\rho,k}^{\rm env}
=
\frac{2^{-j}}{(1+n_j)(1+E_j)}
}
\qquad ((\rho,k)\in\mathcal Z_j).
\]

This schedule depends only on height shell, multiplicity count, and a residual-carrier evaluator envelope. It does **not** depend on the off-critical displacement \(q(\rho)\).

---

## Trace-class theorem

Since nontrivial zeros lie in the critical strip,

\[
0\le q(\rho)^2\le \frac14.
\]

For each shell,

\[
\sum_{(\rho,k)\in\mathcal Z_j}
\omega_{\rho,k}^{\rm env}q(\rho)^2\|\Pi_RY^a_{\rho,k}\|^2
\le
\frac14 2^{-j}.
\]

Therefore

\[
\boxed{K_R^{\omega^{\rm env}}\in\mathcal S_1(H_R).}
\]

---

## Separation survives

If every weight is strictly positive, then

\[
\operatorname{tr}K_R^\omega=0
\]

forces

\[
q(\rho)=0
\]

for every visible residual zero-evaluator direction. So weighting does not destroy separation on the residual carrier.

---

## What remains open

The trace-class problem is not the last ledger gate. The completed squeeze still requires a finite source audit budget:

\[
\boxed{
C_{\rm src}^\omega
=
\sup_N\operatorname{tr}(F_N^\Omega K_R^\omega)<\infty.
}
\]

If this fails, then the weighted ledger is trace-class but not source-compatible.

---

## Stronger analytic schedules

If a polynomial evaluator envelope is proved, one may use

\[
\omega_{\rho,k}^{\rm poly}
=(1+|\Im\rho|)^{-B}(1+k)^{-2}.
\]

If a stretched-exponential envelope is proved, one may use

\[
\omega_{\rho,k}^{\rm exp}
=
\exp(-B(1+|\Im\rho|)^\nu)(1+k)^{-2}.
\]

The envelope-normalized schedule is always the conservative fallback, provided shell envelopes are finite.

---

## Completed residual squeeze

With a trace-class weighted ledger and strong window exhaustion,

\[
P_N\uparrow I_{H_R}
\Rightarrow
\operatorname{tr}((I-P_N)K_R^\omega(I-P_N))\to0.
\]

Then

\[
\operatorname{tr}(G_RK_R^\omega)
\le
\frac{C_{\rm src}^\omega}{\Lambda_N^\Omega}
+
\operatorname{tr}((I-P_N)K_R^\omega(I-P_N)).
\]

So residual mass collapses if

\[
\Lambda_N^\Omega\to\infty,
\qquad
C_{\rm src}^\omega<\infty,
\qquad
\operatorname{tr}((I-P_N)K_R^\omega(I-P_N))\to0.
\]

---

## Bottom line

\[
\boxed{\text{Step 147 closes the trace-class ledger gate by a lawful positive weighted schedule.}}
\]

The next gate is source compatibility:

\[
\boxed{\textbf{Step 148: source-compatible weight normalization audit.}}
\]

Target:

\[
\sup_N\operatorname{tr}(F_N^\Omega K_R^\omega)<\infty.
\]
