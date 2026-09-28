# Ensemble Learning: From Weak Models to Strong Predictors

English graduate lecture for COMP 5212. The lecture follows linear and logistic regression directly. It assumes gradients and likelihood, with no GLM prerequisite. The approved 16:9 Beamer theme is preserved.

**52 logical slides, 72 presentation pages with staged reveals, 52 handout pages.**

## New teaching sequence

| Slides | Content | Core minutes |
|---|---|---:|
| 1-4 | Regression bridge, goals, real applications | 5 |
| 5-19 | AdaBoost behavior, worked example, derivation and training bound | 27 |
| 20-21 | Netflix recommendation-system prediction blending | 4 |
| 22-31 | Residual correction, gradient interpretation, logistic loss and validation | 22 |
| 32-35 | Ad-click prediction and electricity demand | 8 |
| 36-47 | Brief trees, bagging, variance, random forests | 17 |
| 48-49 | Kinect body-part recognition | 4 |
| 50-52 | Comparison and sources | 3 |

This is a 90-minute core route, not a promise to cover every detail at the same pace. Allow 110-120 minutes for all derivations and application discussion. For the core route, treat the population-risk connection back to logistic regression, detailed correlation numbers, and OOB derivation as reading slides; keep AdaBoost's coefficient/update derivations and the conditional training-error guarantee. Explain the algorithm's behavior before deriving its coefficients. The decision-tree primer comprises the first three content frames of foundations.tex and sits immediately before bagging. Six static transition pages introduce the main phases; use each for a brief pause and next-step question. They are included in the timing allocations.

## Phase transitions

Six editable transition files mark AdaBoost in action, its theory, residual learning, the tree primer, bagging, and random forests. The middle-of-module transitions are included from adaboost.tex and foundations.tex. The slide map and notes reflect this nested order.

## Compile and present

```sh
latexmk -pdf main.tex
latexmk -pdf handout.tex
```

A standard TeX Live / MacTeX / MiKTeX installation is sufficient. For Overleaf, upload this entire folder, select main.tex for staged reveals or handout.tex for one complete page per logical slide. No network, shell escape, external fonts or Python is needed for compilation. All figures are editable native LaTeX. Python scripts only reproduce the constructed examples.

The presentation and handout PDFs are included. Readable speaker notes are in instructor-notes.md; each TeX frame also contains a note. To display notes on a second screen, uncomment the indicated line in main.tex.

## Optional one-minute GLM mention

The default presentation skips GLM. To include the brief distribution/link connection, uncomment this line in main.tex:

```tex
\input{optional-glm.tex}
```

This adds one slide after the opening goals. It does not introduce any GLM derivation or change prerequisites. Recompile both documents; downstream numbers shift by one.

## Evidence and reproducibility

Four primary-source applications: Netflix recommendation-system prediction blending, Facebook ad-click prediction, electricity-demand forecasting, and Kinect body-part recognition. The Netflix case is a broader ensemble application, with historical rating-prediction metrics; its blending procedure is not presented as AdaBoost. Published chart values are in examples/published-case-results.csv. Pipeline figures are explicitly schematic; constructed examples are not presented as empirical benchmarks. Source ledgers document metric and deployment scope.

Run these from this folder to regenerate constructed examples:

```sh
python3 examples/adaboost_example.py
python3 examples/generate_boosting.py
python3 examples/foundations_generate.py
```

## Mathematical conventions

- An ensemble combines multiple models; boosting and bagging are both ensemble strategies.
- AdaBoost uses labels -1/+1, real scores and weighted votes. Observation weights D and learner coefficients alpha are different quantities. Its training-error bound requires positive weighted edges at successive rounds; it does not guarantee test accuracy.
- For squared loss, the negative gradient equals the ordinary residual y-F. Other losses produce pseudo-residuals; logistic loss with 0/1 labels gives y-p and updates scores, not probabilities directly.
- A sum of linear models on exactly the same features is still linear. Nonlinear threshold rules or other suitable base functions provide the flexible examples here.
- Bagging often uses deep unstable trees; it does not require AdaBoost's weak-learning assumption. The variance formula has explicit equal-variance/correlation assumptions. Random forests also randomize candidate features.
- The textbook forest module describes label voting; the Kinect case averages leaf probabilities. Neither is a guarantee of improvement on every dataset.

## Review

All physical presentation pages and reveals are visually reviewed; handouts are matched to final reveals. The optional GLM source is separately compiled and inspected. The source ZIP is extracted and both entry points rebuilt to check portability. Exact counts above refer to the default route.
