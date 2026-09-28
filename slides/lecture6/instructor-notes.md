# Instructor notes: Ensemble Learning

Linear/logistic regression leads directly to ensembles. Six short transition frames mark the phases. GLM remains optional and excluded. Numbers below match the default presentation.

## 1. Ensemble Learning

This lecture follows linear and logistic regression directly; no GLM lecture is required. Begin with a concrete weighted combination of weak rules, reveal how AdaBoost learns the combination, then derive it. Residual fitting leads to gradient boosting. A short decision-tree primer precedes bagging and random forests. Allow approximately 90 minutes for the core route and 110-120 minutes for all details and application discussion. A one-slide optional GLM bridge is available but disabled in main.tex.

## 2. From one score to a sum of rules

The sigmoid is s(z)=1/(1+exp(-z)). An intercept is included in the linear score. Feature expansion is another way to enrich a linear predictor; ensemble learning instead fits and combines multiple component functions. An ensemble is the umbrella term; boosting and bagging are two different construction strategies. This slide previews gradient boosting, where the previous regression or classification loss can be retained. AdaBoost first gives a particularly clean derivation using exponential loss and minus/plus-one labels; explicitly announce that change. Sums of linear functions of exactly the same features remain linear, so expressive gains require suitable nonlinear or varied rules, for example threshold functions. A weak model here means a simple component with limited individual predictive ability; the formal weighted-edge assumption will be stated when proving the AdaBoost training bound.

## 3. Learning Goals

Keep the audience oriented to the central question: how should models cooperate? AdaBoost focuses later rules through observation weights; gradient boosting fits a loss-derived correction target; bagging fits models independently and averages. These are all ensemble methods. The tree primer is deliberately postponed until before bagging, with one-split threshold rules explained locally in the boosting examples. The four real applications motivate different choices and evaluation metrics.

## 4. Where do ensembles become useful?

Read the grid across each row: movie-rating prediction, click prediction, load forecasting, Kinect. Use these applications as motivation; the later case slides give primary sources and scope. These are historical examples, not descriptions of current product architectures. Small arithmetic examples remain useful for deriving the update rules. Diagrams explain pipelines; reported performance figures are explicitly labeled.

## 5. Phase 1: AdaBoost

Pause on the question and explain that the first phase is about watching the mechanism work. The next slide defines a decision stump directly as a one-split rule, so a tree lecture is not required yet. A simple rule is the initial intuition; the positive weighted-edge assumption for the formal guarantee will come later.

## 6. Can Weak Rules Work Together?

Open the ensemble mathematics with this concrete example. A stump is simply an if-then rule with one threshold: here predict minus one when x is below 2.5, otherwise plus one. No general tree construction is needed yet. The labels alternate in blocks: minus, plus, minus, plus. No one-dimensional stump can represent all three changes. The shown stump predicts minus below 2.5 and plus above it; observations 5 and 6 are wrong. Pause before revealing the question. All data are deliberately constructed, not measured. Both stump orientations are allowed. Here labels are minus one and plus one, unlike the zero/one convention used for Bernoulli likelihood.

## 7. Two Kinds of Weight

Introduce notation without an optimization objective yet. D is a probability distribution over the n training observations; it is not a distribution over labels. Alpha is a coefficient on a fitted rule and need not sum to one across rounds. F is a real-valued score and is not restricted to minus one and plus one. A positive F predicts plus one, a negative F predicts minus one; use a fixed tie rule. Later rounds reweight relative to correctness of the latest fitted rule, equivalently in proportion to exponential loss under the accumulated score. Weak in this introductory discussion describes a limited rule class, not an unqualified theorem assumption. The positive-edge condition needed for the guarantee will be stated explicitly when deriving the bound.

## 8. AdaBoost: The Algorithm

Present the recipe now and use the next two slides to see it work; derive both formulas from a single loss afterward. This is discrete binary AdaBoost, not multiclass SAMME or Real AdaBoost. For now the base learner searches simple threshold rules and their reversed orientations. With a perfect learner, one can return that learner directly, which avoids the infinite coefficient. If the weighted error is above one half and the learner class is closed under sign reversal, flip the prediction first; at one half there is no edge. A finite requested T is a maximum, not an obligation to proceed through these boundary cases. Use validation data to select model size in applications. Primary source: Freund and Schapire 1997; Schapire 2003 Figure 1 in the symmetric coefficient convention.

