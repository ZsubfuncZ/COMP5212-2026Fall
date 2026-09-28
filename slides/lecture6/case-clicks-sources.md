# Click prediction case: source and review

Primary source: He et al. (2014), *Practical Lessons from Predicting Clicks on Ads at Facebook*, ADKDD.

- Author-hosted PDF: https://quinonero.net/Publications/predicting-clicks-facebook.pdf
- Publisher DOI: https://doi.org/10.1145/2648584.2648589
- Meta publication record: https://ai.meta.com/research/publications/practical-lessons-from-predicting-clicks-on-ads-at-facebook/

Verified September 24, 2026 from the full primary PDF.

| Slide element | Exact location |
|---|---|
| Architecture, supervised leaf encoding, linear classifier | Figure 1 (p. 2); Section 3.1 (p. 3) |
| Evaluation dates, normalized entropy | Section 2 (p. 2), equation (1) |
| Published ratios: 100, 99.43, 96.58 | Table 1 (p. 4) |
| Feature confidentiality; sample-count confidentiality | Sections 5.2 (p. 7), 6 (p. 8) |

The chart transcribes the table, with no simulated performance. Its horizontal axis starts at zero. 3.42% is computed against trees alone; relative to LR the reduction is approximately 2.87%. The abstract and surrounding prose inconsistently state an improvement exceeding 3% against both baselines, so those claims are not repeated. Results are historical offline prediction comparisons, not a causal estimate of revenue or click lift. No current architecture or confirmed production-deployment claim is made. The original schematic is editable and does not represent disclosed proprietary feature definitions.

Teaching plan: first connect tree feature construction to the previous logistic-regression lecture; reveal its mathematical form. Then compare published loss ratios with their normalization explicit. Allow approximately four minutes total.
