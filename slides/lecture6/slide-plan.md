# Final slide map: From weak models to strong predictors

52 logical slides; 72 presentation pages; 52 handout pages. Six transition slides are included. The optional GLM frame is excluded. Detailed plans: adaboost-plan.md, boosting-plan.md, foundations-plan.md, transition-plan.md and PLAN.md.

| Slide | Title | Module | Figure / layout | Reveal |
|---:|---|---|---|---|
| 1 | Ensemble Learning | `intro.tex` | Native text / equations / diagram | Static |
| 2 | From one score to a sum of rules | `intro.tex` | Native text / equations / diagram | Staged |
| 3 | Learning Goals | `intro.tex` | Native text / equations / diagram | Static |
| 4 | Where do ensembles become useful? | `case-roadmap.tex` | Native text / equations / diagram | Static |
| 5 | Phase 1: AdaBoost | `transition-01-adaboost.tex` | Native text / equations / diagram | Static |
| 6 | Can Weak Rules Work Together? | `adaboost.tex` | adaboost-stump | Staged |
| 7 | Two Kinds of Weight | `adaboost.tex` | Native text / equations / diagram | Static |
| 8 | AdaBoost: The Algorithm | `adaboost.tex` | Native text / equations / diagram | Static |
| 9 | One Update, New Weights | `adaboost.tex` | adaboost-weights | Static |
| 10 | Three Stumps, One Classifier | `adaboost.tex` | adaboost-votes | Static |
| 11 | Phase 2: Why AdaBoost Works | `transition-02-theory.tex` | Native text / equations / diagram | Static |
| 12 | A Loss for the Accumulated Vote | `adaboost.tex` | adaboost-margin | Static |
| 13 | Stagewise Fitting and Weights | `adaboost.tex` | Native text / equations / diagram | Staged |
| 14 | Choosing a Weak Learner | `adaboost.tex` | Native text / equations / diagram | Staged |
| 15 | Deriving the Vote Weight | `adaboost.tex` | Native text / equations / diagram | Staged |
| 16 | Why Mistakes Receive More Weight | `adaboost.tex` | Native text / equations / diagram | Staged |
| 17 | Bounding the Training Error | `adaboost.tex` | Native text / equations / diagram | Staged |
| 18 | When Labels Are Wrong | `adaboost.tex` | adaboost-loss-comparison | Static |
| 19 | Back to Logistic Regression | `adaboost.tex` | Native text / equations / diagram | Staged |
| 20 | Movie ratings: two views of taste | `case-recommendations.tex` | case-recommendations-pipeline | Staged |
| 21 | A blend improves rating prediction | `case-recommendations.tex` | case-recommendations-results | Static |
| 22 | Phase 3: Learning a Correction | `transition-03-residuals.tex` | Native text / equations / diagram | Static |
| 23 | Keep the model; learn a correction | `boosting.tex` | Native text / equations / diagram | Staged |
| 24 | One correction lowers squared error | `boosting.tex` | boosting-residual | Staged |
| 25 | Correct what the previous model missed | `boosting.tex` | boosting-rounds | Static |
| 26 | Why squared loss leads to residuals | `boosting.tex` | Native text / equations / diagram | Staged |
| 27 | Gradient descent in prediction space | `boosting.tex` | Native text / equations / diagram | Staged |
| 28 | The gradient boosting algorithm | `boosting.tex` | Native text / equations / diagram | Static |
| 29 | Classification still uses the logistic loss | `boosting.tex` | Native text / equations / diagram | Staged |
| 30 | Simple corrections build a flexible fit | `boosting.tex` | boosting-fit | Static |
| 31 | Use validation to choose when to stop | `boosting.tex` | boosting-loss | Static |
| 32 | Ad clicks: learn features with trees | `case-clicks.tex` | case-clicks-pipeline | Staged |
| 33 | Does the hybrid predict clicks better? | `case-clicks.tex` | case-clicks-results | Static |
| 34 | Forecast electricity demand | `case-load.tex` | case-load-pipeline | Staged |
| 35 | What is known when we predict? | `case-load.tex` | case-load-timeline | Static |
| 36 | Phase 4: A Brief Look at Trees | `transition-04-trees.tex` | Native text / equations / diagram | Static |
| 37 | A tree predicts within regions | `foundations.tex` | foundations-partition | Static |
| 38 | Choose a split by reducing error | `foundations.tex` | Native text / equations / diagram | Static |
| 39 | Deep trees can be unstable | `foundations.tex` | foundations-depth-error, foundations-bootstrap | Staged |
| 40 | Phase 5: Bagging | `transition-05-bagging.tex` | Native text / equations / diagram | Static |
| 41 | Bagging averages bootstrap fits | `foundations.tex` | Native text / equations / diagram | Static |
| 42 | Why averaging can reduce variance | `foundations.tex` | Native text / equations / diagram | Staged |
| 43 | Correlation limits the benefit | `foundations.tex` | foundations-correlation | Static |
| 44 | Phase 6: Random Forests | `transition-06-forests.tex` | Native text / equations / diagram | Static |
| 45 | Random forests vary each split | `foundations.tex` | Native text / equations / diagram | Static |
| 46 | Out-of-bag prediction | `foundations.tex` | Native text / equations / diagram | Static |
| 47 | Two ways to build a stronger predictor | `foundations.tex` | Native text / equations / diagram | Static |
| 48 | Kinect: trees recognize body parts | `case-forests.tex` | case-kinect-pipeline | Staged |
| 49 | From tree probabilities to joint positions | `case-forests.tex` | case-kinect-forest | Static |
| 50 | How do the models work together? | `closing.tex` | Native text / equations / diagram | Static |
| 51 | References and further reading | `closing.tex` | Native text / equations / diagram | Static |
| 52 | Sources for the application cases | `case-references.tex` | Native text / equations / diagram | Static |
