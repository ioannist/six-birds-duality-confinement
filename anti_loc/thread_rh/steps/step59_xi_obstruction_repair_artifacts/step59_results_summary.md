# Step 59 — Ξ-Obstruction and Repair Calculus

## Purpose

This step gives a standalone obstruction-and-repair calculus for the adequacy residual

\[
\Xi_C(D\mid L).
\]

Here \(L\) is the native probe family of a formed layer and \(D\) is a layer-dissolving probe family.  The residual \(\Xi\) measures the part of \(D\) that is invisible to \(L\) in the audit geometry.

## Core object

On the legal energy quotient

\[
E_C=(\ker C)^\perp,
\qquad C_0=C|_{E_C}>0,
\]

with null-legal probes \(L,D\), define

\[
T_L=L_0C_0^{-1/2},
\qquad
T_D=D_0C_0^{-1/2}.
\]

Let \(P_L\) be the projection onto \(\operatorname{Ran}(T_L^*)\). Then

\[
\Xi_C(D\mid L)=T_D(I-P_L)T_D^*.
\]

Equivalently,

\[
\Xi_C(D\mid L)=K_{DD}-K_{DL}K_{LL}^{\dagger}K_{LD}.
\]

## Main theorem

For an adequacy budget \(\Omega\), the adequacy claim

\[
\Xi_C(D\mid L)\preceq\Omega
\]

fails iff there exists a dissolving recombination witness \(z\) such that

\[
z^*(\Xi_C(D\mid L)-\Omega)z>0.
\]

Thus every adequacy failure has a native blind-spot witness.

## Repair calculus

The proof-strengthening repairs are:

1. **Native strict extension**: add native probes \(M\), so \(L^+=[L;M]\). Then

\[
\Xi_C(D\mid L^+)
=
\Xi_C(D\mid L)-K_{DM\mid L}K_{MM\mid L}^{\dagger}K_{MD\mid L}
\preceq
\Xi_C(D\mid L).
\]

2. **Faithful native restoration**: undo native coarsening or add the hidden native readout. Coarsening can only increase \(\Xi\).

3. **Defect-paid dissolving bridge**: if \(D'=BDU+R\), then

\[
\Xi(D'\mid L')
\preceq
(1+t)B\Xi(D\mid L)B^*+(1+t^{-1})\Xi(R\mid L').
\]

4. **Null-mode repair**: if \(D\) sees \(\ker C\), the true capacity is infinite. Repair requires quotienting, annihilation, audit strengthening, or a scope nonclaim.

5. **Budget repair**: raising \(\Omega\) can make the inequality true, but this weakens the claim; it does not reduce the blind spot.

## Predictive repair

If

\[
\Xi_{j+1}\preceq(1+\varepsilon_j)A_j\Xi_jA_j^*+E_j
\]

and the budgets satisfy the same recurrence, adequacy propagates. In a common response space, summable defects preserve predictive adequacy.

A stronger collapse theorem says that if

\[
\Xi_{j+1}\preceq(1-\alpha_j)\Xi_j+E_j,
\]

with \(\prod_j(1-\alpha_j)=0\) and sufficiently vanishing accumulated residuals, then \(\Xi_j\to0\).

## Interpretation

A \(\Xi\)-obstruction is a blind spot in the layer's official senses. A real repair must make that blind spot visible, reduce the bridge residual, or record a narrower claim. Repeating the same native family or checking a public shadow does not repair intrinsic adequacy.
