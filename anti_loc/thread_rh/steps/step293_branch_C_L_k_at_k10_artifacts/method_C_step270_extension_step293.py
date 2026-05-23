#!/usr/bin/env python3
"""Step 293 Method C wrapper.

Step 270 computed projected values by calling the inherited Step 269
projected_k formula after computing raw delta_Dk.  This wrapper records the
same extension route for k=8,9,10 and reuses the centralized computation.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step293_branch_C_L_k_at_k10_artifacts")
MAIN = ART / "method_A_projected_pipeline_step293.py"
OUT = ART / "L_k_method_C_step293.csv"


def main() -> None:
    if not OUT.exists():
        subprocess.run([sys.executable, str(MAIN)], check=True)
    print(f"Method C Step270-extension ledger: {OUT}")


if __name__ == "__main__":
    main()
