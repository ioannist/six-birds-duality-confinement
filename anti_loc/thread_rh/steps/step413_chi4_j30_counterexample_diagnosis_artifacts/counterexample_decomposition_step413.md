# Step 413 Counterexample Diagnosis

## Inherited Statements Cited

- Step 411: `L''(rho) = 2L'(rho)*g'(rho)` with close-pair contribution `g'_near = -1/(rho_nearest-rho)`.
- Step 412: `L(s, chi_4)` had one apparent exceptional zero at `j=30`, and the close-pair-only predictor failed using the first-30-zero table.

## Corrected Neighbor Geometry

For `L(s, chi_4) = beta(s) = 4^(-s)(zeta(s,1/4)-zeta(s,3/4))`:

```text
T29 = 64.9761705730959993486059247358
T30 = 67.6369208635460683980549911506
T31 = 68.3658845038344229612337381444
```

Hence

```text
s_bwd = T30 - T29 = 2.6607502904500690494490664148
s_fwd = T31 - T30 = 0.728963640288354563178746993803
s_min = 0.728963640288354563178746993803
```

The true nearest neighbor is `j=31` above `j=30`. Step 412 truncated the zero list at 30, so it incorrectly used the backward neighbor and produced the apparent counterexample.

## Exact Values

At `rho30 = 1/2 + i*T30`:

```text
L'(rho30)  = 0.940307136563014872066119116745 - 2.05645174324429747840510338302 i
L''(rho30) = 1.74907673401781231012473702928 + 10.1550130365662268799998870846 i
Re L''(rho30) = +1.74907673401781231012473702928
```

The exact regular logarithmic derivative is

```text
g'(rho30) = L''/(2L') = -1.88128109348854280022835749539 + 1.28547650766985036378586838395 i.
```

## Decomposition

Using the odd-character archimedean logarithmic derivative

```text
arch_chi4'(s) = -1/2 log(4/pi) - 1/2 psi((s+1)/2),
```

and `g'_near = -1/(rho31-rho30) = +i/s_fwd`, the real contributions to `2L'g'` are:

```text
Archimedean A:  -6.75302795071881
Close-pair B:   +5.64212432441989
Regular tail C: +2.85998036031673
Total:          +1.74907673401781
```

## Diagnosis

The single Step 412 χ4 counterexample is not structural. It is a boundary truncation artifact: after computing `T31`, the close-pair term has the correct positive sign.

The full sign is a cancellation:

```text
negative Archimedean term + positive close-pair term + positive regular tail.
```

The close-pair term is necessary but not sufficient by itself to overcome the Archimedean term; the regular far-zero residual supplies the remaining positive contribution.