## 9. One Update, New Weights

Work out the normalization explicitly if time permits: raw correct weights are one over eight times one over square root three, raw mistake weights are one over eight times square root three, and Z is square root three over two. The bar chart is generated from exact rational weights, not hand-adjusted numbers. D2 is used to choose h2. It is not a prediction probability for any class. Reproducible evidence is in examples/adaboost_example.py and adaboost-results.json.

## 10. Three Stumps, One Classifier

The numerical search considers thresholds 1.5 through 7.5 and both stump orientations. It breaks ties by the smallest threshold, then the positive orientation. The second-round distribution has individual weights one twelfth except observations 5 and 6 at one fourth. After round two, D3 for the pairs 1--2, 3--4, 5--6, 7--8 is respectively 0.05, 0.25, 0.15, 0.05 per observation. The third learner therefore has weighted error one fifth although its unweighted error is one half. Every round's exponential loss falls: 0.8660, 0.6455, 0.5164. Training classification error need not decrease on each round, because the optimized criterion is exponential loss. Zero training error here says nothing by itself about test performance. Displayed coefficients are rounded; the plotted scores use full precision.

## 11. Phase 2: Why AdaBoost Works

The worked example has shown what the algorithm does. Now ask whether both types of weight can follow from one optimization principle. Introduce exponential loss on the next slide. Keep the later training-error guarantee separate from test performance: the constructed example's zero training error is not a generalization statement.

## 12. A Loss for the Accumulated Vote

We have seen the algorithm succeed on the constructed example. Now derive the algorithm from an objective, beginning with the signed margin. Recall that F is a real-valued score, not a probability. A positive margin means agreement between the observed sign and the predicted sign. Zero is a tie; fix a deterministic tie convention, and later count all zero margins as errors for a conservative bound. A correct example with a small margin still has nonzero loss. A very negative margin has a rapidly growing penalty. We use the mean loss; multiplying by n would not change the minimizer. Exponential loss is the optimization criterion for this derivation, not Bernoulli negative log likelihood.

## 13. Stagewise Fitting and Weights

The old model is fixed throughout this round, so its total exponential loss is a positive constant with respect to the new learner and its coefficient. Minimizing the new loss therefore means minimizing Z. This algebra derives the sample weights from the objective; reweighting is not an extra heuristic. An example with a large positive margin receives little weight, and an example with a negative margin receives more. At F zero, all weights are one over n. Source: Schapire's 2003 overview, Section 3; forward stagewise viewpoint in Friedman, Hastie and Tibshirani.

## 14. Choosing a Weak Learner

The sum of weights on correct predictions is one minus epsilon because D is normalized. For a positive coefficient, the multiplier of epsilon is positive, so the same weak learner minimizes the objective at every fixed positive coefficient. In the finite example we enumerate all candidate stumps exactly. A practical tree-growing procedure may only approximately minimize weighted error. Assume the selected learner has an edge, epsilon below one half; when both orientations are available a learner worse than chance can be flipped.

## 15. Deriving the Vote Weight

Differentiate before revealing the solution. The second derivative is the original positive Z expression, so this stationary point is the unique minimizer in alpha. These are weights on learners, whereas D contains weights on observations. For epsilon equal to zero, the optimum is approached as alpha goes to infinity; stop with the perfect weak learner rather than computing an infinite coefficient. At epsilon equal to one half, alpha is zero and there is no improvement. The exact coefficient here uses no learning-rate shrinkage; adding shrinkage changes the exact-normalizer conclusions later.

## 16. Why Mistakes Receive More Weight

The normalizer keeps weights summing to one. The displayed relative multiplier holds for any one mistaken and one correctly classified observation, even if their previous weights differed. With the exact alpha formula and an error strictly between zero and one half, mistakes collectively have mass one half under the next distribution. That does not mean the next learner has error one half: the next learner is a different rule. The weak learner can fit weighted data directly; this update does not require resampling observations.

## 17. Bounding the Training Error

