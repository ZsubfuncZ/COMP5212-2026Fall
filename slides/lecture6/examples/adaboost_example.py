#!/usr/bin/env python3
"""Reproduce and verify the eight-point discrete AdaBoost lecture example.

Python standard library only. Run from any directory. Exact rational sample
weights remove floating-point ambiguities when weak learners tie.
"""
import csv
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = ROOT / "examples"
X = list(range(1, 9))
Y = [-1, -1, 1, 1, -1, -1, 1, 1]


def coords(xs, ys):
    return " ".join(f"({x:.8g},{y:.10g})" for x, y in zip(xs, ys))


def run():
    d = [Fraction(1, 8)] * 8
    score = [0.0] * 8
    rounds = []
    product_z = 1.0
    checks = []
    for t in range(1, 4):
        candidates = []
        for k in range(1, 8):
            threshold = k + 0.5
            for orientation in (1, -1):
                h = [orientation * (1 if x >= threshold else -1) for x in X]
                error = sum((di for di, yi, hi in zip(d, Y, h) if yi != hi), Fraction())
                candidates.append((error, threshold, -orientation, h))
        error, threshold, neg_orientation, h = min(candidates, key=lambda item: item[:3])
        assert 0 < error < Fraction(1, 2)
        alpha = 0.5 * math.log(float((1 - error) / error))
        z = sum(float(di) * math.exp(-alpha * yi * hi) for di, yi, hi in zip(d, Y, h))
        d_next = [di / (2 * (error if yi != hi else (1 - error)))
                  for di, yi, hi in zip(d, Y, h)]
        updated = [si + alpha * hi for si, hi in zip(score, h)]
        loss_before = sum(math.exp(-yi * si) for yi, si in zip(Y, score)) / len(Y)
        loss_after = sum(math.exp(-yi * si) for yi, si in zip(Y, updated)) / len(Y)
        product_z *= z
        derivative = -(1 - float(error)) * math.exp(-alpha) + float(error) * math.exp(alpha)
        assert sum(d_next) == 1
        assert abs(z - 2 * math.sqrt(float(error * (1 - error)))) < 1e-14
        assert abs(derivative) < 1e-14
        assert abs(loss_after - loss_before * z) < 1e-14
        assert abs(loss_after - product_z) < 1e-14
        assert all(abs(float(dn) - float(di) * math.exp(-alpha * yi * hi) / z) < 1e-14
                   for dn, di, yi, hi in zip(d_next, d, Y, h))
        assert sum(dn for dn, yi, hi in zip(d_next, Y, h) if yi != hi) == Fraction(1, 2)
        predicted = [1 if si >= 0 else -1 for si in updated]
        training_error = sum(yi != pi for yi, pi in zip(Y, predicted)) / len(Y)
        assert training_error <= loss_after + 1e-14
        rounds.append({"round": t, "threshold": threshold, "orientation": -neg_orientation,
                       "weighted_error": float(error), "weighted_error_exact": str(error),
                       "alpha": alpha, "Z": z, "weights_before": list(map(float, d)),
                       "weights_before_exact": list(map(str, d)), "h": h,
                       "weights_after": list(map(float, d_next)),
                       "weights_after_exact": list(map(str, d_next)),
                       "score": updated, "prediction": predicted,
                       "training_error": training_error, "exponential_loss": loss_after,
                       "normalizer_product": product_z})
        checks.append(f"Round {t}: exact normalization, alpha derivative, update, Z, loss product, and bound PASS")
        d, score = d_next, updated
    assert [r["weighted_error_exact"] for r in rounds] == ["1/4", "1/6", "1/5"]
    assert rounds[-1]["prediction"] == Y
    return rounds, checks


