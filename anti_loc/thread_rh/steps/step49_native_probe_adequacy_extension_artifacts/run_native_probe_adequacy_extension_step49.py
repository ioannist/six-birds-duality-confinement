
import numpy as np

def psd_sqrt_inv(A, tol=1e-10):
    vals, vecs = np.linalg.eigh((A+A.T)/2)
    inv = np.zeros_like(vals)
    inv[vals>tol] = 1.0/np.sqrt(vals[vals>tol])
    return (vecs*inv)@vecs.T

def pinv(A, tol=1e-10):
    vals, vecs = np.linalg.eigh((A+A.T)/2)
    inv = np.zeros_like(vals)
    inv[vals>tol] = 1.0/vals[vals>tol]
    return (vecs*inv)@vecs.T

def conditional_residual(Cinv, L, D):
    KLL = L@Cinv@L.T
    KDL = D@Cinv@L.T
    KDD = D@Cinv@D.T
    return KDD - KDL@pinv(KLL)@KDL.T

if __name__ == '__main__':
    Cinv = np.eye(3)
    L = np.array([[1.,0.,0.]])
    D = np.array([[0.,1.,0.]])
    M = np.array([[0.,1.,0.]])
    R0 = conditional_residual(Cinv,L,D)
    R1 = conditional_residual(Cinv,np.vstack([L,M]),D)
    print('before', R0, 'after', R1)
