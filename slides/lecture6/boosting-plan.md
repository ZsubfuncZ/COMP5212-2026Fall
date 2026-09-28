# Residual learning and gradient boosting: slide plan

Audience: graduate ML, after logistic regression and AdaBoost's behavior and theory. Approximately 24 minutes; the formal decision-tree introduction follows this module. Preserve the approved Beamer theme, use simple fitted functions or one-split rules until that introduction, and retain the reproducible nonlinear example. All nine frames have delivery notes.

| Frame | Teaching move / evidence | Layout | Build |
|---|---|---|---|
| 1. Keep the model; learn a correction | AdaBoost's additive update extends to regression; residuals as desired corrections | Additive equation and fitting targets | Reveal correction targets |
| 2. One correction lowers squared error | Exact four-point example with a one-split rule, shrinkage one half | Editable plot and arithmetic | Reveal update |
| 3. Correct what the previous model missed | Three successive corrections on the same data; recompute residuals each time | Native three-panel plot and MSE table | Static |
| 4. Why squared loss leads to residuals | Differentiate squared loss; exact expansion and descent condition | Short derivation | Reveal derivative then loss change |
| 5. Gradient descent in prediction space | A vector of predictions has an unconstrained gradient; fit a function to extend the direction to new inputs | Prediction-space formula and pseudo-target regression | Reveal function fit |
| 6. The gradient boosting algorithm | Constant initialization, pseudo-residuals, fit, finite descent step, shrinkage | Compact numbered algorithm | Static |
| 7. Classification still uses the logistic loss | Bernoulli score gradient gives y-p, not a class-label residual | Equation bridge and numeric probability examples | Reveal pseudo-residuals |
| 8. Simple corrections build a flexible fit | Original computed 60-observation run, shallow partition functions, stages 1/10/60 | Native plot | Static |
| 9. Use validation to choose when to stop | Original computed training/validation MSE histories | Native loss plot | Static |

Native figures are computed teaching examples, clearly distinguished from the sourced applications that follow. Source: Friedman (2001), *Greedy Function Approximation: A Gradient Boosting Machine*, Sections 2-4 and Algorithms 1-2. Notes distinguish squared-loss residuals from general pseudo-residuals and explain that fitting an arbitrary weak learner need not provide descent. No change to the theme, AdaBoost, foundations, real-world cases, or main ordering.
