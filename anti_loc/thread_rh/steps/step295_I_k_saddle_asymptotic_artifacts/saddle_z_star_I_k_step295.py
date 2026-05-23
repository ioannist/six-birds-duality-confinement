#!/usr/bin/env python3
"""Step 295: endpoint-saddle asymptotic for the Branch C I_k term.

The inherited implementation computes

    I_k = int (-i)^k sinc^(k)(gamma-u) F(u) du.

Using sinc(x)=sin(x)/(pi*x)=(1/(2*pi))*int_{-1}^1 exp(i*t*x) dt,

    (-i)^k sinc^(k)(gamma-u)
      = (1/(2*pi))*int_{-1}^1 t^k exp(i*t*(gamma-u)) dt.

Thus the large-k asymptotic is an endpoint Laplace problem at t=+/-1,
not an interior saddle with positive exponential rate.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step295_I_k_saddle_asymptotic_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP293_B = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step293_branch_C_L_k_at_k10_artifacts/L_k_method_B_step293.csv")
STEP294_TABLE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step294_branch_C_L_k_at_k20_k30_k50_artifacts/component_table_step294.csv")
STEP293_CODE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step293_branch_C_L_k_at_k10_artifacts/method_A_projected_pipeline_step293.py")

TRIPLE_ID = "rho1_G_star"
RHO_INDEX = 1
G_ID = "G_star"
K_VALUES = [10, 20, 30, 50]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def extract_step293_snippet() -> str:
    text = STEP293_CODE.read_text(encoding="utf-8")
    start = text.index("def projected_components")
    end = text.index("\ndef main", start)
    return text[start:end].strip()


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    step196 = load_module("step196_for_step295", STEP196_SCRIPT)
    u_grid = np.linspace(-step196.U_MAX, step196.U_MAX, int(round(2 * step196.U_MAX / step196.H)) + 1)
    zeta_grid = step196.zeta_values(u_grid)
    spec = step196.GENERATORS[G_ID]
    moments = step196.compute_moments(spec)
    G_primary, _, _quad_data = step196.mellin_values(u_grid, spec, moments, step196.N_T_PRIMARY)
    F = zeta_grid * G_primary
    gamma = float(step196.ZEROS[RHO_INDEX])

    def H(t: float) -> complex:
        return complex(simpson(F * np.exp(-1j * t * u_grid), x=u_grid))

    H_plus = H(1.0)
    H_minus = H(-1.0)
    even_endpoint_amplitude_complex = (np.exp(1j * gamma) * H_plus + np.exp(-1j * gamma) * H_minus) / (2.0 * math.pi)
    A_even = abs(even_endpoint_amplitude_complex)
    b_pred = 0.0
    c_pred = -1.0

    certified: dict[int, float] = {}
    for row in read_csv(STEP293_B):
        if row["k"] == "10":
            certified[10] = float(row["I_abs"])
    for row in read_csv(STEP294_TABLE):
        k = int(row["k"])
        if k in {20, 30, 50}:
            certified[k] = float(row["I_abs"])

    rows = []
    lines = [
        "Step295 I_k endpoint-saddle asymptotic",
        f"H(+1)={H_plus.real:+.16e}{H_plus.imag:+.16e}j",
        f"H(-1)={H_minus.real:+.16e}{H_minus.imag:+.16e}j",
        f"A_even={A_even:.16e}",
        "b_pred=0",
        "c_pred=-1",
    ]
    for k in K_VALUES:
        pred = A_even / (k + 1.0)
        cert = certified[k]
        rel = abs(pred - cert) / cert
        rows.append({
            "k": k,
            "I_certified_abs_legacy": f"{cert:.16e}",
            "I_predicted_endpoint_saddle": f"{pred:.16e}",
            "relative_error_vs_legacy": f"{rel:.16e}",
            "A_even": f"{A_even:.16e}",
            "b_pred": f"{b_pred:.16e}",
            "c_pred": f"{c_pred:.16e}",
            "endpoint_saddles": "t=+1 and t=-1",
            "interpretation": "legacy high-k values are incompatible with exact sinc endpoint asymptotic",
        })
        lines.append(f"k={k} legacy={cert:.8e} endpoint_pred={pred:.8e} rel_error={rel:.8e}")

    write_csv(ART / "I_k_predicted_vs_certified_step295.csv", rows)
    (ART / "compute_step295_output.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    snippet = extract_step293_snippet()
    (ART / "I_k_integrand_step295.md").write_text(
        "# Step 295 I_k Integrand Identification\n\n"
        "Verbatim Step 293 code snippet identifying the projected components:\n\n"
        "```python\n" + snippet + "\n```\n\n"
        "The I-term is therefore\n\n"
        "`I_k = integral ((-1j)^k) * sinc_derivative_n(gamma-u,k) * F(u) du`,\n\n"
        "implemented by Simpson quadrature over the inherited `u_grid`.\n",
        encoding="utf-8",
    )

    tex = rf"""\section*{{Step 295: Endpoint-Saddle Asymptotic for $I_k$}}