def write_figures(rounds):
    FIG.mkdir(exist_ok=True)
    negative = coords([x for x, y in zip(X, Y) if y == -1], [-1] * 4)
    positive = coords([x for x, y in zip(X, Y) if y == 1], [1] * 4)
    (FIG / "adaboost-stump.tex").write_text(r"""% Generated original synthetic illustration.
\begin{tikzpicture}
\begin{axis}[width=.94\linewidth,height=3.9cm,xmin=.5,xmax=8.5,ymin=-1.5,ymax=1.5,
 xlabel={Feature $x$},ylabel={Label or prediction},xtick={1,...,8},ytick={-1,1},
 yticklabels={$-1$,$+1$},axis lines=left,tick label style={font=\small},
 label style={font=\small},legend style={draw=none,font=\small,at={(.5,1.12)},anchor=south,legend columns=3}]
\addplot[inkplot,thick] coordinates {(.5,-1) (2.5,-1) (2.5,1) (8.5,1)};
\addlegendentry{First stump $h_1$}
\addplot[only marks,mark=*,mark size=4pt,blueplot] coordinates {""" + negative + r"""};
\addlegendentry{Observed $y=-1$}
\addplot[only marks,mark=*,mark size=4pt,redplot] coordinates {""" + positive + r"""};
\addlegendentry{Observed $y=+1$}
\draw[titlered,thick,dashed] (axis cs:5,-1) circle[radius=7pt];
\draw[titlered,thick,dashed] (axis cs:6,-1) circle[radius=7pt];
\node[font=\small,text=titlered,anchor=south] at (axis cs:5.5,-.75) {two mistakes};
\end{axis}
\end{tikzpicture}
""", encoding="utf-8")
    (FIG / "adaboost-margin.tex").write_text(r"""% Analytic exponential loss, not fitted data.
\begin{tikzpicture}
\begin{axis}[width=.98\linewidth,height=4.7cm,xmin=-2,xmax=3,ymin=0,ymax=8,
 xlabel={Margin $m=yF(x)$},ylabel={Loss},axis lines=left,xtick={-2,0,2},ytick={0,1,4,8},
 tick label style={font=\small},label style={font=\small},clip=false]
\addplot[blueplot,very thick,domain=-2:3,samples=90] {exp(-x)};
\addplot[inkplot,dashed] coordinates {(0,0) (0,8)};
\node[font=\small,text=blueplot] at (axis cs:1.5,2.2) {$e^{-m}$};
\node[font=\scriptsize,anchor=north east] at (axis cs:-.1,7.8) {wrong};
\node[font=\scriptsize,anchor=north west] at (axis cs:.1,7.8) {correct};
\end{axis}
\end{tikzpicture}
""", encoding="utf-8")
    (FIG / "adaboost-weights.tex").write_text(r"""% Exact weights in adaboost-results.json; bars grouped by observation.
\begin{tikzpicture}
\begin{axis}[width=.99\linewidth,height=4.8cm,ybar,bar width=5pt,
 xmin=.4,xmax=8.6,ymin=0,ymax=.29,xlabel={Observation $i$},ylabel={Weight},
 xtick={1,...,8},ytick={0,.125,.25},yticklabels={$0$,$1/8$,$1/4$},
 axis lines=left,tick label style={font=\small},label style={font=\small},
 legend style={draw=none,font=\small,at={(.5,1.04)},anchor=south,legend columns=2}]
\addplot[fill=lightplot,draw=blueplot] coordinates {""" + coords(X, rounds[0]["weights_before"]) + r"""};
\addlegendentry{$D_1$}
\addplot[fill=redplot!70,draw=redplot] coordinates {""" + coords(X, rounds[0]["weights_after"]) + r"""};
\addlegendentry{$D_2$}
\end{axis}
\end{tikzpicture}
""", encoding="utf-8")
    final_score = rounds[-1]["score"]
    (FIG / "adaboost-votes.tex").write_text(r"""% Computed final scores after three rounds.
\begin{tikzpicture}
\begin{axis}[width=.98\linewidth,height=4.2cm,xmin=.5,xmax=8.5,ymin=-1.12,ymax=.95,
 xlabel={Feature $x$},ylabel={$F_3(x)$},xtick={1,...,8},ytick={-1,0,1},axis lines=left,
 tick label style={font=\small},label style={font=\small}]
\addplot[inkplot,thin,dashed] coordinates {(.5,0) (8.5,0)};
\addplot[inkplot,thick] coordinates {(.5,""" + str(final_score[0]) + ") " + coords([2.5,2.5,4.5,4.5,6.5,6.5,8.5], [final_score[0],final_score[2],final_score[2],final_score[4],final_score[4],final_score[6],final_score[6]]) + r"""};
\addplot[only marks,mark=*,mark size=4pt,blueplot] coordinates {""" + coords([x for x,y in zip(X,Y) if y==-1],[s for s,y in zip(final_score,Y) if y==-1]) + r"""};
\addplot[only marks,mark=*,mark size=4pt,redplot] coordinates {""" + coords([x for x,y in zip(X,Y) if y==1],[s for s,y in zip(final_score,Y) if y==1]) + r"""};
\end{axis}
\end{tikzpicture}
""", encoding="utf-8")
    (FIG / "adaboost-loss-comparison.tex").write_text(r"""% Analytic losses at a common score convention: m=yF.
\begin{tikzpicture}
\begin{axis}[width=.98\linewidth,height=4.7cm,xmin=-3,xmax=3,ymin=0,ymax=21,
 xlabel={Margin $m=yF(x)$},ylabel={Loss},axis lines=left,xtick={-3,0,3},ytick={0,5,10,20},
 tick label style={font=\small},label style={font=\small},
 legend style={draw=none,font=\small,at={(1,1)},anchor=north east}]
\addplot[redplot,very thick,domain=-3:3,samples=100] {exp(-x)};
\addlegendentry{$e^{-m}$}
\addplot[blueplot,very thick,domain=-3:3,samples=100] {ln(1+exp(-x))};
\addlegendentry{$\log(1+e^{-m})$}
\end{axis}
\end{tikzpicture}
""", encoding="utf-8")


def main():
    rounds, checks = run()
    write_figures(rounds)
    result = {"description": "Constructed teaching data; no random sampling or external dataset.",
              "x": X, "y": Y, "tie_break": "Smallest threshold, then positive orientation.",
              "rounds": rounds, "checks": checks}
    (OUT / "adaboost-results.json").write_text(json.dumps(result, indent=2) + "\n")
    with (OUT / "adaboost-rounds.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["round", "i", "x", "y", "D_before", "h", "alpha", "F", "D_after", "prediction"])
        for r in rounds:
            for i, (x,y) in enumerate(zip(X,Y)):
                writer.writerow([r["round"],i+1,x,y,r["weights_before"][i],r["h"][i],r["alpha"],r["score"][i],r["weights_after"][i],r["prediction"][i]])
    print("\n".join(checks))
    for r in rounds:
        print(f"t={r['round']} threshold={r['threshold']} orientation={r['orientation']:+d} "
              f"epsilon={r['weighted_error_exact']} alpha={r['alpha']:.10f} "
              f"training_error={r['training_error']:.2f} exponential_loss={r['exponential_loss']:.10f}")
    print("Three-round predictions equal all eight labels: PASS")


if __name__ == "__main__":
    main()
