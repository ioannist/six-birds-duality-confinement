# Step 295 I_k Integrand Identification

Verbatim Step 293 code snippet identifying the projected components:

```python
def projected_components(step269, gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, quad_data, k: int, n_terms: int) -> tuple[complex, complex, complex, complex]:
    delta = step269.delta_Dk(gamma, quad_data, k)
    I = complex(simpson(((-1j) ** k) * step269.sinc_derivative_n(gamma - u_grid, k) * F, x=u_grid))
    R = 0j
    for n in range(n_terms):
        mu = float(pswf["vals"][n])
        psi_Dk = step269.psi_derivative_n_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n], k)
        J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        R += psi_Dk * J_n
    L = delta - I - R
    return delta, I, R, L
```

The I-term is therefore

`I_k = integral ((-1j)^k) * sinc_derivative_n(gamma-u,k) * F(u) du`,

implemented by Simpson quadrature over the inherited `u_grid`.
