# Step 434 Quantum-Semiclassical Operator Setup

## Hilbert space

Use the Sierra half-line setting:

```text
H_space = L^2([l_x, infinity), dx)
```

with `l_x > 0`. Momentum is formally `p_hat = -i hbar d/dx`.

## Classical Hamiltonian

```text
H_cl(x,p) = x (p + l_p^2/p).
```

The additional `l_p^2/p` term closes the classical trajectories that are open for Berry-Keating `xp`.

## Quantization

A symmetric formal quantization is

```text
H_tilde = (1/2)[ x (p_hat + l_p^2 p_hat^{-1}) + (p_hat + l_p^2 p_hat^{-1}) x ].
```

The inverse momentum operator and the lower endpoint `x=l_x` force a domain/self-adjoint-extension analysis. Sierra's framework supplies a U(1) family of self-adjoint extensions.

## Smooth counting

Bohr-Sommerfeld quantization yields the smooth Riemann-von Mangoldt shape:

```text
N(E) ~= (E/(2pi hbar)) [ log(E/(2pi e l_x l_p)) ] + constant.
```

With `l_x l_p = 2pi hbar`, this matches the average zero counting. It does not derive the prime-fluctuation term.
