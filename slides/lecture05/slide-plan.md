# Slide plan

| Slide | Topic | Module | PDF build behavior |
|---|---|---|---|
| 1 | Logistic Regression | `motivation.tex` | Static |
| 2 | Learning Goals | `motivation.tex` | Static |
| 3 | Same inputs, a different prediction | `motivation.tex` | Staged reveal |
| 4 | Motivation: detecting defective parts | `motivation.tex` | Staged reveal |
| 5 | Probabilities and decisions | `motivation.tex` | Staged reveal |
| 6 | OLS with binary responses | `motivation.tex` | Staged reveal |
| 7 | The logistic function | `formulation.tex` | Staged reveal |
| 8 | A linear model for log-odds | `formulation.tex` | Staged reveal |
| 9 | Why start with a linear score? | `formulation.tex` | Staged reveal |
| 10 | Model and notation | `formulation.tex` | Static |
| 11 | Decision thresholds and boundaries | `formulation.tex` | Static |
| 12 | Worked example: score to decision | `formulation.tex` | Staged reveal |
| 13 | What do we learn from the data? | `formulation.tex` | Staged reveal |
| 14 | What does conditional likelihood measure? | `mle.tex` | Staged reveal |
| 15 | Gaussian errors assign density to residuals | `mle.tex` | Staged reveal |
| 16 | The Gaussian likelihood leads to squared error | `mle.tex` | Staged reveal |
| 17 | Differentiating gives the normal equations | `mle.tex` | Staged reveal |
| 18 | Are the least-squares coefficients unique? | `mle.tex` | Staged reveal |
| 19 | The probability of an observed binary label | `mle.tex` | Staged reveal |
| 20 | Bernoulli likelihood and binary cross-entropy | `mle.tex` | Staged reveal |
| 21 | Express the same loss through the score | `mle.tex` | Staged reveal |
| 22 | Which probabilities enter the likelihood? | `mle.tex` | Staged reveal |
| 23 | Response models and their fitting losses | `mle.tex` | Staged reveal |
| 24 | A confident mistake incurs a large loss | `optimization.tex` | Static |
| 25 | The derivative becomes a prediction residual | `optimization.tex` | Staged reveal |
| 26 | From one observation to the whole sample | `optimization.tex` | Staged reveal |
| 27 | The logistic objective is convex | `optimization.tex` | Staged reveal |
| 28 | Gradient descent for logistic regression | `optimization.tex` | Static |
| 29 | One gradient step by hand | `optimization.tex` | Staged reveal |
| 30 | How large can the learning rate be? | `optimization.tex` | Staged reveal |
| 31 | Loss curves: the step size changes the trajectory | `optimization.tex` | Static |
| 32 | Gradient descent moves across loss contours | `optimization.tex` | Static |
| 33 | The optimized score gives a probability curve | `optimization.tex` | Static |
| 34 | Separable data can send the MLE to infinity | `optimization.tex` | Static |
| 35 | Evaluate the loss without overflow | `optimization.tex` | Static |
| 36 | One item, one defect label | `softmax.tex` | Static |
| 37 | One linear score for each class | `softmax.tex` | Static |
| 38 | Softmax probabilities | `softmax.tex` | Static |
| 39 | Three scores, three probabilities | `softmax.tex` | Staged reveal |
| 40 | Categorical likelihood | `softmax.tex` | Staged reveal |
| 41 | Cross-entropy and log-sum-exp | `softmax.tex` | Staged reveal |
| 42 | The gradient is a probability residual | `softmax.tex` | Static |
| 43 | Binary logistic regression is the $K=2$ case | `softmax.tex` | Static |
| 44 | A reference class removes redundant parameters | `softmax.tex` | Static |
| 45 | Stable computation uses score differences | `softmax.tex` | Static |
| 46 | Three classes partition the feature plane | `softmax.tex` | Static |
| 47 | Temperature changes concentration | `softmax.tex` | Static |
| 48 | Categorical outputs in vision and language | `softmax.tex` | Static |
| 49 | Softmax also supplies attention weights | `softmax.tex` | Static |
| 50 | One fitting principle, three response models | `closing.tex` | Static |
| 51 | References and further reading | `closing.tex` | Static |
