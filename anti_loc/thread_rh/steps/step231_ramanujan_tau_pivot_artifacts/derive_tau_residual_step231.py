#!/usr/bin/env python3
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step231_ramanujan_tau_pivot_artifacts")

text = """Step 231 tau residual derivation
Delta(z)=q prod(1-q^n)^24=sum tau(n)q^n.
L(tau,s)=sum tau(n)n^-s.
Lambda_tau(s)=(2*pi)^(-s) Gamma(s)L(tau,s), paired by s <-> 12-s.
Critical line: Re(s)=6.
Residual Xi_tau: off-critical-line zero defect for L(tau,s).
CRE audit: not equivalent to Riemann RH; not natively proved.
Verdict: V_tau_outside_dichotomy.
"""

(OUT / "derive_tau_residual_output_step231.txt").write_text(text)
print(text)
