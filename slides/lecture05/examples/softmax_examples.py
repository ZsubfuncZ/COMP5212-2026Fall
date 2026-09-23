#!/usr/bin/env python3
"""Recompute lecture examples and verify the softmax matrix gradient.

Python standard library only. No files are written. The editable PGFPlots
figures evaluate the same analytical functions directly in LaTeX.
"""
from math import exp, fsum, isclose, log


def softmax(scores, temperature=1.0):
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    maximum = max(scores)
    values = [exp((score - maximum) / temperature) for score in scores]
    normalizer = fsum(values)
    return [value / normalizer for value in values]


def cross_entropy(scores, true_class):
    """true_class is a zero-based index; slides number classes starting at 1."""
    maximum = max(scores)
    return maximum - scores[true_class] + log(
        fsum(exp(score - maximum) for score in scores)
    )


def scores_for_rows(X, W):
    return [
        [fsum(x[j] * W[j][k] for j in range(len(x)))
         for k in range(len(W[0]))]
        for x in X
    ]


def objective(X, W, labels):
    return fsum(cross_entropy(z, y)
                for z, y in zip(scores_for_rows(X, W), labels)) / len(X)


def gradient(X, W, labels):
    P = [softmax(z) for z in scores_for_rows(X, W)]
    return [
        [fsum(X[i][j] * (P[i][k] - (labels[i] == k))
              for i in range(len(X))) / len(X)
         for k in range(len(W[0]))]
        for j in range(len(W))
    ]


def check_examples():
    z = [2.0, 1.0, 0.0]
    probabilities = softmax(z)
    print("Logits:", z)
    print("Exponentials:", [round(exp(v), 9) for v in z])
    print("Normalizer:", f"{fsum(exp(v) for v in z):.9f}")
    print("Probabilities:", [round(p, 9) for p in probabilities])
    print("Per-label cross-entropies:",
          [round(cross_entropy(z, k), 9) for k in range(3)])
    for T in [0.5, 1.0, 2.0, 4.0]:
        p = softmax(z, T)
        print(f"T={T:g}:", [round(value, 9) for value in p])
        assert max(range(3), key=p.__getitem__) == 0
    assert all(isclose(a, b, abs_tol=1e-14)
               for a, b in zip(probabilities, softmax([1002, 1001, 1000])))
    assert isclose(probabilities[0] / probabilities[1], exp(1), rel_tol=1e-14)
    assert isclose(fsum(probabilities), 1, abs_tol=1e-14)

    # Two examples, three features INCLUDING intercept, and three class columns.
    X = [[1.0, 0.2, -0.5], [1.0, -0.7, 0.9]]
    W = [[0.1, -0.2, 0.0], [0.3, 0.4, -0.1], [-0.2, 0.6, 0.2]]
    labels = [0, 2]
    analytic = gradient(X, W, labels)
    h = 1e-6
    maximum_error = 0.0
    for j in range(3):
        assert isclose(fsum(analytic[j]), 0, abs_tol=1e-14)
        for k in range(3):
            plus = [row[:] for row in W]
            minus = [row[:] for row in W]
            plus[j][k] += h
            minus[j][k] -= h
            numeric = (objective(X, plus, labels) - objective(X, minus, labels)) / (2*h)
            maximum_error = max(maximum_error, abs(analytic[j][k] - numeric))
    assert maximum_error < 1e-8
    print("Matrix-gradient finite-difference maximum error:", maximum_error)

    # Interior checks of the three analytical decision polygons.
    for u1, u2, expected in [(1.2, -0.8, 0), (-0.95, 1.05, 1), (-1.05, -1.05, 2)]:
        scores = [u1, u2, 0.0]
        assert max(range(3), key=scores.__getitem__) == expected
    print("PASS: probabilities, shifts, temperature ordering, gradient, decision regions")


if __name__ == "__main__":
    check_examples()
