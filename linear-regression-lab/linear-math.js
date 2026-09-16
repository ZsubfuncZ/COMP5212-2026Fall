/* LinearMath: deterministic, dependency-free numerical routines for teaching.
 * Browser: globalThis.LinearMath. Node: require('./linear-math.js').
 *
 * X is ALWAYS an explicit n-by-p design; no function inserts an intercept.
 * In ridge/lasso, options.intercept=true (default) exempts column 0 from the
 * penalty. Supply a column of ones if that coefficient represents an intercept.
 * Objectives:
 *   OLS:   ||Xw-y||^2/(2n)
 *   ridge: ||Xw-y||^2/(2n) + lambda*||w_penalized||^2/2
 *   lasso: ||Xw-y||^2/(2n) + lambda*||w_penalized||_1
 * Returned `loss` is the DATA term; `objective` includes `penalty`.
 * Polynomial ridge penalizes MONOMIAL coefficients on the supplied [-1,1]
 * domain. Changing basis or units changes this penalty.
 * Kernel ridge uses ||y-b-K alpha||^2/(2n) + lambda*alpha'K alpha/2.
 * The unpenalized intercept is implemented by centering K and y, including
 * the correct training-derived centering for a new kernel vector.
 */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LinearMath = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const EPS = Number.EPSILON;
  const vectorLike = a => Array.isArray(a) || ArrayBuffer.isView(a);
  function checkVector(a, name, length) {
    if (!vectorLike(a) || !a.length || (length !== undefined && a.length !== length)) {
      throw new Error(name + ': expected a nonempty vector' + (length === undefined ? '' : ' of length ' + length));
    }
    for (const v of a) if (!Number.isFinite(v)) throw new Error(name + ': all entries must be finite');
  }
  function checkMatrix(X, y) {
    if (!Array.isArray(X) || !X.length || !vectorLike(X[0]) || !X[0].length) {
      throw new Error('X: expected a nonempty rectangular matrix');
    }
    const p = X[0].length;
    for (const row of X) checkVector(row, 'X row', p);
    if (y !== undefined) checkVector(y, 'y', X.length);
    return [X.length, p];
  }
  function checkLambda(lambda) {
    if (!Number.isFinite(lambda) || lambda < 0) throw new Error('lambda must be finite and nonnegative');
  }
  function sum(a) {
    let s = 0, correction = 0;
    for (const v of a) {
      const t = s + v;
      correction += Math.abs(s) >= Math.abs(v) ? (s - t) + v : (v - t) + s;
      s = t;
    }
    return s + correction;
  }
  function mean(a) { checkVector(a, 'mean'); return sum(a) / a.length; }
  function dot(a, b) {
    if (!vectorLike(a) || !vectorLike(b) || a.length !== b.length) throw new Error('dot: vector lengths must match');
    let s = 0, correction = 0;
    for (let j = 0; j < a.length; j++) {
      const v = a[j] * b[j], t = s + v;
      correction += Math.abs(s) >= Math.abs(v) ? (s - t) + v : (v - t) + s;
      s = t;
    }
    return s + correction;
  }
  function matvec(X, w) {
    const [, p] = checkMatrix(X);
    checkVector(w, 'weights', p);
    return X.map(row => dot(row, w));
  }
  function mse(actual, predicted) {
    checkVector(actual, 'actual');
    if (predicted !== undefined) checkVector(predicted, 'predicted', actual.length);
    let s = 0;
    for (let i = 0; i < actual.length; i++) {
      const r = actual[i] - (predicted === undefined ? 0 : predicted[i]);
      s += r * r;
    }
    return s / actual.length;
  }
  function rng(seed = 1) {
    let a = Number(seed) >>> 0;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function normal(random = Math.random) {
    return Math.sqrt(-2 * Math.log(Math.max(Number.MIN_VALUE, 1 - random()))) * Math.cos(2 * Math.PI * random());
  }
  function identity(p) { return Array.from({ length: p }, (_, i) => Array.from({ length: p }, (_, j) => +(i === j))); }

  /* Direct one-sided Jacobi SVD. Rotate columns of X, never form X'X.
   * B=X V has mutually orthogonal columns; their norms are singular values.
   * Full p-column U/V storage includes zero columns in U for null directions.
   * The rank threshold is max(n,p)*eps*s_max, stated in returned diagnostics.
   * This is a numerical rank decision, not a statistical noise threshold.
   */
  function svd(X) {
    const [n, p] = checkMatrix(X);
    let scale = 0;
    for (const row of X) for (const x of row) scale = Math.max(scale, Math.abs(x));
    if (!scale) return {
      U: Array.from({ length: n }, () => Array(p).fill(0)), V: identity(p),
      singularValues: Array(p).fill(0), rank: 0, tolerance: 0,
      condition: Infinity, sweeps: 0, converged: true
    };
    // Column storage makes all inner products and rotations contiguous.
    const B = Array.from({ length: p }, (_, j) => X.map(row => row[j] / scale));
    const Vcols = identity(p);
    const initialLargestNorm = Math.sqrt(Math.max(...B.map(col => dot(col, col))));
    const zeroNorm = EPS * Math.max(n, p) * initialLargestNorm;
    const maxSweeps = Math.max(40, 8 * p);
    let converged = false, sweeps = 0;
    for (; sweeps < maxSweeps; sweeps++) {
      let rotated = false;
      for (let a = 0; a < p - 1; a++) for (let b = a + 1; b < p; b++) {
        const aa = dot(B[a], B[a]), bb = dot(B[b], B[b]);
        if (Math.sqrt(aa) <= zeroNorm || Math.sqrt(bb) <= zeroNorm) continue;
        const ab = dot(B[a], B[b]);
        if (Math.abs(ab) <= 4 * EPS * Math.sqrt(aa) * Math.sqrt(bb)) continue;
        const tau = (bb - aa) / (2 * ab);
        const t = (tau >= 0 ? 1 : -1) / (Math.abs(tau) + Math.hypot(1, tau));
        if (!t) continue;
        const c = 1 / Math.hypot(1, t), s = c * t;
        for (let i = 0; i < n; i++) {
          const u = B[a][i], v = B[b][i];
          B[a][i] = c * u - s * v; B[b][i] = s * u + c * v;
        }
        for (let i = 0; i < p; i++) {
          const u = Vcols[a][i], v = Vcols[b][i];
          Vcols[a][i] = c * u - s * v; Vcols[b][i] = s * u + c * v;
        }
        rotated = true;
      }
      if (!rotated) { converged = true; sweeps++; break; }
    }
    if (!converged) throw new Error('Direct Jacobi SVD did not converge');
    const norms = B.map(col => Math.sqrt(dot(col, col)));
    const order = Array.from({ length: p }, (_, j) => j).sort((a, b) => norms[b] - norms[a]);
    const singularValues = order.map(j => norms[j] * scale);
    const tolerance = Math.max(n, p) * EPS * singularValues[0];
    const rank = Math.min(n, singularValues.filter(s => s > tolerance).length);
    const U = Array.from({ length: n }, (_, i) => order.map(j => norms[j] > 0 ? B[j][i] / norms[j] : 0));
    const V = Array.from({ length: p }, (_, i) => order.map(j => Vcols[j][i]));
    return {
      U, V, singularValues, rank, tolerance,
      condition: rank === p ? singularValues[0] / singularValues[p - 1] : Infinity,
      sweeps, converged
    };
  }
  function spectralSolve(s, y) {
    const n = y.length, p = s.V.length, weights = Array(p).fill(0);
    for (let j = 0; j < s.rank; j++) {
      const u = Array.from({ length: n }, (_, i) => s.U[i][j]);
      const a = dot(u, y) / s.singularValues[j];
      for (let k = 0; k < p; k++) weights[k] += s.V[k][j] * a;
    }
    return weights;
  }
  function result(X, y, weights, penalty = 0) {
    const predictions = matvec(X, weights);
    const error = mse(y, predictions);
    return {
      weights, predictions, residuals: Array.from(y, (v, i) => v - predictions[i]),
      mse: error, loss: error / 2, penalty, objective: error / 2 + penalty
    };
  }
  function diagnostics(s) {
    return { rank: s.rank, singularValues: s.singularValues, condition: s.condition,
      tolerance: s.tolerance, svdSweeps: s.sweeps };
  }
  function ols(X, y) {
    checkMatrix(X, y);
    const s = svd(X);
    return Object.assign(result(X, y, spectralSolve(s, y)), diagnostics(s));
  }
  function ridge(X, y, lambda = 0, options = {}) {
    const [n, p] = checkMatrix(X, y); checkLambda(lambda);
    const first = options.intercept === false ? 0 : 1;
    const original = svd(X);
    if (!lambda) return Object.assign(result(X, y, spectralSolve(original, y)), diagnostics(original), { lambda });
    // Project out the unpenalized column before augmentation. For a column
    // of ones this is exactly centering X and y. It also prevents very large
    // lambda from making the unpenalized intercept look numerically absent.
    const column0 = X.map(row => row[0]), norm0 = dot(column0, column0);
    const y0 = first && norm0 ? dot(column0, y) / norm0 : 0;
    const offsets = Array.from({ length: p - first }, (_, j) =>
      first && norm0 ? dot(column0, X.map(row => row[j + first])) / norm0 : 0);
    if (first && p === 1) return Object.assign(result(X, y, [y0]), diagnostics(original), { lambda });
    const augmented = X.map(row => row.slice(first).map((v, j) => v - (first ? row[0] * offsets[j] : 0)));
    const target = Array.from(y, (v, i) => v - (first ? column0[i] * y0 : 0));
    for (let j = 0; j < p - first; j++) {
      const row = Array(p - first).fill(0); row[j] = Math.sqrt(n) * Math.sqrt(lambda);
      augmented.push(row); target.push(0);
    }
    const slopes = spectralSolve(svd(augmented), target);
    const weights = first ? [norm0 ? y0 - dot(offsets, slopes) : 0, ...slopes] : slopes;
    const penalty = lambda * sum(weights.slice(first).map(w => w * w)) / 2;
    return Object.assign(result(X, y, weights, penalty), diagnostics(original), { lambda });
  }

  function softThreshold(value, threshold) {
    checkLambda(threshold);
    if (!Number.isFinite(value)) throw new Error('softThreshold: value must be finite');
    return value > threshold ? value - threshold : value < -threshold ? value + threshold : 0;
  }
  function gradientFromResidual(X, residual) {
    const n = X.length, p = X[0].length;
    return Array.from({ length: p }, (_, j) => -sum(X.map((row, i) => row[j] * residual[i])) / n);
  }
  function lassoKKT(weights, gradient, lambda, first) {
    let violation = 0;
    for (let j = 0; j < weights.length; j++) {
      const v = j < first ? Math.abs(gradient[j]) : weights[j] !== 0
        ? Math.abs(gradient[j] + lambda * Math.sign(weights[j]))
        : Math.max(0, Math.abs(gradient[j]) - lambda);
      violation = Math.max(violation, v);
    }
    return violation;
  }
  /* Exact one-coordinate minimization, cyclic order. The stopping criterion
   * is an absolute KKT infinity-norm residual, not a small parameter change.
   * Collinearity can make coefficients nonunique and convergence slow.
   */
  function lasso(X, y, lambda = 0, options = {}) {
    const [n, p] = checkMatrix(X, y); checkLambda(lambda);
    const first = options.intercept === false ? 0 : 1;
    const maxIter = options.maxIter === undefined ? 10000 : options.maxIter;
    const tol = options.tol === undefined ? 1e-8 : options.tol;
    if (!Number.isInteger(maxIter) || maxIter < 1) throw new Error('maxIter must be a positive integer');
    if (!Number.isFinite(tol) || tol <= 0) throw new Error('tol must be finite and positive');
    if (!lambda) {
      const model = ols(X, y), gradient = gradientFromResidual(X, model.residuals);
      const kktViolation = lassoKKT(model.weights, gradient, 0, first);
      return Object.assign(model, { lambda, iterations: 0, converged: kktViolation <= tol,
        kktViolation, kktTolerance: tol, gradient });
    }
    const weights = options.initial === undefined ? Array(p).fill(0) : Array.from(options.initial);
    checkVector(weights, 'initial weights', p);
    let residual = Array.from(y, (v, i) => v - dot(X[i], weights));
    const columns = Array.from({ length: p }, (_, j) => X.map(row => row[j]));
    const norm2 = columns.map(col => dot(col, col) / n);
    let iterations = 0, converged = false, kktViolation = Infinity, gradient;
    for (; iterations < maxIter; iterations++) {
      for (let j = 0; j < p; j++) {
        const old = weights[j];
        const rho = dot(columns[j], residual) / n + norm2[j] * old;
        const next = norm2[j] > 0 ? (j < first ? rho : softThreshold(rho, lambda)) / norm2[j] : 0;
        weights[j] = next;
        for (let i = 0; i < n; i++) residual[i] += columns[j][i] * (old - next);
      }
      // Recompute from original data so accumulated updates cannot fake KKT.
      residual = Array.from(y, (v, i) => v - dot(X[i], weights));
      gradient = gradientFromResidual(X, residual);
      kktViolation = lassoKKT(weights, gradient, lambda, first);
      if (kktViolation <= tol) { converged = true; iterations++; break; }
    }
    const penalty = lambda * sum(weights.slice(first).map(Math.abs));
    return Object.assign(result(X, y, weights, penalty), {
      lambda, iterations, converged, kktViolation, kktTolerance: tol, gradient
    });
  }

  function scalarFit(x, y) {
    checkVector(x, 'x'); checkVector(y, 'y', x.length);
    const model = ols(Array.from(x, v => [1, v]), y);
    return Object.assign(model, { intercept: model.weights[0], slope: model.weights[1],
      predict: value => model.weights[0] + model.weights[1] * value });
  }
  function polynomialRow(x, degree) {
    const row = [1];
    for (let j = 1; j <= degree; j++) row.push(row[j - 1] * x);
    return row;
  }
  function fitPolynomial(x, y, degree = 1, lambda = 0) {
    checkVector(x, 'x'); checkVector(y, 'y', x.length); checkLambda(lambda);
    if (!Number.isInteger(degree) || degree < 0 || degree > 30) throw new Error('degree must be an integer from 0 through 30');
    for (const v of x) if (v < -1 || v > 1) throw new Error('fitPolynomial: training x must lie in [-1,1]');
    const model = ridge(Array.from(x, v => polynomialRow(v, degree)), y, lambda, { intercept: true });
    model.degree = degree; model.basis = 'monomial';
    model.predict = value => {
      if (!Number.isFinite(value)) throw new Error('predict: value must be finite');
      let total = 0;
      for (let j = degree; j >= 0; j--) total = total * value + model.weights[j];
      return total;
    };
    return model;
  }

  /* Symmetric Jacobi eigensolver for the already-defined kernel matrix.
   * This is NOT used to compute the OLS singular values from a Gram matrix.
   */
  function symmetricEigen(matrix) {
    const n = matrix.length, A = matrix.map(row => row.slice()), V = identity(n);
    let scale = 0;
    for (const row of A) for (const x of row) scale = Math.max(scale, Math.abs(x));
    const tol = Math.max(Number.MIN_VALUE, 4 * EPS * scale);
    let converged = n <= 1 || !scale;
    for (let sweep = 0; !converged && sweep < 80; sweep++) {
      let off = 0;
      for (let p = 0; p < n - 1; p++) for (let q = p + 1; q < n; q++) {
        const apq = A[p][q]; off = Math.max(off, Math.abs(apq));
        if (Math.abs(apq) <= tol) continue;
        const tau = (A[q][q] - A[p][p]) / (2 * apq);
        const t = (tau >= 0 ? 1 : -1) / (Math.abs(tau) + Math.hypot(1, tau));
        const c = 1 / Math.hypot(1, t), s = t * c;
        A[p][p] -= t * apq; A[q][q] += t * apq;
        A[p][q] = A[q][p] = 0;
        for (let k = 0; k < n; k++) {
          if (k !== p && k !== q) {
            const a = A[k][p], b = A[k][q];
            A[k][p] = A[p][k] = c * a - s * b;
            A[k][q] = A[q][k] = s * a + c * b;
          }
          const a = V[k][p], b = V[k][q];
          V[k][p] = c * a - s * b; V[k][q] = s * a + c * b;
        }
      }
      converged = off <= tol;
    }
    if (!converged) throw new Error('Kernel eigensolver did not converge');
    const order = Array.from({ length: n }, (_, j) => j).sort((a, b) => A[b][b] - A[a][a]);
    return { values: order.map(j => A[j][j]), vectors: V.map(row => order.map(j => row[j])) };
  }
  function kernelRidge(x, y, lambda = 0.01, gamma = 1) {
    checkVector(x, 'x'); checkVector(y, 'y', x.length); checkLambda(lambda);
    if (!Number.isFinite(gamma) || gamma < 0) throw new Error('gamma must be finite and nonnegative');
    const trainX = Array.from(x), n = x.length, yMean = mean(y);
    const kernel = (a, b) => gamma === 0 ? 1 : Math.exp(-gamma * (a - b) * (a - b));
    const K = trainX.map(a => trainX.map(b => kernel(a, b)));
    const rowMeans = K.map(mean), grandMean = mean(rowMeans);
    const Kc = K.map((row, i) => row.map((v, j) => v - rowMeans[i] - rowMeans[j] + grandMean));
    const yc = Array.from(y, v => v - yMean), eig = symmetricEigen(Kc);
    const maxEigen = Math.max(0, eig.values[0]);
    // Centering nearly constant kernels subtracts numbers near one. Its
    // absolute roundoff is governed by K, not only by the much smaller Kc.
    const originalNormBound = Math.max(...K.map(row => sum(row.map(Math.abs))));
    const tolerance = n * EPS * Math.max(maxEigen, originalNormBound);
    const eigenvalues = eig.values.map(v => Math.max(0, v));
    const alpha = Array(n).fill(0);
    for (let j = 0; j < n; j++) {
      if (!lambda && eigenvalues[j] <= tolerance) continue;
      const projection = dot(eig.vectors.map(row => row[j]), yc);
      const coefficient = projection / (eigenvalues[j] + n * lambda);
      for (let i = 0; i < n; i++) alpha[i] += eig.vectors[i][j] * coefficient;
    }
    // Centering annihilates constants. Enforce this constraint explicitly to
    // remove harmless null-direction roundoff from the dual representation.
    const alphaMean = mean(alpha);
    for (let i = 0; i < n; i++) alpha[i] -= alphaMean;
    const predict = value => {
      if (!Number.isFinite(value)) throw new Error('predict: value must be finite');
      const k = trainX.map(v => kernel(value, v)), newMean = mean(k);
      return yMean + dot(k.map((v, j) => v - newMean - rowMeans[j] + grandMean), alpha);
    };
    const predictions = trainX.map(predict), error = mse(y, predictions);
    // Equivalent RKHS norm computed spectrally avoids tiny negative roundoff.
    let norm2 = 0;
    for (let j = 0; j < n; j++) {
      const a = dot(eig.vectors.map(row => row[j]), alpha);
      norm2 += eigenvalues[j] * a * a;
    }
    const penalty = lambda * norm2 / 2;
    return {
      x: trainX, alpha, intercept: yMean - dot(rowMeans, alpha), predict,
      lambda, gamma, yMean, rowMeans, grandMean, eigenvalues,
      rank: eigenvalues.filter(v => v > tolerance).length, tolerance,
      predictions, residuals: Array.from(y, (v, i) => v - predictions[i]),
      mse: error, loss: error / 2, penalty, objective: error / 2 + penalty
    };
  }
  function gradientStats(X, y, theta) {
    const [n, p] = checkMatrix(X, y); checkVector(theta, 'theta', p);
    const residual = Array.from(y, (v, i) => v - dot(X[i], theta));
    const spectral = svd(X);
    return { gradient: gradientFromResidual(X, residual), loss: mse(residual) / 2,
      L: spectral.singularValues[0] * spectral.singularValues[0] / n };
  }

  return { rng, normal, mean, mse, dot, matvec, svd, ols, ridge, lasso,
    softThreshold, scalarFit, fitPolynomial, kernelRidge, gradientStats };
});
