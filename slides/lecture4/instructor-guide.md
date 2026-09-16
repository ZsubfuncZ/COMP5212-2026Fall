# Linear Regression: Instructor Guide

74 logical slides, 99 PDF pages, exactly five sections. Fourteen frames have two or three reveal stages. The PDF page count differs from the logical slide number shown in the footer. All explanations and numerical examples below correspond to the final source order.

## Teaching sequence

| Section | Logical slides | PDF pages | Focus |
|---|---:|---:|---|
| 1. Electricity motivation | 3-9 | 3-21 | Electricity use, a mean baseline, local approximation, and model choice. |
| 2. Formulation and closed-form derivation | 10-25 | 22-39 | Squared loss; scalar and matrix derivations; uniqueness; projection; outlier influence. |
| 3. Ill-conditioning and remedies | 26-44 | 40-60 | SVD, perturbations, coefficient variance, roundoff, QR, numerical rank, scaling, and remedies. |
| 4. Regularization: Ridge and Lasso | 45-59 | 61-78 | Ridge filters and bias-variance; Lasso geometry, subgradients, coordinate descent, paths, and validation. |
| 5. Feature expansion: polynomials and kernels | 60-74 | 79-99 | Polynomial representation, conditioning, kernel identities, centered kernel Ridge, and extrapolation. |

## Pacing

A complete treatment fits four 90-minute meetings. The opening can take about 15-18 minutes: accept one or two student responses at each prompt rather than extending every discussion. Detailed speaker notes offer additional explanations for a slower route.

1. **Foundations (slides 1-25):** electricity motivation, formulation, scalar and matrix least squares, and projection. Use the closed-form demonstration after the hand calculation.
2. **Conditioning (slides 26-44):** SVD, controlled perturbations, statistical sensitivity, numerical solvers, and the remedy table. Leave time for students to reproduce the two-sensor example.
3. **Regularization (slides 45-59):** Ridge and Lasso. Ask students to derive the scalar soft-threshold rule before running coordinate descent. Compare paths and validation errors in the lab.
4. **Feature expansion (slides 60-74):** polynomial features, valid kernels, centered kernel Ridge, bandwidth, and extrapolation. Revisit the original electricity operating range at the end.

A shorter two-meeting route can emphasize slides 1-25, 31-36, 38, 43-46, 51-58, 61-65, 67, and 70-74. Assign the full SVD, directional variance, and centered dual derivations as guided reading; do not rush through their equations.

## How to use the reveals

Present the PDF in normal full-screen mode and advance one page per click. There are no automatic timed transitions. A repeated logical slide number indicates another build of the same frame. Prompts precede evidence or answers in the electricity sequence, the scalar least-squares example, the response-perturbation example, the Lasso geometry/threshold/path examples, and three feature-expansion examples.

Use the 10-20-second pause cues in the notes. The new coefficient-path and geometry plots are analytical constructions, not measurements from a real facility. Do not switch directly to Beamer handout mode: some `\only` sequences replace content and require an explicit final-state handout layout.

## Conventions and teaching checks

- The data-fit loss is $\mathrm{SSE}/(2n)$ throughout. Ridge adds $\lambda\lVert w\rVert_2^2/2$; Lasso adds $\lambda\lVert w\rVert_1$.
- The intercept is unpenalized. Center training features and responses; fit all preprocessing within each training fold. Standardization uses average squared column norm equal to one when stated.
- An analytic inverse is shown only with its full-rank condition. Actual least-squares computations should use an appropriate QR or SVD solver.
- A stable algorithm does not remove mathematical sensitivity. Scaling, new information, truncation, and shrinkage address different causes.
- Lasso zeros describe a chosen feature representation. Correlated inputs can make selected features unstable, and duplicate columns can leave coefficients nonunique.
- Polynomial and kernel Ridge penalties depend on feature scaling. The weighted polynomial kernel map includes the required square-root factors.
- A centered kernel predictor must use the training centering convention for a new point. An unpenalized intercept is recovered separately.
- All lecture data and costs are constructed or simulated. The industrial energy application is real; the numerical curves are teaching examples.

## Web demonstrations

The online lab uses these eight anchors. The accompanying offline HTML can also be opened directly; PDF hyperlinks point to the online version.

