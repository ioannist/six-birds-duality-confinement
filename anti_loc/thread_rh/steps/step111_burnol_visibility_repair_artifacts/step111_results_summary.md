# Step 111: Burnol-native coefficient visibility repair

## Purpose

Step 110 showed that the source-coercivity route splits into two independent gates:

- source strength on coefficient space: \(\gamma_N\);
- coefficient visibility of boundary packets: \(c_N\).

Step 111 asks whether the collapse of \(c_N\) is caused by using a naive short-Dirichlet dictionary, and whether a Burnol/co-Poisson-native dictionary can repair visibility.

## Main finite identity

Let \(M_N : Y_{\mathcal B,N} \to H_N\) synthesize a finite Burnol/Sonine boundary dictionary and let \(D_N : \mathbb C^{I_N} \to H_N\) synthesize coefficient atoms. With

\[
R_N = D_N^\dagger M_N
\]

and \(P_N\) the projection onto \(\operatorname{Ran}D_N\),

\[
R_N^* H_N R_N = M_N^*P_NM_N
              = G_{\mathcal B,N} - E_{\mathrm{coef},N}^*E_{\mathrm{coef},N}.
\]

Therefore

\[
c_N = 1 - \|E_{\mathrm{coef},N}G_{\mathcal B,N}^{-1/2}\|^2.
\]

This makes the coefficient blind spot exactly a finite \(\Xi\)-type adequacy residual.

## Repair theorem

If \(D_N\subset D_N^+\), then

\[
c_N(D_N^+)\ge c_N(D_N).
\]

If the Burnol-native dictionary spans the boundary dictionary up to residual \(\varepsilon_N\), then

\[
c_N\ge 1-\varepsilon_N^2.
\]

So native extension can repair visibility, but only if the extension is declared before the target test. Otherwise it is smuggling.

## Toy audit

The toy audit compared three dictionaries:

- ordinary integer Dirichlet atoms;
- compact-log co-Poisson interval atoms;
- Burnol-native packet atoms.

The ordinary integer dictionary left the worst-direction visibility essentially zero in this toy model. The co-Poisson interval dictionary improved substantially once enough intervals were included. The native packet dictionary reached high visibility much faster.

This is not RH evidence. It shows that coefficient visibility is a real, dictionary-dependent gate.

## Bottom line

The active construction target is now

\[
\text{construct non-smuggled Burnol/co-Poisson atoms with } c_N \not\to 0,
\]

and combine it with

\[
\gamma_N c_N \to \infty.
\]
