# Gradient boosting sources and evidence

## Primary method source

Jerome H. Friedman (2001), *Greedy Function Approximation: A Gradient Boosting Machine*, Annals of Statistics 29(5), 1189-1232. https://doi.org/10.1214/aos/1013203451

The author's February 1999 preprint was read from this academic mirror: https://www.cse.iitb.ac.in/~soumen/readings/papers/Friedman1999GreedyFuncApprox.pdf . Sections 2-3 motivate prediction/function-space descent and fitting a constrained negative-gradient direction; Algorithm 1 gives generic boosting; Section 4.1 and Algorithm 2 give squared-loss residual learning; Section 4.4 gives binary logistic likelihood. The lecture uses labels 0/1 and the full log-odds score, so its y-p pseudo-residual differs in convention from the paper's +/-1 and half-log-odds notation. All mathematical exposition is independently written; no paper figure is copied.

## Teaching derivations

- Expanding squared loss gives the exact change -eta times the residual inner product plus eta squared times the squared correction norm divided by two. The slide states positive alignment as the condition for a sufficiently small positive step to decrease loss.
- Fitting to negative derivatives produces pseudo-residuals. Ordinary residuals y-F apply to squared loss; logistic loss gives y-sigmoid(F).
- Generic line search is displayed in its idealized finite-minimizer form. Notes describe a finite descent step when an exact minimizer is unavailable, and justify shrinkage for the convex score losses taught here.

## Reproducible figures

Run `python3 examples/generate_boosting.py` (standard library only). The preserved seed 521223 experiment uses 60 training and 500 independent validation observations, target mean sin(1.6x)+0.22x, Gaussian noise SD 0.38, depth-two fitted partition functions, minimum leaf size three, shrinkage 0.12, and 300 rounds. Native PGFPlots output, CSV data, and a JSON result ledger accompany the package. These are constructed teaching examples, not real-world measurements.

The new three-round figure reuses the original four observations (1,1,3,3) and shrinkage 1/2. Its MSE values are 1/4, 1/16, and 1/64 after rounds 1-3. Arithmetic is asserted in the generator. Logistic loss derivatives are checked by finite differences; computed training MSE is asserted nonincreasing. The original train/validation data and numerical trajectory are unchanged by this revision.
