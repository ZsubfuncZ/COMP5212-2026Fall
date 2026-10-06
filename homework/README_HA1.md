# Hands-On Assigment 1 

# Supervised Learning: Regression and Classification with Real and Synthetic Data

This assignment contains two scalar regression tasks and two binary classification tasks. Each task type is represented by one real dataset and one synthetic dataset. Each task provides approximately 20 raw features and 5,000 labeled observations. 

Select **one** regression task and **one** classification task. **Clearly identify both tasks in your submission.**

For each task, analyze the data, identify potential issues, and design appropriate preprocessing steps. Train and validate models, using controlled comparisons to explain their performance. Your final score will be based on your models’ performance on unseen test data, their training error, and the quality of your technical report.

 **Model selection:**  Basic linear and logistic regression, along with variants using expanded feature sets, are recommended, but you may also use other models.



## 1. Package Structure and Getting Started

```text
.
├── README.md
├── requirements.txt
├── load_example.py
├── manifest.json
└── datasets/
    ├── sarcos_regression/
    │   ├── train.csv
    │   ├── cv_folds.csv
    │   ├── data_dictionary.md
    │   └── metadata.json
    ├── cooling_regression/
    │   ├── train.csv
    │   ├── cv_folds.csv
    │   ├── data_dictionary.md
    │   └── metadata.json
    ├── credit_classification/
    │   ├── train.csv
    │   ├── cv_folds.csv
    │   ├── data_dictionary.md
    │   └── metadata.json
    └── execution_classification/
        ├── train.csv
        ├── cv_folds.csv
        ├── data_dictionary.md
        └── metadata.json
```

Each `train.csv` contains a `sample_id` column, the input features, and one target column. Use `sample_id` only to identify observations; it must not be a model input. Each `cv_folds.csv` contains two columns, `sample_id` and `fold`, with fold numbers from 0 to 4. Align the two files using `sample_id`, rather than relying on row order. The fold number must not be used as a feature either.

**Cross-validation** evaluates a model configuration using five different training–validation splits of the supplied labeled data. Use it to compare models and choose hyperparameters before final testing.

For each selected dataset, the **5,000 provided observations are already assigned to five folds of 1,000 observations each**, numbered **0–4** in `cv_folds.csv`. Keep these assignments and run the following five experiments for each model configuration:

| Experiment | Folds used for training | Fold used for validation | Training observations | Validation observations |
|---|---|---|---:|---:|
| 1 | 1, 2, 3, 4 | 0 | 4,000 | 1,000 |
| 2 | 0, 2, 3, 4 | 1 | 4,000 | 1,000 |
| 3 | 0, 1, 3, 4 | 2 | 4,000 | 1,000 |
| 4 | 0, 1, 2, 4 | 3 | 4,000 | 1,000 |
| 5 | 0, 1, 2, 3 | 4 | 4,000 | 1,000 |

**Train a fresh model from scratch in each experiment**, using the same configuration. Fit all learned preprocessing, including imputation and scaling, only on that experiment's 4,000 training observations, then apply it to the 1,000 validation observations. 

**The instructor's held-out test set is separate from these 5,000 observations.** It is not one of the five folds and must not be used for preprocessing, model selection, or hyperparameter tuning. It is reserved for final evaluation; the final testing mechanism and submission interface will be announced separately.

Each dataset directory also contains `metadata.json`, which lists the input columns, target column, and data checksums. The root-level `manifest.json` records SHA-256 hashes for the data files in this release.

Read the `data_dictionary.md` in each directory before running `load_example.py` to inspect the data and fold assignments. The example script demonstrates data loading and basic checks. Python 3.10 or later is recommended. Run the following commands from the package root:

```bash
python -m pip install -r requirements.txt
python load_example.py
python load_example.py --dataset cooling_regression
```



## 2. Prediction Tasks

