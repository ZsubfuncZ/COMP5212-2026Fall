# Sources for the ensemble-foundations module

1. Leo Breiman, *Bagging Predictors*, technical report 421 (1994; published 1996).
   https://statistics.berkeley.edu/tech-reports/421
   Supports bootstrap replication, aggregation by regression mean/classification plurality vote, and motivation through unstable predictors. The slides avoid a universal improvement claim.
2. Leo Breiman and Adele Cutler, *Random Forests: classification description*.
   https://www.stat.berkeley.edu/~breiman/forests/cc_home.htm
   Sections Overview and The out-of-bag error estimate: bootstrap n rows, a fresh random candidate feature subset at each node, tree voting and OOB prediction. The historical site's blanket no-overfitting and unbiased-evaluation claims are deliberately not used.
3. Scikit-learn authors, *Decision Trees*, mathematical formulation.
   https://scikit-learn.org/stable/modules/tree.html#mathematical-formulation
   Supports greedy axis-aligned partitions, weighted child impurity, regression mean leaves, classification frequency leaves and Gini impurity. Only mathematical mechanisms are used, not version-dependent defaults.

Rechecked 2026-09-24. All plotted data are constructed illustrations, not empirical benchmarks. All numbers and curves are generated in `examples/foundations_generate.py`. The variance identity and bootstrap exclusion probability are derived in the slides from the stated assumptions.

## Revision for the boosting-first lecture

The primer is now three frames, followed by bagging and random forests. The statement that bagging often uses deep, unstable trees is supported by Breiman’s instability motivation and the Breiman–Cutler construction that grows full trees. This is distinguished from AdaBoost’s weighted weak-learning condition; no claim is made that averaging arbitrary weak predictors satisfies a boosting theorem. Classification Gini detail is confined to the split slide and notes. The plotted constructed data and all numerical results are unchanged.
