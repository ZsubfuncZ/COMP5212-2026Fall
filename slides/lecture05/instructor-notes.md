# Instructor notes

51 logical slides. Notes are also embedded in the Beamer source.

Full route: about 90–110 minutes. A roughly 60-minute route omits slides 5, 9, 12, 17, 18, 22, 27, 30, 32, 33, 35, 44, 46, and 47.

## 1. Logistic Regression

This lecture follows linear regression. The sequence is motivation, binary problem formulation, maximum likelihood for Gaussian and Bernoulli responses, gradient descent, and multiclass softmax. All plotted samples and numerical examples are constructed for teaching. Full delivery is about 90 minutes; the README includes a shorter route.

## 2. Learning Goals

Use these goals as the map. Students already know least squares and basic matrix derivatives; connect each new expression to those earlier ideas. The final application distinguishes class probabilities from attention weights.

## 3. Same inputs, a different prediction

Pause before revealing the right-hand probability. Reuse the manufacturing setting from the linear-regression lecture: the inputs can be similar even though the output is now an event. This changes the conditional response model and the fitting criterion.

## 4. Motivation: detecting defective parts

Ask students whether the next part must have the same label as its nearest neighbor. The overlap motivates a probability rather than a deterministic physical rule. The sensor is only one available feature; temperature, vibration and machine age could also be included. This is a realistic application setting, but the observations are deliberately constructed, not an industrial dataset. Do not imply the association is causal.

## 5. Probabilities and decisions

The two probabilities are hypothetical. A binary flag discards the difference between 55 percent and 95 percent risk. Ask which part should be inspected first when only one inspection slot is available and costs are otherwise equal. The decision threshold can be selected according to the application; this lecture focuses on fitting the probabilities. A numerical probability is useful only to the extent that it agrees with the data-generating distribution; logistic form alone does not guarantee calibration.

## 6. OLS with binary responses

Avoid claiming that least squares cannot be applied to binary outcomes or that it requires Gaussian responses simply to define an estimator. The issue shown here is the unrestricted linear probability model: its predictions can leave the unit interval, and the Bernoulli conditional variance changes with the mean. Squared probability error is itself a valid proper scoring rule; the Bernoulli likelihood motivates the cross-entropy used in this lecture. The OLS line is computed from the same constructed data as the motivation plot.

## 7. The logistic function

Ask students to identify the score for probability one half and the scores needed for probabilities near zero or one. Derive the derivative by differentiating (1+exp(-z)) inverse. Its maximum is one quarter at zero, and it becomes small in either tail. This saturation will matter for curvature in gradient-based optimization. The logistic function is a modeling choice, not the only possible link for binary probabilities.

## 8. A linear model for log-odds

The transformation turns a probability in (0,1) into any real number, making an additive linear model possible. Stress that this is an assumption about conditional log-odds, not a theorem that every binary dataset must satisfy. Local linear approximation to a smooth log-odds function is one motivation for a useful baseline. Feature expansion can make the log-odds nonlinear in the original measurements while preserving linearity in the fitted coefficients.

## 9. Why start with a linear score?

This is a local first-order approximation, not a statement that the true response is exactly logistic. It requires smooth log-odds and probabilities away from zero and one near the expansion point. The unknown scale over which linearity is reasonable motivates trying the model, then assessing error and considering transformed features.

## 10. Model and notation

This reuses the linear-regression notation: theta includes the intercept and X includes a constant column. The symbol p is a dimension; pi denotes a probability, preventing the common collision of p as both dimension and fitted probability. Later expressions s(X theta) apply the logistic function elementwise. Conditioning on the inputs is implicit in the likelihood. No full-rank condition is needed just to define this model or its loss.

## 11. Decision thresholds and boundaries

The figure uses score -1+x1+0.8x2, with constructed class labels. Since the logistic function is strictly increasing, taking the logit of the threshold yields the displayed inequality. For fixed linear features and nonzero w, the boundary is a hyperplane. Raising the threshold shrinks the region classified as positive. This plot illustrates fixed-model decisions, not estimates fitted to the shown points.

## 12. Worked example: score to decision

Give students 20 seconds for the table, then reveal it. Pause again before the threshold calculation. Distinguish the raw measurement x, the real-valued score z, the probability pi and the binary decision. The threshold is an application choice separate from the model parameters. At exactly the boundary, the chosen greater-than-or-equal convention predicts class one.

## 13. What do we learn from the data?

The probability model has been specified; the fitting criterion is still to be derived. Accuracy alone treats probability .51 and .99 the same for a positive label. Likelihood provides a differentiable probability-based criterion. An argmin is a useful formulation here, but the separation caveat later explains when no finite unregularized optimizer exists.