| Directory | Task and source | Raw features | Target column | Required prediction |
|---|---|---:|---|---|
| `sarcos_regression` | Real data: robot inverse dynamics | 21 | `torque_1` | A real number |
| `cooling_regression` | Synthetic data: building cooling load | 20 | `cooling_load_kw` | A real number |
| `credit_classification` | Real data: credit card default | 20 | `default_next_month` | Probability of class 1 |
| `execution_classification` | Synthetic data: order execution risk | 20 | `high_slippage` | Probability of class 1 |

The feature counts refer to the raw input variables provided in the files, excluding sample identifiers and targets. One-hot encoding, missingness indicators, and justified feature engineering may increase the model's input dimension. Document these changes in your report.

### 2.1 Robot Joint Torque Regression: SARCOS

**Background:** Controlling a robot requires determining the torques needed to drive its joints from their current states. This task uses real observations from a robot with seven degrees of freedom. The inputs are seven joint positions, seven joint velocities, and seven joint accelerations. 

**Prediction target: ** The target is the torque at the first joint.

**Input feature:** Positions, velocities, and accelerations have different meanings and scales, and the joints may interact. Examine how scaling affects regularized models. Large observations may correspond to real extreme operating conditions. The data come from the [SARCOS dataset provided by Gaussian Processes for Machine Learning](https://gaussianprocess.org/gpml/data/). The target retains the numerical representation used in the original source. Consult the accompanying data dictionary for individual field definitions.

### 2.2 Building Cooling Load Regression: Synthetic Data

**Background:** Cooling load is the rate at which heat must be removed to maintain indoor conditions. This task simulates a building with four zones and predicts its total cooling load in kW. 

**Predition target:** The target is generated from a simplified heat balance.

**Input feature:** There are 4 zones, where each zone has five input variables: area, the outdoor-minus-indoor temperature difference, a heat transfer coefficient, solar irradiance, and internal heat gains.  Interactions between variables have a physical interpretation: for example, area and heat transfer conditions jointly affect heat flow. 

### 2.3 Credit Card Default Classification: Real Data

**Background:** This task uses historical records of credit card customers in some area to predict default in the following month. The observations come from a customer cohort in 2005.

**Prediction taregt:** Whether a customer defaults on their credit card payment in the following month.

**Input feature:** The inputs are credit limit, age, and six months of repayment status, bill amounts, and payment amounts. Of the original dataset's 23 predictors, this assignment omits sex, education, and marital status, leaving 20 variables.

Source: [UCI Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients). 

### 2.4 Order Execution Risk Classification: Synthetic Data

**Background:** In a limit order book, an order may need to consume liquidity at several price levels. Even if the current book appears sufficient, market changes before execution can increase the cost of the trade. 

**Prediction target:** This task predicts whether the order's execution slippage exceeds a specified threshold.

**Input feature:** The inputs include prices and displayed quantities at four levels on each side of the book, giving 16 variables. Order size, order direction, execution delay, and recent volatility bring the total to 20. The target `high_slippage=1` indicates slippage greater than 5 basis points (0.05%); otherwise, the target is 0. See the data dictionary for the definition of slippage and each input.

## 3. Required Experiments

### 3.1 Data Diagnosis

For each task, provide a brief diagnosis covering at least the following:

- The types, meanings, units, or coding conventions of the inputs and target.
- The ranges, missingness rates, skewness, and potentially suspicious observations for numerical variables. For classification tasks, also report class proportions.
- Which variables are suitable as continuous inputs, and which may require categorical encoding or another representation.
- The preprocessing you plan to apply based on these observations, and which variables you will leave unchanged.

### 3.2 Preprocessing and Controlled Comparisons

For each task, select at least **one** justified preprocessing operation and evaluate it in a controlled comparison. Use the same learner, folds, and tuning budget in both conditions, changing only the selected operation as far as possible. You may use the examples below or propose your own:

| Task | Example comparison |
|---|---|
| Robot torque regression | Ridge with and without standardization |
| Building cooling load regression | Two imputation methods, or including versus omitting missingness indicators |
| Credit card default classification | Repayment status as numerical versus categorical inputs |
| Order execution risk classification | Raw prices versus prices expressed relative to the mid-price |

The comparison condition must still include any processing needed to make the model run. For example, when comparing standardization, use the same imputation method in both conditions. Report the results for each fold and the differences between conditions. Explain why the operation helped, had no effect, or reduced performance. 

### 3.3 Baseline Models, Bagging, and an Improvement

Compare at least the following three approaches for each task:

1. **A baseline model.** Use Linear Regression or Ridge for regression, and Logistic Regression for classification. Explain your preprocessing, regularization, and hyperparameter choices.
2. **A bagged version of the baseline.** Fit multiple baseline models to bootstrap samples of the training observations. For regression, average their numerical predictions. For classification, average their predicted probabilities of class 1. Record the number of base models and other settings, and assess whether bagging improves performance or stability.
3. **One improvement.** This may involve feature engineering motivated by the application or another model covered in the course. Explain your choice and use a fair comparison to determine what accounts for any improvement.

When assessing the effect of bagging itself, use the same base-model type and feature representation as in the single-model comparison. If you also change regularization or other settings, describe those changes separately. Include preprocessing for the base models in a reproducible fitting procedure.

**Do not** assume that bagging will help. Distinguish estimation variability due to finite samples from underfitting caused by a model's inability to represent the underlying relationship.

### 3.4 Training Sample Size and Generalization

Choose at least one task and plot a learning curve that compares training and validation performance at no fewer than three training sample sizes. Draw smaller training samples from the training portion of each fold while keeping its validation portion fixed. For classification, pay attention to class proportions when subsampling.

Discuss whether additional training observations continue to improve performance, and whether the observed gaps are more plausibly attributable to model expressiveness, estimation variability, or unpredictability in the data. Avoid drawing conclusions from small differences in a single run.

## 4. Validation and Reporting Results

Use **RMSE** as the primary comparison metric for regression and also report MAE. Use **log loss** as the primary comparison metric for classification and also report ROC-AUC. Check that predicted probabilities are valid. Classification models must output the probability of class 1, rather than only a 0/1 label. Use a consistent numerical clipping rule when calculating log loss and document that rule.

## 5. Submission and Reproducibility

Submit the following materials:

- **An experimental report.** Include data diagnosis, preprocessing comparisons, model comparisons, a learning curve for at least one task, and an interpretation of the results. Put repetitive tables and implementation details in an appendix.
- **Runnable code.** Provide the complete workflow from the original CSV files to predictions, together with an entry point for reproducing the main experiments in the report.
- **Instructions and dependencies.** Document environment setup, execution commands, random seeds, key hyperparameters, and how to predict on new observations. 

Use the supplied data for your experiments. Do not download additional labels from the public source datasets to match observations, augment training, or obtain answers for held-out observations. You may consult the dataset sources, method documentation, and other public materials, but disclose the external resources you use. Because the original labels for the two real datasets are public, this restriction is necessary for the assignment's experiments to remain interpretable.

The mechanism for evaluating models on the instructor's held-out test set and the final submission interface will be announced once the training and testing arrangements are finalized.

**AI tools** are permitted in this assignment, but **you must disclose how you used them**. Include an **AI Use Disclosure** in your report that names the tools used and describes their specific contributions, such as model implementation or deployment, hyperparameter search, and data preprocessing or analysis. Identify the relevant code, experiments, or report sections. If you did not use AI, state this explicitly.

You remain responsible for the correctness of your submission and for explaining your methods and results.

**Report readability contributes to your grade.** Present a clear, logically organized account of your work, use consistent notation, label figures and tables, and explain what the results show. Concise, precise explanations are preferred to unnecessary length, whether or not AI was used.

## 7. References

- [SARCOS dataset](https://gaussianprocess.org/gpml/data/)
- [UCI credit card default dataset and variable descriptions](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)
- [scikit-learn: Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)
- [scikit-learn: Avoiding data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage)
- [scikit-learn: Model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)