| Demo | Link | Suggested use |
|---|---|---|
| Fit | [Open fit](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#fit) | After slides 4-5: compare a mean baseline with a line. |
| Closed form | [Open closed form](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#closed-form) | After slide 16: inspect the hand calculation and residuals. |
| Conditioning | [Open conditioning](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#conditioning) | Slides 31-39 and 44: perturb responses and compare coefficients with predictions. |
| Ridge and Lasso | [Open ridge and lasso](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#regularization) | Slides 46-59: vary the penalty and observe paths, sparsity, and validation error. |
| Polynomial features | [Open polynomial features](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#polynomial) | Slides 61-63: compare degree, fit, and validation. |
| Kernel Ridge | [Open kernel ridge](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#kernel) | Slides 64-72: compare similarity scale, penalty, and predictions. |
| Gradient descent | [Open gradient descent](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#gradient-descent) | Slides 41-43: vary the step size and feature scaling. |
| Outliers | [Open outliers](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#outliers) | Slide 25: vary input leverage and response displacement separately. |

## Logical-slide and PDF-page map

| Slide | PDF pages | Builds | Title |
|---:|---:|---:|---|
| 1 | 1 | 1 | Linear Regression |
| 2 | 2 | 1 | Five questions for linear regression |
| 3 | 3 | 1 | 1. Electricity motivation |
| 4 | 4-6 | 3 | Tomorrow's electricity use? |
| 5 | 7-9 | 3 | What does the input buy us? |
| 6 | 10-12 | 3 | But the world is nonlinear |
| 7 | 13-15 | 3 | Zoom in. What changes? |
| 8 | 16-18 | 3 | Why linear models appear everywhere |
| 9 | 19-21 | 3 | How much complexity do we need? |
| 10 | 22 | 1 | 2. Formulation and closed-form derivation |
| 11 | 23 | 1 | Linear in the parameters |
| 12 | 24 | 1 | What counts as a good fit? |
| 13 | 25 | 1 | First solve for the intercept |
| 14 | 26 | 1 | Centering reveals the slope formula |
| 15 | 27 | 1 | What if every input is the same? |
| 16 | 28-30 | 3 | Least squares by hand |
| 17 | 31 | 1 | Build the design matrix first |
| 18 | 32 | 1 | Expand the quadratic before differentiating |
| 19 | 33 | 1 | Derive the gradient using a differential |
| 20 | 34 | 1 | Normal equations give a global minimum |
| 21 | 35 | 1 | When is the analytic solution unique? |
| 22 | 36 | 1 | Least squares as a projection |
| 23 | 37 | 1 | Derive the projection matrix |
| 24 | 38 | 1 | A Pythagorean proof of the best fit |
| 25 | 39 | 1 | How one outlier can move the line |
| 26 | 40 | 1 | 3. Ill-conditioning and remedies |
| 27 | 41 | 1 | Unique predictions, unique parameters? |
| 28 | 42 | 1 | The compact singular value decomposition |
| 29 | 43 | 1 | Least squares in singular coordinates |
| 30 | 44 | 1 | Rank deficiency and minimum norm |
| 31 | 45 | 1 | Collinearity destabilizes coefficients |
| 32 | 46 | 1 | Full rank does not imply stability |
| 33 | 47 | 1 | A controlled near-collinear design |
| 34 | 48-50 | 3 | A tiny response change |
| 35 | 51 | 1 | Which predictions remain stable? |
| 36 | 52 | 1 | Sampling variance in weak directions |
| 37 | 53 | 1 | Roundoff in the Gram matrix |
| 38 | 54 | 1 | Least squares via QR |
| 39 | 55 | 1 | Numerical rank is a tolerance decision |
| 40 | 56 | 1 | Case discussion: two similar sensors |
| 41 | 57 | 1 | Why gradient descent converges |
| 42 | 58 | 1 | Ill-conditioning slows gradient descent |
| 43 | 59 | 1 | Feature scale changes optimization |
| 44 | 60 | 1 | Choose the right remedy |
| 45 | 61 | 1 | 4. Regularization: Ridge and Lasso |
| 46 | 62 | 1 | Ridge trades bias for stability |
| 47 | 63 | 1 | Ridge filters singular directions |
| 48 | 64 | 1 | Directional bias and variance under ridge |
| 49 | 65 | 1 | Ridge stabilizes the controlled example |
| 50 | 66 | 1 | Balance bias and variance |
| 51 | 67 | 1 | Can regularization remove a feature? |
| 52 | 68-69 | 2 | Why do corners encourage zeros? |
| 53 | 70 | 1 | Optimality at a zero coefficient |
| 54 | 71-72 | 2 | Soft-thresholding creates exact zeros |
| 55 | 73 | 1 | Deriving a coordinate-descent update |
| 56 | 74-75 | 2 | Ridge and Lasso trace different paths |
| 57 | 76 | 1 | Correlated features complicate selection |
| 58 | 77 | 1 | Choose a penalty for the modeling task |
| 59 | 78 | 1 | Training error cannot select the model |
| 60 | 79 | 1 | 5. Feature expansion: polynomials and kernels |
| 61 | 80 | 1 | Can a linear model bend? |
| 62 | 81-83 | 3 | How much curvature is useful? |
| 63 | 84 | 1 | Expansion can bring back ill-conditioning |
| 64 | 85-87 | 3 | A dot product can hide six features |
| 65 | 88 | 1 | Compare points without listing features |
| 66 | 89 | 1 | Why the solution lies in the training span |
| 67 | 90 | 1 | Kernel ridge: solve in sample space |
| 68 | 91 | 1 | Center a new point in the same space |
| 69 | 92 | 1 | Which similarities are valid kernels? |
| 70 | 93-95 | 3 | How local is an RBF similarity? |
| 71 | 96 | 1 | Bandwidth and penalty do different jobs |
| 72 | 97 | 1 | Beyond the observed range? |
| 73 | 98 | 1 | Return to tomorrow's electricity forecast |
| 74 | 99 | 1 | Further reading and editable examples |

## Complete speaker notes

### Slide 1: Linear Regression

PDF pages 1; 1 build(s).

This English lecture develops linear regression in exactly five sections: electricity motivation; formulation and the closed-form least-squares derivation; ill-conditioning and remedies; Ridge and Lasso regularization; and polynomial features and kernels. The opening electricity example uses sparse visual prompts and staged reveals. Several worked examples also keep answers hidden until a later build. Advance one PDF page at a time in ordinary full-screen presentation mode; the logical slide number stays unchanged during each reveal. The instructor guide maps every logical slide to its PDF pages and includes the complete speaker notes. All numerical data are constructed for teaching, while the industrial energy application is supported by Department of Energy guidance.


### Slide 2: Five questions for linear regression

PDF pages 2; 1 build(s).

Suggested time: 1 minute. Present the five questions as the structure of one modeling investigation. The initial industrial electricity example supplies the target and an operating range. The second section turns a visual fit into an optimization problem and derives the scalar and matrix solutions. The third separates uniqueness, sensitivity, and numerical computation. The fourth deliberately changes the objective using Ridge and Lasso. The final section changes the representation using polynomial features and kernels. Ask students to keep identifying which part of the modeling pipeline changes at each step. The course is entirely about continuous-response regression.


### Slide 3: 1. Electricity motivation

PDF pages 3; 1 build(s).

Suggested time: 30 seconds. Pause before the next section and pose its central question: What makes a simple linear model worth trying? Invite one prediction, then use the examples and derivations to test it.


### Slide 4: Tomorrow's electricity use?

PDF pages 4-6; 3 build(s).

Suggested time: 3 minutes. Build 1: show only the factory and tomorrow's production plan. Ask which measurements students would want before making a forecast; wait 15 seconds and accept two suggestions. Do not name a regression method yet. Build 2: reveal historical production, weather, shifts, and electricity use. Explain that this is a real application category: the U.S. Department of Energy describes regression-based energy prediction using production, weather, occupancy, and operating hours. The factory and every numerical value in this lecture are constructed teaching examples, not measurements from a named facility. Build 3: distinguish an input available at prediction time from the future response. Electricity forecasts can inform budgeting and flag unusual consumption; unusual consumption alone does not prove waste or causality. On the next slide, hold weather and shifts conceptually comparable and use production as the single predictor. Source: [https://www1.eere.energy.gov/manufacturing/eguide/iso_step_2_4.html](https://www1.eere.energy.gov/manufacturing/eguide/iso_step_2_4.html).


### Slide 5: What does the input buy us?

PDF pages 7-9; 3 build(s).

Suggested time: 4 minutes. Build 1: let students look at the points for 15 seconds and make a numerical forecast at 5.5 tonnes. Ask for an explanation before revealing any model. Build 2: reveal the sample mean, 201.2 kWh/day. Wait 10 seconds and ask where the horizontal line systematically misses. Build 3: reveal the fitted line and its prediction of approximately 219 kWh/day. The exact coefficients are b=23.4727272727 and w=35.5454545455. The observations are generated at x=4,4.2,...,6 from m(x)=100+5x+3x squared, plus a fixed sequence of small deviations. The straight line uses a pattern over a narrow range even though the constructed underlying mean is curved. Do not yet reveal the generating formula; the next slides examine that issue. No validation result is claimed: the small dataset is only a visual example, and usefulness must be assessed on unseen days. For daily forecasting, reserve later days as a chronological holdout; fit the mean, preprocessing, and regression on the training period only. The mean-baseline web demonstration is available at [https://regression-lab-graduate-2026.whu38f.chatgpt.site/#fit](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#fit).


### Slide 6: But the world is nonlinear

PDF pages 10-12; 3 build(s).

Suggested time: 3 minutes. Build 1: reveal the constructed mean over a much wider production range, but do not show a line. Ask whether this shape alone rules out trying linear regression and wait 15 seconds. Build 2: reveal the green operating window from 4 to 6 tonnes per day. Ask students to revisit their answer using where predictions will actually be made. Build 3: reveal the tangent at x=5. The full mean is m(x)=100+5x+3x squared; the tangent is L(x)=25+35x. This tangent is an analytic first-order approximation, not the sample OLS fit shown earlier. Their coefficients need not agree because OLS is estimated from noisy observations over a finite range. The curve is deliberately simple enough to inspect exactly. The lesson concerns the input distribution and prediction domain: a local approximation that works near typical operation may fail after a regime change or when extrapolated. No claim is made that a real factory follows this quadratic law.


### Slide 7: Zoom in. What changes?

PDF pages 13-15; 3 build(s).

Suggested time: 4 minutes. Build 1: show only the wide-range panel. Ask what students expect if we zoom around x=5, and pause for 10 seconds. Build 2: reveal the middle panel, whose range matches the previous observations. Pause again before asking how large the approximation error now is relative to the several-kWh deviations in the scatterplot. Build 3: reveal the narrow panel. All panels use the same m(x)=100+5x+3x squared and tangent L(x)=25+35x. The exact difference is m(x)-L(x)=3(x-5) squared, so the maximum gaps are 75, 3, and 0.12 kWh on radii 5, 1, and 0.2. Both horizontal and vertical axes are rescaled, and the numerical gaps prevent a misleading purely visual claim. Smaller neighborhoods improve this smooth approximation but may contain fewer samples for estimation. Noise size here is illustrative; do not imply that these finite data determine the population noise variance. The derivative predicts first-order change, not exact equality on a finite interval.


### Slide 8: Why linear models appear everywhere

PDF pages 16-18; 3 build(s).

Suggested time: 4 minutes. Build 1: ask students to recall the meaning of a derivative before showing a Taylor formula. Wait 15 seconds. Build 2: reveal the scalar first-order approximation and name its two ingredients: level and sensitivity. Build 3: generalize to several inputs, then set h=x-x0 and collect the intercept. The target m is the conditional mean relevant to squared-error prediction, which need not have the same smoothness as a physical mechanism. Differentiability at x0 means m(x0+h)=m(x0)+gradient m(x0) transpose h+r(h), with r(h)/norm(h) tending to zero. It does not mean exact equality in a neighborhood. With a bounded Hessian near x0, the remainder is bounded by a constant times norm(h) squared. Even then, a wide-range OLS fit is not generally the tangent. Local smoothness motivates trying the model, while validation determines whether the approximation is adequate at the scale of the actual prediction problem. Reference: MIT's first-order approximation notes, [https://math.mit.edu/~djk/18_022/chapter04/section01.html](https://math.mit.edu/~djk/18_022/chapter04/section01.html).


### Slide 9: How much complexity do we need?

PDF pages 19-21; 3 build(s).

Suggested time: 3 minutes. Build 1: invite a vote and pause for 15 seconds. Interpret unknown scale broadly: we may not yet know the sample size needed, the relevant input range, the curvature, or how accurate the application requires predictions to be. Build 2: suggest a simple linear baseline because it is comparatively easy to fit, inspect, and compare. This is a modeling heuristic, not a theorem that linear regression is universally optimal or literally always appropriate. Strong prior knowledge, structural constraints, or the target type may point elsewhere immediately. Build 3: reveal the next decision only after asking what evidence would justify more complexity. Evaluate on a validation split matching intended use, inspect residual patterns, and consider interactions, transformed features, regularization, or a different model. A repeated pattern is a diagnostic lead, not proof of a particular mechanism. Reserve a final test set for the end of model selection. Linear models remain useful benchmarks even when a more flexible model eventually wins.


### Slide 10: 2. Formulation and closed-form derivation

PDF pages 22; 1 build(s).

Suggested time: 30 seconds. Pause before the next section and pose its central question: How do residuals determine the best-fitting parameters? Invite one prediction, then use the examples and derivations to test it.


### Slide 11: Linear in the parameters

PDF pages 23; 1 build(s).

Suggested time: 3 minutes. Emphasize that the model class depends on the representation. Polynomial regression is nonlinear in the original inputs but linear in its parameters, so the same least-squares methods apply. The meaning of the intercept depends on where the features are zero; centering therefore changes its interpretation. From here onward, $X$ denotes a design matrix with a constant column, and its $p$ columns already include the intercept. Unless explicitly stated otherwise, regularization applies only to $w$ and does not penalize $b$. Ask: what interaction between the original inputs is introduced by adding $x_1x_2$?

**Further reading.**

-  Tengyu Ma and Andrew Ng, CS229 Lecture Notes, Chapters 1-3 and 8-9. [https://cs229.stanford.edu/main_notes.pdf](https://cs229.stanford.edu/main_notes.pdf)


### Slide 12: What counts as a good fit?

PDF pages 24; 1 build(s).

Suggested time: 4 minutes. This plot shows loss as a function of the residual. Keep it distinct from an objective function in parameter space or a prediction curve in data space. Ask students to calculate what happens when a residual grows from 1 to 3: squared loss grows ninefold, whereas absolute loss grows threefold. Squared loss is smooth and convex, which makes computation convenient; its statistical motivation follows on the next slide. Point out the sign convention in advance: residuals are $y$ minus prediction, while gradients often contain prediction minus $y$.


### Slide 13: First solve for the intercept

PDF pages 25; 1 build(s).

Suggested time: 5 minutes. Before differentiating, imagine moving a fitted line upward without changing its slope. All predictions increase together. If the mean residual is positive, an upward move should initially lower the loss; this anticipates the sign of the derivative. Write the residual as $e_i=y_i-b-wx_i$, apply the chain rule, and track the minus sign from differentiating with respect to $b$. The factor of two cancels the one-half in the objective. Setting the derivative to zero gives the residual-sum condition, and dividing by the positive sample size introduces the sample means. Stress that this result is valid for every fixed slope, before we have solved for the best slope. Substituting $x=\bar x$ into the resulting line gives prediction $\bar y$. Ask what happens if we forbid the intercept: the residuals need not sum to zero and the fitted line need not pass through the sample centroid. Further reading: CS229 Lecture Notes, [https://cs229.stanford.edu/main_notes.pdf](https://cs229.stanford.edu/main_notes.pdf).


### Slide 14: Centering reveals the slope formula

PDF pages 26; 1 build(s).

Suggested time: 6 minutes. Substitute the intercept expression into every residual and simplify before differentiating again. The residual becomes the centered response minus the slope times the centered input. Students can now treat this as a one-parameter quadratic. Differentiate the profiled objective with respect to $w$, collect the terms multiplying $w$, and only then divide by the sum of centered squared inputs. Ask why that last division needs an assumption. If all inputs are identical, there is no observed change in input from which a slope could be learned. With positive input variation, the profiled curvature is $\sum_i(x_i^c)^2/n>0$, so the stationary slope is its unique global minimum. The slope can also be written as sample covariance divided by sample variance when the same normalization is used in both quantities. Neither formula implies a causal effect. Preview the next numerical example: students will calculate a centered cross-product of one and a centered sum of squares of two. Further reading: CS229 Lecture Notes, [https://cs229.stanford.edu/main_notes.pdf](https://cs229.stanford.edu/main_notes.pdf).


### Slide 15: What if every input is the same?

PDF pages 27; 1 build(s).

Suggested time: 5 minutes. Present repeated measurements at one operating load. More repetitions can estimate the mean response at that load, but they do not reveal how the response changes with load. Since $x_i=c$, the predictions depend only on the combination $b+cw$. Minimizing squared loss chooses that combination to equal the sample mean, leaving infinitely many possible parameter pairs. Do not report the slope as zero merely because the usual slope formula has zero numerator and denominator; zero is one optional selection, not an identified conclusion. At a new input $x_*\ne c$, the prediction depends on the unconstrained slope. Connect this to the geometry of centering: the centered input has zero inner product with the all-ones vector because its entries sum to zero. For nonconstant inputs this separates intercept and slope directions; here the entire slope direction vanishes. Ask whether collecting many more observations at exactly the same load resolves the slope problem. It does not. Further reading: Hastie, Tibshirani and Friedman, Chapter 3, [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/).


### Slide 16: Least squares by hand

PDF pages 28-30; 3 build(s).

Suggested time: 5 minutes. Build 1: give students 30 seconds to calculate from the inputs only. Build 2: reveal the means and fitted coefficients; pause 15 seconds before asking for residuals. Build 3: reveal predictions, residuals, and the three loss conventions.  First ask students to find $\bar{x}=1$ and $\bar{y}=\frac{5}{3}$, then calculate a numerator of 1 and a denominator of 2. The residuals are $-\frac{1}{6}$, $\frac{1}{3}$, and $-\frac{1}{6}$, so their squared sum is $\frac{1}{36}+\frac{1}{9}+\frac{1}{36}=\frac{1}{6}$. Training MSE is $\frac{1}{18}$. This course uses $J=\frac{\mathrm{MSE}}{2}$, hence $J=\frac{1}{36}$. Warn against interchanging SSE, MSE, and an objective with the $\frac{1}{2}$ factor. Verify that the residual is orthogonal to both the constant column and the input column, preparing for the matrix and geometric interpretations. All values are constructed for teaching.


### Slide 17: Build the design matrix first

PDF pages 31; 1 build(s).

Suggested time: 5 minutes. Build this matrix from a concrete example with load, temperature, and their interaction. Ask students how many columns it has after adding an intercept, and whether adding a polynomial term changes the sample count. A row describes one observation in feature space; a column records one feature across all observations. Explain that $w$ is a vector of $d$ slope coefficients, so stacking it below the scalar intercept gives $p=d+1$ parameters. Matrix multiplication computes all predictions at once, and its dimensions reveal immediately that the result lies in sample space, not parameter space. Ask students to reconstruct one scalar prediction from a row. No rank or distributional assumptions are needed to define the objective. The matrix may be rectangular or have redundant columns. An important notation check is that the raw input dimension need not equal $d$: feature maps can add interactions or basis functions. Later, full column rank will be a condition on this completed design matrix. Further reading: CS229 Lecture Notes, [https://cs229.stanford.edu/main_notes.pdf](https://cs229.stanford.edu/main_notes.pdf).


### Slide 18: Expand the quadratic before differentiating

PDF pages 32; 1 build(s).

Suggested time: 5 minutes. Ask students to expand the product without memorized matrix-calculus rules. The order of multiplication matters: transposing $X\theta$ gives $\theta^{\mathsf T}X^{\mathsf T}$, not $X^{\mathsf T}\theta^{\mathsf T}$. Check the dimensions of all four expanded terms and verify that each is a scalar. To combine the cross terms, transpose one scalar and use the reversal rule for a product. This is an opportunity to distinguish matrix equality from a visually similar but dimensionally invalid expression. Set $A=X^{\mathsf T}X$ and $c=X^{\mathsf T}y$ if the notation feels heavy: the objective becomes $(\theta^{\mathsf T}A\theta-2\theta^{\mathsf T}c+y^{\mathsf T}y)/(2n)$. Ask which term disappears upon differentiation and which contributes curvature. Neither Gaussian noise nor invertibility has appeared in the calculation. Even a rank-deficient design gives the same expanded quadratic, so we should postpone division or inversion until after checking its conditions. Further reading: CS229 Lecture Notes, [https://cs229.stanford.edu/main_notes.pdf](https://cs229.stanford.edu/main_notes.pdf).


### Slide 19: Derive the gradient using a differential

PDF pages 33; 1 build(s).

Suggested time: 6 minutes. Explain a differential as the first-order change caused by an arbitrary small parameter perturbation. Define $r$ as prediction minus response to align its sign with the eventual gradient; remind students that the earlier residual $e$ has the opposite sign. Apply the product rule to $r^{\mathsf T}r$, then use the fact that the two resulting scalar terms are equal. Substituting $dr=X\,d\theta$ places all dependence on the perturbation at the right. The gradient is a column vector, so its transpose is the coefficient multiplying that perturbation. Ask students to check its dimension: $X^{\mathsf T}$ maps an $n$-vector back to a $p$-vector. Then recover the componentwise formula and show that the constant column produces the intercept derivative derived earlier. As a sign check, when every prediction is too low, the intercept gradient is negative, so a gradient-descent step raises the intercept. This derivation requires only ordinary differentiability of a finite quadratic. Further reading: CS229 Lecture Notes, [https://cs229.stanford.edu/main_notes.pdf](https://cs229.stanford.edu/main_notes.pdf).


### Slide 20: Normal equations give a global minimum

PDF pages 34; 1 build(s).

Suggested time: 6 minutes. Begin by asking whether a stationary point is always a minimum. In a general objective it is not, so we need an additional argument. Differentiate the gradient once more to obtain the constant Hessian. For an arbitrary vector $v$, rewrite its quadratic form as a squared norm divided by the positive sample size. This proves positive semidefiniteness and hence convexity. The last displayed identity offers an even more concrete certificate: expand the objective at $\widehat\theta+v$, and the linear cross term vanishes because the normal equations hold. The remaining increase is nonnegative for every displacement. Explain that ordinary least squares always attains its infimum in finite dimensions: its attainable fitted vectors form a closed subspace with a closest point to $y$. If $Xv=0$, moving along $v$ changes neither fitted values nor loss; that possibility explains why semidefinite curvature need not identify unique parameters. Further reading: Hastie, Tibshirani and Friedman, Chapter 3, [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/).


### Slide 21: When is the analytic solution unique?

PDF pages 35; 1 build(s).

Suggested time: 5 minutes. Prove each implication rather than treating the inverse as a starting point. Full column rank means the null space contains only zero, so the Hessian quadratic form is strictly positive for any nonzero direction. A symmetric positive-definite matrix is invertible, which now permits the analytic formula. Ask students whether one hundred samples and ten parameters guarantee uniqueness: duplicated or linearly dependent columns can still violate the condition. Then distinguish exact singularity from near dependence. Positive definiteness gives uniqueness in exact arithmetic, but a tiny positive eigenvalue may still amplify small measurement changes or floating-point error. This prepares the motivation for the expanded ill-conditioning section. Avoid teaching students to compute an explicit inverse simply because it appears in the derivation. QR and SVD work directly with the original design and are usually safer numerical routes. A normal-equation linear solve also differs from explicitly forming an inverse, although it still inherits the conditioning of the Gram matrix. Further reading: scikit-learn Linear Models, [https://scikit-learn.org/stable/modules/linear_model.html](https://scikit-learn.org/stable/modules/linear_model.html).


### Slide 22: Least squares as a projection

PDF pages 36; 1 build(s).

Suggested time: 4 minutes. Each coordinate in this figure is a sample dimension; this is not an input-$x$ versus output-$y$ scatterplot. Here $n=2$ and $p=1$, so model predictions lie on the line $\mathrm{span}([1,1]^{\top})$. The closest point in this prediction subspace to $y$ is $\hat{y}=(1,1)$. The residual $(1,-1)$ has zero inner product with $(1,1)$. When $X$ has full column rank, $P_X=X(X^{\top}X)^{-1}X^{\top}$. For a rank-deficient $X$, use the pseudoinverse: the projected fitted values $\hat{y}$ remain unique even when the parameters do not.

**Further reading.**

-  Hastie, Tibshirani and Friedman, The Elements of Statistical Learning, 2nd ed., Chapters 2-4 and 7. Author-hosted book: [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/)


### Slide 23: Derive the projection matrix

PDF pages 37; 1 build(s).

Suggested time: 6 minutes. Start from the unique coefficient formula and multiply by $X$ to move from parameter space into sample space. The resulting matrix $P$ is $n$ by $n$, not $p$ by $p$. Ask what it should do to a response vector already perfectly representable by the model. Verify this expectation using $PX=X$. For symmetry, use the symmetry of $X^{\mathsf T}X$ and of its inverse. For idempotence, keep parentheses visible and cancel the central Gram matrix with its inverse. Explain the meanings before presenting the terminology: symmetry makes the projection orthogonal, while idempotence means a second projection has no further effect. The last identity states that the removed component is orthogonal to every feature column. Only this inverse-based expression requires full column rank; with redundant columns, the same orthogonal projection exists and can be written $XX^+$ using the Moore-Penrose pseudoinverse. Fitted values are therefore less ambiguous than a particular choice of coefficients. Further reading: Hastie, Tibshirani and Friedman, Chapter 3, [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/).


### Slide 24: A Pythagorean proof of the best fit

PDF pages 38; 1 build(s).

Suggested time: 6 minutes. Point back to the two-dimensional projection picture and name the two legs of the right triangle. For any alternative fitted vector $z$ in the model subspace, both $\widehat y$ and $z$ belong to that subspace, so their difference does too. The least-squares residual is orthogonal to the entire subspace and therefore to that difference. Expanding the squared norm removes the cross term and proves that no competing fitted vector has lower error. This proof also shows uniqueness of fitted values even when parameters are not unique. If the model includes an intercept, the all-ones vector is one of its columns, so residual orthogonality gives zero residual sum and equality of the observed and fitted sample means. Ask whether this says the conditional mean of the true error is zero: it does not. Sample orthogonality is enforced by optimization, whereas exogeneity and independence are assumptions about the data-generating process. Without an intercept, the zero-sum conclusion need not hold. Further reading: Hastie, Tibshirani and Friedman, Chapter 3, [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/).


### Slide 25: How one outlier can move the line

PDF pages 39; 1 build(s).

Suggested time: 4 minutes. First place the outlier near the center of the $x$ values and vary only $y$. Then move it toward the edge of the $x$ range and compare the fits. Distinguish a residual outlier from a high-leverage point: one is far from its prediction; the other has an extreme input location. Their combination usually has greater influence. Huber loss is quadratic for small residuals and approximately absolute loss for large residuals, so it reduces the effect of vertical outliers. It does not automatically protect against arbitrary high-leverage points. Do not delete outliers mechanically: investigate measurement error, different populations, or genuine rare events first. The plotted data are constructed for teaching.

**Further reading.**

-  scikit-learn official user guide, Linear Models. [https://scikit-learn.org/stable/modules/linear_model.html](https://scikit-learn.org/stable/modules/linear_model.html)

**Web demonstration.** [https://regression-lab-graduate-2026.whu38f.chatgpt.site/#outliers](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#outliers)


### Slide 26: 3. Ill-conditioning and remedies

PDF pages 40; 1 build(s).

Suggested time: 30 seconds. Pause before the next section and pose its central question: Why can a unique solution still be unreliable? Invite one prediction, then use the examples and derivations to test it.


### Slide 27: Unique predictions, unique parameters?

PDF pages 41; 1 build(s).

Suggested time: 3 minutes. Use two identical columns, $x_1=x_2$. The model can identify $w_1+w_2$ but cannot identify the two coefficients separately. All parameter vectors with the same coefficient sum give the same predictions on the observed design. If those two features are no longer equal in future data, the solutions may behave differently. Distinguish three claims: unique training fitted values, unique parameters, and robust predictions on future inputs. Minimum norm is an additional selection rule, not a scientific conclusion forced by the data.

**Further reading.**

-  Hastie, Tibshirani and Friedman, The Elements of Statistical Learning, 2nd ed., Chapters 2-4 and 7. Author-hosted book: [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/)

**Web demonstration.** [https://regression-lab-graduate-2026.whu38f.chatgpt.site/#conditioning](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#conditioning)


### Slide 28: The compact singular value decomposition

PDF pages 42; 1 build(s).

Suggested time: 5 minutes. Begin by checking the dimensions of all three factors rather than presenting the SVD as a black box. Multiplying a parameter vector by $V_r^{\mathsf T}$ expresses its identifiable part in orthonormal parameter coordinates. Multiplication by $\Sigma_r$ stretches each coordinate, and multiplication by $U_r$ maps it into the sample prediction space. Ask students to verify $Xv_j=s_j u_j$ directly using orthonormality. These are directions of combinations of features, not necessarily individual original columns. A small singular value therefore indicates weak information about a particular coefficient combination. Compact means that only the $r$ strictly positive singular values are retained in this exact algebraic statement. Numerical decisions about which values count as positive come later. If the design includes an intercept, that column participates in this decomposition until we explicitly separate and center it for ridge regression.


### Slide 29: Least squares in singular coordinates

PDF pages 43; 1 build(s).

Suggested time: 6 minutes. Decompose the response into its projection $U_rU_r^{\mathsf T}y$ and the perpendicular component $(I-U_rU_r^{\mathsf T})y$. The two components are orthogonal, so the squared norm splits by the Pythagorean theorem. Next express the parameter vector as a component in the span of $V_r$ plus a null-space component. The latter disappears after multiplication by $X$. The first term in the displayed objective now consists of $r$ independent scalar quadratics. Differentiate one of them and divide by the strictly positive singular value to obtain its minimizer. The remaining response component cannot be represented by any parameter choice. Multiplying the entire objective by the course convention $1/(2n)$ changes none of these minimizers. Ask which part of the derivation would fail if one tried to divide by a zero singular value. That question motivates both the pseudoinverse and the next frame.


### Slide 30: Rank deficiency and minimum norm

PDF pages 44; 1 build(s).

Suggested time: 5 minutes. The scalar derivation fixed every identifiable coordinate, but said nothing about the null-space component. Adding any such component leaves the predictions unchanged, so it describes the complete family of minimizers. The row space of $X$ and its null space are orthogonal. This gives the norm identity and shows why the pseudoinverse selects a unique vector even when ordinary least squares does not identify unique parameters. Work through the one-row example: the data determine only the sum of the two coefficients. Squaring and minimizing $a^2+(1-a)^2$ gives $a=1/2$. Ask whether equal coefficients prove equal causal effects; the answer is no. Also ask about a future input $(1,-1)$, whose prediction depends on the chosen null-space component. Unique fitted values refer to the observed design, not necessarily to arbitrary future feature patterns.


### Slide 31: Collinearity destabilizes coefficients

PDF pages 45; 1 build(s).

Suggested time: 5 minutes. The figure shows five perturbed fits constructed for teaching. The coefficient sum stays near 2, while the individual coefficients vary substantially. Ask whether a weight changing from positive to negative necessarily means that the predictions have changed dramatically. In the web demonstration, gradually increase the correlation, inspect the condition number and parameters, and then compare predictions. Standardization improves conditioning caused by units, but it cannot change the fact that two features are nearly identical. Regularization suppresses unstable directions at the cost of introducing bias. This figure is a constructed sensitivity example, not an empirical finding. Exact construction: $x_1$ consists of 30 equally spaced values on $[-1,1]$, and $x_2=x_1+0.01\cos(2.1i)$. In fit $k$, the labels are $y=x_1+x_2+a_k\cos(2.1i)$, where $a_k$ is respectively $-0.023$, $0.035$, $-0.052$, $0.018$, and $-0.034$. Each OLS fit includes an intercept and has a coefficient sum of 2.

**Further reading.**

-  scikit-learn official user guide, Linear Models. [https://scikit-learn.org/stable/modules/linear_model.html](https://scikit-learn.org/stable/modules/linear_model.html)

**Web demonstration.** [https://regression-lab-graduate-2026.whu38f.chatgpt.site/#conditioning](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#conditioning)


### Slide 32: Full rank does not imply stability

PDF pages 46; 1 build(s).

Suggested time: 5 minutes. Compare an exactly singular matrix with a full-rank matrix whose smallest singular value is extremely small. The second has a unique solution, yet the division by its smallest singular value can magnify a small response perturbation. The displayed bound is absolute and assumes the design is held fixed. A relative bound also depends on the response geometry. When the fitted vector is nonzero, one may bound the relative parameter change by $\kappa_2(X)\|\Delta y\|_2/\|\widehat y\|_2$, which introduces the angle between $y$ and its projection if normalized by $\|y\|_2$. Perturbing $X$ is a different problem, and general least-squares bounds contain additional residual-angle effects. Consequently, neither a small residual nor one arbitrary condition-number threshold fully diagnoses reliability. Reference: LAPACK Users' Guide, error bounds for linear least squares, [https://www.netlib.org/lapack/lug/node83.html](https://www.netlib.org/lapack/lug/node83.html).


### Slide 33: A controlled near-collinear design

PDF pages 47; 1 build(s).

Suggested time: 6 minutes. This constructed design separates the two information directions exactly, so it allows us to derive sensitivity without numerical approximations or an arbitrary random example. The first observation measures the sum of the coefficients. The second measures their difference multiplied by $\epsilon$. Verify that the two right singular vectors have unit length and zero inner product. Then multiply the displayed matrix by each vector to obtain the two singular values. For $\epsilon=10^{-4}$ the matrix has condition number $10^4$, even though its determinant is nonzero. At $\epsilon=0$ the second observation no longer contains coefficient information and rank falls to one. No intercept is included: adding one to this two-row example would change the rank structure. The same construction works with any two orthonormal vectors in a larger sample space, so the mechanism is not specific to a square system.


### Slide 34: A tiny response change

PDF pages 48-50; 3 build(s).

Suggested time: 6 minutes. Build 1: show the response perturbation and two scalar equations; pause 20 seconds for a predicted effect on the coefficients. Build 2: reveal the symbolic solution and ask students to substitute epsilon=0.0001 and delta=0.001. Build 3: reveal the large numerical change.  Ask students to solve the two scalar observation equations before showing the parameter vector. The first equation fixes the sum at one, whereas the perturbed second equation requires the difference to become $\delta/\epsilon$. Adding and subtracting the equations yields the two coefficients. This is a sensitivity calculation with the exact same design matrix before and after the response perturbation. No optimization error, finite-precision effect, or stochastic estimation argument is needed. The unperturbed parameter norm is $1/\sqrt2$, so the numerical example has a tenfold relative coefficient change from a response change of only one part in a thousand. The condition number is $10^4$, and this particular choice of response and perturbation realizes that relative amplification. Ask what would happen if the perturbation instead pointed along $q_1$: it would change the coefficient sum without division by $\epsilon$.


### Slide 35: Which predictions remain stable?

PDF pages 51; 1 build(s).

Suggested time: 5 minutes. The matrix $XX^+$ is an orthogonal projector, whose Euclidean operator norm is at most one. This explains why the fitted training vector can be insensitive in absolute norm even when the coefficients are highly sensitive. The statement holds for fixed $X$ and response perturbations; it is not a universal guarantee about future data or perturbations of the design. To analyze a future input, insert the singular expansion of the coefficient change and inspect its alignment with the weak right singular directions. In our example, the two future vectors respectively isolate the stable sum and the unstable difference. The second vector departs from the near-equality pattern seen at substantial scale in the training data. It is not outside the algebraic span of this full-rank toy design; the issue is that the difference direction was observed only at tiny magnitude. Discuss how this resembles correlated sensors separating after deployment.


### Slide 36: Sampling variance in weak directions

PDF pages 52; 1 build(s).

Suggested time: 5 minutes. Begin with the correctly specified conditional linear model and substitute it into the pseudoinverse expression. Full column rank makes $X^+X=I$, leaving a linear transformation of the noise. The orthonormal left singular vectors imply that the projected noise components have variance $\sigma^2$ and are uncorrelated under the stated covariance assumption. They need not be independent unless additional distributional assumptions, such as Gaussian noise, are imposed. Dividing each component by its singular value yields the directional variance formula. This is a repeated-sampling statement conditional on the design, distinct from the previous deterministic perturbation calculation, though both share the same amplification mechanism. The two-row toy model has no residual degrees of freedom for estimating $\sigma^2$ internally; the covariance derivation assumes a specified noise variance or a larger suitable sample. It does not justify reporting classical standard errors from an exactly interpolating two-observation fit.


### Slide 37: Roundoff in the Gram matrix

PDF pages 53; 1 build(s).

Suggested time: 7 minutes. Separate two facts. In exact arithmetic, the eigenvalues of the Gram matrix are the squared singular values, so its spectral condition number is squared. In floating-point arithmetic, forming that matrix may additionally destroy the small differences needed to recover weak directions. This example uses an explicit, reproducible binary64 operation sequence: form epsilon squared, compute one plus and one minus that value, then subtract the two rounded results. The small eigenvalue becomes $2^{-53}$ rather than approximately $2\times10^{-16}$. For the response $q_2$, the right-hand side is $(\epsilon,-\epsilon)$, and solving the represented Gram system along its difference direction gives the coefficient shown. The large error already exists in the rounded problem, without blaming a particular triangular solver. Other operation orders, precisions, factorizations, and responses can behave differently. In particular, general least-squares forward-error bounds also depend on residual geometry when the design is perturbed.


### Slide 38: Least squares via QR

PDF pages 54; 1 build(s).

Suggested time: 6 minutes. Reuse the projection decomposition from the SVD derivation. The component of $y$ perpendicular to the columns of $Q$ cannot be changed by any parameter choice, so minimizing the other component gives the triangular system. Explain that practical Householder QR applies a sequence of orthogonal transformations and need not explicitly construct a dense $Q$. Back substitution then solves for the coefficients. Suitable QR-based least-squares implementations have small normwise backward error, meaning they solve a nearby least-squares problem. That statement does not promise a small forward coefficient error when the underlying problem is ill conditioned. Also distinguish Householder QR from potentially unstable implementations of classical Gram-Schmidt. If numerical rank is uncertain, use a documented rank-aware solver and inspect its tolerance. Reference: LAPACK documents QR/LQ, complete orthogonal factorization, and SVD drivers at [https://www.netlib.org/lapack/explore-html/topics.html](https://www.netlib.org/lapack/explore-html/topics.html).


### Slide 39: Numerical rank is a tolerance decision

PDF pages 55; 1 build(s).

Suggested time: 6 minutes. Exact rank is an algebraic property, but software must decide whether a computed small singular value is distinguishable from roundoff or is useful given measurement uncertainty. Define a relative threshold explicitly so that students can reproduce which directions are retained. The displayed estimator is least squares restricted to the retained right singular subspace. If the original matrix is mathematically full rank, discarding a nonzero direction is a modeling or regularization choice, not merely a different way to compute the same exact minimizer. A tolerance based on dimension and unit roundoff is only an arithmetic heuristic; it is not automatically appropriate for noisy sensors or for the prediction task. Ask what information the discarded $u_j^{\mathsf T}y$ component contained and what bias its removal could introduce. Document feature scaling, rank threshold, residuals, and sensitivity checks, then use independent validation to assess the actual consequences.


### Slide 40: Case discussion: two similar sensors

PDF pages 56; 1 build(s).

Suggested time: 6 minutes. These are deliberately constructed values in common standardized units. Let the two fitted models have the same intercept and a coefficient difference of $(10,-10)$. Subtract their predictions to derive the formula before showing the two rows. If future test observations continue to have almost equal sensor readings, the two models remain close even though the coefficients disagree strongly. A future regime in which the sensors differ can expose this uncertainty. The issue is both statistical identification and the location of future inputs. Ask groups to propose an additional experiment or independent measurement that distinguishes the sensor contributions. Resampling can reveal variability but cannot create the missing information. Dropping a sensor or applying ridge imposes a useful modeling choice whose adequacy still requires validation. Correlated observational sensor values alone do not identify a causal effect.


### Slide 41: Why gradient descent converges

PDF pages 57; 1 build(s).

Suggested time: 4 minutes. For a quadratic objective this is an exact error recursion, not a local approximation. Along eigenvector $j$ of the Hessian, the error is multiplied by $1-\eta\lambda_j$. Contraction in every nonzero-curvature direction requires an absolute value below 1, giving $0<\eta<\frac{2}{L}$. With full column rank, $H$ is positive definite and the parameters converge to the unique solution. Under rank deficiency, zero-curvature directions do not contract, and the initial null-space component is retained. Gradient methods are motivated by large samples, sparse data, and online updates; we need not assume that the normal equations are always unusable. Over the full interval $0<\eta<\frac{2}{L}$, the slowest direction is determined by the largest absolute contraction factor. When $\eta$ exceeds $\frac{1}{L}$, the largest-eigenvalue direction can become the bottleneck, so the smallest curvature is not unconditionally the slowest direction.

**Further reading.**

-  Tengyu Ma and Andrew Ng, CS229 Lecture Notes, Chapters 1-3 and 8-9. [https://cs229.stanford.edu/main_notes.pdf](https://cs229.stanford.edu/main_notes.pdf)

**Web demonstration.** [https://regression-lab-graduate-2026.whu38f.chatgpt.site/#gradient-descent](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#gradient-descent)


### Slide 42: Ill-conditioning slows gradient descent

PDF pages 58; 1 build(s).

Suggested time: 5 minutes. Expand the error in an orthonormal eigenbasis of the symmetric Hessian. Each coordinate is multiplied by $1-\eta\lambda_j$. The worst contraction is the maximum absolute multiplier. To minimize this maximum on the eigenvalue interval $[\mu,L]$, balance the two endpoint magnitudes: $1-\eta\mu=-(1-\eta L)$. Solving gives $\eta_*=2/(L+\mu)$ and the displayed factor. This is a statement about the worst initial error direction under a constant step size, not a claim that every run achieves the bound or that all optimization algorithms have the same rate. Conjugate gradients, preconditioning, and regularization can behave differently. For rank-deficient designs, zero-curvature directions keep their initial components, so the full parameter-error contraction needs revision. The same singular spectrum now explains estimation sensitivity, the conditioning of the normal equations, and the speed of elementary gradient descent.


### Slide 43: Feature scale changes optimization

PDF pages 59; 1 build(s).

Suggested time: 4 minutes. This figure uses explicit quadratic examples with condition numbers 100 and 1. The vertical axis is the objective gap relative to its initial value, and the horizontal axis is iteration count. It illustrates how curvature ratios affect the speed of comparable optimization problems; it is not a speed guarantee for arbitrary real data. In the website, increase the learning rate until the iterations diverge, then adjust feature scaling. Explain that an invertible rescaling can preserve the OLS function space, whereas with a fixed $L_2$ penalty it also changes what equally large weights mean. This makes scaling particularly important before regularization. Exact definitions for the curves: Hessians $\mathrm{diag}(0.01,1)$ and $I$, initial error $[1,0]^{\top}$ for both, and step size $0.8$ for both. Their relative objective gaps are $0.992^{2t}$ and $0.2^{2t}$, respectively.

**Web demonstration.** [https://regression-lab-graduate-2026.whu38f.chatgpt.site/#gradient-descent](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#gradient-descent)


### Slide 44: Choose the right remedy

PDF pages 60; 1 build(s).

Suggested time: 4 minutes. Give students a poorly conditioned fit and ask for a remedy before revealing the table; wait 15 seconds. A stable QR or SVD computation controls avoidable numerical error, but it cannot eliminate the mathematical sensitivity of the least-squares solution. Scaling changes coordinates and can improve numerical behavior, although it does not remove exact dependence between columns or guarantee a well-conditioned design. Collecting observations that distinguish similar features can add information. Truncating singular directions or introducing a coefficient penalty changes the estimator and trades some flexibility for stability. Ridge and Lasso are therefore the next section, rather than being described as interchangeable numerical solvers. In the demonstration, keep the perturbation fixed and compare both coefficient changes and predictions at observed versus new feature patterns.


### Slide 45: 4. Regularization: Ridge and Lasso

PDF pages 61; 1 build(s).

Suggested time: 30 seconds. Pause before the next section and pose its central question: How much flexibility should the data be allowed to use? Invite one prediction, then use the examples and derivations to test it.


### Slide 46: Ridge trades bias for stability

PDF pages 62; 1 build(s).

Suggested time: 5 minutes. Continue using the average loss with its $\frac{1}{n}$ factor: the normal equations must therefore contain $n\lambda$. After centering the features and labels and handling the intercept separately, write $X_c=USV^{\top}$. Then $\hat{w}_{\lambda}=V\,\mathrm{diag}\!\left(\frac{s_j}{s_j^2+n\lambda}\right)U^{\top}y_c$. The shrinkage factors in prediction directions are $\frac{s_j^2}{s_j^2+n\lambda}$. Under Gaussian noise and a Gaussian prior on the weights, MAP estimation has the same form, with $n\lambda=\frac{\sigma^2}{\tau^2}$. The numerical regularization strength depends on whether the loss is summed or averaged. Do not equate this $\lambda$ directly with a parameter from another library.

**Further reading.**

-  Hastie, Tibshirani and Friedman, The Elements of Statistical Learning, 2nd ed., Chapters 2-4 and 7. Author-hosted book: [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/)

**Web demonstration.** [https://regression-lab-graduate-2026.whu38f.chatgpt.site/#regularization](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#regularization)


### Slide 47: Ridge filters singular directions

PDF pages 63; 1 build(s).

Suggested time: 7 minutes. Begin with the full objective in $b$ and $w$. Its derivative with respect to the unpenalized intercept sets the mean residual to zero, giving $b=\bar y-\bar z^{\mathsf T}w$. Substitution centers both the feature matrix and the response. Centering preserves the meaning of a separate unpenalized intercept; simply penalizing an augmented design with an identity matrix would not. Rotate the centered slope vector into right singular coordinates. Each scalar objective is $(s_j a_j-c_j)^2/(2n)+\lambda a_j^2/2$, whose derivative yields the displayed normal equation. Multiplying the resulting coefficient by $s_j$ gives the fitted-value shrinkage factor $h_j$. These are two different filters: $s_j/(s_j^2+n\lambda)$ acts on coefficients, whereas $h_j$ acts on predictions. Feature scaling changes the meaning of the coefficient penalty, so the singular spectrum and the numerical value of lambda should be interpreted in the chosen representation.


### Slide 48: Directional bias and variance under ridge

PDF pages 64; 1 build(s).

Suggested time: 6 minutes. Substitute $y_c=Z_cw_*+\xi_c$ into the spectral ridge formula. Each retained coordinate becomes a deterministic shrinkage of the true coefficient plus a transformed noise term. Because the nonzero left singular vectors of the centered design are orthogonal to the constant vector, centering the noise does not change their projected variance of $\sigma^2$. The mean and variance therefore follow directly without requiring Gaussian noise. The final equation is coefficient mean squared error in one direction, not automatically prediction error at an arbitrary future point. In-sample prediction weights that coordinate by its singular value, while a future input weights it by its alignment with $v_j$. For rank-deficient designs, true null-space coefficients contribute additional unidentifiable bias under the minimum-norm ridge choice. The variance decreases with lambda, but total risk need not improve for every signal or at every future input. Validation is needed because the true directional signal strengths are unknown.


### Slide 49: Ridge stabilizes the controlled example

PDF pages 65; 1 build(s).

Suggested time: 7 minutes. This table uses exactly the earlier two-column design and the same response perturbation, with no intercept added. There are two observations, so the mean-loss ridge denominator contains $n\lambda=2\lambda$. Inserting the two singular values and projecting back to the original coefficients gives the displayed closed forms. Verify that setting lambda to zero recovers $5.5$ and $-4.5$. For the illustrative signal $y_{\mathrm{true}}=q_1$, the unperturbed coefficients are $0.5$ and $0.5$, and the small component along $q_2$ is deliberately introduced as noise. Ridge suppresses that component while also introducing a smaller bias in the strong direction. The increasing training MSE is therefore expected and is not evidence that optimization failed. This construction does not establish a universally best lambda: if the weak component carried real predictive signal, excessive shrinkage would remove it. Choose the penalty using validation data representative of future feature patterns.


### Slide 50: Balance bias and variance

PDF pages 66; 1 build(s).

Suggested time: 4 minutes. This plot deliberately uses a verifiable one-dimensional estimator rather than claiming a universal U-shaped curve. Let the true mean be $\mu=1$, let the unshrunk estimator have variance 1, and shrink it by $a=\frac{1}{1+\lambda}$. Its squared bias is $(1-a)^2$, its variance is $a^2$, and the noise term is fixed at 0.15. Expected prediction error is the sum of these three terms. More general nonlinear models or complicated training procedures need not produce a simple U shape, but this example shows clearly how increased bias can reduce total error. Ask students to differentiate and find that the reducible error is minimized at $\lambda=1$. Explicit assumptions: the unshrunk estimator $T$ is unbiased, $\mathrm{E}[T]=\mu=1$ and $\mathrm{Var}(T)=1$, and is independent of the new-observation noise, whose variance is 0.15.

**Further reading.**

-  Hastie, Tibshirani and Friedman, The Elements of Statistical Learning, 2nd ed., Chapters 2-4 and 7. Author-hosted book: [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/)

**Web demonstration.** [https://regression-lab-graduate-2026.whu38f.chatgpt.site/#regularization](https://regression-lab-graduate-2026.whu38f.chatgpt.site/#regularization)


### Slide 51: Can regularization remove a feature?

PDF pages 67; 1 build(s).

Suggested time: 4 minutes. Pause for 15 seconds before displaying the objective and ask what might be gained by using only a few of many available sensors. Possible answers include lower acquisition cost and a simpler prediction rule. Then distinguish that practical preference from a guarantee that omitted variables are irrelevant. The absolute-value penalty changes the objective and is nondifferentiable at zero; its behavior cannot be understood by pretending the derivative there is zero. The intercept stays outside the penalty. Minimizing over it produces the same centering identity as before. Scale each nonconstant feature using a training-fold mean and the square root of its average squared centered value, so the squared column norm divided by n equals one. Remove constant columns before this scaling. The penalty acts on the standardized coefficients; converting back to original units is part of reporting the fitted model. Further reading: Tibshirani, Regression Shrinkage and Selection via the Lasso, 1996, [https://doi.org/10.1111/j.2517-6161.1996.tb02080.x](https://doi.org/10.1111/j.2517-6161.1996.tb02080.x).


### Slide 52: Why do corners encourage zeros?

PDF pages 68-69; 2 build(s).

Suggested time: 4 minutes. Build 1: show squared-loss contours centered at the unconstrained estimate (2,0.4) and ask students to predict the first point of contact as the contours expand. Wait 15 seconds. Build 2: reveal the contact points. In this isotropic example, the L2 ball projects the estimate radially to approximately (1.1767,0.2353), while projection onto the L1 ball gives (1.2,0). The latter is a corner, hence an exact zero. Both sets have radius parameter 1.2, but they are different constraints and do not produce the same fit. This is constrained geometry: minimizing squared loss subject to a norm bound. Suitable penalty and constraint parameters can describe the same optimum, but t is not lambda and should not be substituted for it. A corner makes sparse optima possible; the statement is not that every Lasso optimum lies at a corner. An optimum can also lie on an edge with several nonzero coefficients.


### Slide 53: Optimality at a zero coefficient

PDF pages 70; 1 build(s).

Suggested time: 5 minutes. First sketch absolute value on the board and ask what derivative could be assigned at its corner. Pause for 10 seconds. The convex subdifferential at zero is the interval from minus one to one, not a single arbitrary number. Differentiate the smooth squared-loss term and combine it with this interval coordinate by coordinate. At a nonzero fitted coefficient the interval becomes a single sign, giving an equality. At a zero coefficient the residual correlation may be anywhere within the threshold. The displayed implication alone is not an independent feature-selection rule: the residual is evaluated at the joint optimum and therefore depends on all fitted coordinates. Together with the nonzero-coordinate equalities, the conditions are necessary and sufficient for this convex optimization problem. The boundary case can have correlation exactly lambda and coefficient zero. Avoid using a strict inequality as a universal characterization.


### Slide 54: Soft-thresholding creates exact zeros

PDF pages 71-72; 2 build(s).

Suggested time: 5 minutes. Build 1: ask students to minimize the scalar function by considering positive, negative, and zero candidates; wait 20 seconds. Under the stated normalized orthogonality condition, the multivariate objective separates into a sum of these scalar objectives plus a constant. For a positive optimum, differentiation gives w equals c minus lambda, valid only if c exceeds lambda. The negative case gives c plus lambda, valid only if c is below minus lambda. Between the two thresholds, the subgradient condition selects zero. Build 2: reveal the graph and formula. The dashed diagonal is the unpenalized estimate, and the highlighted example lies on the flat zero segment. Standardized columns are not generally orthogonal; unit column norms alone do not justify applying this formula once to all coefficients. That distinction motivates the next coordinate-descent derivation.


### Slide 55: Deriving a coordinate-descent update

PDF pages 73; 1 build(s).

Suggested time: 6 minutes. Pause before the update and ask which part of the residual must exclude coordinate j. Using the full residual without adding back the current contribution would solve the wrong scalar problem. Expand the squared norm while treating every other coefficient as fixed. The column squared norm sets the quadratic curvature a_j, and its correlation with the partial residual gives c_j. Completing the square or applying the same subgradient cases yields soft-thresholding divided by a_j. A zero column has a_j equal to zero and should have been removed; do not divide by zero. In implementation, update the maintained residual after each coefficient change and cycle until an objective or KKT-based convergence check is satisfied. Convexity avoids spurious local minima; rank deficiency can still leave nonunique coefficients. Warm starts are an efficiency strategy, not a different statistical objective. See the squared-error coordinate updates in Friedman, Hastie and Tibshirani, 2010, [https://pmc.ncbi.nlm.nih.gov/articles/PMC2929880/](https://pmc.ncbi.nlm.nih.gov/articles/PMC2929880/).


### Slide 56: Ridge and Lasso trace different paths

PDF pages 74-75; 2 build(s).

Suggested time: 4 minutes. Build 1: ask students to predict the qualitative coefficient paths and pause for 15 seconds. Build 2: reveal two exact analytic examples, not paths estimated from a claimed real dataset. The normalized orthogonal feature design makes both formulas explicit. Ridge divides each nonzero coefficient by one plus lambda and approaches zero continuously without reaching it at a finite penalty in this example. Lasso reaches zero at the coefficient's absolute unpenalized value, so the three knots occur at 0.35, 0.8, and 2. The red and black paths eventually share the horizontal axis; this overlap is intentional. General correlated Lasso paths can enter and leave the active set, so this simple ordering is not a universal rule. The same numerical lambda in the two penalties is not a claim of equal complexity or equal predictive performance. Choose each model's tuning parameter by validation.


### Slide 57: Correlated features complicate selection

PDF pages 76; 1 build(s).

Suggested time: 5 minutes. Ask which sensor a sparse method should retain when the two columns are identical, and pause for 15 seconds. There is no information in these data that distinguishes them. Write s equals w1 plus w2. The triangle inequality makes the L1 penalty at least the absolute value of s, with equality for same-sign coefficients. The resulting scalar optimum is soft-thresholding of one at 0.2, namely 0.8. Thus every nonnegative decomposition listed in the table attains the same minimum. A solver may return one representative or a split depending on its update order and conventions. For a merely highly correlated design the solution can be unique yet unstable under small changes. An L2 component can encourage grouping and improve uniqueness, but that is a different objective. Neither Lasso nor Ridge turns coefficient selection into a causal conclusion.


### Slide 58: Choose a penalty for the modeling task

PDF pages 77; 1 build(s).

Suggested time: 4 minutes. Begin by asking whether interpretability means small coefficients or few retained features; these are different preferences. The table describes useful tendencies, not universal winners. Ridge need not improve error for every signal, and Lasso can omit relevant variables or retain irrelevant ones when observations are limited or features are correlated. Both losses use SSE divided by 2n, so the displayed penalty conventions must be kept consistent when comparing software settings. The intercept remains unpenalized in both cases. Evaluate the entire preprocessing-and-fitting procedure within each training fold. In the web demonstration, change the penalty while holding the simulated sample fixed, then compare coefficient trajectories and independent validation error. Ask students to state what changed in the objective and what remained the same in the data.


### Slide 59: Training error cannot select the model

PDF pages 78; 1 build(s).

Suggested time: 3 minutes. Give this trap: standardize the entire data set, then split it randomly. The validation procedure now uses distributional information from the test set. A more obvious leak is using the realized end-of-day electricity total as an input to a forecast made that morning. Ask: when each machine has multiple records, does randomly splitting rows evaluate prediction on new machines? The answer depends on the intended application. Scaling, missing-value imputation, and feature selection must all be fitted within the training fold of cross-validation. Repeatedly inspecting test results to choose parameters turns the test set into a validation set.

**Further reading.**

-  Tengyu Ma and Andrew Ng, CS229 Lecture Notes, Chapters 1-3 and 8-9. [https://cs229.stanford.edu/main_notes.pdf](https://cs229.stanford.edu/main_notes.pdf)


### Slide 60: 5. Feature expansion: polynomials and kernels

PDF pages 79; 1 build(s).

Suggested time: 30 seconds. Pause before the next section and pose its central question: How can a linear estimator represent nonlinear patterns? Invite one prediction, then use the examples and derivations to test it.


### Slide 61: Can a linear model bend?

PDF pages 80; 1 build(s).

Suggested time: 2 minutes. Ask which object must enter linearly for a model to be called linear regression: the raw input or the unknown coefficients? The cubic curve is still linear in its coefficients. The intercept is separate, so the displayed feature vector excludes a constant. The constructed observations use 14 equally spaced x values on [-1,1], a mean 0.7 sin(pi x)+0.25x, and fixed pseudo-random normal deviations with standard deviation 0.16. A cubic least-squares fit is shown. The plot is a teaching example, not a physical law. Any fixed feature map can replace raw inputs in the design matrix; least squares, ridge, and Lasso can all be applied to the resulting columns. Reference for the feature-map viewpoint: Ng and Ma, Stanford CS229 kernel notes, section 1.1, [https://cs229.stanford.edu/summer2019/cs229-notes3.pdf](https://cs229.stanford.edu/summer2019/cs229-notes3.pdf).


### Slide 62: How much curvature is useful?

PDF pages 81-83; 3 build(s).

Suggested time: 4 minutes. Build 1: show only the 14 training observations. Ask students to choose a polynomial degree and justify their choice; wait 15 seconds. Build 2: reveal the three OLS curves fitted to exactly the same training points, without regularization. Ask which will predict new observations best, then wait 15 seconds. Build 3: reveal the 13 separate validation points and their measured MSE. They use x values equally spaced from -0.95 to 0.95 and fresh independent deviations from the same constructed mean. Degree 3 has the lowest validation MSE among these three candidates, while degree 12 has the lowest training MSE. This is one finite constructed split, not a universal ranking. Repeatedly adapting candidates to one small validation set can overfit model selection; reserve a test set for a final assessment. Values are 0.179332/0.145546 for degree 1, 0.030043/0.014866 for degree 3, and 0.000670/0.289744 for degree 12. The monomial fits were solved with an SVD least-squares routine; no normal-equation inverse was formed.


### Slide 63: Expansion can bring back ill-conditioning

PDF pages 84; 1 build(s).

Suggested time: 3 minutes. The figure computes the 2-norm condition number of the full design, including the constant, at 30 equally spaced inputs on [-1,1]. Degree 12 gives 17968.47 for monomials and 2.65166 for the Chebyshev basis. The basis polynomials satisfy T0=1, T1=x, and Tj=2x T(j-1)-T(j-2). Both full-rank designs span exactly the same degree-at-most-q functions; in exact arithmetic their unregularized least-squares fitted values agree. Better coordinates improve numerical computation, but do not remove statistical uncertainty or justify more degrees. Scale raw input ranges before generating high powers; fit any data-dependent preprocessing on training data only. A general non-orthogonal coordinate change does not preserve the Euclidean norm of coefficients. Therefore equal numeric ridge penalties in monomial and Chebyshev coordinates impose different priors on functions; the displayed comparison concerns OLS conditioning only. Polynomial features in d variables through degree q have binomial(d+q,q) distinct terms, including the constant, so feature counts also grow quickly.


### Slide 64: A dot product can hide six features

PDF pages 85-87; 3 build(s).

Suggested time: 4 minutes. Build 1: ask students to expand the square silently; wait 20 seconds. Build 2: show the six-component feature map and ask why three entries carry a square-root-of-two factor; wait 10 seconds. Build 3: reveal the identity. The cross term is 2 x1 x2 z1 z2, so sqrt(2) must multiply the interaction feature on both inputs. The linear terms likewise have coefficient 2. This is the inhomogeneous degree-two polynomial kernel; the constant feature is part of its feature-map identity. When we later fit a separate unpenalized intercept and center feature vectors, this constant feature becomes zero. Do not claim that isotropic ridge on this weighted feature map equals isotropic ridge on the unscaled list [1,x1,x2,x1 squared,x1x2,x2 squared]; they produce the same function class but different penalties. The algebra here is exact. Source for polynomial kernel identities: Stanford CS229 kernel notes, section 1.4, [https://cs229.stanford.edu/summer2019/cs229-notes3.pdf](https://cs229.stanford.edu/summer2019/cs229-notes3.pdf).


### Slide 65: Compare points without listing features

PDF pages 88; 1 build(s).

Suggested time: 2 minutes. All monomials of total degree at most 3 in 100 variables give binomial(103,3)=176851 distinct terms, including a constant. The weighted polynomial kernel computes the relevant feature dot product through the original 100-dimensional dot product. Kernels can also correspond to infinite-dimensional feature spaces. This changes the computational dependence rather than making training free: a dense n by n Gram matrix takes quadratic storage, and its direct Cholesky factorization takes cubic time. For very large n, low-rank kernel approximations, random features, iterative solves, or an explicit feature model may be preferable. These are extensions, not developed here. Source for kernel computation and large-n cost: Stanford CS229T notes, section 4.7, [https://web.stanford.edu/class/cs229t/2016/notes.pdf](https://web.stanford.edu/class/cs229t/2016/notes.pdf).


### Slide 66: Why the solution lies in the training span

PDF pages 89; 1 build(s).

Suggested time: 4 minutes. First eliminate the unpenalized intercept analytically: b equals the response mean minus the training feature mean inner product with w. Let H=I-11 transpose/n, yc=Hy, and Phi_c=H Phi. The objective then has the displayed centered form. Decompose w into the span of the centered training feature vectors and its orthogonal complement. Their squared norms add by Pythagoras; the orthogonal component contributes exactly zero to each training prediction. Since lambda is positive, a minimizing w has no orthogonal component, hence w=Phi_c transpose alpha. This is the finite-sample representer argument. The same reasoning works in the Hilbert feature space of a PSD kernel, where the finite training span is closed. Do not set lambda to zero in the step that forces the orthogonal component to vanish. At lambda=0 it is one possible minimum-norm choice, not every minimizer. The next slide finds a convenient unique alpha even when Phi_c is rank deficient.


### Slide 67: Kernel ridge: solve in sample space

PDF pages 90; 1 build(s).

Suggested time: 4 minutes. Differentiate the centered primal ridge objective and multiply its first-order condition by n. Define alpha by the residual divided by n lambda, which is legitimate because lambda is strictly positive. The stationarity equation immediately gives w=Phi_c transpose alpha. Substitution in the definition of alpha yields (Kc+n lambda I) alpha=yc. This derivation does not cancel Kc and therefore remains valid even when centering makes Kc singular. For any nonzero vector v, v transpose (Kc+n lambda I) v is at least n lambda times its squared norm, so the system has a unique solution. Use a Cholesky or another appropriate stable linear solve in code; the inverse notation only states the closed form. A raw representation w=Phi_c transpose alpha may have many coefficient vectors, but this scaled-residual construction selects one unique alpha. Its entries sum to zero because Kc 1=0 and yc sums to zero. The n lambda factor follows from this lecture's SSE/(2n)+lambda norm(w) squared/2 convention. Compare the unnormalized convention in Stanford CS229 Problem Set 2, problem 1: [https://see.stanford.edu/materials/aimlcs229/ps2_solution.pdf](https://see.stanford.edu/materials/aimlcs229/ps2_solution.pdf).


### Slide 68: Center a new point in the same space

PDF pages 91; 1 build(s).

Suggested time: 3 minutes. Let the training feature mean be phi_bar. The i-th centered kernel entry is inner product(phi(x_i)-phi_bar, phi(x)-phi_bar). Expanding gives k(x_i,x) minus the mean over training j of k(x_j,x), minus the mean over training j of k(x_i,x_j), plus the grand mean of K. The compact vector expression H[k(x)-K1/n] contains all four terms. Never recompute a mean from validation or future inputs, and do not center a single new point by itself. The fitted function is y_bar+inner product(phi(x)-phi_bar,w), which gives the displayed prediction after w=Phi_c transpose alpha. Equivalently, the uncentered-feature intercept is b=y_bar-inner product(phi_bar,w). Centering the target and leaving the intercept unpenalized also avoids treating the constant part of an inhomogeneous polynomial kernel as a penalized intercept. This formula is valid with an implicit feature space and is used for all RBF fits shown next.


### Slide 69: Which similarities are valid kernels?

PDF pages 92; 1 build(s).

Suggested time: 3 minutes. The quadratic-form identity proves necessity for an inner-product kernel. A symmetric real function is a valid positive-semidefinite kernel precisely when all its finite Gram matrices are PSD; one matrix with a negative quadratic form rules it out. The top 2 by 2 matrix is a valid Gram matrix for two feature vectors but does not alone certify an arbitrary kernel function on all points. The bottom matrix has nonnegative entries yet c=(1,-1) gives c transpose K c=-2, so it cannot be a Gram matrix. Show this arithmetic if students conflate positive entries with positive semidefiniteness. The listed kernels are standard PSD examples under the stated parameter restrictions. Distinct samples do not guarantee that every valid kernel's Gram matrix is nonsingular; centering always gives at least the constant-vector null direction. Source: Stanford CS229 kernel notes, section 1.4, [https://cs229.stanford.edu/summer2019/cs229-notes3.pdf](https://cs229.stanford.edu/summer2019/cs229-notes3.pdf).


### Slide 70: How local is an RBF similarity?

PDF pages 93-95; 3 build(s).

Suggested time: 4 minutes. Build 1: show only five input locations and ask which of 0.25 and 0.8 should be more similar to zero; wait 10 seconds. Build 2: reveal the RBF definition and its interpretable distance scale. Ask what happens when ell increases, then pause for a prediction. Build 3: reveal the three curves. At fixed nonzero distance, increasing ell increases similarity, broadening the neighborhood. The horizontal positions of points are their signed offsets from the fixed center zero; vertical zero is just a marker baseline, not a target value. The graph is a kernel section, not a fitted response curve. In kernel ridge, coefficients may be positive or negative, so similarity is not itself the final influence or prediction. For multiple input coordinates, scales determine distances; train-only standardization and a validated bandwidth are part of the model. The RBF has an infinite-dimensional feature representation, but KRR still solves the finite system from the previous slides.


### Slide 71: Bandwidth and penalty do different jobs

PDF pages 96; 1 build(s).

Suggested time: 3 minutes. Both panels use the same 14 training observations and the same centered-kernel prediction formula as earlier. The left panel changes the kernel, hence which functions and norms the model prefers. The right panel keeps the kernel fixed and changes shrinkage within that feature space. For a fixed centered Gram eigenvalue d, the fitted-response filter is d/(d+n lambda); changing the bandwidth changes both eigenvectors and eigenvalues, not simply this scalar denominator. In the left panel the validation MSE for ell=.12,.40,1.00 at lambda=.001 is .03343,.02524,.01685. In the right panel the MSE for lambda=.0001,.01,.30 at ell=.40 is .02561,.02250,.15297. These are measured on the 13 validation observations already shown. Do not pick parameters from visual smoothness alone. A broad kernel combined with a very small penalty may still fit detail; neither ell nor lambda has a universal one-dimensional complexity ranking across arbitrary data and rescaling. The diagrams use constructed data, and no claim of global optimality among all hyperparameters is made.


### Slide 72: Beyond the observed range?

PDF pages 97; 1 build(s).

Suggested time: 3 minutes. The blue band is the training input range [-1,1]. The two curves show a degree-three OLS fit and RBF KRR with ell=.4 and lambda=.001, each fit only to the same observations in that window. Both curves extend outside it by mathematical convention. The polynomial grows according to its highest-degree terms. For the RBF with an unpenalized intercept, as a new input moves infinitely far from every training input, raw kernel values tend to zero and the prediction tends to the fitted intercept b, which is not necessarily the sample response mean. With the centered formula and sum(alpha)=0, this limit is y_bar-(K1/n) transpose alpha. Do not say that centered RBF predictions always revert to y_bar. The plotted finite window need not have reached that limit. Ask students how they would validate for a factory switching to a much larger production range: an ordinary random split within the old range cannot directly test that new regime. The model and the dataset jointly determine what can be assessed. End with the lab: compare degree, basis, penalty, and bandwidth while keeping the validation split fixed.


### Slide 73: Return to tomorrow's electricity forecast

PDF pages 98; 1 build(s).

Suggested time: 5 minutes. Return to the production plan used at the beginning and ask students to outline a complete forecasting procedure. They should specify which inputs are available before the target is observed, how the chronological split matches future deployment, and what baseline will be used. Ask a volunteer to derive the normal equations and another to explain why an invertible Gram matrix can still be a poor computational route. Then ask when shrinkage or a richer representation could improve generalization. A low training error does not answer those questions. Reserve two minutes for individual written answers and three minutes for discussion. The five sections should now form one chain: motivation, formulation, stability, regularization, and representation.


### Slide 74: Further reading and editable examples

PDF pages 99; 1 build(s).

Source details: Department of Energy industrial energy guide, [https://www1.eere.energy.gov/manufacturing/eguide/iso_step_2_4.html](https://www1.eere.energy.gov/manufacturing/eguide/iso_step_2_4.html). Hastie, Tibshirani and Friedman, The Elements of Statistical Learning, author-hosted book, [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/). Trefethen and Bau, Numerical Linear Algebra, SIAM, 1997. Tibshirani, Regression Shrinkage and Selection via the Lasso, Journal of the Royal Statistical Society Series B, 58(1), 1996, pages 267-288, [https://doi.org/10.1111/j.2517-6161.1996.tb02080.x](https://doi.org/10.1111/j.2517-6161.1996.tb02080.x). Friedman, Hastie and Tibshirani, Regularization Paths for Generalized Linear Models via Coordinate Descent, Journal of Statistical Software, 33(1), 2010, pages 1-22; the squared-error section is relevant here, [https://pmc.ncbi.nlm.nih.gov/articles/PMC2929880/](https://pmc.ncbi.nlm.nih.gov/articles/PMC2929880/). The web lab is [https://regression-lab-graduate-2026.whu38f.chatgpt.site](https://regression-lab-graduate-2026.whu38f.chatgpt.site). All numerical lecture examples are constructed for teaching; the source files expose the plotted values and analytical calculations.