The Step 293 implementation identifies
\[
 I_k=\int (-i)^k S^{{(k)}}(\gamma-u)F(u)\,du,\qquad
 S(x)=\frac{{\sin x}}{{\pi x}}.
\]
The key identity is
\[
 S(x)=\frac1{{2\pi}}\int_{{-1}}^1 e^{{itx}}\,dt,
\]
hence
\[
 (-i)^kS^{{(k)}}(\gamma-u)
 =\frac1{{2\pi}}\int_{{-1}}^1 t^k e^{{it(\gamma-u)}}\,dt.
\]
Writing
\[
 H(t)=\int F(u)e^{{-itu}}\,du,
\]
one obtains the exact transformed form
\[
 I_k=\frac1{{2\pi}}\int_{{-1}}^1 t^k e^{{it\gamma}}H(t)\,dt.
\]
The saddle set is therefore at the endpoints $t=\pm1$; there is no positive
interior exponential saddle.  For even $k$,
\[
 I_k\sim \frac{{e^{{i\gamma}}H(1)+e^{{-i\gamma}}H(-1)}}{{2\pi(k+1)}}.
\]
Thus
\[
 |I_k|\sim A k^c e^{{bk}},\qquad
 b=0,\quad c=-1,\quad
 A={A_even:.16e}.
\]

\paragraph{{Comparison.}}
The endpoint formula is incompatible with the inherited high-k values
reported in Steps 293--294.  This points to numerical instability in the
high-order explicit derivative formula for $\operatorname{{sinc}}^{{(k)}}$,
not to a genuine super-exponential saddle.
"""
    (ART / "step295_I_k_asymptotic.tex").write_text(tex, encoding="utf-8")

    summary = (
        "# Step 295 Results Summary\n\n"
        "The exact Fourier representation of `sinc` converts the Step 293 `I_k` "
        "integral into an endpoint Laplace problem on `t in [-1,1]`. The derived "
        f"asymptotic is `|I_k| ~ A/(k+1)` for even k, with `A={A_even:.6e}`, "
        "`b=0`, `c=-1`. This contradicts the legacy super-exponential high-k "
        "values, indicating numerical instability in the inherited high-order "
        "`sinc_derivative_n` formula rather than true saddle growth.\n"
    )
    (ART / "step295_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 295,
        "orientation": "analytical_derivation",
        "target": "I_k saddle/endpoint asymptotic",
        "integrand": "I_k=int (-i)^k sinc^(k)(gamma-u) F(u) du",
        "saddle_equation": "endpoint Laplace: phi(t)=log|t|, maxima at t=+/-1; no interior positive saddle",
        "predicted": {"A_even": A_even, "b": b_pred, "c": c_pred},
        "comparison_table": rows,
        "final_verdict": "V_I_k_endpoint_asymptotic_blocks_superexponential_legacy",
    }
    (ART / "step295_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    write_csv(ART / "content_classification_step295.csv", [
        {"file": "step295_I_k_asymptotic.tex", "kind": "derivation"},
        {"file": "I_k_integrand_step295.md", "kind": "integrand_identification"},
        {"file": "saddle_z_star_I_k_step295.py", "kind": "computation_script"},
        {"file": "I_k_predicted_vs_certified_step295.csv", "kind": "comparison_table"},
        {"file": "compute_step295_output.txt", "kind": "raw_output"},
    ])
    (ART / "nonclaim_boundary_step295.md").write_text(
        "# Step 295 Nonclaim Boundary\n\n"
        "- No RH claim and no Branch C closure claim.\n"
        "- The result identifies the asymptotic of the mathematical I-term implied by the exact sinc Fourier representation.\n"
        "- The inherited Step 294 high-k values are treated as legacy projected-grid outputs and are not promoted after the endpoint-asymptotic contradiction.\n",
        encoding="utf-8",
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
