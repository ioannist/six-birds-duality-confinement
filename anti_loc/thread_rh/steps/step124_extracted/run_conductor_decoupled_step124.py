#!/usr/bin/env python3
"""Sanity checks for Step 124 conductor-decoupled theorem."""

def feasible(theta, tau, a, alpha=2.0, eta=1.0, beta=1.0):
    return (a+alpha*tau)/eta + a/beta < theta

cases = [
    (0.35,1.0,0.02,False),
    (0.60,0.15,0.02,True),
    (0.75,0.08,0.03,True),
]
for theta,tau,a,expected in cases:
    got = feasible(theta,tau,a)
    assert got == expected, (theta,tau,a,got,expected)
print('Step 124 feasibility checks passed.')
