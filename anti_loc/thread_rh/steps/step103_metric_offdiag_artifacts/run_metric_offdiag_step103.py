import numpy as np, pandas as pd, math
# Reproduces basic coefficients for |1-r e^{i theta}|^{-2}
for p in [2,3,5]:
    r=1/math.sqrt(p)
    coeff0=1/(1-r*r)
    print(p, coeff0)
