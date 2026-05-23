# Step 429 Necessity Derivation Attempt

Start from the Hadamard split at a simple critical-line zero:

```text
L''(rho) = 2 L'(rho) g'(rho),
g'(rho) = arch(rho) + g_near(rho) + g_rest(rho).
```

Define

```text
A(rho) = 2 Re[L'(rho)(arch(rho)+g_rest(rho))],
B(rho) = 2 Re[L'(rho)g_near(rho)].
```

Then

```text
Re L''(rho) = A(rho) + B(rho).
```

The desired necessity statement is

```text
Re L''(rho) >= 0  =>  B(rho) > 0.
```

Equivalently, one must rule out the case

```text
B(rho) <= 0 and A(rho) >= -B(rho).
```

The functional equation supplies the phase-line constraint for `L'(rho)`, and the nearest-neighbor term makes `B` exactly a signed projection of that line. However, the implication above still requires a phase-sensitive upper bound or sign rule for the regular term `A`. The functional equation alone does not bound `A` relative to `B`.

Step 427 is the concrete obstruction: three zeta zeros had positive `Re zeta''` with `B>0` but `|A|>|B|`, because the regular residual `A` was itself positive and dominant. Those cases are compatible with necessity but show that a proof cannot be close-pair-only; it must control the regular Hadamard remainder.

## Conclusion

The derivation is partial. The functional equation derives the phase line behind the observed rule, but theorem-grade necessity stalls at the missing inequality:

```text
B(rho) <= 0  =>  A(rho) < -B(rho).
```

A proof of that inequality would need a phase-sensitive bound for `arch+g_rest`, not just a magnitude bound.
