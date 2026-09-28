# Ensemble lecture revision

User feedback: skip GLM or mention it very briefly; transition from linear/logistic regression through weak models to stronger models; begin with AdaBoost, then theory; explain residual learning; briefly introduce trees immediately before bagging. Preserve four sourced applications and exclude XGBoost.

Audience: graduate COMP 5212 students who know linear/logistic regression, MLE, and gradients. Format: English Beamer source and PDF presentation/handout, exact existing theme. Core route approximately90 minutes; complete detailed route110-120minutes.

Sequence and slide jobs:
1. Title: From weak models to strong predictors.
2. Linear/logistic recap: replace one fixed score with a learned sum; no GLM prerequisite.
3. Learning goals and route: AdaBoost behavior, derivation/guarantee, residual and gradient boosting, brief trees, bagging/forests.
4. Application roadmap: recommendations, clicks, electricity, Kinect in teaching order.
5 onward. AdaBoost behavior before derivation: one-split rule illustration, algorithm/weights, two numerical example frames, margin loss, stagewise fitting, h selection, alpha derivation, D update, training bound, limitations, logistic connection. Exact map owned by AdaBoost module plan.
Next. Recommendation-system case after AdaBoost.
Next. Residual boosting with regression example, repeated correction plot, squared-loss derivation, functional gradient, generic algorithm, logistic residuals, validation. Exact map owned by boosting module plan.
Next. Click and load cases4frames.
Next. Brief decision trees3frames: regions, how splits chosen/classification extension, capacity/instability. Bagging/resampling, variance algebra, correlation, random forests, OOB, comparison. Exact map owned by foundations plan.
Next. Kinect2frames.
Final. Method comparison and references.
Optional GLM bridge as standalone one-frame input in main.tex, excluded by default; covers conditional distribution/link only, no GLM derivation.

Visual rules: retain theme/macros byte-for-byte, all equations native LaTeX, all figures editable. Existing measured case data/source scope preserved. All illustrative data explicitly constructed. Check every rendered overlay and handout, source packaging portability.

Final frame-by-frame ordering: see slide-plan.md.

## Latest revision

# Recommendation case and phase transitions

User request: replace the facial-recognition example with another practical example, preferably recommendations; add a transition page before the next phase. Interpret the target as the two Viola-Jones face-detection slides. Retain Kinect body-pose example, all mathematics, and existing style.

Format and audience: graduate COMP5212, English LaTeX Beamer. Planned final size: 52 logical slides/72 presentation pages, including six phase transitions; previous size: 46 logical slides/66 pages. Presentation and complete handout; full source ZIP.

Replacement: two sourced Netflix recommendation-system frames. The official Netflix 2012 article reports SVD 0.8914, RBM 0.8990, linear blend 0.88 RMSE; it reports adapting both algorithms for production. Explicitly a broader ensemble application, not a claim it uses AdaBoost. Include pipeline, simple prediction-blending equation and reported results with evaluation scope. Do not create invented measurements. Remove face-case sources/figures/CSV rows from new package; update roadmap, references, transitions, notes, and README.

Six short, static phase transitions, each one teaching question and next objective, same approved theme:
1. Before AdaBoost: imperfect threshold rules -> stronger classifier.
2. Between numerical AdaBoost example and loss derivation: which objective produces the weights?
3. Before residual/gradient boosting: what correction should be learned next?
4. Before three-frame tree primer: how does a fitted rule become a tree?
5. After tree instability and before bagging: can averaging stabilize predictions?
6. After correlation and before random forests: how can the trees become less correlated?

All inserts have speaker notes; phase numbers1-6. Keep previous case and derivation source facts. Full final source and every rendered physical page to be checked; handout must match final reveal. Package rebuilt from a fresh extraction.
