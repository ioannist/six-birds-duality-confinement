#!/usr/bin/env python3
"""Step 293 Method B wrapper.

The heavy computation is centralized in method_A_projected_pipeline_step293.py
because it builds the inherited Step 269 PSWF/Sonine objects once and writes all
three method ledgers.  Method B is the component split

    L_k = delta_Dk - I_k - R_k

with delta_Dk supplied by the Leibniz product derivative and I_k, R_k supplied
by the inherited projected-kernel corrections.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step293_branch_C_L_k_at_k10_artifacts")
MAIN = ART / "method_A_projected_pipeline_step293.py"
OUT = ART / "L_k_method_B_step293.csv"


def main() -> None:
    if not OUT.exists():
        subprocess.run([sys.executable, str(MAIN)], check=True)
    print(f"Method B component-split ledger: {OUT}")


if __name__ == "__main__":
    main()
