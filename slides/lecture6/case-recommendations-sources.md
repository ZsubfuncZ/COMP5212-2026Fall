# Netflix recommendation case: plan and sources

## Slide plan written before authoring

Audience: graduate machine-learning students, after the AdaBoost derivation.
Purpose: replace the face-detection example with a documented recommendation
application, while distinguishing general prediction blending from AdaBoost.
Use the existing Beamer theme, editable TikZ figures, and short visible text.

1. **Movie ratings: two views of taste.** Introduce the user–movie rating task
   and a schematic two-branch pipeline: rating history feeds SVD and RBM,
   whose predicted ratings feed a linear blend. First show the pipeline; then
   reveal a generic blend equation and the ensemble interpretation. Two builds.
2. **A blend improves rating prediction.** Show the three reported RMSE values
   in a labelled dot plot. State the historical production connection and the
   measurement's scope. One build. Lower error is the main visible point.

## Primary evidence

Xavier Amatriain and Justin Basilico, *Netflix Recommendations: Beyond the
5 stars (Part 1)*, Netflix Technology Blog, April 6, 2012.

https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429

In the section “The Netflix Prize and the Recommendation Problem,” the
authors report SVD RMSE 0.8914, RBM RMSE 0.8990, and linear-blend RMSE 0.88.
These are the only empirical values in the replacement figures. The article
does not identify the exact evaluation split or the blend coefficients.
It states that adapted versions of the two algorithms entered production.
That is a historical statement from 2012, not a description of today's system.

## Interpretation and scope

- The diagram explains a generic prediction blend. Its formula permits an
  intercept and fitted coefficients; neither the intercept nor the coefficients
  of Netflix's blend are claimed to be known.
- The two component predictors need not be weak learners. This is a broader
  ensemble application, not an application of the AdaBoost derivation.
- The values measure offline rating-prediction error. They do not measure
  recommendation ranking, watch time, retention, or revenue.
- The plot uses a clearly labelled enlarged RMSE axis, not truncated bars.
- The case does not equate the two-model blend with the complete 2007 or 2009
  competition-winning ensemble, and does not combine results across those years.

## Figure provenance

- `figures/case-recommendations-pipeline.tex`: original explanatory TikZ
  diagram; no fabricated individual ratings or inference outputs.
- `figures/case-recommendations-results.tex`: original TikZ/PGFPlots dot plot
  of the three numbers from the Netflix article above, preserving its precision.

## Visual verification

Isolated proof passed: two logical frames and three physical pages, all rendered
and inspected at 1500 pixels on the long edge. No clipping, overlap, or unreadable
labels remained. The final LaTeX log has no overfull/underfull boxes or warnings.
The first reveal preserves the diagram and adds the formula and interpretation.
The dot plot matches the three source values. Full-deck integration is reviewed
separately by the coordinating agent.
