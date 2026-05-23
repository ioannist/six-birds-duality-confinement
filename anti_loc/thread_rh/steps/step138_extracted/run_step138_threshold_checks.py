#!/usr/bin/env python3
import math, numpy as np

def primes(n):
    ps=[]; x=2
    while len(ps)<n:
        ok=True
        for p in ps:
            if p*p>x: break
            if x%p==0: ok=False; break
        if ok: ps.append(x)
        x+=1
    return ps

def incidence_walsh_matrix(k):
    M=np.array([[1.0]])
    for p in primes(k):
        r=p**-0.5
        A=np.array([[1,0],[r,1]],float)
        W=np.array([[1,1],[1,-1]],float)/math.sqrt(2)
        M=np.kron(M,W@A)
    pop=np.array([int(i).bit_count() for i in range(1<<k)])
    return M,pop

if __name__ == '__main__':
    k=6; R=5; K=2
    M,pop=incidence_walsh_matrix(k)
    rows=np.where(pop>=R)[0]
    low=np.where(pop<=K)[0]
    tail=np.where(pop>K)[0]
    L=np.linalg.norm(M[np.ix_(rows,low)],2)
    T=np.linalg.norm(M[np.ix_(rows,tail)],2)
    print({'k':k,'R':R,'K':K,'L':float(L),'T':float(T),'delta_tail_0.01':float(L+0.01*T)})
