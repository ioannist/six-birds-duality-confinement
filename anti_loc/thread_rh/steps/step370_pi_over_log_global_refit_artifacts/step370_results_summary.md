# Step 370 Results Summary

Dataset: exact Step 324 `gamma_vs_d_k_step324.csv` with 15 rows. Here `d` is the minimum neighboring-zero gap, not a defect order.

Inherited citations:
- Step 324: constant-A model `gamma = 4.118419*T^-0.996855 - 0.039179*d^0.408668`, RMSE `0.014046`.
- Step 366: proposed `A_predicted(T)=pi/log(T/(2*pi))` after the rho_1 coefficient match.
- Step 367: per-zero `gamma*T` comparison was ambiguous and scattered.
- Step 369: no defect-order axis exists in the Branch C evaluator; Step 324's `d` is a zero-gap variable.

M1 refit RMSE: `0.0140462`.
M2 bare pi/log RMSE: `0.0154804`; ratio vs M1 `1.1021`.
M3 scaled pi/log RMSE: `0.019097`; ratio vs M1 `1.35958`; fitted C `0.786243`.

Corrected local `A_j` comparison using Step 324 B,beta: mean rel err `1.44195`, median `1.43556`, max `2.31286`, std `0.684217`.

Verdict: `scaled_pi_over_log_shape_supported`.