The first inequality follows observation by observation: a nonpositive margin has exponential loss at least one, while the indicator is zero for a positive margin. The product identity follows by repeatedly using J at round t equals J at round t minus one times Zt. Substituting the exact unshrunk alpha gives the square root expression. Use log(1-u) less than or equal to minus u to obtain the exponential bound. This finite-run conclusion is conditional on a uniform positive edge under every distribution D_t encountered along the run. A standard sufficient weak-learning assumption is that the base learner can achieve this edge for any distribution over the training observations. Being slightly better than chance under D1 alone is insufficient. No weak-learning condition is guaranteed merely by choosing a simple model class. The bound can be loose: the example has zero training error but exponential loss about 0.5164 after three rounds. Source: Freund and Schapire 1997 and Schapire 2003 Section 3.

## 18. When Labels Are Wrong

The two curves use the common margin m equals yF. Exponential loss grows exponentially as a prediction becomes confidently wrong; logistic loss grows approximately linearly in the same limit. Both are unbounded, so the contrast does not establish absolute robustness of logistic loss. Sensitivity to mislabeled examples follows directly from the reweighting formula; do not claim every AdaBoost fit overfits or that boosting cannot generalize well. In practice inspect persistent high-weight observations, validate stopping and learner depth, and consider losses appropriate to the problem. The next module develops a method that can use differentiable losses other than the exponential loss.

## 19. Back to Logistic Regression

This is a pointwise, unrestricted population-risk result. At probability zero or one the optimum is approached at an infinite score. The factor two is essential for the convention alpha equal to half log odds: the AdaBoost exponential-risk score is half the log odds, whereas the logistic score previously used is the full log odds. A finite constrained AdaBoost model does not automatically provide calibrated probabilities through this conversion, and exponential loss is not the Bernoulli negative log likelihood. This provides the conceptual bridge to gradient boosting: choose a loss, then add simple functions to reduce it. After the recommendation-system application, the next method module starts with squared error because fitting residuals makes the update tangible, then extends the idea to logistic loss. Source: Friedman, Hastie and Tibshirani's additive logistic regression paper, exponential criterion lemma; Schapire 2003 Section 6.

## 20. Movie ratings: two views of taste

Here u denotes a user, i a movie, and each f predicts that user's rating. Matrix factorization is commonly called SVD in this context; RBM is a restricted Boltzmann machine. The schematic and equation explain a generic linear blend, not a reconstruction of Netflix's exact formula. The source does not publish the coefficients or an intercept. Do not assume equal weights or weights summing to one. This is prediction blending, not AdaBoost, and its component models need not be weak learners. It broadens the ensemble idea beyond the specific sequential algorithm just derived. Different model families can make complementary errors, but improvement must be checked on held-out data.

## 21. A blend improves rating prediction

All three RMSE values come from the same Netflix article: SVD 0.8914, RBM 0.8990, and linear blend 0.88. Preserve the reported precision; the source does not specify the exact evaluation split. The dot plot has an enlarged, explicitly labelled horizontal axis, rather than bars with a truncated baseline. These historical offline scores do not measure watch time, ranking quality, retention, or revenue. Netflix reported engineering changes before putting the two underlying algorithms into production; this slide does not claim that the pictured fixed blend was deployed unchanged or is used today. The two-model example is not the complete prize-winning ensemble.

## 22. Phase 3: Learning a Correction

Keep the additive model but change the fitting target. Squared loss leads to ordinary residuals; other differentiable losses lead to negative-gradient targets. The preceding recommendation case demonstrates model combination and should not be identified with the discrete AdaBoost algorithm. The next phase derives a sequential correction procedure explicitly.

## 23. Keep the model; learn a correction

This is the conceptual transition from AdaBoost's additive classification score to boosting for a continuous response. The weak model now produces a real-valued correction, not a class label. Start with the ordinary residual intuition under squared loss; the next slides derive why it is the correct target in that case. For other losses the fitting targets are negative loss derivatives, and generally are not y minus F. A simple fitted function may be a one-split rule, a smooth spline, or another restricted regression function. The existing model stays fixed while the next correction is learned.

## 24. One correction lowers squared error

Retain the original four-point example before introducing function-space gradients. All four residual targets are fitted exactly by a single threshold rule. With shrinkage one half the MSE falls from one to one quarter. The plotted first correction is part of the same teaching calculation, not a measured application. The factor one half in the per-observation loss makes its negative derivative exactly equal to the ordinary residual. The averaging factor in MSE affects its numerical scale, not the optimal fit.

## 25. Correct what the previous model missed

