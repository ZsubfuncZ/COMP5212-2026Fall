# Lecture 3 motivation examples and visualizations

The revised deck keeps the original lecture sequence and style, adding 13 motivation examples plus 5 editable visual companions before the relevant definitions, proofs, or bounds. The supplied compiled deck had 66 slides; the revised deck has 84 slides.

The visual companions use native TikZ diagrams rather than external images, so the points, axes, thresholds, intervals, and loan boundary remain editable in LaTeX. External images were not needed because the concepts are geometric and schematic.

## Files

- `lecture3_motivated.pdf`: complete revised 84-slide deck.
- `lecture3_motivated.tex`: full editable Beamer source.
- `motivation_examples.pdf`: the 18 added slides only.
- `motivation_examples.tex`: standalone source for all added slides.
- `insertion_guide.md`: this map and teaching notes.
- `assets/logo.png`: the original course logo.

Compile from the unpacked package with pdfLaTeX:

```sh
pdflatex lecture3_motivated.tex
pdflatex lecture3_motivated.tex
pdflatex motivation_examples.tex
pdflatex motivation_examples.tex
```

Search the full source for `% MOTIVATION M01`–`M13` or `% MOTIVATION V01`–`V05`.

## Insertion map

Each added slide appears immediately before its anchor. “Original” refers to the supplied compiled PDF; “revised” refers to the full revised PDF.

| ID | Added slide | Before original slide / anchor | Revised slide |
|---|---|---|---|

| M01 | Fitting Random Labels | 7: Random Signs as a Stress Test | 7 |
| M02 | Repeated and Distinct Inputs | 12: Expected Rademacher Complexity | 14 |
| M03 | Mixing Two Predictors | 14: Convexification Does Not Increase Complexity | 18 |
| M04 | Prediction Errors on Four Examples | 15: From Hypotheses to Loss Functions | 20 |
| M05 | Swapping Two Samples | 18: Proof Roadmap | 24 |
| M06 | Many Cutoffs, Five Predictions | 29: Restriction of a Class to a Sample | 36 |
| M07 | 101 Vectors, Many Sign Draws | 33: Massart's Lemma | 42 |
| M08 | An Interval Labeling Game | 39: Shattering and VC Dimension | 49 |
| M09 | Counting Interval Patterns | 48: Sauer's Lemma | 61 |
| M10 | Extending a Prediction Pattern | 49: Sauer's Lemma: Proof Setup | 63 |
| M11 | A Data Budget for Interval Rules | 57: Sample Complexity from the VC Bound | 72 |
| M12 | Unseen Labels | 61: Lower Bound: Realizable Case | 77 |
| M13 | A Nearly Fair Label Coin | 64: Lower Bound: Non-Realizable Case | 81 |
| V01 | Visual: Spam Score and Random Labels | 7: Random Signs as a Stress Test | 8 |
| V02 | Visual: Repeated and Distinct Patients | 12: Expected Rademacher Complexity | 15 |
| V03 | Visual: Threshold and Interval Rules | 29: Restriction of a Class to a Sample | 37 |
| V04 | Visual: Shattering as a Labeling Game | 39: Shattering and VC Dimension | 50 |
| V05 | Visual: Linear Loan Boundary | 44: Linear Separators in $\mathbb{R}^2$: VC Dimension $3$ | 56 |

For a shorter lecture, keep M01, V01, M02, V02, M06, V03, M07, M08, V04, and M09. These cover noise fitting, sample dependence, finite-sample restriction, Massart’s counting shortcut, and the VC/Sauer transition. M03–M05, M10, V05, and M11–M13 provide additional motivation for convexification, loss classes, symmetrization, linear separators, sample complexity, and lower bounds.

## Teaching notes


**M01 — Fitting Random Labels.** Gives the random-sign score an observable meaning before any Rademacher notation. Ask students to improve the threshold row. No one-sided increasing threshold exceeds two matches for this outcome. The scores are 0, 0, and 1. This is one draw, not the empirical Rademacher complexity; the next slides average the best score over all draws.

**M02 — Repeated and Distinct Inputs.** Separates randomness in the signs from randomness in the sample before expected complexity is defined. The same function must predict the same value at both copies of a. For distinct inputs the class can choose the two signs independently. The expected value 3/4 assumes the explicitly stated uniform distribution; another distribution changes it.

**M03 — Mixing Two Predictors.** Makes the convex-hull statement concrete with an ensemble of two real-valued predictors. For fixed signs, every weighted score lies between the two endpoint scores. This concerns the real-valued mixture; taking the sign or a majority vote is a different class.

**M04 — Prediction Errors on Four Examples.** Shows the data being evaluated by a generalization theorem before defining a loss class. Read the error vector against the true labels. Its average is the training error. Random signs in the later complexity calculation probe loss functions and are distinct from the observed labels.