## 14. What does conditional likelihood measure?

The same expression has two roles. As a sampling model, theta is fixed and y varies; as a likelihood, the observed y is fixed and theta varies. We condition on the inputs, so we do not need a probability model for X to define this criterion. The displayed factorization assumes conditionally independent responses and that each response distribution depends on X through its own feature vector. For a continuous response, f is a density, not the probability of observing an exact real number. A likelihood is also not a probability distribution over theta. We first revisit Gaussian linear regression, then return to the binary response model.

## 15. Gaussian errors assign density to residuals

We temporarily change the response family to revisit linear regression; this slide is not a Gaussian model for a binary variable. Conditional on the design, the errors are independent and identically distributed with mean zero and the same positive variance. Consequently the responses are independent but generally have different conditional means. The plotted curve is the analytic standard normal density, so sigma equals one in the illustration. The marked residuals zero and two have densities about 0.399 and 0.054. These are density heights, not point probabilities; the area over an interval gives a probability. The Gaussian assumption is what connects this particular likelihood calculation to squared residuals.

## 16. The Gaussian likelihood leads to squared error

Take the negative logarithm one factor at a time. The exponential contributes the squared residual divided by twice the variance, and the normalizing factors contribute n/2 times log(2 pi sigma squared). At any fixed positive sigma, the first term is constant in theta and the second has a positive scale, so the minimizers are exactly the least-squares solutions. If sigma is also estimated and the minimum SSE is positive, the joint Gaussian MLE has a least-squares coefficient vector and variance SSE/n. If the data can be fit exactly, the likelihood becomes unbounded as sigma approaches zero, so a joint finite MLE with strictly positive variance need not exist. We keep sigma fixed here to isolate the coefficient argument.

## 17. Differentiating gives the normal equations

The factor one over two n changes the scale of the objective but not its unpenalized minimizers. Expand the squared norm, noting that the two cross terms are the same scalar. The derivative of theta transpose A theta is twice A theta when A is symmetric; here A is X transpose X. Setting the gradient to zero gives the normal equations. The Hessian is X transpose X divided by n and is positive semidefinite, so stationarity is sufficient for global optimality. This conclusion does not require X to have full column rank, and it does not require Gaussian errors: it is a property of the least-squares objective itself.

## 18. Are the least-squares coefficients unique?

The inverse formula is a mathematical expression, not a recommendation to form a matrix inverse numerically. QR or SVD is preferable for computation, especially when the design is ill-conditioned. Full column rank requires n at least p. When the design is rank deficient, adding any vector in its null space leaves every fitted response unchanged. The Moore--Penrose solution lies in the row space of X and is orthogonal to that null space, making it the unique solution with smallest Euclidean norm. In the fixed-variance Gaussian model, all these least-squares solutions also maximize the likelihood; likelihood alone does not select the minimum-norm member.

## 19. The probability of an observed binary label

We now return to the binary labels and logistic mean model introduced earlier. Ask the audience to check the exponents separately for y equal to zero and one. Pi is always the probability of class one; it is not always the probability of the label we actually observed. A negative label receives probability one minus pi. The Bernoulli model specifies conditional variance pi times one minus pi, so there is no separate constant residual variance parameter analogous to sigma squared. The logistic link was already chosen as a model for the mean; the Bernoulli likelihood by itself does not determine that link.

## 20. Bernoulli likelihood and binary cross-entropy

Independence is the step that makes the joint probability a product. Because log is strictly increasing, maximizing the product and maximizing its log have the same optimizers when they exist. Negating converts a maximization into a minimization; dividing by n yields the mean loss used in the optimization section. The division changes gradient scale and must be coordinated with a penalty coefficient when a regularizer is added. Products of many probabilities may underflow numerically, another reason to work with log-likelihoods. Calling this maximum likelihood does not guarantee a finite maximizer: separation can send coefficient magnitudes to infinity. That existence issue is examined later.

## 21. Express the same loss through the score

Use pi equal to exp(z) divided by one plus exp(z), and one minus pi equal to one divided by one plus exp(z), to obtain the two log identities. After substitution, the coefficients multiplying softplus are y and one minus y, so they add to one. This form will make the derivative particularly simple in the next module. It is exactly the earlier Bernoulli loss composed with the logistic link, not a different statistical criterion. The literal evaluation log(1+exp(z)) can overflow. A stable implementation uses max(z,0)-y z+log1p(exp(-abs(z))) or a library binary-cross-entropy-with-logits routine. The displayed formula is for the mathematical derivation.

## 22. Which probabilities enter the likelihood?

