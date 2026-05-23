import numpy as np, csv, os
rng=np.random.default_rng(57)
base=os.path.dirname(__file__)
rows=[]
for n in [4,6,8,10]:
    for trial in range(10):
        A=rng.normal(size=(n,n))
        C=A.T@A + 0.5*np.eye(n)
        Ci=np.linalg.inv(C)
        m=max(1,n//2); p=max(1,n//3)
        L=rng.normal(size=(m,n))
        D=rng.normal(size=(p,n))
        KLL=L@Ci@L.T
        KDL=D@Ci@L.T
        KLD=KDL.T
        KDD=D@Ci@D.T
        Xi=KDD-KDL@np.linalg.pinv(KLL)@KLD
        # projection formula
        T_L=L@np.linalg.inv(np.linalg.cholesky(C)).T # not exact C^{-1/2}; use eig next
        w,V=np.linalg.eigh(C)
        Cminushalf=V@np.diag(1/np.sqrt(w))@V.T
        TL=L@Cminushalf
        TD=D@Cminushalf
        # projector onto range TL.T via SVD
        U,s,Vt=np.linalg.svd(TL.T,full_matrices=False)
        r=(s>1e-10).sum()
        P=U[:,:r]@U[:,:r].T if r>0 else np.zeros((n,n))
        Xi_proj=TD@(np.eye(n)-P)@TD.T
        proj_err=np.linalg.norm(Xi-Xi_proj,ord=2)
        # optimal residual identity random Amap
        Amap=rng.normal(size=(p,m))
        Astar=KDL@np.linalg.pinv(KLL)
        lhs=(D-Amap@L)@Ci@(D-Amap@L).T
        rhs=Xi+(Amap-Astar)@KLL@(Amap-Astar).T
        opt_err=np.linalg.norm(lhs-rhs,ord=2)
        min_eig=np.linalg.eigvalsh(Xi).min()
        rows.append([n,trial,proj_err,opt_err,min_eig])
with open(os.path.join(base,'xi_scaffold_identity_checks_step57.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['n','trial','projection_error','optimal_residual_error','min_eig_Xi']); w.writerows(rows)
print('wrote', len(rows), 'rows')
