/* HighDimMath: deterministic teaching datasets and numerically checked paths.
 * Load after linear-math.js. Node: require('./highdim-math.js').
 * All d coordinates are slopes; X and y are centered. There is no intercept
 * column. X columns in the regularization lab have mean-square norm 1;
 * y is centered but is NOT scaled. Validation uses training transformations.
 * Ridge: SSE/(2n) + lambda ||theta||_2^2/2.
 * Lasso: SSE/(2n) + lambda ||theta||_1.
 * Reported l0 counts |theta_j| > 1e-8. Coefficients themselves are not rounded.
 */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./linear-math.js'));
  else root.HighDimMath = factory(root.LinearMath);
})(typeof globalThis !== 'undefined' ? globalThis : this, function (M) {
  'use strict';
  if (!M || typeof M.svd !== 'function') throw new Error('HighDimMath requires LinearMath first');
  const ZERO_TOLERANCE = 1e-8, KKT_TOLERANCE = 1e-7, MAX_ITERATIONS = 30000;
  const conditioningCache = new Map(), regularizationCache = new Map();
  const zeros = n => Array(n).fill(0);
  const norm = a => Math.sqrt(M.dot(a, a));
  const mean = a => M.mean(a);
  function checkD(d) {
    if (!Number.isInteger(d) || d < 5 || d > 60) throw new Error('d must be an integer from 5 through 60');
  }
  function finiteRange(value, min, max, name) {
    if (!Number.isFinite(value) || value < min || value > max) throw new Error(name + ' must lie in [' + min + ', ' + max + ']');
  }
  function seedValue(seed) {
    if (!Number.isFinite(seed)) throw new Error('seed must be finite');
    return seed >>> 0;
  }
  function remember(cache, key, value) {
    if (cache.has(key)) cache.delete(key);
    cache.set(key, value);
    if (cache.size > 8) cache.delete(cache.keys().next().value);
    return value;
  }
  function recall(cache, key) {
    if (!cache.has(key)) return null;
    return remember(cache, key, cache.get(key));
  }
  /* Twice-reorthogonalized modified Gram-Schmidt, against the constant vector
   * too when centered=true. Only used when a seed/dimension changes. */
  function orthonormalColumns(rows, cols, random, centered) {
    const result = [];
    for (let j = 0; j < cols; j++) {
      let v, length;
      do {
        v = Array.from({ length: rows }, () => M.normal(random));
        for (let pass = 0; pass < 2; pass++) {
          if (centered) {
            const offset = mean(v);
            for (let i = 0; i < rows; i++) v[i] -= offset;
          }
          for (const q of result) {
            const projection = M.dot(q, v);
            for (let i = 0; i < rows; i++) v[i] -= projection * q[i];
          }
        }
        length = norm(v);
      } while (length < 1e-10);
      result.push(v.map(x => x / length));
    }
    return result;
  }
  function columnsToRows(columns) {
    return Array.from({ length: columns[0].length }, (_, i) => columns.map(column => column[i]));
  }
  function conditioningData(d = 20, seed = 1) {
    checkD(d); seed = seedValue(seed);
    const key = d + ':' + seed, cached = recall(conditioningCache, key);
    if (cached) return cached;
    const n = 2 * d, random = M.rng(seed);
    const Ucols = orthonormalColumns(n, d, random, true);
    const Vcols = orthonormalColumns(d, d, random, false);
    const baselineCoordinates = Array.from({ length: d - 1 }, () => M.normal(random));
    const scale = 1.5 / norm(baselineCoordinates);
    baselineCoordinates.push(0);
    for (let j = 0; j < d - 1; j++) baselineCoordinates[j] *= scale;
    const theta = zeros(d);
    for (let j = 0; j < d - 1; j++) for (let k = 0; k < d; k++) theta[k] += baselineCoordinates[j] * Vcols[j][k];
    return remember(conditioningCache, key, {
      n, d, seed, Ucols, Vcols, U: columnsToRows(Ucols), V: columnsToRows(Vcols),
      baselineCoordinates, theta, weakLeft: Ucols[d - 1], weakRight: Vcols[d - 1],
      baselineNorm: norm(theta), intercept: false
    });
  }
  function conditioning(d = 20, epsilon = 1e-3, delta = 0.005, seed = 1) {
    finiteRange(epsilon, 1e-6, 1, 'epsilon');
    finiteRange(delta, -0.01, 0.01, 'delta');
    const data = conditioningData(d, seed), { n, Ucols, Vcols, theta } = data;
    // Above epsilon=.3 lift the strong-spectrum floor so epsilon remains the
    // smallest singular value, including the well-conditioned epsilon=1 case.
    const floor = Math.max(0.3, epsilon);
    const singularValues = Array.from({ length: d - 1 }, (_, j) => 1 - (1 - floor) * j / (d - 2));
    singularValues.push(epsilon);
    const X = Array.from({ length: n }, () => zeros(d)), y = zeros(n);
    for (let k = 0; k < d; k++) for (let i = 0; i < n; i++) {
      const a = Ucols[k][i] * singularValues[k];
      y[i] += a * data.baselineCoordinates[k];
      for (let j = 0; j < d; j++) X[i][j] += a * Vcols[k][j];
    }
    const amplitude = delta / epsilon;
    const perturbedTheta = theta.map((v, j) => v + amplitude * data.weakRight[j]);
    const yPerturbed = y.map((v, i) => v + delta * data.weakLeft[i]);
    const normPath = Array.from({ length: 101 }, (_, j) => {
      const value = (j - 50) / 5000;
      return { delta: value, norm: Math.hypot(data.baselineNorm, value / epsilon) };
    });
    const predictionsBefore = M.matvec(X, theta), predictionsAfter = M.matvec(X, perturbedTheta);
    return {
      n, d, seed: data.seed, epsilon, delta, X, y, yPerturbed,
      U: data.U, V: data.V, weakLeft: data.weakLeft, weakRight: data.weakRight,
      theta: theta.slice(), perturbedTheta, coefficientBefore: theta.slice(), coefficientAfter: perturbedTheta.slice(),
      norm: data.baselineNorm, perturbedNorm: norm(perturbedTheta),
      coefficientChange: Math.abs(amplitude), predictionChange: Math.abs(delta), responseChange: Math.abs(delta),
      measuredCoefficientChange: norm(perturbedTheta.map((v, j) => v - theta[j])),
      measuredPredictionChange: norm(predictionsAfter.map((v, i) => v - predictionsBefore[i])),
      condition: 1 / epsilon, rank: d, singularValues, normPath,
      predictionsBefore, predictionsAfter,
      residualNormBefore: norm(y.map((v, i) => v - predictionsBefore[i])),
      residualNormAfter: norm(yPerturbed.map((v, i) => v - predictionsAfter[i])),
      intercept: false,
      equations: {
        design: 'X = U diag(sigma_1, ..., sigma_d) V^T',
        perturbation: 'y_delta = y + delta u_d',
        coefficients: 'theta_delta = theta + (delta/epsilon) v_d',
        coefficientChange: '||theta_delta-theta||_2 = |delta|/epsilon',
        predictionChange: '||X theta_delta-X theta||_2 = |delta|',
        norm: '||theta_delta||_2 = sqrt(1.5^2 + (delta/epsilon)^2)'
      }
    };
  }
  function arRows(n, d, rho, random) {
    const innovation = Math.sqrt(1 - rho * rho);
    return Array.from({ length: n }, () => {
      const row = [M.normal(random)];
      for (let j = 1; j < d; j++) row.push(rho * row[j - 1] + innovation * M.normal(random));
      return row;
    });
  }
  function gramStatistics(X, y) {
    const n = X.length, d = X[0].length;
    const columns = Array.from({ length: d }, (_, j) => X.map(row => row[j]));
    const gram = Array.from({ length: d }, () => zeros(d));
    for (let j = 0; j < d; j++) for (let k = 0; k <= j; k++) gram[j][k] = gram[k][j] = M.dot(columns[j], columns[k]) / n;
    return { columns, gram, correlation: columns.map(column => M.dot(column, y) / n) };
  }
  function gramGradient(gram, correlation, weights) {
    return gram.map((row, j) => M.dot(row, weights) - correlation[j]);
  }
  function directGradient(dataset, weights) {
    const residual = dataset.X.map((row, i) => M.dot(row, weights) - dataset.y[i]);
    return dataset.columns.map(column => M.dot(column, residual) / dataset.n);
  }
  function kktViolation(weights, gradient, lambda, kind) {
    let violation = 0;
    for (let j = 0; j < weights.length; j++) {
      const value = kind === 'ridge' ? Math.abs(gradient[j] + lambda * weights[j])
        : weights[j] !== 0 ? Math.abs(gradient[j] + lambda * Math.sign(weights[j]))
          : Math.max(0, Math.abs(gradient[j]) - lambda);
      violation = Math.max(violation, value);
    }
    return violation;
  }
  function fitPoint(dataset, weights, lambda, kind, iterations, converged) {
    const gradient = directGradient(dataset, weights);
    const violation = kktViolation(weights, gradient, lambda, kind);
    const l1 = weights.reduce((a, b) => a + Math.abs(b), 0), l2 = norm(weights);
    const trainMSE = M.mse(dataset.y, M.matvec(dataset.X, weights));
    const validationMSE = M.mse(dataset.validationY, M.matvec(dataset.validationX, weights));
    const penalty = lambda * (kind === 'ridge' ? l2 * l2 / 2 : l1);
    return {
      lambda, weights: weights.slice(), l1, l2,
      l0: weights.filter(w => Math.abs(w) > ZERO_TOLERANCE).length,
      exactNonzeros: weights.filter(w => w !== 0).length,
      zeroTolerance: ZERO_TOLERANCE, iterations,
      converged: converged && violation <= KKT_TOLERANCE,
      kktViolation: violation, kktTolerance: KKT_TOLERANCE,
      trainMSE, validationMSE, loss: trainMSE / 2, penalty, objective: trainMSE / 2 + penalty,
      kind
    };
  }
  function coordinateDescent(dataset, lambda, initial) {
    const { d, gram, correlation } = dataset, weights = initial.slice();
    let gradient = gramGradient(gram, correlation, weights), iterations = 0, converged = false;
    // A large lambda can certify the all-zero solution without a sweep.
    if (kktViolation(weights, gradient, lambda, 'lasso') <= KKT_TOLERANCE * 0.5) converged = true;
    while (!converged && iterations < MAX_ITERATIONS) {
      for (let j = 0; j < d; j++) {
        const rho = gram[j][j] * weights[j] - gradient[j];
        const next = M.softThreshold(rho, lambda) / gram[j][j];
        const difference = next - weights[j];
        weights[j] = next;
        if (difference) for (let k = 0; k < d; k++) gradient[k] += gram[k][j] * difference;
      }
      iterations++;
      // Recompute from fixed data; no accumulated-gradient stopping artifact.
      gradient = gramGradient(gram, correlation, weights);
      if (kktViolation(weights, gradient, lambda, 'lasso') <= KKT_TOLERANCE * 0.5) {
        gradient = directGradient(dataset, weights);
        converged = kktViolation(weights, gradient, lambda, 'lasso') <= KKT_TOLERANCE;
      }
    }
    return fitPoint(dataset, weights, lambda, 'lasso', iterations, converged);
  }
  function spectralWeights(svd, projections, n, lambda) {
    const d = svd.V.length, weights = zeros(d);
    for (let j = 0; j < svd.rank; j++) {
      const s = svd.singularValues[j];
      const amplitude = lambda ? s * projections[j] / (s * s + n * lambda) : projections[j] / s;
      for (let k = 0; k < d; k++) weights[k] += svd.V[k][j] * amplitude;
    }
    return weights;
  }
  function regularization(d = 20, rho = 0.6, noise = 0.7, seed = 1) {
    checkD(d); finiteRange(rho, 0, 0.9, 'rho');
    if (!Number.isFinite(noise) || noise < 0) throw new Error('noise must be finite and nonnegative');
    seed = seedValue(seed);
    const key = [d, rho, noise, seed].join(':'), cached = recall(regularizationCache, key);
    if (cached) return cached;
    const n = 2 * d + 20, validationN = Math.max(240, 4 * d), random = M.rng(seed);
    const rawTruth = zeros(d);
    [1.8, -1.4, 1, 0.7, -0.5].forEach((value, j) => { rawTruth[j] = value; });
    const rawX = arRows(n, d, rho, random), rawValidationX = arRows(validationN, d, rho, random);
    const rawY = rawX.map(row => M.dot(row, rawTruth) + noise * M.normal(random));
    const rawValidationY = rawValidationX.map(row => M.dot(row, rawTruth) + noise * M.normal(random));
    const xMeans = Array.from({ length: d }, (_, j) => mean(rawX.map(row => row[j])));
    const xScales = Array.from({ length: d }, (_, j) => Math.sqrt(mean(rawX.map(row => (row[j] - xMeans[j]) ** 2))));
    const transform = rows => rows.map(row => row.map((value, j) => (value - xMeans[j]) / xScales[j]));
    const X = transform(rawX), validationX = transform(rawValidationX), yMean = mean(rawY);
    const y = rawY.map(value => value - yMean), validationY = rawValidationY.map(value => value - yMean);
    const { gram, correlation, columns } = gramStatistics(X, y);
    const lambdaMax = Math.max(...correlation.map(Math.abs));
    // Exactly lambda=0, plus 61 logarithmic values including lambdaMax at i=36.
    const lambdas = [0, ...Array.from({ length: 61 }, (_, i) => lambdaMax * Math.pow(10, -3 + i / 12))];
    const dataset = {
      n, d, validationN, seed, rho, noise, X, y, validationX, validationY,
      rawX, rawY, rawValidationX, rawValidationY,
      rawTruth, truth: rawTruth.map((w, j) => w * xScales[j]),
      xMeans, xScales, yMean, yScale: 1,
      gram, correlation, columns, lambdaMax, intercept: false,
      standardization: 'Training X column mean 0, RMS 1; training y mean 0 (unscaled); validation uses training means and scales.'
    };
    const svd = M.svd(X), projections = Array.from({ length: d }, (_, j) => M.dot(svd.U.map(row => row[j]), y));
    const ridge = lambdas.map(lambda => fitPoint(dataset, spectralWeights(svd, projections, n, lambda), lambda, 'ridge', 0, true));
    const lasso = Array(lambdas.length);
    let initial = zeros(d);
    for (let i = lambdas.length - 1; i >= 1; i--) {
      lasso[i] = coordinateDescent(dataset, lambdas[i], initial);
      initial = lasso[i].weights;
    }
    // At lambda=0 both methods explicitly use the same minimum-norm OLS fit.
    lasso[0] = fitPoint(dataset, ridge[0].weights, 0, 'lasso', 0, true);
    const normPaths = {};
    for (const [kind, path] of [['ridge', ridge], ['lasso', lasso]]) {
      normPaths[kind] = {};
      for (const metric of ['l1', 'l2', 'l0']) normPaths[kind][metric] = path.map((point, index) => ({ lambda: point.lambda, value: point[metric], index }));
    }
    const bestIndex = path => path.reduce((best, point, index) => point.validationMSE < path[best].validationMSE ? index : best, 0);
    return remember(regularizationCache, key, Object.assign({}, dataset, {
      dataset, lambdas, ridge, lasso, normPaths,
      bestValidationIndex: { ridge: bestIndex(ridge), lasso: bestIndex(lasso) },
      singularValues: svd.singularValues, rank: svd.rank, condition: svd.condition,
      zeroTolerance: ZERO_TOLERANCE, kktTolerance: KKT_TOLERANCE,
      allConverged: ridge.every(point => point.converged) && lasso.every(point => point.converged),
      svdCount: 1,
      objectives: {
        ridge: '||X theta-y||_2^2/(2n) + lambda ||theta||_2^2/2',
        lasso: '||X theta-y||_2^2/(2n) + lambda ||theta||_1'
      }
    }));
  }
  function clearCache() { conditioningCache.clear(); regularizationCache.clear(); }
  function cacheInfo() { return { conditioning: conditioningCache.size, regularization: regularizationCache.size, limit: 8 }; }
  return {
    conditioningData, conditioning, regularization, clearCache, cacheInfo,
    ZERO_TOLERANCE, KKT_TOLERANCE, MAX_ITERATIONS,
    version: '1.0.0'
  };
});
