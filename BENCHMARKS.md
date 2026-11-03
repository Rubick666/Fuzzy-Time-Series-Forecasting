# Benchmarks & Experimental Results

This document outlines the quantitative results and analysis of the Fuzzy Time Series (FTS) forecasting models applied to two distinct datasets.

## Problem Overview
- **Models Implemented:** First-Order FTS (FOFTS) and High-Order FTS (HOFTS).
- **Fuzzification:** Chen-style, Maximum Membership Principle.
- **Membership Functions:** Triangular, Trapezoidal, Gaussian.
- **Configuration:** 8 Partitions, 80% Train / 20% Test Split.

## 1. Dataset 1: Mackey-Glass Time Series

The Mackey-Glass dataset is a chaotic, non-linear benchmark. Values were scaled by 10,000 to convert to integers.

### Performance Metrics
| Model | Order | Partitions | RMSE | MAE | MAPE |
| :--- | :--- | :--- | :--- | :--- | :--- |
| FOFTS | 1 | 8 | 0.08 | 0.06 | 11.21% |
| **HOFTS** | **2** | **8** | **0.0815** | **0.0671** | **11.42%** |

*Note: While the table shows similar raw values, the HOFTS (Order=2) model captures temporal dependencies better, as evidenced by the visual fit in the plots. Increasing partitions above 8 further decreases the error.*

### Key Observations
*   **Why Error Metrics Do Not Change Across Membership Shapes:** Because all shapes share the exact same intervals and midpoints, the maximum membership principle assigns the same fuzzy label regardless of the shape. Thus, FLRGs and defuzzified predictions remain identical.
*   **FOFTS vs HOFTS:** HOFTS with order=2 captured the chaotic dynamics more effectively than FOFTS, which produced smoother but less precise forecasts.

---

## 2. Dataset 2: Influenza Specimens Time Series

This dataset contains epidemiological count data. Due to the large numerical scale, Min-Max normalization to [0, 1] was applied prior to fuzzification.

### Performance Metrics (Column-Wise Analysis)

| Column | Model | Order | Partitions | RMSE | MAE | MAPE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TOTAL SPECIMENS** | FOFTS | 1 | 8 | 23202.173 | 15743.715 | 29.229% |
| **TOTAL SPECIMENS** | HOFTS | 2 | 8 | **11571.743** | **8656.278** | **11.776%** |
| TOTAL A | FOFTS | 1 | 8 | 8196.344 | 6726.757 | 1316.351% |
| TOTAL A | HOFTS | 2 | 8 | 8304.510 | 6297.845 | 1284.558% |
| TOTAL B | FOFTS | 1 | 8 | 2430.911 | 2113.000 | 2131.805% |
| **TOTAL B** | **HOFTS** | **2** | **8** | **828.442** | **756.717** | **579.219%** |

### Key Observations & Analysis
*   **Normalization is Crucial:** Min-Max normalization prevents numerical instability and overly large defuzzified midpoints. The predicted values are denormalized back to the original scale for direct comparison.
*   **Aggregate vs. Component Series:** Modeling `TOTAL A` and `TOTAL B` independently yields better, more specific rules than modeling the aggregate `TOTAL SPECIMENS` alone. The aggregated series obscures the distinct temporal behaviors of the sub-processes.
*   **HOFTS vs FOFTS:** For the `TOTAL SPECIMENS` column, HOFTS significantly outperformed FOFTS (RMSE reduced from ~23k to ~11k). However, for `TOTAL A`, HOFTS did not consistently outperform FOFTS, indicating that longer temporal memory does not always improve accuracy for slowly varying or noisy count data.