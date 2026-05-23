
# Step 48: Native Probe Adequacy / Exhaustivity Theorem

This step proves when a native probe-family membrane is strong enough to imply
there are no layer-dissolving needles.

The key point is:

\[
\text{no native needles} \not\Rightarrow \text{no layer-dissolving needles}
\]

unless the declared native family is adequate/exhaustive for the layer-dissolving
readouts.

## Main definitions

Let

\[
C_\Gamma=\Gamma^*C\Gamma
\]

be the packaged audit, and let

\[
L_\Gamma:E\to Y
\]

be the native probe family. Its currency matrix is

\[
K_L=L_\Gamma C_\Gamma^\dagger L_\Gamma^*.
\]

Let

\[
D_\Gamma:E\to Z
\]

be a layer-dissolving probe family, with currency

\[
K_D=D_\Gamma C_\Gamma^\dagger D_\Gamma^*.
\]

## Exact adequacy theorem

If the dissolving family factors through the native family,

\[
D_\Gamma=A L_\Gamma,
\]

then

\[
K_D=A K_L A^*.
\]

Therefore,

\[
K_L\preceq\Theta_Y
\Rightarrow
K_D\preceq A\Theta_YA^*.
\]

So a native membrane transfers to a dissolving membrane only through an adequacy bridge.

## Defective adequacy theorem

If

\[
D_\Gamma=A L_\Gamma+R,
\]

then for every \(t>0\),

\[
K_D
\preceq
(1+t)A K_LA^*
+
(1+t^{-1})K_R,
\]

where

\[
K_R=R C_\Gamma^\dagger R^*.
\]

Thus if

\[
K_L\preceq\Theta_Y,
\qquad
K_R\preceq\Xi,
\]

then

\[
K_D
\preceq
(1+t)A\Theta_YA^*
+
(1+t^{-1})\Xi.
\]

## Blind-spot theorem

Exact adequacy holds iff

\[
\ker L_\Gamma\subseteq \ker D_\Gamma.
\]

If this fails, there is a blind-spot vector \(v\) such that

\[
L_\Gamma v=0,
\qquad
D_\Gamma v\ne0.
\]

So the native family cannot detect a dissolving probe.

If such a vector is low-energy or zero-energy, the dissolving capacity can be large or infinite.

## Closure scope

This keeps the closure-only assumption honest:

\[
\text{formed closure + adequate native family + membrane budget}
\Rightarrow
\text{no layer-dissolving needles}.
\]

Without adequacy, the result is only:

\[
\text{no native needles}.
\]

The status should be `native_only`, `support_only`, or `failed_adequacy`, not accepted layer membrane.

## Layman version

A layer may have safe native probes but still have a hidden way to break it.

Adequacy says:

> every way of dissolving the layer must be visible through the declared native probes, up to an audited defect.

If the native probes have blind spots, a needle can hide there.
