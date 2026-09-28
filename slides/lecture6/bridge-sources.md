# Regression bridge and optional GLM slide

The main lecture assumes only linear/logistic regression and gradients. The GLM slide is excluded by default.

- Taylor, Stanford STATS305B, Generalized linear models: https://web.stanford.edu/class/stats305b/notes/GLM_I.html . Conditional distribution, predictor, link; Gaussian identity, Bernoulli logit, Poisson log canonical examples. Same primary source as the preceding GLM lecture.
- Squared loss and Bernoulli negative log likelihood use the preceding regression lecture conventions. Gradient boosting keeps a differentiable loss and learns an additive score. Sources in boosting-sources.md.
- The introductory additive expression is a model class, not a guarantee that arbitrary weak predictors improve. The later AdaBoost theorem states the weighted-edge hypothesis; the bagging module explains variance and correlation assumptions.
