#!/usr/bin/env python3
"""Reproduce five native PGFPlots teaching figures (Python standard library).

Run from any directory: python3 examples/generate_foundation_figures.py
All observations are constructed examples, not empirical manufacturing data.
No external libraries, downloads, or stochastic runs are required.
"""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)

X_RAW = [0.2, 0.7, 1.1, 1.6, 2.1, 2.5, 3.1, 3.6, 4.0, 4.4,
         4.9, 5.3, 5.7, 6.2, 6.7, 7.1, 7.6, 8.1, 8.7, 9.4]
Y = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1]


def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def softplus(z):
    return max(z, 0.0) + math.log1p(math.exp(-abs(z)))


def linspace(a, b, count=121):
    return [a + (b - a) * k / (count - 1) for k in range(count)]


def coordinates(points):
    return " ".join(f"({x:.10g},{y:.10g})" for x, y in points)


def plot(options, points, legend=None):
    result = r"\addplot[" + options + "] coordinates {" + coordinates(points) + "};\n"
    if legend is not None:
        result += r"\addlegendentry{" + legend + "}\n"
    return result


def figure(name, options, body, comment=""):
    text = r"""% Native PGFPlots; reproduced by examples/generate_foundation_figures.py.
% Constructed observations / analytical teaching example, not empirical data.
\begingroup
\definecolor{blueplot}{HTML}{4E79A7}
\definecolor{redplot}{HTML}{D95F59}
\definecolor{inkplot}{HTML}{111111}
\begin{tikzpicture}
\begin{axis}[
width=\linewidth,height=4.0cm,font=\scriptsize,
tick label style={font=\scriptsize},label style={font=\scriptsize},
axis line style={black!45},tick style={black!45},
grid=major,grid style={black!10},scaled ticks=false,
clip=true,unbounded coords=jump,
legend style={font=\tiny,draw=none,fill=white,fill opacity=.94,text opacity=1,
  legend cell align=left,inner sep=2pt,row sep=1pt},
""" + options + "\n]\n" + body + r"""
\end{axis}
\end{tikzpicture}
\endgroup
"""
    (FIGURES / name).write_text(("% " + comment + "\n" if comment else "") + text)


def binary_points():
    return (plot("blueplot,only marks,mark=o,mark size=2.0pt,thick,forget plot",
                 [(x, y) for x, y in zip(X_RAW, Y) if y == 0])
            + plot("redplot,only marks,mark=triangle*,mark size=2.6pt,forget plot",
                   [(x, y) for x, y in zip(X_RAW, Y) if y == 1]))


figure("motivation.tex", r"""xmin=0,xmax=10,ymin=-.15,ymax=1.18,
xlabel={Operating intensity (scaled units)},ylabel={Defect indicator $y$},
xtick={0,2,4,6,8,10},ytick={0,1}""",
       binary_points(), "Twenty fixed observations; the two classes overlap.")

mean_x, mean_y = sum(X_RAW) / len(Y), sum(Y) / len(Y)
slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(X_RAW, Y)) / sum((x - mean_x)**2 for x in X_RAW)
intercept = mean_y - slope * mean_x
figure("ols-binary.tex", r"""xmin=-2,xmax=12,ymin=-.5,ymax=1.6,
xlabel={Operating intensity (scaled units)},ylabel={Fitted response},
xtick={-2,0,4,8,12},ytick={0,.5,1},legend pos=north west""",
       plot("black!40,densely dashed,no marks,forget plot", [(-2, 0), (12, 0)])
       + plot("black!40,densely dashed,no marks,forget plot", [(-2, 1), (12, 1)])
       + plot("inkplot,thick,no marks", [(x, intercept + slope * x) for x in [-2, 12]], "OLS line")
       + binary_points(), f"OLS on the same 20 observations: intercept={intercept:.12g}, slope={slope:.12g}.")

figure("sigmoid.tex", r"""xmin=-6,xmax=6,ymin=0,ymax=1,
xlabel={Linear score $z$},ylabel={$\operatorname{s}(z)$},
xtick={-6,-3,0,3,6},ytick={.1,.5,.9}""",
       plot("redplot,very thick,no marks", [(z, sigmoid(z)) for z in linspace(-6, 6)]))

boundary_zero = [(-.7, -.9), (-.4, .6), (.2, -.9), (.3, .25), (.7, -1.0),
                 (1.1, -.3), (1.4, -1.25), (1.9, -.75), (1.0, 1.0)]
boundary_one = [(-.3, 2.0), (.3, 2.35), (.8, .9), (1.3, 1.9), (1.8, .3),
                (2.3, 1.4), (2.9, -.3), (3.2, 2.2), (3.6, .8), (2.25, -1.15)]
figure("boundary.tex", r"""xmin=-1,xmax=4,ymin=-2,ymax=3,
xlabel={$x_1$},ylabel={$x_2$},xtick={-1,0,1,2,3,4},ytick={-2,0,2},
legend style={at={(.5,1.02)},anchor=south},legend columns=2""",
       plot("blueplot,only marks,mark=o,thick,mark size=1.8pt", boundary_zero, "$y=0$")
       + plot("redplot,only marks,mark=triangle*,mark size=2.4pt", boundary_one, "$y=1$")
       + plot("inkplot,thick,no marks", [(x, (1-x)/.8) for x in [-1, 4]], r"$\tau=0.5$")
       + plot("inkplot,thick,dashed,no marks", [(x, (1+math.log(4)-x)/.8) for x in [-1, 4]], r"$\tau=0.8$"),
       "Score z=-1+x1+0.8*x2. Classification predicts 1 above each threshold boundary.")

probabilities = linspace(.01, .99, 121)
figure("logloss.tex", r"""xmin=0,xmax=1,ymin=0,ymax=4.7,
xlabel={Predicted probability $\pi$},ylabel={Loss},
xtick={0,.25,.5,.75,1},ytick={0,1,2,3,4},legend pos=north east""",
       plot("redplot,thick,no marks", [(p, -math.log(p)) for p in probabilities], r"$y=1$: $-\log\pi$")
       + plot("blueplot,thick,dashed,no marks", [(p, -math.log1p(-p)) for p in probabilities], r"$y=0$: $-\log(1-\pi)$"))

logits = linspace(-6, 6)

print("Generated five native teaching figures: motivation, OLS binary, sigmoid, boundary, log loss.")
