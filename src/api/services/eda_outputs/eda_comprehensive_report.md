
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-06 21:15:33
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 1,000
- **Total Features:** 54 (engineered)
- **Delinquency Rate:** 46.50%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 13.38% of total variance
- **PC2:** 9.96% of total variance
- **PC3:** 7.93% of total variance
- **First 5 PCs:** 45.62% of total variance
- **Components for 80% variance:** 1
- **Components for 95% variance:** 1

### Key Insights from PCA

1. **Dimensionality Reduction:** The dataset's 54 features can be effectively 
   reduced to a smaller number of components while retaining most variance.

2. **Feature Relationships:** PCA reveals underlying relationships between different risk factors
   and borrower characteristics.

3. **Risk Patterns:** The principal components help identify natural groupings of borrowers
   based on their risk profiles.


## 🔍 Feature Importance Analysis

This section identifies the most important features for each principal component based on their loadings. Features with higher absolute loadings have more influence on the component.

### PC1 (13.38% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3313 | 📈 Positive (High) | Higher values increase component score |
| 2 | `total_payments_made` | 0.3228 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `late_payments` | 0.3172 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `on_time_payments` | 0.3135 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `total_amount_paid` | 0.2953 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `days_since_last_payment` | -0.2816 | 📉 Negative (Medium) | Higher values decrease component score |
| 7 | `payment_consistency` | 0.2338 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `program_type_encoded` | 0.2085 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `days_since_disbursement` | 0.2016 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `loan_progress_pct` | 0.1983 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.331)
- `total_payments_made` (loading: 0.323)
- `late_payments` (loading: 0.317)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.282)

**Component Statistics:**
- Maximum loading magnitude: 0.3313
- Average loading magnitude: 0.2704
- Loading standard deviation: 0.0541

---

### PC2 (9.96% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `loan_amount` | 0.3726 | 📈 Positive (High) | Higher values increase component score |
| 2 | `education_value` | 0.3724 | 📈 Positive (High) | Higher values increase component score |
| 3 | `current_balance` | 0.3570 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `monthly_payment` | 0.3544 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.3311 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `down_payment` | 0.2394 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `payment_to_income_ratio` | 0.2246 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `debt_to_income_ratio` | 0.2200 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `total_payments_made` | -0.1323 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `on_time_payments` | -0.1304 | 📉 Negative (Low) | Higher values decrease component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `loan_amount` (loading: 0.373)
- `education_value` (loading: 0.372)
- `current_balance` (loading: 0.357)

**Negative Drivers:** Features that decrease this component:
- `total_payments_made` (loading: -0.132)
- `on_time_payments` (loading: -0.130)

**Component Statistics:**
- Maximum loading magnitude: 0.3726
- Average loading magnitude: 0.2734
- Loading standard deviation: 0.0962

---

### PC3 (7.93% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.3048 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.2995 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `low_income_risk` | 0.2667 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `debt_to_income_ratio` | 0.2533 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_type_encoded` | 0.2418 | 📈 Positive (Low) | Higher values increase component score |
| 6 | `payment_to_income_ratio` | 0.2322 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `average_starting_salary` | 0.2287 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `days_to_maturity` | 0.2239 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `loan_progress_pct` | -0.2189 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `low_employment_rate` | -0.2181 | 📉 Negative (Low) | Higher values decrease component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.305)
- `low_income_risk` (loading: 0.267)
- `debt_to_income_ratio` (loading: 0.253)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.300)
- `loan_progress_pct` (loading: -0.219)
- `low_employment_rate` (loading: -0.218)

**Component Statistics:**
- Maximum loading magnitude: 0.3048
- Average loading magnitude: 0.2488
- Loading standard deviation: 0.0320

---

### PC4 (7.37% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `loan_term_years` | 0.3640 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_term_months` | 0.3640 | 📈 Positive (High) | Higher values increase component score |
| 3 | `days_to_maturity` | 0.3445 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `long_term_loan_risk` | 0.3334 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `employment_status_encoded` | -0.2789 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `annual_income_cad` | 0.2693 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `low_income_risk` | -0.2439 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `current_balance` | 0.2169 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `payment_to_income_ratio` | -0.1928 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `debt_to_income_ratio` | -0.1754 | 📉 Negative (Low) | Higher values decrease component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `loan_term_years` (loading: 0.364)
- `loan_term_months` (loading: 0.364)
- `days_to_maturity` (loading: 0.344)

**Negative Drivers:** Features that decrease this component:
- `employment_status_encoded` (loading: -0.279)
- `low_income_risk` (loading: -0.244)
- `payment_to_income_ratio` (loading: -0.193)

**Component Statistics:**
- Maximum loading magnitude: 0.3640
- Average loading magnitude: 0.2783
- Loading standard deviation: 0.0707

---

### PC5 (6.98% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `typical_tuition_cad` | 0.4150 | 📈 Positive (High) | Higher values increase component score |
| 2 | `program_difficulty` | 0.3910 | 📈 Positive (High) | Higher values increase component score |
| 3 | `high_difficulty_program` | 0.3722 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `education_roi` | -0.3640 | 📉 Negative (Medium) | Higher values decrease component score |
| 5 | `average_starting_salary` | 0.3275 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `loan_to_education_value_ratio` | -0.1974 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `ltv_ratio` | -0.1974 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `pos_duration` | 0.1822 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `high_ltv_risk` | -0.1643 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `job_market_outlook_encoded` | -0.1526 | 📉 Negative (Low) | Higher values decrease component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `typical_tuition_cad` (loading: 0.415)
- `program_difficulty` (loading: 0.391)
- `high_difficulty_program` (loading: 0.372)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.364)
- `loan_to_education_value_ratio` (loading: -0.197)
- `ltv_ratio` (loading: -0.197)

**Component Statistics:**
- Maximum loading magnitude: 0.4150
- Average loading magnitude: 0.2764
- Loading standard deviation: 0.1060

---



## 📈 Generated Visualizations

All interactive charts and reports have been saved to the `C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\services\eda_outputs` directory:

### 📊 Interactive Visualizations
1. **pca_scree_plot.html** - Variance explained by each component
2. **pca_scatter_plot.html** - PC1 vs PC2 scatter plot colored by risk
3. **pca_biplot_pc1_vs_pc2.html** - Biplot showing feature loading vectors
4. **pca_feature_contributions.html** - Feature contributions to each PC
5. **feature_correlation_heatmap.html** - Correlation matrix of original features
6. **pca_clustering_k3.html** - K-means clustering on PCA components

### 📄 Analysis Reports
7. **eda_comprehensive_report.md** - Markdown version of this report
8. **eda_comprehensive_report.html** - HTML version with enhanced styling

## Business Implications

### Risk Segmentation
The PCA analysis reveals natural risk segments that can be used for:
- Targeted intervention strategies
- Customized loan products
- Proactive risk management

### Feature Importance
The principal components identify the most important combinations of features
for delinquency prediction, enabling more efficient risk assessment.

### Portfolio Management
Understanding the principal components helps in:
- Diversification strategies
- Risk concentration analysis
- Performance monitoring

---
*This report was generated automatically by the Exploratory Data Analysis system.*
