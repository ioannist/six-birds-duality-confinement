#!/usr/bin/env python3
"""Sanity checks for Step 123 balanced-length formulas."""
import numpy as np

alpha=2.0
eta=1.0
theta=0.22
Q=np.logspace(2,10,50)

def total_error(Q,a,t,base=0.1):
    return base + (Q**a)*(1+Q**t)**alpha*(Q**(-theta*eta))

# Feasible polynomial regime should have decreasing Muntz component.
a,t=0.02,0.06
assert a+alpha*t < theta*eta
E=total_error(Q,a,t,base=0.05)
assert E[-1] < E[0]

# Supercritical polynomial regime should eventually grow.
a,t=0.12,0.08
assert a+alpha*t > theta*eta
E=total_error(Q,a,t,base=0.05)
assert E[-1] > E[0]

# Positive floor: if E <= 1-sigma then c >= sigma for sigma in (0,1).
for sigma in [0.1,0.3,0.7]:
    E=1-sigma
    c=1-E*E
    assert c >= sigma

print('Step 123 balanced-length checks passed.')