These probabilities are constructed for arithmetic practice, not estimated from an empirical dataset. Before revealing the last column, ask which factor should be used for the second observation. The correct factor is 0.3, not 0.7. The individual negative log-likelihoods are approximately 0.2231, 1.2040, and 0.9163, which sum to 2.3434 and average to 0.7811. No thresholded prediction enters this calculation. A probability of 0.4 for a positive label contributes a finite loss even if a threshold of one half would classify it incorrectly. Changing the decision threshold cannot change this likelihood when the fitted probabilities are held fixed.

## 23. Response models and their fitting losses

The loss row suppresses positive scale factors and parameter-independent terms from the fixed-variance Gaussian negative log-likelihood. The two choices in a conditional regression model are a response family and a model for its mean. A Bernoulli family combined with a probit mean, for example, is also fit by maximum likelihood but is not logistic regression. Conversely, least squares is an optimization criterion that remains defined without Gaussian noise, including when applied to binary observations. Its statistical properties then depend on the assumptions appropriate to that setting. The Gaussian assumptions in this module explain a likelihood interpretation of least squares; they are not prerequisites for writing or solving the OLS problem. Next we differentiate the logistic objective and examine how to optimize it.

## 24. A confident mistake incurs a large loss

This is loss as a function of a single predicted probability. It is different from the later optimization curve, which shows average loss against iteration. For a positive label the loss diverges as its assigned probability approaches zero; the negative-label curve is reflected horizontally. The curves are analytical and the numerical examples use natural logs.

## 25. The derivative becomes a prediction residual

Pause before multiplying the two derivatives. The sigmoid derivative cancels the denominators introduced by the Bernoulli log loss. For a positive example with low probability, pi minus y is negative, so descent tends to increase its score. Do not add another sigmoid-derivative factor after this cancellation. All expressions are for finite scores.

## 26. From one observation to the whole sample

Least squares in this table uses SSE divided by 2n; logistic regression uses mean binary cross-entropy without a factor of one half. The algebraic pattern is the same, but the predictions and curvature differ. The intercept is already represented by the first column of X.

## 27. The logistic objective is convex

D has strictly positive diagonal entries at finite scores, so a full-column-rank X gives a positive-definite Hessian there. Curvature can nevertheless approach zero as scores diverge. Later the two-point separation example shows a strictly convex objective with an unattained infimum. Feature scaling and near-collinearity still influence optimization.

## 28. Gradient descent for logistic regression

This is full-batch gradient descent. Each update costs O(np) and does not require a matrix inverse. At zero initialization all binary probabilities equal one half. For large datasets one can replace the full gradient by a mini-batch average, producing stochastic rather than necessarily monotone loss traces. Fit any feature scaling on training data only.

## 29. One gradient step by hand

Pause before the numerical gradient. Average the residuals (.5,.5,-.5) to get 1/6. Average x times residual to get -1/3. At the new parameters, the three scores are (-.5,-1/6,1/6). The loss is computed using natural logarithms. This three-point example is separable and is only used to show one update; the following convergence experiment uses the earlier 20-point overlapping sample.

## 30. How large can the learning rate be?

The norm of X is its spectral norm, so its square is the largest eigenvalue of X transpose X. The displayed descent inequality follows from the smoothness bound with g equal to the gradient. The inequality also gives descent for 0<eta<2/Lbar, but eta at most 1/Lbar is a simple conservative rule. This bound concerns the unregularized mean BCE objective; adding a slope ridge penalty changes the bound. Backtracking is a practical alternative.

## 31. Loss curves: the step size changes the trajectory

This figure is generated by examples/generate_optimization.py, not drawn by hand. The rates are .1/Lbar, 1/Lbar and 10/Lbar. All use the same fixed 20 observations. The safe rate decreases the loss from .693147 to .411371; the very large rate oscillates. A rate above the sufficient bound need not diverge on every dataset, so describe the observed oscillation rather than asserting a universal outcome. This is a training loss curve and does not by itself establish generalization.

## 32. Gradient descent moves across loss contours

All contour coordinates are computed from the actual mean BCE of the fixed defect sample. They are not arbitrary ellipses. The script solves for points on five loss levels and checks their objective residuals. The star marks the independently computed optimum. The feature is still (raw intensity minus five)/two, and the axes are intercept and slope in these coordinates.

## 33. The optimized score gives a probability curve

The fit is the converged gradient-descent solution for the same 20-point dataset. An independent Newton computation supplies a high-accuracy reference, and the script checks agreement; Newton is not a required lecture topic. The observations are constructed. The sensor feature scaling is explicit because it determines both the coefficient units and the safe learning-rate bound.

