# PerformanceMath API

Load `linear-math.js`, then `performance-math.js`. Browser global: `PerformanceMath`.
For CommonJS, put the two assets beside one another and call `require('./performance-math.js')`.
`HighDimMath` is needed to create the high-dimensional training objects, but is not a runtime dependency of PerformanceMath itself.

## `evaluate(actual, predicted)`

Returns `{mae, mse, rmse, r2, n, sse, sst, reason?}`. Both inputs must be nonempty equally sized arrays or numeric typed arrays containing only finite numbers; invalid inputs throw. No input is mutated.

- `mae = sum(abs(actual - predicted))/n`.
- `sse = sum((actual - predicted)²)` and `mse = sse/n`; RMSE is the square root of MSE.
- `sst = sum((actual - mean(actual))²)` uses the targets in **the set being evaluated**. For a test-set call this is the test-target mean, never the training-target mean.
- `r2 = 1 - sse/sst`; a negative R² is retained. The constant mean predictor has R² zero on nonconstant targets.
- If every target equals the same value, including a perfect prediction or a singleton, `r2` is `null` and `reason` is `'undefined-constant-target'`. The other error metrics remain available.

Compensated sums, scaled squares, and centering relative to an offset reduce roundoff and avoid unnecessary overflow/underflow. A residual that cannot be represented as a finite JavaScript number throws a RangeError. A squared total larger than JavaScript's representable range can still be Infinity; values below it can be zero. R² is calculated from normalized quantities so underflow of the displayed squared totals does not turn a nonconstant target into a constant target. A caller should handle a diverged fit before attempting to evaluate its predictions.

## `scalar(seed, kind, noise, count = 300)`

Returns `{x, y, n, description}`. Noise is a nonnegative Gaussian standard deviation. The seed must be finite and is reduced to unsigned 32-bit form, matching LinearMath. `count` is a positive safe integer.

| kind | x distribution | response before noise |
| --- | --- | --- |
| `energy` | Uniform[4, 6] | 100 + 5x + 3x² |
| `curve` | Uniform[-1, 1] | sin(πx) + 0.35x |
| `rank-deficient` | Uniform[-2, 2] | 0.7 + 1.6x |
| `gradient` | Uniform[-2, 2] | 0.8 + 1.6x |

Use the requested training noise setting. Typical gradient noise is `0.3`. For the rank-deficient lab, build the test design with the same feature identity as the training design.

## `regularizationTest(a, seed, count = 300)`

`a` is a `HighDimMath.regularization(...)` result, or its `.dataset`. Required fields: `rawTruth`, `rho`, `noise`, `xMeans`, `xScales`, and `yMean`.

Returns `{X, y, centeredY, n, description}`. New raw feature rows are stationary Gaussian AR(1): first coordinate N(0,1), then `x[j] = rho*x[j-1] + sqrt(1-rho²)*z[j]`. Raw responses are `dot(rawX, a.rawTruth) + a.noise*z`.

`X[i][j] = (rawX[i][j] - a.xMeans[j])/a.xScales[j]` uses training statistics unchanged. `y` remains raw and `centeredY[i] = y[i] - a.yMean`. Do not recenter or rescale the test sample. Evaluate a fitted path point with:

```js
const test = PerformanceMath.regularizationTest(a, seed);
const prediction = LinearMath.matvec(test.X, point.weights).map(v => v + a.yMean);
const metrics = PerformanceMath.evaluate(test.y, prediction);
```

## `conditioningTest(a, seed, count = 300)`

`a` is a `HighDimMath.conditioning(...)` result. Required fields: `V`, `singularValues`, training sample count `n`, and unperturbed `theta`.

Returns `{X, y, n, description}`. Each test row is `V diag(s/sqrt(n_train)) z`, with independent standard Gaussian coordinates `z`. Its covariance is `V diag(s²/n_train) Vᵀ`, matching `X_trainᵀ X_train/n_train`. Responses are noiseless `y = X theta`; they do not use the perturbed target or `perturbedTheta`.

The weak right-singular direction has test variance `epsilon²/n_train`. A coefficient displacement `delta/epsilon` therefore produces expected test MSE `delta²/n_train` in that direction. A large coefficient displacement can coexist with a small test error under this distribution. This does not establish robustness under a distribution shift that puts more mass along the weak direction.

## Reproducibility and separation

Each call derives fresh, purpose-tagged seeds from the supplied seed and creates local LinearMath RNGs. Scalar kinds, the two high-dimensional labs, feature draws, and noise draws have distinct purposes. The function never advances a training/validation RNG, modifies a training result, caches a caller-owned array, or uses a selected model/fit/lambda/radius/probe as input. The same call repeats bit for bit. Increasing count preserves the existing sample prefix. Changing noise preserves feature draws. In conditioning, changing only delta leaves the test sample identical.

Generate the sample from the same training-data seed and data-generating parameters whenever the UI redraws. Keep hyperparameter selection on validation data; the test set is for reporting performance after fitting or selecting a model.

## Tests

Run `node performance-math.test.cjs`. Dependencies are read beside the test file if present, otherwise from `../../site/dist/`. The tests exercise the browser global branch with the existing LinearMath and HighDimMath assets. They cover hand calculations, negative/constant R², floating-point centering, invalid inputs, scalar truths, independent streams, prefix reproducibility, unchanged training preprocessing, covariance orientation, and the weak-direction test-risk calculation.
