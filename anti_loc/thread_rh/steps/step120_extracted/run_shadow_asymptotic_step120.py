
import numpy as np

def shadow_defect(B, D):
    # B: H x d Burnol synthesis with full column rank
    # D: H x m Dirichlet synthesis
    QD, _ = np.linalg.qr(D)
    PD = QD @ QD.T
    G = B.T @ B
    vals, vecs = np.linalg.eigh(G)
    invsqrt = vecs @ np.diag(1/np.sqrt(np.maximum(vals, 1e-14))) @ vecs.T
    E = (np.eye(B.shape[0])-PD) @ B @ invsqrt
    s = np.linalg.svd(E, compute_uv=False)[0]
    return s, 1-s*s

if __name__ == '__main__':
    rng = np.random.default_rng(120)
    H, d, m = 32, 6, 12
    B, _ = np.linalg.qr(rng.normal(size=(H,d)))
    D, _ = np.linalg.qr(np.concatenate([B + 0.1*rng.normal(size=(H,d)), rng.normal(size=(H,m-d))], axis=1))
    delta, c = shadow_defect(B, D)
    print({'delta_BD': float(delta), 'c_visibility': float(c)})
