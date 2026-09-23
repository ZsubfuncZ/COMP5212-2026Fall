# Softmax lecture section: sources and slide plan

Accessed 2026-09-22. The section has 14 frames, each with speaker notes.
Every diagram and numerical example is an original analytical teaching example.
No empirical accuracy or calibration results are plotted.

## Primary sources

1. Tengyu Ma and Andrew Ng, **CS229 Lecture Notes**, Section 2.3, printed pages
   25–27. Current retrieved document dated August 23, 2026.
   Exact URL: <https://cs229.stanford.edu/main_notes.pdf>
   Supports the multiclass logits, categorical probabilities, negative
   log-likelihood, and per-class derivative. This lecture uses samples as rows
   of `X`, classes as columns of `W`, mean rather than summed loss, and includes
   the intercept in the first augmented feature coordinate. Raw features are
   `x`, augmented features are `tilde x=(1,x^T)^T`. The matrix gradient and
   pairwise identities are derived in this convention.

2. Alex Krizhevsky, Ilya Sutskever, and Geoffrey Hinton (2012), **ImageNet
   Classification with Deep Convolutional Neural Networks**, Section 3.5,
   PDF page 4.
   Exact URL:
   <https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf>
   Supports the original architecture's final 1000-way softmax and the
   multinomial logistic objective. No accuracy figures are used.

3. Yoshua Bengio, Réjean Ducharme, Pascal Vincent, and Christian Jauvin (2003),
   **A Neural Probabilistic Language Model**, JMLR 3:1137–1155.
   Exact URL: <https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf>
   Printed page 1142 gives the word-softmax and corpus likelihood. Page 1146
   describes subtracting the largest logit to stabilize exponentiation.

4. Ashish Vaswani et al. (2017), **Attention Is All You Need**.
   Canonical record: <https://arxiv.org/abs/1706.03762>
   Full text inspected: <https://arxiv.org/html/1706.03762v7>
   Section 3.2.1, equation (1), defines scaled dot-product attention as
   softmax-normalized compatibility scores followed by multiplication with
   value vectors. Section 3.4 describes the separate linear/softmax vocabulary
   output. Section 3.2.3 explains causal masks. The lecture distinguishes
   attention mixture weights from a label-likelihood classifier.

5. Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger (2017), **On
   Calibration of Modern Neural Networks**, ICML/PMLR 70.
   Publication record: <https://proceedings.mlr.press/v70/guo17a.html>
   Full text: <https://proceedings.mlr.press/v70/guo17a/guo17a.pdf>
   Section 4, equation (9), specifies positive temperature, unchanged class
   prediction, and fitting by held-out NLL. The lecture does not claim that
   arbitrary softening improves calibration, nor that fitted temperature
   guarantees calibration on a new distribution.

## Slide plan

| Local frame | Teaching point | Layout and evidence | Reveal |
|---|---|---|---|
| S01 | A primary-defect task has one categorical label | Three-row label table, original inspection example | Static |
| S02 | K class logits form XW | Definition and dimensions | Static |
| S03 | Exponentiate and normalize across classes | Softmax formula and argmax identity | Static |
| S04 | Numerical logits produce a probability vector | Table and native probability bars for (2,1,0) | Probabilities/bars on step 2 |
| S05 | Categorical likelihood selects observed labels | One-hot likelihood and MLE | MLE on step 2 |
| S06 | MLE gives cross-entropy and LSE minus true score | Two equations plus numerical loss | Logit form on step 2 |
| S07 | Gradient is X transpose times P minus Y, divided by n | Scalar derivative and dimensioned matrix equation | Static |
| S08 | Binary logistic uses a score difference | Binary identity and general pairwise log odds | Static |
| S09 | A baseline removes common-shift redundancy | Invariance and parameter transformation | Static |
| S10 | Subtract-max stabilizes probabilities and loss | Stable equations and large-logit example | Static |
| S11 | Winning score ties define linear boundaries | Original PGFPlots three-region geometry | Static |
| S12 | Positive temperature preserves argmax | Original analytical probability curves | Static |
| S13 | Vision and next-token outputs use categorical likelihood | Two application equations, primary paper notes | Static |
| S14 | Attention softmax normalizes mixture weights | Attention formula and two-use comparison | Static |

## Numerical examples and integration

- `examples/softmax_examples.py` uses Python's standard library and writes no
  files. It recomputes all table values, checks score-shift invariance and
  temperature ordering, checks the 2-by-3 design / 3-by-3 parameter matrix
  gradient against finite differences, and checks interior points of the
  decision regions.
- Figures are editable native PGFPlots/TikZ. Their colors come from `theme.tex`.
- The decision plot uses raw coordinates `(u1,u2)` and augmented
  `tilde x=(1,u1,u2)`, avoiding confusion between intercept and feature indexing.
- The section needs no new shared macros. It uses `\R`, `\sigm`, `\lead`,
  `\definitionbox`, `\takeaway`, and `\logfig` already supplied by the copied
  theme/macros, plus standard AMS/TikZ/PGFPlots commands.
- `\input{softmax.tex}` after the binary section adds exactly 14 frames, with
  three two-step builds using `\uncover` (17 presentation pages, 14 handout
  pages). Compilation and rendered inspection belong to the root
  deck build; they are intentionally not performed by this module author.

## Linear and binary derivations

Also checked against the Gaussian probabilistic interpretation, logistic regression, and generalized linear model sections of the 2022 CS229 notes: https://cs229.stanford.edu/notes2022fall/main_notes.pdf .
