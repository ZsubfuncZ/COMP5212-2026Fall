# AdaBoost module plan — behavior before derivation

Audience: graduate machine learning students continuing from linear and logistic regression. No GLM, decision-tree, or bagging prerequisite. Target: 30–35 minutes within the ensemble lecture. Preserve the approved theme and the original reproducible eight-point example. Explain a decision stump as a threshold rule; defer the general decision-tree lesson until before bagging.

Narrative: first see how a sequence of limited rules produces a better vote; then derive the rule weights and observation weights from exponential loss; then state precisely what the training guarantee does and does not establish. Residual fitting and gradient boosting follow.

| Frame | Teaching move and evidence | Layout and reveal | Speaker-note emphasis |
|---|---|---|---|
| 1 | A threshold rule misses two of eight points | Large original data/stump plot; reveal next-rule question | Define stump without tree prerequisites; constructed data |
| 2 | Distinguish weights on observations from weights on rules | Two columns, one equation family each; static | D sums to one, alpha is a vote coefficient, F is a score |
| 3 | Present the recipe before proving it | Numbered AdaBoost procedure | Establish edge and stopping cases; derive the formulas later |
| 4 | Two mistakes acquire half the weight | First-round calculations beside D1/D2 bars | Observation weights are not class probabilities |
| 5 | Three threshold rules classify all eight points | Round table, two explicit scores, vote curve | Training success is not test evidence; errors need not decrease every round |
| 6 | Ask which loss produces this recipe | Margin definition and exponential-loss curve | Begin theory after concrete behavior; distinguish a score from probability |
| 7 | Add one rule; normalize old exponential losses | Stagewise factorization; reveal D and Z | Reweighting follows from the criterion |
| 8 | The best positive direction minimizes weighted error | Correct/incorrect partition and monotonicity | Exact greedy choice versus approximate practical learner |
| 9 | Differentiate to find the rule coefficient | Derivative then boxed alpha; reveal | Conditions 0 < epsilon < 1/2; exact unshrunk coefficient |
| 10 | Derive the next distribution | Normalized update, correct/error factors; reveal ratio | Relative weight increases by (1−epsilon)/epsilon |
| 11 | Convert per-round improvement into a conditional guarantee | Product identity and edge bound; reveal | Uniform positive edge on every encountered distribution; training only |
| 12 | Explain noise sensitivity | Exponential/logistic margin-loss comparison | Do not equate falling training loss with good generalization |
| 13 | Connect exponential risk to probability and other losses | Pointwise conditional-risk derivation; reveal | Population optimum, factor two, no finite-model calibration claim |

All 12 original teaching frames and their mathematics are retained, with one new setup frame. The algorithm and both numerical-example frames now precede the loss derivation. Primary sources: Freund and Schapire (1997), Schapire (2003), Friedman, Hastie and Tibshirani (2000). Convention throughout: F=sum(alpha*h), alpha=0.5 log((1−epsilon)/epsilon), binary labels ±1.

Module content counts above exclude the separately authored phase-transition inputs. See slide-plan.md for final global numbering.
