#!/usr/bin/env python3
import math, numpy as np

def phi(): return (1+math.sqrt(5))/2

def lambda_plus(t): return (2+t+math.sqrt(t*(4+t)))/2

def one_prime_matrix_norm(sigma,p):
    t=p**(-sigma)
    return math.sqrt(lambda_plus(t))

if __name__ == '__main__':
    print('raw one-prime norm phi =', phi())
    for sigma in [1,2,3]:
        print('p=2 sigma', sigma, 'norm', one_prime_matrix_norm(sigma,2))
    print('status: algebraic formulas loaded')
