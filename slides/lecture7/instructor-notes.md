# Instructor notes

This is an 80-minute lecture with 37 main slides. Slides 38–44 are optional details. The main lecture ends at the understanding check on slide 37. Slide numbers below refer to logical slides, not PDF pages; staged reveals repeat the same slide number. The handout shows every step on one page per slide.

## Timing and teaching prompts

| Slide | Minutes | Teaching move |
|---|---:|---|
| 1 | 1 | Introduce the lecture as the next step after linear models, AdaBoost, and bagging. |
| 2 | 2 | State the route: partition, average, then correct. |
| 3 | 3 | Trace one point with x1 > 5 and x2 <= 3. Match the path to region R2. |
| 4 | 2 | Distinguish a class-proportion estimate from a hard class prediction. A constant leaf can serve either task. |
| 5 | 3 | Calculate the four residual squares around 5, then around 1.5 and 8.5. Ask why the means must change for every candidate split. |
| 6 | 3 | Compute Gini from class proportions. Emphasize weighting by child sample counts. A large pure child and a small impure child should not count equally. |
| 7 | 2 | The search is greedy and recursive. Sorting enables an efficient scan; a locally best root need not belong to the globally best tree. |
| 8 | 2 | Explain maximum depth, minimum leaf size, and pruning. Validation chooses the complexity penalty. Standard leaf-constant regression trees extrapolate poorly beyond observed target ranges. |
| 9 | 3 | Missing direction is learned locally at a node. Going right does not imply that the unknown feature is numerically above the threshold. The same route can lead to different downstream leaves. |
| 10 | 3 | A surrogate predicts the primary split's branch assignment, not the original target. Distinguish classical surrogate routing from learned default directions. Neither is automatic in every tree implementation. |
| 11 | 2 | Discuss a near tie between root candidates. Small sample perturbations can change the entire subtree, motivating variance reduction. |
| 12 | 3 | Separate resampling rows per tree from choosing a feature subset per node. Trees can grow deeply subject to implementation settings. For scikit-learn classification, average class probabilities and then take argmax. |
| 13 | 2 | Ask what happens when one predictor is always the best root split. Random feature subsets allow other useful predictors to contribute. |
| 14 | 3 | Derive the variance of an average using B variance terms and B(B-1) covariance terms. The model assumes equal variances and equal pairwise correlations at a fixed x over repetitions of the training experiment. It is an explanatory model, not an exact description of every forest. |
| 15 | 3 | Trace sample A through the inclusion matrix. The sample may appear in many trees and still have valid OOB predictions from the others. An OOB average requires at least one eligible tree. |
| 16 | 2 | Distinguish total draws across the forest from draws per tree. Derive the exclusion probability, then its exponential approximation. The m > n rows illustrate alternative sampling schemes; not every library exposes them. |
| 17 | 2 | Ask which forecasting inputs would be available before the decision. Distinguish a recent publication from the dates of its observations. |
| 18 | 2 | Read the chart as a within-protocol comparison. Discuss whether the near tie between flexible models supports a universal winner claim. |
| 19 | 2 | Recall AdaBoost's sequential construction. Here, a differentiable loss supplies derivative statistics for the next learner. |
| 20 | 2 | Demonstrate unregularized residual fitting. Keep the correction separate from the updated ensemble prediction. |
| 21 | 2 | Define the score carefully: a response prediction for squared loss, a logit for binary cross-entropy. The sigmoid is applied after summing trees. |
| 22 | 2 | Fix the existing ensemble. Optimize a new tree's partition and leaf values. These formulas use an unshrunk proposal; learning-rate shrinkage follows. |
| 23 | 3 | Expand around the current score. Drop constants only with respect to the new tree. The Taylor approximation is exact for the quadratic loss but generally approximate for logistic loss. |
| 24 | 1 | Verify the two derivative pairs. Both the current scores and the derivatives remain fixed while the current tree is grown. |
| 25 | 3 | Differentiate the scalar quadratic. Define every subscript: v is a leaf; Iv is its sample set; Gv and Hv are sums. In the scalar L2 formulation, this closes the leaf-value optimization. |
| 26 | 3 | Substitute optimal leaf values into parent and child objectives. Show why there is one additional leaf and therefore one gamma penalty. The displayed gain already subtracts gamma. |
| 27 | 2 | Explicitly restart from scores 5: this is not the next round after slide 20. Now lambda=1 and gamma=0. Compute one positive and one negative gradient aloud. |
| 28 | 3 | Pause before revealing why 2.5 is the best threshold. Check that each child has H=2 and G of opposite sign. Both the structure and leaf corrections have now been determined. |
| 29 | 1 | Apply eta=.3 to get corrections of +/-0.7. New scores are still imperfect, which motivates additional rounds. |
| 30 | 2 | Reset to a different, explicitly binary example: current logit 0, probability .5, lambda=0. A positive leaf increases positive-class probability. Its value is neither a class label nor a probability. |
| 31 | 1 | Reassemble one full boosting round. Earlier trees stay fixed. In classification, use current logits to recompute probabilities and derivatives for the next round. |
| 32 | 2 | Explain that min_child_weight is a sum of Hessians. It equals a sample count only for the stated squared-loss setup without additional weights. Fit the number of rounds using validation, not the final test. |
| 33 | 1 | Identify the prediction unit and the patient-level split before discussing any reported metric. |
| 34 | 2 | Explain that ranking metrics, calibration, and decision consequences answer different questions. A retrospective comparison is not an outcome trial. |
| 35 | 1 | Show the role of structured features inside a larger deployed workflow; human review remains part of the system. |
| 36 | 2 | Compare training strategies and aggregation. Avoid implying that any one method is best on every structured dataset. |
| 37 | 2 | Use the two questions and the nonlinear probability-change follow-up below. |

