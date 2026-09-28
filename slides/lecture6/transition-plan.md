# Phase transitions

Audience: graduate machine-learning students following linear and logistic regression. These six static divider slides mark the existing lecture's conceptual phases without adding another derivation or a new application claim.

Visual source: the existing `theme.tex` and `macros.tex`. Preserve the red centered titles, blue definition boxes, peach takeaway boxes, shared margins, and small page number. Each slide has one preceding connection, one large central question, and one brief next step. No builds; the lecturer pauses on the question before advancing. Visible text is approximately 30–50 words per frame.

| File | Insertion point | Teaching move and source | Layout / build | Notes |
|---|---|---|---|---|
| `transition-01-adaboost.tex` | Before the first AdaBoost behavior slide | Move from one linear score to cooperation among simple rules; follows `intro.tex` and motivates `adaboost.tex`. | Phase title, preceding connection, central question in blue, next step in peach; static. | Distinguish the simple-rule intuition from the formal weak-learning assumption introduced later. |
| `transition-02-theory.tex` | After the three-stump example, before exponential loss | Turn observed success into a derivation of both types of weight and a qualified training-error guarantee. | Same; static. | Zero training error in the example is not a generalization claim. |
| `transition-03-residuals.tex` | After the recommendation case, before residual learning | Retain the additive structure and ask what target the next model should fit; follows AdaBoost and previews `boosting.tex`. | Same; static. | Do not imply the recommendation application used AdaBoost. |
| `transition-04-trees.tex` | After electricity forecasting, before the tree primer | Explain the learner before introducing an ensemble that resamples it; previews the first three `foundations.tex` frames. | Same; static. | Trees were only informal simple rules earlier; now make their mechanics explicit. |
| `transition-05-bagging.tex` | After tree instability, before bagging | Turn sensitivity to resampling into a reason to aggregate independently fitted trees. | Same; static. | Bagged trees need not be weak stumps; averaging has conditions and does not guarantee lower test error. |
| `transition-06-forests.tex` | After the correlation plot, before the random-forest algorithm | Ask how to address the shared-prediction limitation of averaging. | Same; static. | Random feature subsets may trade lower correlation against weaker individual trees; out-of-bag assessment follows. |

Verification: compile the six frames with the package's unchanged theme and macros in an isolated proof; render all six physical pages; visually inspect all text, spacing, boxes, title width, and footer visibility. Root agent performs final integrated compilation and page-number verification.
