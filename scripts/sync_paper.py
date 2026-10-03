#!/usr/bin/env python3
"""Synchronize the RH or duality-confinement editable manuscript.

The modular paper tree is the sole editable source. Generated standalone and
selected collection files are replaced atomically to protect hard links.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "rh": "Tsiokos_2026_Riemann_Hypothesis_via_Self_Dual_Trace_Confinement_A_Conditional_Closure.tex",
    "duality_confinement": "Tsiokos_2026_Self_Dual_Trace_Confinement_A_Six_Birds_Structural_Law_for_Formed_Closures_Under_Involutive_Self_Duality.tex",
}


def replace(path: Path, data: bytes) -> None:
    if path.exists() and path.read_bytes() == data:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(data)
    try:
        temporary.chmod(0o644)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper", choices=PAPERS)
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--public-dir", type=Path)
    args = parser.parse_args()
    if args.public_dir and not args.public_dir.is_dir():
        parser.error("--public-dir must be an existing directory")
    paper = ROOT / "paper" / args.paper
    if args.build:
        subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-outdir=build", "main.tex"],
            cwd=paper,
            check=True,
        )
    bbl = paper / "build/main.bbl"
    pdf = paper / "build/main.pdf"
    if not bbl.is_file() or not pdf.is_file():
        parser.error("build/main.bbl or build/main.pdf missing; use --build")
    expanded = subprocess.run(
        ["latexpand", "--expand-bbl", "build/main.bbl", "main.tex"],
        cwd=paper,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout
    expanded = b"\n".join(line.rstrip() for line in expanded.splitlines()) + b"\n"
    data = (
        f"% Generated from paper/{args.paper}/main.tex by scripts/sync_paper.py.\n"
        "% Edit the modular sources and regenerate this copy.\n"
    ).encode() + expanded
    name = PAPERS[args.paper]
    targets = [
        (paper / "build/main_flat.tex", data),
        (ROOT / name, data),
        (ROOT / name.replace(".tex", ".pdf"), pdf.read_bytes()),
    ]
    if args.public_dir:
        targets.append((args.public_dir / name, data))
    stale = [str(path) for path, content in targets
             if not path.exists() or path.read_bytes() != content]
    if args.check:
        if stale:
            print("Stale generated files:\n" + "\n".join(stale))
            return 1
    else:
        for path, content in targets:
            replace(path, content)
    print(("Checked" if args.check else "Synchronized") + f" {args.paper}: {len(targets)} artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
