# AdaBoost validation

## Numerical checks

Run `python3 examples/adaboost_example.py` from the lecture directory, or invoke the script by absolute path from anywhere. Python's standard library is sufficient.

All checks pass for each of the three rounds:

- Exhaustive weak-learner search with exact rational observation weights.
- Observation weights sum exactly to one.
- The derivative of the scalar stage objective vanishes at the stated alpha.
- The normalized exponential update agrees with the exact rational update.
- The normalizer equals `2*sqrt(epsilon*(1-epsilon))`.
- New exponential loss equals old loss multiplied by the normalizer.
- Mean exponential loss equals the cumulative normalizer product.
- Training classification error is bounded by the exponential loss.
- The previous learner's mistakes receive exactly half the next weight distribution.
- The final three-round classifier matches all eight constructed labels.

| Round | Threshold | Orientation | Weighted error | Alpha | Training error | Mean exponential loss |
|---|---|---|---|---|---|---|
| 1 | 2.5 | positive above threshold | 1/4 | 0.5493061443 | 0.25 | 0.8660254038 |
| 2 | 6.5 | positive above threshold | 1/6 | 0.8047189562 | 0.25 | 0.6454972244 |
| 3 | 4.5 | positive below threshold | 1/5 | 0.6931471806 | 0.00 | 0.5163977795 |

## Mathematical scope

The derivation uses binary labels and weak predictions in {−1,+1}, no shrinkage, F0=0, and a strictly positive weak-learner edge at nonterminal iterations. Perfect-learner and no-edge cases are handled separately. The training-error theorem is not a test-error theorem. The exponential-loss population optimum is half the log odds, so its probability interpretation contains sigmoid(2F), not sigmoid(F). A finite fitted AdaBoost score is not automatically calibrated.

## Layout checks

The 12-frame module compiled in the inherited Beamer theme with 19 presentation pages. Every physical page and reveal was rendered at 1400 pixels and inspected. Final checks found no clipped equations, overlapping objects, missing reveals, title wrapping, or hidden content. The final proof compilation has no overfull boxes, underfull boxes, warnings, or TeX errors. Figures retain editable native PGFPlots source.