## 34. Separable data can send the MLE to infinity

This simple full-rank two-observation example is completely separable. The infimum is zero but no finite unregularized maximum-likelihood estimate exists. For this example adding lambda w squared over two with lambda>0 yields a finite optimum. In general an unpenalized intercept can still diverge when only one class is observed. Near separation also leads to weak curvature.

## 35. Evaluate the loss without overflow

The algebraic identity avoids exponentiating a large positive score. A stable sigmoid uses 1/(1+exp(-z)) for z>=0 and exp(z)/(1+exp(z)) for z<0. Standardization must use training statistics. The analogous softmax implementation subtracts the largest logit before exponentiating, which is introduced in the next section.

## 36. One item, one defect label

This is a constructed inspection task, not an empirical dataset. The label policy selects one primary defect even if several physical defects could coexist. If the task instead records every defect present, it becomes a multilabel problem and the categorical model here no longer expresses that target. Ask students what information is lost by collapsing all three labels into defective versus nondefective. Reference for the categorical setup: CS229 notes, Section 2.3, <https://cs229.stanford.edu/main_notes.pdf>.

## 37. One linear score for each class

The raw feature vector is x. Its augmented vector is tilde x, with a leading one. Each row of X is the transpose of an augmented vector, so the first column of X consists of ones and the first row of W holds the K intercepts. This orientation matters later: X transposed times a matrix of probability residuals has exactly the same p by K shape as W. A logit is an unrestricted real score. It becomes a log odds only after taking a difference between two class scores. Source: CS229 notes, Section 2.3, <https://cs229.stanford.edu/main_notes.pdf>.

## 38. Softmax probabilities

Exponentiation preserves score ordering, and the common positive denominator preserves it again. The displayed decision rule minimizes expected zero-one loss under the model, with a fixed rule for ties. Different error costs can require a different decision rule. Contrast the shared denominator with independently fitted binary probabilities: K independent sigmoid outputs need not sum to one. Source: CS229 notes, Section 2.3, <https://cs229.stanford.edu/main_notes.pdf>.

## 39. Three scores, three probabilities

These values come directly from the analytical softmax formula and are rounded only for display. The exact probabilities are approximately 0.665240956, 0.244728471, and 0.090030573. Scratch is the predicted class, but the other classes retain positive probability. A ratio such as pi1 divided by pi2 equals exp(2 minus 1), without needing the normalizing constant. The example is original. Formula reference: <https://cs229.stanford.edu/main_notes.pdf>, Section 2.3.

## 40. Categorical likelihood

Condition on the observed design X. The one-hot vector contains exactly one entry equal to one, so each categorical likelihood term reduces to the probability assigned to the observed class. The argmax notation describes the maximum-likelihood objective. A finite maximizer can fail to exist on separable data, as in binary logistic regression, and the unrestricted K-column parameterization has a common-shift ambiguity discussed shortly. No optimization algorithm is introduced here. Source: CS229 notes, Section 2.3, <https://cs229.stanford.edu/main_notes.pdf>.

## 41. Cross-entropy and log-sum-exp

Substitute log P_ik equals z_ik minus log-sum-exp of the row. Since the one-hot row sums to one, the normalization term appears once, leaving LSE(z) minus the true class score. Natural logarithms measure the loss in nats. For the same logits, the losses for Scratch, Dent, and Stain are about 0.407606, 1.407606, and 2.407606. The example illustrates that the probability of the observed label controls the loss even when the predicted label stays unchanged. Source: CS229 notes, Section 2.3, <https://cs229.stanford.edu/main_notes.pdf>.

## 42. The gradient is a probability residual

Differentiate log-sum-exp to obtain softmax, then differentiate minus the selected score to obtain minus the one-hot target. Apply the chain rule to z_ik equals augmented tilde x_i transposed w_k and average across observations. The design X has those augmented feature vectors as rows. This gives the displayed p by K matrix without a transposition ambiguity. Because each row of P minus Y sums to zero, the gradient columns also sum to zero. That identity foreshadows the common-shift invariance. The formula is for the unregularized mean negative log-likelihood. Source: CS229 notes, equations 2.16--2.19, <https://cs229.stanford.edu/main_notes.pdf>.

## 43. Binary logistic regression is the $K=2$ case

For the binary comparison, map class 1 to binary target one and class 2 to binary target zero. The binary coefficient vector is the difference w1 minus w2. Setting w2 to zero recovers the familiar single-vector logistic parameterization. For K classes, a single logit has no absolute probabilistic meaning. Its difference from another logit specifies their log probability ratio. These identities are algebraic consequences of softmax. Background definitions: <https://cs229.stanford.edu/main_notes.pdf>, Sections 2.1 and 2.3.

