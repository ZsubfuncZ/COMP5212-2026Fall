# Instructor test data

Each of the four `data/<dataset>/test.csv` files contains 3,000 labeled held-out examples. The columns match the corresponding training CSV, including the target and `sample_id`. Keep these files and benchmark results private until final evaluation.

These are the original held-out files, recovered after confirming that all four training CSVs in your revised HA1.zip match the original files byte for byte. They are not split out of the students' 5,000 training observations. There is no overlap in sample IDs or exact feature vectors between the provided training and test sets, and feature vectors are unique within each split. Manifest hashes allow the files to be checked.

## Use with the revised scripts

Extract this folder beside `train.py`, `test.py`, and `datasets/`. Implement a method in `train.py`, then run in the same Python process:

```python
import train as training
import test as testing

dataset = "cooling_regression"
model = training.train(f"datasets/{dataset}/train.csv", method="baseline", seed=2026)
report = testing.test(f"instructor_test_data/data/{dataset}/test.csv", model)
print(report["metrics"])
```

The supplied evaluator computes MSE, RMSE, MAE, and R² for regression; log loss, ROC-AUC, accuracy, and F1 for classification. A model is passed in memory, so no save/load implementation is required. Use a trusted, instructor-controlled copy of the evaluator when marking. Choose preprocessing, models, and hyperparameters using training cross-validation before opening test results.

## Sampling and distribution

- Cooling and execution: independent draws from the same fixed generators as training, using separate seeds. Missingness and observation noise follow the same mechanisms.
- Credit: disjoint stratified subsets of the same deduplicated UCI credit-card cohort. Training and test positive rates are approximately 22.04% and 22.03%. This is a within-cohort evaluation, not a future-time test.
- SARCOS: the original GPML training and test source files, respectively. The selected test set excludes any exact feature vector in the selected training set. This follows the benchmark split, rather than a fresh random split of one pooled source table.

The real datasets are observational: their provenance does not establish strict statistical independence. If a literal i.i.d. guarantee is essential, use the synthetic tasks. `reproduction_config.json` records original seeds; `data_audit.json` records dimensions, missingness, fold counts, and overlap checks. No dataset was chosen or resampled on the basis of the new model results.