Each column displays one round: the upper panel compares observed responses with the previous and updated predictions, while the lower panel shows the newly computed residual targets and the fitted correction. The first, second and third residual magnitudes are one, one half and one quarter. Half of each correction is added, leaving residual magnitudes one half, one quarter and one eighth. This particularly simple dataset keeps the same split location; general datasets may require different rules at later rounds. It demonstrates recomputation and shrinkage, not the claim that any weak learner guarantees progress or that all datasets follow this geometric decrease. All coordinates and MSE values are generated and checked by examples/generate_boosting.py.

## 26. Why squared loss leads to residuals

Derive the expansion by substituting r_i minus eta h_i into one half the sum of squared residuals. For a nonzero correction, the exact sufficient interval is zero less than eta less than twice the residual inner product divided by the squared norm of h. If h fits the residuals better than the zero function in squared error, expanding that fitting inequality gives twice the residual inner product greater than the squared norm of h, so positive alignment follows. This makes the requirement on the weak learner concrete; fitting an arbitrary function is not itself a guarantee of improvement. The equality h=r is unconstrained steepest descent at the training coordinates.

## 27. Gradient descent in prediction space

Friedman (2001) formulates stagewise additive modeling as gradient descent in function space. On the training sample the gradient is an n-dimensional vector, which is a useful concrete way to explain the functional interpretation. A restricted learner approximates that direction and gives predictions away from the training inputs. Least-squares fitting to pseudo-residuals does not replace the original loss: it is the subproblem for finding a direction. The original loss is used to choose the step and to evaluate the model. An approximate fit must have positive alignment with the negative gradient to be a descent direction. The function class need not consist of trees. Using an average rather than a sum in L scales all gradient coordinates by the same constant, which can be absorbed by the step.

## 28. The gradient boosting algorithm

The displayed idealized line search assumes a finite minimizer exists. If it does not, or exact minimization is impractical, choose a finite loss-reducing step. For convex losses along a direction, shrinking an exact improving line-search step toward zero preserves nonincrease. Squared loss and logistic loss are convex in the score. A weak fit aligned with the negative gradient admits a sufficiently small descent step for a differentiable loss; without this alignment there is no general improvement guarantee. For squared-loss partition functions with residual means in each region, rho equals one whenever the correction is nonzero. Thus the original numerical experiment directly uses nu times h. The constant initializer is the sample mean for squared loss and the logit of the class proportion for binary log loss when both classes occur. This is Friedman (2001) Algorithm 1 with explicit shrinkage and numerical caveats in the notes.

## 29. Classification still uses the logistic loss

Explicitly switch from AdaBoost's plus/minus-one labels to zero/one labels. The response minus current probability is a pseudo-residual with respect to the score; it is not y minus the score and it is not the residual of a thresholded class prediction. Regress these real-valued targets on x. Corrections are added to the score, and the sigmoid is applied after summing; do not add predicted probabilities. For an observed positive label, a small predicted probability gives a larger positive correction target than a probability close to one. The optimal constant score is the logit of the observed class proportion if both classes occur. For stable numerical evaluation, use max(F,0)-yF+log1p(exp(-abs(F))). The example generator checks this gradient by finite differences. The chosen score convention is the log odds; it differs by a factor of two from some plus/minus-one formulations in Friedman's presentation.

## 30. Simple corrections build a flexible fit

The curves preserve the original computed run: seed 521223, target mean sin(1.6x)+0.22x, and independent Gaussian noise with standard deviation 0.38. Each base learner is a greedy depth-two regression tree with at least three training observations per leaf, introduced here simply as a fitted piecewise-constant correction with at most four intervals. Formal tree structure comes later. Each fit uses the residuals left by the current model, and the sum has more partitions than one constituent. Curves show rounds 1, 10 and 60 of the same run. The dashed conditional mean is known because this is a simulated teaching example, not a measured real-world result.

## 31. Use validation to choose when to stop

The loss curves preserve the original computed teaching experiment. The validation minimum occurs at 71 rounds with validation MSE 0.214306; after 300 rounds it is 0.246702. Training MSE decreases monotonically and reaches 0.019923. These are properties of this realization, not universal stopping choices. The validation set chooses the stopping point; an additional untouched test set is needed for a final evaluation of the selected workflow. Shrinkage, base-function complexity and rounds interact and should be tuned together. Here we plot MSE, whereas the earlier derivation used one half the unnormalized sum of squared errors; their minima are identical. Real applications in the following case studies use task-appropriate validation.

