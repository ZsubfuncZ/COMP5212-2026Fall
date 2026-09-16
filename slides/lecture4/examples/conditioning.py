"""Reproduce the controlled examples using Python binary64 arithmetic."""
import json
import math
from pathlib import Path

epsilon = 1e-4
delta = 1e-3
w = (0.5 + delta / (2 * epsilon), 0.5 - delta / (2 * epsilon))
assert w == (5.5, -4.5)
assert abs(w[0] + w[1] - 1) < 1e-14
assert abs(epsilon * (w[0] - w[1]) - delta) < 1e-14
assert abs((w[0] - 0.5) - (w[1] - 0.5) - 10) < 1e-14

# The exact explicit operation sequence printed on the floating-point slide.
e = 1e-8
d = 1.0 + e * e
c = 1.0 - e * e
small_eigenvalue = d - c
rounded_gram_coefficient = e / small_eigenvalue
exact_coefficient = 1.0 / (2 * e)
assert d == 1.0
assert c == 1.0 - 2.0**-53
assert small_eigenvalue == 2.0**-53
assert abs(rounded_gram_coefficient / exact_coefficient - 1 - 0.8014398509481985) < 1e-15

ridge = []
for lam in (0.0, 1e-6, 1e-4):
    common = 1 / (2 * (1 + lam))
    difference = delta * epsilon / (2 * (epsilon * epsilon + lam))
    weights = [common + difference, common - difference]
    prediction = [sum(weights), epsilon * (weights[0] - weights[1])]
    residual = [prediction[0] - 1, prediction[1] - delta]
    mse = sum(v*v for v in residual) / 2
    gradient = [(residual[0] + epsilon * residual[1]) / 2 + lam * weights[0],
                (residual[0] - epsilon * residual[1]) / 2 + lam * weights[1]]
    assert max(map(abs, gradient)) < 1e-15
    ridge.append(dict(lambda_=lam, weights=weights, training_mse=mse,
                      strong_shrink=1/(1+lam),
                      weak_shrink=epsilon**2/(epsilon**2+lam)))

report = dict(condition_number=1/epsilon, perturbed_weights=w,
              perturbation_norm=delta/(math.sqrt(2)*epsilon),
              binary64=dict(epsilon=e, gram_diagonal=d, gram_offdiagonal=c,
                            gram_small_eigenvalue=small_eigenvalue,
                            exact_small_eigenvalue=2*e*e,
                            coefficient_from_rounded_gram=rounded_gram_coefficient,
                            exact_coefficient=exact_coefficient,
                            relative_error=abs(rounded_gram_coefficient/exact_coefficient-1)),
              ridge=ridge)
Path(__file__).with_name('conditioning-results.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
