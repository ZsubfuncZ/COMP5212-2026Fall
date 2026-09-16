# High-dimensional linear regression numerical model

Copy `highdim-math.js` beside the existing `linear-math.js`; load LinearMath first.
The local `linear-math.js` is an unchanged copy of the existing site asset, included
only so the Node verification script can run in this isolated directory.

```js
const C = HighDimMath.conditioning(d, epsilon, delta, seed);
const R = HighDimMath.regularization(d, rho, noise, seed);
const index = 25; // UI penalty slider is an integer from 0 to 61.
const lambda = R.lambdas[index];
const ridge = R.ridge[index], lasso = R.lasso[index];
```

## Conditioning

- `d` integer 5–60, `epsilon` 1e-6–1, `delta` −0.01–0.01. `n=2d`.
- `conditioningData(d,seed)` caches the fixed orthonormal centered `U`, orthogonal
  `V`, and baseline `theta`. Changing epsilon or delta never resamples them.
- `X=U diag(s) Vᵀ` is explicitly materialized. The first d−1 singular values run
  from 1 to `max(.3,epsilon)`; the final one equals epsilon. Thus epsilon really
  remains the smallest singular value, and `condition=1/epsilon`, including ε=1.
- Baseline theta has norm 1.5 and is perpendicular to the weak right direction.
  `y=X theta`; `yPerturbed=y+delta u_d`; the exact OLS response is
  `perturbedTheta=theta+(delta/epsilon)v_d`.
- Fields: `X,y,yPerturbed,theta,perturbedTheta,norm,perturbedNorm,
  coefficientChange,predictionChange,responseChange,condition,rank,singularValues,
  n,d,seed,epsilon,delta,U,V,weakLeft,weakRight,normPath`.
- `normPath` contains 101 `{delta,norm}` points on [−.01,.01]; the y value is the
  coefficient L2 norm. `coefficientBefore/After` alias the before/after vectors.
- `predictionsBefore/After`, `measuredCoefficientChange`,
  `measuredPredictionChange`, and `residualNormBefore/After` support live witnesses.
  `equations` contains plain-text exact formulas.
- Computing the model does not invoke an SVD. Known-factor answers are verified
  against a fresh direct SVD in the tests, including epsilon=1e-6 and d=60.

## Regularization

- `d` integer 5–60, `rho` 0–.9, nonnegative noise, finite seed. `n=2d+20`.
- Raw Gaussian AR(1) columns have population correlation `rho^|j-k|`. Generating
  slopes are `[1.8,-1.4,1,.7,-.5,0,...]`; `rawTruth` gives these values. `truth`
  gives their equivalents after training feature standardization.
- X is centered and standardized to column RMS 1. y is centered and **unscaled**.
  Independent validation rows use training `xMeans`, `xScales`, and `yMean`.
  No intercept column is present or exempted from penalties.
- Objective: ridge `SSE/(2n)+lambda*L2²/2`; lasso `SSE/(2n)+lambda*L1`.
- `lambdas` has **62 ascending values**: 0 plus 61 logarithmic values from
  `.001*lambdaMax` to `100*lambdaMax`. Index 37 equals lambdaMax exactly.
  `lambdaMax=max_j |X_jᵀy|/n`.
- `ridge` and `lasso` contain 62 points with
  `{lambda,weights,l1,l2,l0,exactNonzeros,converged,kktViolation,kktTolerance,
  iterations,trainMSE,validationMSE,loss,penalty,objective,zeroTolerance,kind}`.
- **l0 is a numerical count `|weight|>1e-8`**, and is not a penalty objective.
  `exactNonzeros` counts literal nonzero floating-point coefficients. Coefficients
  are never rounded or thresholded after fitting. Lasso's soft-threshold update
  produces exact zero coefficients; finite ridge generally retains all features.
- L1, L2, and L0 paths are separately available as
  `normPaths.ridge.l1`, `.l2`, `.l0` and `normPaths.lasso.l1`, `.l2`, `.l0`.
  Each is `[{lambda,value,index},...]`.
- Both paths start with the same minimum-norm OLS solution at lambda=0. A single
  direct SVD supplies all ridge fits. Lasso uses descending warm starts and exact
  cyclic coordinate minimization. Final KKT residuals are recomputed from X/y
  directly, with absolute infinity tolerance 1e-7 and a 30,000-sweep cap.
- Dataset matrices and diagnostics are top-level. `dataset` contains only fixed
  data/statistics, without paths; `bestValidationIndex.{ridge,lasso}` and
  `allConverged` are convenience fields. Validation selection is a teaching aid,
  not an independent final test-error estimate.
- Results are read-only by convention. `regularization` caches eight datasets
  keyed by `(d,rho,noise,seed)`; changing the selected penalty reads existing paths.
  Conditioning has a separate eight-entry cache. `clearCache()` / `cacheInfo()`
  are available for verification.

## Verification

Run `node highdim-math.test.js`. Tests cover dimensions 5, 20, and 60; centered
orthogonal factors; exact formulas; direct OLS spectrum/fit cross-checks;
independent augmented-SVD ridge; independent residual-update lasso; direct-data
KKT conditions at every path point; noiseless sparse truth; rho=.9 and noise=2;
training-only transformations; separate norm paths; resampling and cache bounds;
and browser UMD loading. The script prints runtime measurements.