## 32. Ad clicks: learn features with trees

A tree is a sequence of feature-threshold questions; a leaf is its final region. This case previews that structure before the brief formal tree primer. Each tree contributes one active leaf indicator. The learned logistic weights replace the original leaf scores; the output is not a sigmoid of their original sum. The diagram is schematic.

## 33. Does the hybrid predict clicks better?

Trees denotes boosted trees. Values are NE ratios, not absolute NE. Here H(p)=-p log(p)-(1-p)log(1-p). The table implies a 2.87 percent improvement over LR; use it instead of the inconsistent prose. Sample counts were undisclosed.

## 34. Forecast electricity demand

The study used separate hourly models and log-transformed demand. Spline learners extend the same residual-fitting principle beyond trees. This is a competition result on real utility records, not evidence of operational deployment or a universal ranking of algorithms.

## 35. What is known when we predict?

The paper combines forward and backward predictions for historical gaps; future-week inputs include forecast temperatures. Teaching implication: using realized future weather changes the task. Match the time split and feature availability to the intended deployment. This principle is separate from the paper's particular validation procedure.

## 36. Phase 4: A Brief Look at Trees

Introduce just enough tree mechanics for the coming bagging discussion: a recursive partition, a leaf prediction, a greedy split, and sensitivity to the training data. Earlier boosting corrections included threshold rules and piecewise-constant functions, while the electricity application used spline learners. Trees are a common choice of base learner, not a requirement of gradient boosting.

## 37. A tree predicts within regions

We have already used simple learners for boosting. Before bagging, collect the essential tree ideas in three slides. Red is the depth-two tree, blue dots are training observations, and the dashed curve is the true mean. Root depth is zero. Each node asks an axis-aligned question; following the questions reaches a terminal leaf. Subsequent thresholds are 0.06287 on the left and 0.85587 on the right. Leaf predictions are 2.348, 3.113, 1.774 and 2.414. A univariate tree uses intervals; multiple features give axis-aligned regions. For squared loss, differentiating a leaf's SSE gives its sample mean.

## 38. Choose a split by reducing error

Both children must contain observations. Candidate thresholds lie between distinct observed feature values, with leaf-size constraints if used. Exhaustive enumeration over all five thresholds gives 3.5 as best. Its child SSE values are each 2/3, giving total 4/3. Greedy local splitting does not guarantee a globally optimal full tree. For classification, predict the most frequent class in the leaf or report its class fractions; these estimates need not be calibrated. Minimize (n_L/n)G_L+(n_R/n)G_R. The same partition mechanism supports regression and classification. Source: scikit-learn tree mathematical formulation.

## 39. Deep trees can be unstable

All figures use the constructed regression mean 2+sin(2*pi*x)+0.8*x with Gaussian noise SD 0.32. The depth curve uses 64 training rows and 800 independent validation draws. Validation MSE is 0.148 at depth 4 and 0.198 at depth 8. Root depth is zero; minimum leaf size is one. Depth, leaf size, or pruning control capacity. The prediction plot shows three depth-eight bootstrap trees in pale colors and their 100-tree mean in blue. Each bootstrap draws 64 indices with replacement; dashed black is the true conditional mean. The single-tree baseline uses all original rows. Bootstrap sensitivity conditional on this sample differs from sampling variability over new datasets, and the improved MSE is an illustration, not a guarantee. If validation selects a model, final assessment needs separate appropriate test data. Bagging commonly averages deep, unstable trees; these need not be the deliberately weak stumps used to introduce boosting.

## 40. Phase 5: Bagging

The previous frame showed sensitivity to bootstrap resampling. Use that observation to motivate a new way for models to cooperate: independently fitted trees can be averaged instead of fitted as successive corrections. Bagging often uses deep, flexible trees, so do not call all these base models weak stumps. The variance calculation will describe when averaging is effective, without promising universally lower test error.

## 41. Bagging averages bootstrap fits

Source: Breiman, Bagging Predictors. Each bootstrap has n draws but repeats some rows and omits others. Trees can be fitted independently conditional on the original dataset. Classification here uses label voting, consistent with the original description; probability averaging is another common convention. A base tree need not be deliberately weak. Bagging can reduce variance for unstable learners but is not a universal improvement for every learner or problem.

