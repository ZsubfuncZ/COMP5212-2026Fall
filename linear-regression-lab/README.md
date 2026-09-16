# Linear Regression Lab · COMP 5212

All pages are in English. Open index.html in a modern browser; no installation or network connection is required. The separate linear-regression-lab.html is the same app bundled into a single offline file.

Experiments: electricity and residuals; high-dimensional OLS sensitivity; multiple optimal solutions with rank deficiency; Ridge/Lasso norm paths; polynomial features; kernel ridge; kernel radius and implicit feature dimensions; gradient descent.

High-dimensional experiments have a 5–60 feature slider and Resample button. Reset restores the default sample. Conditioning uses n=2d; regularization uses n=2d+20, training-standardized features, and centered responses. Norms refer to d slopes. Every regularization chart compares both methods; l0 counts coefficients of magnitude greater than 1e-8. Lambda=0 and 61 positive log-spaced values are included.

The conditioning simulation perturbs the weakest singular direction, illustrating a controlled worst-direction sensitivity. Resampling changes X and y while preserving its prescribed spectrum and norm curve. The rank-deficient simulation shows a whole null-space family with identical predictions and loss.

Numerical conventions and explanations of model behavior are included in the app. highdim-numerics.md documents the model API and solver details.

The Kernel radius & dimensions page uses k(x,z)=exp(-(x-z)^2/(2*l^2)). Radius is the RBF length scale, not a hard cutoff. Change radius on a fixed sample, compare the similarity curve, and inspect input dimension 1, infinite RBF feature dimension, and finite n-by-n Gram matrix size. The fit uses n dual coefficients and an unpenalized intercept without constructing feature vectors.

Every experiment reports test MAE, MSE, RMSE, and R² on 300 reproducible observations from an independent random stream. Models in the same table share the test sample. Changing fitted coefficients, λ, kernel radius, or display controls keeps that sample fixed. Resample changes the data; Reset restores the original sample. Test samples are never used to fit models or preprocessing statistics. Repeated model selection using these scores turns the test sample into a tuning set.

Regularization predictions use training feature means/scales and restore the training response mean, so reported errors are in original response units. Conditioning test inputs follow the simulation's prescribed covariance and have noiseless targets. The rank-deficient test design preserves the duplicate columns. R² uses the test-target mean, may be negative, and is undefined for constant targets. Diverged gradient descent has unavailable scores. See performance-numerics.md for details.

Classroom challenges, discussion prompts, and teaching-note controls have been removed. The model controls, resampling, formulas, and visualizations remain available.