Total: 80 minutes. If discussion runs long, move the surrogate details or the production-workflow slide to follow-up reading; preserve time for the gain calculation.

## Answers to the final questions

1. Only the 30 trees that did not train on the sample may contribute to its OOB prediction. Their predictions are combined and compared with its target.
2. With a positive learning rate eta, the leaf changes the logit by -0.8 eta, so the positive-class probability decreases. Two samples that reach the same leaf receive the same logit increment, but generally different probability increments because sigmoid is nonlinear. Their previous ensemble scores can differ even when the new tree places them in the same leaf.

## Additional mathematical qualifications

- Numerical features use axis-aligned thresholds here. Categorical splits and more general tree structures are outside the main lecture.
- A forest's bootstrap samples are drawn independently conditional on the observed training set. The variance illustration also reflects variation across possible training data; do not confuse this with saying that independently seeded algorithms must have conditionally correlated outputs.
- OOB is a useful internal assessment under suitable sampling assumptions. It is not claimed to be an exactly unbiased estimate for every forest, dataset, or tuning procedure.
- The XGBoost derivation uses scalar leaves, a smooth loss, and an L2 leaf penalty. L1 penalties, sample weights, output constraints, ranking objectives, multiclass Hessian approximations, and vector leaves require modified formulas or additional bookkeeping.
- The basic teaching description searches useful local splits. Actual grow/prune ordering and depth-wise versus loss-guided expansion depend on the configured tree method.
- A direction for previously unseen missingness must use an implementation-specific fallback. Native support should be verified for the selected estimator, objective, and settings.

## Appendix guide

| Slide | Use |
|---|---|
| 38 | Divider marking the end of the timed lecture. |
| 39 | Practical model evaluation and leakage discussion. |
| 40 | Connect second-order boosting to weighted least squares on Newton pseudo-targets. |
| 41 | Extend the scalar-logit picture to multiclass scores and softmax. |
| 42 | Explain histogram search and how missing G/H statistics enter a candidate split. |
| 43 | Derive the chance that a sample has no OOB tree. |
| 44 | Optional operational comparison; discuss why different thresholds and unmatched comparator sensitivity limit its interpretation. |

## Presenting the reveals

Advance one PDF page at a time during a derivation or worked example. Allow students to calculate before revealing the next step. Space is reserved for hidden content, so equations and diagrams stay in place as the explanation develops. Use the static handout when distributing complete slides for reading or printing.