## 44. A reference class removes redundant parameters

The common factor exp(c) cancels in numerator and denominator. At parameter level, replacing W by W plus a times the all-ones row adds c(x)=tilde x transposed a to every score for that input. Here tilde x is the augmented feature vector. Subtracting w_K from all columns therefore preserves the entire conditional distribution. A sum-to-zero constraint is another possible convention. Additional data conditions are needed for a unique finite maximum-likelihood solution. A penalty can select a representative, so a penalty specified in one parameterization must be transformed carefully before claiming equivalence to another. The proof here is direct algebra from the softmax definition in <https://cs229.stanford.edu/main_notes.pdf>.

## 45. Stable computation uses score differences

This is a numerical use of common-shift invariance, distinct from choosing a fixed baseline class to parameterize the model. Large negative shifted logits can underflow to zero, but the denominator still contains a one. Computing the log-likelihood directly in the displayed form retains a finite loss for ordinary finite logits even when a tiny probability would round to zero. Prefer a library's fused log-softmax or cross-entropy operation. The subtract-maximum procedure is described in Bengio et al., A Neural Probabilistic Language Model, page 1146, <https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf>.

## 46. Three classes partition the feature plane

The regions are analytical, not estimated from a dataset. Class 1 wins when u1 is at least u2 and at least zero. Class 2 wins when u2 is at least u1 and at least zero. Class 3 wins when both features are nonpositive. A pairwise equality line is an actual decision boundary only where those tied classes achieve the largest score. For example, the negative part of u1 equals u2 lies inside class 3 and is not a boundary. The geometry is linear in the chosen features. A nonlinear learned feature map can yield curved boundaries in the original inputs. Reference for the underlying logits: <https://cs229.stanford.edu/main_notes.pdf>.

## 47. Temperature changes concentration

The graph fixes z=(2,1,0). As T tends to infinity the distribution approaches uniform. As T tends to zero from above it concentrates on the unique maximum here; tied maxima would share the limiting mass. Positive temperature preserves all score orderings, although it changes sampling behavior. Calibration concerns whether predicted probabilities match observed frequencies over data, not how uncertain one output looks. A temperature chosen to minimize held-out negative log-likelihood is a fitted calibration method, with generalization assessed separately. Source: Guo et al., On Calibration of Modern Neural Networks, Section 4, <https://proceedings.mlr.press/v70/guo17a/guo17a.pdf>.

## 48. Categorical outputs in vision and language

A neural classifier can learn h jointly with its linear output layer. Its final softmax has the categorical likelihood studied here, while the full model can be nonlinear in the original input. AlexNet's 1000-way output and multinomial logistic objective are described in Section 3.5: <https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf>. Neural language models also use a categorical output distribution, historically over words and now often over subword tokens. Bengio et al. give the softmax output and corpus log-likelihood on page 1142: <https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf>. The Transformer's decoder-output softmax appears in Section 3.4: <https://arxiv.org/html/1706.03762v7>. The sequence factorization conditions on preceding tokens; it does not assume the tokens themselves are independent.

## 49. Softmax also supplies attention weights

For each query, softmax normalizes compatibility scores across available key positions. The resulting row weights mix value vectors. In the displayed equation, K_key denotes the key matrix, distinct from the number K of output classes, and d_k is the key dimension. Without dropout, and with at least one allowed key, each attention row sums to one. Causal masks remove forbidden positions before normalization. The standard attention layer does not assign a categorical target label to each query and train that row with the supervised label likelihood derived earlier. The output layer can separately use a softmax over vocabulary with a token likelihood. Source: Vaswani et al., Attention Is All You Need, Sections 3.2.1 and 3.4, <https://arxiv.org/html/1706.03762v7>; canonical paper record: <https://arxiv.org/abs/1706.03762>.

## 50. One fitting principle, three response models

The Gaussian row assumes fixed positive homoscedastic variance and suppresses terms and positive scales that do not affect the coefficient optimum. Logistic and softmax models need a chosen score/feature model in addition to the response family. Likelihood fitting, numerical optimization, and decision making are distinct parts of the pipeline. Close by tracing one example from input to score, probability, loss, and update.

## 51. References and further reading

All titles are clickable in the PDF. The source package records the exact primary-source URLs and sections used. Every plotted observation, curve, and worked number in this lecture is either an explicit analytical construction or a reproducible computation on constructed teaching data. No figure is presented as a measured industrial performance result. The Gaussian/logistic derivations also follow the earlier 2022 CS229 notes, <https://cs229.stanford.edu/notes2022fall/main_notes.pdf>.
