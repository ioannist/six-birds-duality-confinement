#!/usr/bin/env python3
"""Reproduce Step 136 finite incidence metric checks."""
import math
import pandas as pd

def primes_upto(n):
    sieve=[True]*(n+1)
    if n>=0: sieve[0]=False
    if n>=1: sieve[1]=False
    for i in range(2,int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i,n+1,i): sieve[j]=False
    return [i for i in range(n+1) if sieve[i]]

def sigma_plus(r):
    return math.sqrt((2+r+math.sqrt(r*r+4*r))/2)

for y in [50,100,500,1000]:
    ps=primes_upto(y)
    norm=math.prod(sigma_plus(1/p) for p in ps)
    print(y, len(ps), norm, math.log(norm))