**M05 — Swapping Two Samples.** Provides a concrete pair-swapping example before introducing the ghost sample and symmetrization proof. An independent sample has the same distribution as the training sample. Swapping either i.i.d. pair negates its difference without changing the joint distribution. The equality is distributional, not a pointwise identity for every fixed pair of samples.

**M06 — Many Cutoffs, Five Predictions.** Motivates restriction to a sample and the subsequent growth function using one concrete threshold problem. There are five observationally distinct cases. Emphasize that agreement on this sample does not mean two hypotheses agree everywhere. Later generalize the table to m+1 patterns; the growth function then takes a maximum over input placements.

**M07 — 101 Vectors, Many Sign Draws.** Poses the computational question that Massart’s lemma answers, using the threshold count already established. The finite set in the lemma is the 101 distinct evaluation vectors, not the infinite parameter set and not the 2^100 sign vectors. The next result gives 10 sqrt(2 log 101)/100 ≈ 0.304 as an upper bound, not an exact complexity.

**M08 — An Interval Labeling Game.** Introduces the quantifier “every labeling of one fixed set” before shattering and VC dimension. On two points an interval can select neither, either one, or both. No three distinct real inputs avoid an ordering, so 101 always defeats an interval. After the definition, return to this example as the lower and upper bounds for VC dimension 2.

**M09 — Counting Interval Patterns.** Motivates a general counting theorem from the gap between polynomial and exponential pattern counts. The answer is yes: Sauer gives 1+m+binom(m,2)=1+m(m+1)/2 for every class of VC dimension 2. Intervals attain that bound. Stress that failure on one specially chosen triple alone would not imply the universal premise.

**M10 — Extending a Prediction Pattern.** Explains the otherwise abstract G1/G2 decomposition before the proof introduces it. The next slide names G1={00,01,11} and G2={00}. The smaller VC dimension of the branching family is the key induction step. This addition is optional if you present Sauer without its proof.

**M11 — A Data Budget for Interval Rules.** Turns a generalization bound into a concrete planning problem before sample complexity notation. Six thousand is sufficient according to this particular theorem, not a necessary minimum. The target concerns population error minus training error, not absolute error below 10%. Existing worked examples later apply the same theorem for two different classes.

**M12 — Unseen Labels.** Gives the information limit before the formal realizable lower bound. The target is selected once and labels are then deterministic, so the example is realizable. The averaging over targets is a proof device. A lower-bound proof uses it to establish the existence of a fixed hard target and controls the probability of observing rare inputs.

**M13 — A Nearly Fair Label Coin.** Explains the quadratic accuracy dependence before the agnostic lower-bound theorem. Choosing the wrong majority label costs excess risk 2γ. The 1/sqrt(n) noise scale suggests n of order 1/γ² for one coin. Across d equally weighted shattered inputs the typical local sample count is m/d, leading to sqrt(d/m). This slide gives intuition, not a derivation of the theorem constants.

**V01 — Visual: Spam Score and Random Labels.** Shows four email scores, an increasing threshold, and an unrestricted lookup rule as a visual noise-fitting stress test. The alternating labels cross a one-sided threshold several times, while a lookup class can memorize the four outcomes. Use it immediately before the formal random-sign definition.

**V02 — Visual: Repeated and Distinct Patients.** Makes repeated versus distinct patient profiles visible as two different sample geometries. Two copies of the same profile must receive the same prediction; two distinct profiles can receive independent predictions. This explains why empirical complexity varies with the sample before averaging over samples.

**V03 — Visual: Threshold and Interval Rules.** Shows a sensor cutoff and a target biomarker interval on number lines. The real-world rules have infinitely many parameter values but only finitely many behaviors on the observed readings. This leads into evaluation vectors and the growth function.

**V04 — Visual: Shattering as a Labeling Game.** Shows all four labelings of two points and the impossible alternating labeling of three interval points. The visual makes the quantifier “every labeling” explicit before shattering and VC dimension are defined.

**V05 — Visual: Linear Loan Boundary.** Shows three non-collinear customer profiles and a linear loan-approval boundary. A line can realize every labeling of three non-collinear profiles, but four points force a geometric obstruction. This motivates the planar halfspace VC-dimension example.


## Small corrections included

The source also fixes a few issues in the supplied deck: the section-slide macro calls now provide the expected empty subtitle argument; VC dimension uses a supremum over nonnegative sample sizes and allows infinity; the rectangle and planar-separator upper-bound explanations handle degenerate point placements; the displayed VC and lower-bound results state a meaningful sample-size regime; Massart’s optimizing parameter states its nondegenerate case; and the rounded linear-separator example is corrected to (0.250).

The theory follows the supplied lecture and Chapter 3 of *Foundations of Machine Learning*. The examples are constructed teaching examples with direct arithmetic checks.
