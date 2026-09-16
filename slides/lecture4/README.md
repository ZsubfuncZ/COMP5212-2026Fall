# Linear Regression

English LaTeX Beamer lecture for COMP 5212, Graduate Machine Learning. The deck has **74 logical slides and 99 PDF pages**, with exactly five sections:

1. Electricity motivation.
2. Formulation and the closed-form least-squares derivation.
3. Ill-conditioning and remedies.
4. Regularization: Ridge and Lasso.
5. Feature expansion: polynomial features and kernels.

The lecture uses the supplied `lecture3.pdf` style: white background, centered red headings, Latin Modern text and mathematics, green bullets, blue formula blocks, peach takeaways, and a centered logical slide number. The source is genuine editable LaTeX, including native TikZ/PGFPlots figures.

## Source files

- `main.tex`: document metadata and cover slide.
- `frames.tex`: slides 2-74, section commands, reveals, and complete English speaker notes. Numbered comments identify each logical slide.
- `theme.tex`: typography, colors, layouts, and reusable commands.
- `figures/*.tex`: 19 referenced vector plot inputs and their editable numerical coordinates.
- `assets/hkust-logo.png`: the logo from the supplied reference.
- `instructor-guide.md`: pacing, all 74 slide notes, reveal cues, exact PDF-page ranges, and eight web-demo links.
- `examples/conditioning.py`: a standard-library Python script reproducing the perturbation, roundoff, and Ridge calculations.
- `examples/conditioning-results.json`: the numerical reference results.

## Compile

Use pdfLaTeX with TeX Live, MacTeX, MiKTeX, or Overleaf. Standard packages are sufficient; no custom fonts, internet access, or shell escape are required.

From this directory:

```sh
latexmk -pdf main.tex
```

Alternatively, run `pdflatex main.tex` twice. The result is `main.pdf`, containing 99 pages in 16:9 format. Upload the source archive to Overleaf, select `main.tex` as the main document, and choose pdfLaTeX.

## Presentation and speaker notes

Fourteen logical frames have two or three staged builds. Present the PDF in ordinary full-screen mode and advance one page at a time. The logical slide number remains the same across a reveal sequence. There are no automatic timed transitions.

The electricity motivation, scalar least-squares calculation, response perturbation, Lasso examples, and feature examples place questions before answers. Edit `\only<1>{...}`, `\only<2>{...}`, and `\uncover<2->{...}` directly. Keep the explanatory paragraphs and the 10-20-second pause cues in `\note{...}`.

Speaker notes are hidden by default. To show each slide alongside its notes, uncomment the existing setting in `main.tex`:

```tex
\setbeameroption{show notes on second screen=right}
```

Use the default presentation mode to retain the reveals. Some frames replace content using `\only`; a compact handout requires a separate final-state layout rather than switching the document class option blindly.

## Mathematical conventions

The data-fit term is `SSE/(2n)`. Ridge adds `lambda/2 * ||w||_2^2`, while Lasso adds `lambda * ||w||_1`. The intercept is unpenalized. Training-fold centering and scaling are part of the fitted procedure. Where normalized columns are assumed, their squared norm divided by `n` is one.

The inverse formula for least squares is stated only with its full-column-rank condition. QR and SVD are used to distinguish numerical computation from mathematical sensitivity. The Lasso sequence includes constrained geometry, subgradients, soft-thresholding, coordinate descent, exact analytic paths, and a duplicate-feature counterexample. Polynomial and kernel sections preserve feature-scaling and centered-prediction details.

Write equations in LaTeX math mode rather than with Unicode approximations. Keep matrices, fractions, and derivations in `aligned`, `gathered`, or display-math environments. Split dense content instead of shrinking an entire frame.

## Interactive examples

The lab is available at:

https://regression-lab-graduate-2026.whu38f.chatgpt.site

Its eight experiments use anchors `#fit`, `#closed-form`, `#conditioning`, `#regularization`, `#polynomial`, `#kernel`, `#gradient-descent`, and `#outliers`. The final resource slide and instructor guide include links. An offline HTML copy can be opened separately when teaching without internet access; PDF links target the online lab.

The industrial energy application is a real use case. All numerical lecture observations, curves, and examples are constructed or simulated for teaching. Source references are included in the notes and final resource slide.

To reproduce the conditioning calculations:

```sh
python3 examples/conditioning.py
```

The roundoff example specifies one binary64 operation sequence. It illustrates information lost by forming a Gram matrix; it is not a universal error prediction for every solver.

## Suggested pacing

Four 90-minute meetings allow discussion and derivations: foundations, conditioning, regularization, then feature expansion. The opening motivation can be delivered in about 15-18 minutes. The instructor guide includes the complete route and a shorter two-meeting selection.