## 42. Why averaging can reduce variance

Randomness can include the training sample and bootstrap or feature randomization. At fixed x, equal variances and equal pairwise correlations yield an exact algebraic identity. With independent bootstrap seeds conditional on a fixed dataset, predictions can be conditionally independent; shared training data induces dependence across repeated datasets. This is a schematic explanation of unconditional prediction variance, not a claim that empirical tree pairs have identical correlations. It removes neither bias nor irreducible noise and is not an MSE guarantee.

## 43. Correlation limits the benefit

Analytical curves plot rho+(1-rho)/B, not estimated learning curves. Nonnegative correlations are illustrative and fixed while B varies. Identical predictions have rho=1, giving no variance reduction. Random forests vary candidate features so a dominant feature does not force similar early splits in every tree. The outcome depends on data and individual-tree strength.

## 44. Phase 6: Random Forests

Connect directly to the preceding covariance formula and correlation plot. More trees reduce the averaging term but do not remove its fixed-correlation limit. Feature subsampling changes how trees are constructed; it may reduce correlation while also weakening individual trees. The algorithm and its tradeoff come next, followed by out-of-bag prediction.

## 45. Random forests vary each split

Source: Breiman and Cutler. Feature subsets are schematic with d=5 and m=2. A fresh subset is drawn at each node, not once per tree or forest. We describe standard bootstrap random forests; other variants exist. Use regression means and classification label votes here. Neither bagging nor forests is guaranteed never to overfit. Tree count mainly controls averaging accuracy; depth, leaf size and feature subsampling also affect the fitted predictor.

## 46. Out-of-bag prediction

The exact exclusion probability is (1-1/n)^n; 0.368 is its large-n limit. For regression average a row's OOB trees, and for classification vote. With too few trees some rows have no OOB prediction. OOB assessment is useful for bagging and bootstrap forests. Repeated tuning against OOB scores can bias selection; final assessment needs an appropriate held-out protocol, especially for dependent or shifted data.

## 47. Two ways to build a stronger predictor

This compares methods already covered rather than announcing AdaBoost. Boosting stages depend on previous stages; bagged trees train independently across trees conditional on the original dataset. Computations within one boosting stage can still be parallel. The AdaBoost training-error bound requires a weighted error below one half at each relevant round; averaging arbitrary models alone has no analogous weak-learning guarantee. Bagging often uses deep trees with high variance, not necessarily weak learners. Variance reduction, bias reduction, and predictive accuracy are not exclusive to one family: state the mechanisms rather than a rigid bias-versus-variance taxonomy. The next case shows randomized forests in Kinect body tracking.

## 48. Kinect: trees recognize body parts

The paper identifies this method as a core Kinect component. The illustration explains the pipeline; it is not a captured camera frame or a model output. First describe the practical need to recover pose after tracking fails, then reveal the classification reformulation.

## 49. From tree probabilities to joint positions

Trees use separate synthetic-image sets and randomized candidate splits, not textbook bootstrap bagging. Leaf probabilities are averaged; spatial mode finding produces joint proposals. The speed is the paper's optimized algorithm, not the complete Kinect system. These historical results do not establish present-day performance.

## 50. How do the models work together?

Avoid equating bagging exclusively with variance reduction or boosting exclusively with bias reduction; these are intuitions, not universal decompositions. The variance formula earlier concerned a fixed input and repeated training samples. AdaBoost's training-error guarantee does not guarantee test performance. For binary gradient boosting, sum scores then apply sigmoid once. For random forests, averaging per-tree probabilities and majority voting need not make identical decisions.

## 51. References and further reading

Clickable primary references. Supporting sections and derivation conventions appear in module source ledgers. Figures distinguish constructed demonstrations, sourced measurements, and explanatory diagrams. The AdaBoost module also cites Schapire2003 for exponential loss and the training-error bound. Numerical scripts validate displayed calculations.

## 52. Sources for the application cases

These historical sources document the applications. Case-specific source ledgers identify sections and metric conventions. Published results were checked against the original papers; no source result is presented as a new experiment.

## Optional GLM bridge

Enable the commented input of optional-glm.tex in main.tex to add one minute of background. It is not a prerequisite. Enabling it increases subsequent slide numbers by one.
