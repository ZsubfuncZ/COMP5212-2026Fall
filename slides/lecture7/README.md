# COMP 5212: Decision Trees, Random Forests, and XGBoost

English lecture slides for an 80-minute graduate machine learning class.

- `lecture_trees.tex`: main Beamer source.
- `lecture_trees_handout.tex`: static handout, with all reveal steps visible.
- `course-style.tex`: visual settings preserved from the supplied `lecture0.zip` template.
- `sections/`: editable lecture sections and application cases.
- `assets/logo.png`: logo from the supplied template.
- `instructor-notes.md`: timing, teaching prompts, answers, and technical qualifications.

The deck contains 37 main slides and 7 appendix slides. Dense derivations and worked examples use staged reveals: advance the PDF to reveal the next step, with the same slide number throughout. There are 87 presentation pages, including reveal steps on 28 slides. The 44-page handout has one complete page per slide. Diagrams, mathematical expressions, and charts remain editable in LaTeX/TikZ/PGFPlots. No external images or downloads are needed to compile.

## Compile

Run from this directory with a recent TeX Live or MiKTeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error lecture_trees.tex
pdflatex -interaction=nonstopmode -halt-on-error lecture_trees.tex
```

Alternatively:

```sh
latexmk -pdf lecture_trees.tex
```

For the static handout, compile `lecture_trees_handout.tex` twice instead.

Required packages are standard: Beamer, Latin Modern, AMS math, TikZ, PGFPlots, booktabs, and hyperref. The deck was compiled with pdfLaTeX (TeX Live 2024).

## Content

The lecture assumes prior coverage of linear regression, logistic regression, AdaBoost, and basic bagging. A four-sample constructed example connects ordinary regression trees, residual fitting, and a regularized XGBoost round. The missing-data and OOB explanations address the distinctions discussed while planning this lecture.

On-slide citations and bibliography slides have been removed as requested. The slides retain the study context, evaluation protocols, and limitations needed to interpret the application results. They distinguish retrospective comparative evidence, reported operational metrics, and verified deployment. No undisclosed business return is inferred from predictive metrics.

All application sources were checked on September 28, 2026. Mathematical examples and schematic diagrams are original teaching illustrations.
