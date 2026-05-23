#!/usr/bin/env python3
"""Finite sanity checks for Step 108.

This script reports the archived sanity metrics. The construction is a toy
finite Sonin projection plus Dirichlet coefficient fit; it is not RH evidence.
"""
import pandas as pd
from pathlib import Path

def main():
    out = Path(__file__).resolve().parent
    sanity = pd.read_json(out / "finite_model_sanity_step108.json", typ="series")
    print(sanity.to_string())

if __name__ == "__main__":
    main()
