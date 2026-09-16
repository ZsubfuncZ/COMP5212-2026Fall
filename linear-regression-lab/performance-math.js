/* PerformanceMath: regression metrics and reproducible, untouched test sets.
 * Load after linear-math.js. Node: require('./performance-math.js').
 * No fitter, training transformation, or validation selection uses test data.
 */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./linear-math.js'));
  else root.PerformanceMath = factory(root.LinearMath);
})(typeof globalThis !== 'undefined' ? globalThis : this, function (M) {
  'use strict';
  if (!M || typeof M.rng !== 'function' || typeof M.normal !== 'function' || typeof M.dot !== 'function') {
    throw new Error('PerformanceMath requires LinearMath first');
  }

  function checkVector(a, name, length) {
    if (!(Array.isArray(a) || (ArrayBuffer.isView(a) && typeof a.length === 'number')) ||
        !a.length || (length !== undefined && a.length !== length)) {
      throw new TypeError(name + ': expected a nonempty vector' + (length === undefined ? '' : ' of length ' + length));
    }
    for (const v of a) if (!Number.isFinite(v)) throw new TypeError(name + ': all entries must be finite');
  }
  function sum(a) {
    let total = 0, correction = 0;
    for (const v of a) {
      const next = total + v;
      correction += Math.abs(total) >= Math.abs(v) ? (total - next) + v : (v - next) + total;
      total = next;
    }
    return total + correction;
  }
  function maxAbs(a) {
    let maximum = 0;
    for (const v of a) maximum = Math.max(maximum, Math.abs(v));
    return maximum;
  }
  // Scale before squaring, so small representable totals do not underflow
  // merely because individual squared terms would underflow.
  function squareSum(scale, normalizedSum) { return scale * (scale * normalizedSum); }
  function evaluate(actual, predicted) {
    checkVector(actual, 'actual'); checkVector(predicted, 'predicted', actual.length);
    const n = actual.length;
    const residuals = Array.from(actual, (v, i) => v - predicted[i]);
    if (residuals.some(v => !Number.isFinite(v))) throw new RangeError('Residual exceeds the finite numeric range');
    const residualScale = maxAbs(residuals);
    const residualUnits = residualScale ? residuals.map(v => v / residualScale) : residuals;
    const residualSquares = sum(residualUnits.map(v => v * v));
    const result = {
      mae: residualScale * (sum(residualUnits.map(Math.abs)) / n),
      mse: squareSum(residualScale, residualSquares / n),
      rmse: residualScale * Math.sqrt(residualSquares / n),
      r2: null, n,
      sse: squareSum(residualScale, residualSquares), sst: 0
    };
    if (Array.from(actual).every(v => v === actual[0])) {
      result.reason = 'undefined-constant-target';
      return result;
    }
    // Center offsets instead of subtracting a rounded, possibly very large
    // target mean. This still uses the mean of this evaluation set, never a
    // training mean. The fallback handles opposite-sign extreme magnitudes.
    let offsets = Array.from(actual, v => v - actual[0]);
    if (offsets.some(v => !Number.isFinite(v))) offsets = Array.from(actual);
    const targetScale = maxAbs(offsets);
    const targetUnits = offsets.map(v => v / targetScale);
    const meanUnit = sum(targetUnits) / n;
    const targetSquares = sum(targetUnits.map(v => (v - meanUnit) ** 2));
    result.sst = squareSum(targetScale, targetSquares);
    const scaleRatio = residualScale / targetScale;
    result.r2 = 1 - scaleRatio * (scaleRatio * (residualSquares / targetSquares));
    return result;
  }

  function checkCount(count) {
    if (!Number.isSafeInteger(count) || count < 1) throw new TypeError('count must be a positive safe integer');
  }
  function checkNoise(noise) {
    if (!Number.isFinite(noise) || noise < 0) throw new TypeError('noise must be finite and nonnegative');
  }
  // Purpose-tagged derived seeds do not consume the training RNG stream.
  // Features and noise get separate streams, so changing noise or count does
  // not redraw an existing feature prefix. All state belongs to one call.
  function stream(seed, purpose) {
    if (!Number.isFinite(seed)) throw new TypeError('seed must be finite');
    let hash = 2166136261;
    const tag = 'performance-test/v1/' + purpose;
    for (let i = 0; i < tag.length; i++) hash = Math.imul(hash ^ tag.charCodeAt(i), 16777619);
    let mixed = ((seed >>> 0) + (hash >>> 0) + 0x9e3779b9) >>> 0;
    mixed = Math.imul(mixed ^ (mixed >>> 16), 0x85ebca6b);
    mixed = Math.imul(mixed ^ (mixed >>> 13), 0xc2b2ae35);
    return M.rng((mixed ^ (mixed >>> 16)) >>> 0);
  }
  const scalarKinds = {
    energy: { low: 4, high: 6, truth: x => 100 + 5 * x + 3 * x * x,
      description: 'Independent test set with separate random streams: x ~ Uniform[4, 6], y = 100 + 5x + 3x² + Gaussian noise.' },
    curve: { low: -1, high: 1, truth: x => Math.sin(Math.PI * x) + 0.35 * x,
      description: 'Independent test set with separate random streams: x ~ Uniform[-1, 1], y = sin(πx) + 0.35x + Gaussian noise.' },
    'rank-deficient': { low: -2, high: 2, truth: x => 0.7 + 1.6 * x,
      description: 'Independent test set with separate random streams: x ~ Uniform[-2, 2], y = 0.7 + 1.6x + Gaussian noise; retain the training feature relation.' },
    gradient: { low: -2, high: 2, truth: x => 0.8 + 1.6 * x,
      description: 'Independent test set with separate random streams: x ~ Uniform[-2, 2], y = 0.8 + 1.6x + Gaussian noise.' },

  };
  function scalar(seed, kind, noise, count = 300) {
    if (!Object.prototype.hasOwnProperty.call(scalarKinds, kind)) throw new TypeError('Unknown scalar test kind: ' + kind);
    checkNoise(noise); checkCount(count);
    const spec = scalarKinds[kind], randomX = stream(seed, 'scalar/' + kind + '/features');
    const randomNoise = stream(seed, 'scalar/' + kind + '/noise');
    const x = Array.from({ length: count }, () => spec.low + (spec.high - spec.low) * randomX());
    const y = x.map(v => spec.truth(v) + noise * M.normal(randomNoise));
    return { x, y, n: count, description: spec.description };
  }
  function regularizationTest(a, seed, count = 300) {
    if (!a || typeof a !== 'object') throw new TypeError('Expected a regularization dataset');
    checkVector(a.rawTruth, 'rawTruth');
    const d = a.rawTruth.length;
    checkVector(a.xMeans, 'xMeans', d); checkVector(a.xScales, 'xScales', d);
    if (a.xScales.some(v => v <= 0)) throw new TypeError('xScales must be positive');
    if (!Number.isFinite(a.rho) || Math.abs(a.rho) > 1) throw new TypeError('rho must lie in [-1, 1]');
    if (!Number.isFinite(a.yMean)) throw new TypeError('yMean must be finite');
    checkNoise(a.noise); checkCount(count);
    const randomX = stream(seed, 'regularization/features'), randomNoise = stream(seed, 'regularization/noise');
    const innovation = Math.sqrt(1 - a.rho * a.rho), X = [], y = [];
    for (let i = 0; i < count; i++) {
      const raw = [M.normal(randomX)];
      for (let j = 1; j < d; j++) raw.push(a.rho * raw[j - 1] + innovation * M.normal(randomX));
      y.push(M.dot(raw, a.rawTruth) + a.noise * M.normal(randomNoise));
      X.push(raw.map((value, j) => (value - a.xMeans[j]) / a.xScales[j]));
    }
    return { X, y, centeredY: y.map(value => value - a.yMean), n: count,
      description: 'Independent test observations from separate random streams, with correlated Gaussian features and the same sparse model. Features use training means and scales; scores use original response units.' };
  }
  function conditioningTest(a, seed, count = 300) {
    if (!a || typeof a !== 'object') throw new TypeError('Expected a conditioning dataset');
    checkVector(a.theta, 'theta');
    const d = a.theta.length;
    checkVector(a.singularValues, 'singularValues', d);
    if (a.singularValues.some(v => v < 0)) throw new TypeError('singularValues must be nonnegative');
    if (!Array.isArray(a.V) || a.V.length !== d) throw new TypeError('V must be a square matrix');
    for (const row of a.V) checkVector(row, 'V row', d);
    if (!Number.isSafeInteger(a.n) || a.n < 1) throw new TypeError('Training n must be a positive safe integer');
    checkCount(count);
    const random = stream(seed, 'conditioning/features'), rootN = Math.sqrt(a.n);
    const X = Array.from({ length: count }, () => {
      const scores = a.singularValues.map(s => (s / rootN) * M.normal(random));
      return a.V.map(row => M.dot(row, scores));
    });
    const y = X.map(row => M.dot(row, a.theta));
    return { X, y, n: count,
      description: 'Independent noiseless Gaussian test rows from a separate random stream: covariance V diag(s²/n_train) Vᵀ, y = Xθ₀. Low variance in weak directions permits large coefficient changes with small test error.' };
  }

  return { evaluate, scalar, regularizationTest, conditioningTest, version: '1.0.0' };
});
