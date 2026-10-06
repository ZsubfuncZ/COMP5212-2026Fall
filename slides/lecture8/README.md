# Lecture 8 — K-means Clustering

This directory contains the editable Beamer source, the compiled PDF, local figures, and the experiment script used in the lecture.

## Main files

- `lecture8.pdf` — compiled slide deck.
- `lecture8.tex` and `course-style.tex` — Beamer entry point and the visual style adapted from the supplied lecture template.
- `sections/` — slide content split into objective, algorithm, theory/practice, applications, JL lemma, and closing sections.
- `sections/motivation_frames.tex` — optional motivation frames that can be inserted before the objective section.
- `sections/motivation_two_examples.tex` — two standalone motivation frames: image color quantization and customer segmentation.
- `sections/motivation_user_behavior.tex` — two standalone frames focused only on customer behavior: feature construction and downstream actions.
- `sections/motivation_user_behavior_onepage.tex` — compact, image-free motivation slide for user-behavior clustering.
- `experiments.py` — deterministic script for the scale, geometry, color-quantization, and JL figures.
- `kmeans_demo.html` — standalone browser demo with random `K`-class data, separate data/algorithm `K` sliders (2–20), and random Lloyd initialization.
- `kmeans_demo_generator.py` — regenerates the 2-D demo, its static preview, and the embedded data.
- `experiment-results.json` — recorded metrics, seeds, package versions, and data provenance.
- `assets/` — local PDF/PNG figures and the course logo.
- `assets/motivation/` — saved image resources and attribution information for the motivation frames.

The theory section includes a four-point fixed-point counterexample showing why uniform random starts can have an unbounded expected approximation ratio. The applications section treats concentric rings with two remedy families—nonlinear feature/kernel representations and graph/density neighborhoods—and works through the radial feature `u = x_1^2 + x_2^2`.

## Recompile

From this directory:

```text
pdflatex -interaction=nonstopmode -halt-on-error lecture8.tex
pdflatex -interaction=nonstopmode -halt-on-error lecture8.tex
```

To regenerate the figures and recorded metrics, run:

```text
MPLCONFIGDIR=work/mplconfig /opt/anaconda3/bin/python3 experiments.py
```

To regenerate the interactive 2-D initialization demo and its deterministic slide preview, run:

```text
MPLCONFIGDIR=work/mplconfig /opt/anaconda3/bin/python3 kmeans_demo_generator.py
```

The examples and implementation references used in the slides include [scikit-learn's color-quantization example](https://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html), [FAISS's IVF index documentation](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes), the [original k-means++ paper](https://theory.stanford.edu/~sergei/papers/kMeansPP-soda.pdf), the [local-search approximation analysis](https://theory.stanford.edu/~sergei/papers/vldb17-km.pdf), and the [Johnson–Lindenstrauss lemma reference](https://cseweb.ucsd.edu/~dasgupta/papers/jl.pdf).
