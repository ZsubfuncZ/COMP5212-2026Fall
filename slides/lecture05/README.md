# Logistic Regression: Likelihood, Optimization, and Softmax

COMP 5212 · Zihan Zhang · English lecture following linear regression.

51 logical slides; 85 presentation pages including staged reveals, plus a 51-page handout. The deck uses the same 16:9 Beamer theme as the previous lecture: red centered headings, green bullets, blue definition boxes, peach takeaways, serif mathematics, and logical slide numbers. `theme.tex` is copied unchanged from the approved preceding deck.

## Ready to present

- `main.pdf`: lecture with staged reveals.
- `handout.pdf`: one complete page per logical slide, without repeated builds.
- `main.tex`: compile this file for the lecture.
- `handout.tex`: compile this file for the handout.
- `instructor-notes.md`: readable notes for all 51 slides.
- `slide-plan.md`: slide-by-slide map.

All files needed to compile are included. The figures are editable native PGFPlots/TikZ; no downloaded images, system-font paths, external services, shell escape, or network access is needed.

## Compile locally or on Overleaf

Upload the extracted package folder to Overleaf and select `main.tex` as the main document. Use pdfLaTeX. For the handout select `handout.tex` instead.

With a standard TeX Live / MacTeX / MiKTeX installation, run from this directory:

```sh
latexmk -pdf main.tex
latexmk -pdf handout.tex
```

Without latexmk, run `pdflatex main.tex` twice (or `pdflatex handout.tex` twice).

To show presenter notes on a second screen, uncomment the indicated `show notes on second screen=right` line in `main.tex`. Notes are hidden by default.

## Lecture structure

| Slides | Topic | Source |
|---|---|---|
| 1–6 | Motivation: numerical outcomes vs events, defects, probabilities, OLS on binary labels | `motivation.tex` |
| 7–13 | Sigmoid, linear log odds, local approximation, notation, decision boundary, fitting problem | `formulation.tex` |
| 14–23 | Conditional likelihood; Gaussian likelihood → least squares; Bernoulli likelihood → BCE | `mle.tex` |
| 24–35 | Loss shape, derivatives, gradient descent, worked update, computed loss/contour plots, separation, stable loss | `optimization.tex` |
| 36–49 | Softmax probabilities, categorical MLE, cross-entropy, gradient, binary relation, stability, boundaries, temperature, applications | `softmax.tex` |
| 50–51 | Synthesis and references | `closing.tex` |

Allow about 90–110 minutes for the full derivations and pauses. A roughly 60-minute route omits slides 5, 9, 12, 17, 18, 22, 27, 30, 32, 33, 35, 44, 46, and 47, retaining the requested motivation, formulation, both MLE arguments, gradient descent with a loss curve, and softmax/MLE/applications.

## Numerical figures and reproducibility

Every plotted observation is a constructed teaching example, not an empirical industrial result. Native analytical plots can be edited directly in `figures/`.

The optimization experiment uses 20 fixed observations (9 positive, 11 negative), the feature `(raw intensity - 5)/2`, mean binary cross-entropy, zero initialization, and exactly 100 full-batch gradient updates. The global curvature bound is Lbar=0.473080155832. Learning rates are 0.1/Lbar, 1/Lbar, and 10/Lbar. The large step is shown to oscillate; the lecture does not claim universal divergence for every step beyond the bound.

The safe run reaches loss 0.411371042878 at (b,w)=(-0.098152266682, 1.570044394495). The curves contain actual computed losses. An independent Newton reference and finite-difference gradient/Hessian checks validate the computation. CSV trajectories, fitted probabilities, contour coordinates, JSON results, and the numerical report are included in `examples/`.

To regenerate the figures or verify numerical examples:

```sh
python3 examples/generate_foundation_figures.py
python3 examples/generate_optimization.py
python3 examples/softmax_examples.py
```

The foundation and softmax examples use Python's standard library. Only optimization regeneration requires NumPy (`python3 -m pip install numpy`); **compiling the slides requires no Python**. The softmax script checks the examples and matrix gradient but does not rewrite its analytical native figures.

## Mathematical conventions

- Binary labels: 0 and 1. Augmented feature x-tilde includes an intercept; X has observations as rows, and p counts all coefficients.
- Logistic loss: mean binary cross-entropy, with natural logs and no factor of one half. Least-squares gradient comparisons use SSE/(2n).
- Gaussian errors justify OLS as an MLE under fixed positive common variance. OLS itself is defined without a Gaussian assumption.
- A Bernoulli likelihood requires a mean model; MLE alone does not dictate the logistic link.
- Convexity does not ensure a finite MLE: separation is treated explicitly.
- Softmax W has shape p-by-K; its columns describe classes. The mean-loss gradient is X-transpose(P-Y)/n. A baseline removes common-shift redundancy, but cannot fix rank deficiency or separation.
- Positive temperature changes concentration without changing the argmax of fixed logits. Calibration requires a separate assessment.
- Output softmax is a categorical probability model. Attention softmax supplies mixture weights and is not itself a supervised categorical label model.

## Combine with the earlier lecture

The theme and helper commands match the previous deck. To build a combined lecture, copy these section files and figures into the earlier project, load `logistic-macros.tex` once after the shared theme, and input the required modules inside the document. Omit the first two frames of `motivation.tex` if the existing lecture already has a cover and goals. Keep each module's figure path consistent; do not load `theme.tex` twice.

## Sources

Clickable references appear on the final slide. Exact primary-source URLs and supporting sections are recorded in `sources.md` and the relevant slide notes.
