# Step 373 Results Summary

Hecke data located and extracted from Steps 320, 321, and 322.  Seven `G_star` Dirichlet-character gamma cells were available.

The Hecke-side height variable used here is the first critical-line zero height `T_Hecke=Im rho_chi`.  There is no Hecke neighbor-gap `d_Hecke` in the inherited data; the requested 4-parameter M1/M2/M3 models therefore reduce to height-only analogs.

Reduced model comparison:

- M1: `gamma=A*T^alpha`, A=`0.180069`, alpha=`0.0819238`, RMSE=`0.0092169`.
- M2: bare `pi/(T log(T/(2*pi)))`, RMSE=`13.4352`, ratio vs M1=`1457.67`.
- M3: scaled pi/log, C=`-0.00698689`, RMSE=`0.184626`, ratio vs M1=`20.0312`.

Five of seven Hecke heights lie at or below `2*pi`, so the zeta law is outside its natural domain and gives negative/singular predictions.

Verdict: `structurally_different_or_data_blocked_current_hecke_first_zero_dataset`.  Current Hecke data are structurally different or data-blocked for this protocol; H6 does not reduce to simple asymptotic-constant identification on the available first-zero dataset.
