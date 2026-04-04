
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-04 17:00:37
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 1,000
- **Total Features:** 47 (engineered)
- **Delinquency Rate:** 5.40%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 13.97% of total variance
- **PC2:** 11.33% of total variance
- **PC3:** 8.23% of total variance
- **First 5 PCs:** 47.99% of total variance
- **Components for 80% variance:** 1
- **Components for 95% variance:** 1

### Key Insights from PCA

1. **Dimensionality Reduction:** The dataset's 47 features can be effectively 
   reduced to a smaller number of components while retaining most variance.

2. **Feature Relationships:** PCA reveals underlying relationships between different risk factors
   and borrower characteristics.

3. **Risk Patterns:** The principal components help identify natural groupings of borrowers
   based on their risk profiles.


## 🔍 Feature Importance Analysis

This section identifies the most important features for each principal component based on their loadings. Features with higher absolute loadings have more influence on the component.

### PC1 (13.97% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3547 | 📈 Positive (High) | Higher values increase component score |
| 2 | `total_payments_made` | 0.3371 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `on_time_payments` | 0.3359 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `payment_consistency` | 0.3298 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `days_since_last_payment` | -0.3293 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `total_amount_paid` | 0.3026 | 📈 Positive (Medium) | Higher values increase component score |
| 7 | `days_since_disbursement` | 0.2473 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `loan_age_days` | 0.2237 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `program_type_encoded` | 0.2232 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `loan_progress_pct` | 0.2222 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.355)
- `total_payments_made` (loading: 0.337)
- `on_time_payments` (loading: 0.336)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.329)

**Component Statistics:**
- Maximum loading magnitude: 0.3547
- Average loading magnitude: 0.2906
- Loading standard deviation: 0.0548

---

### PC2 (11.33% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `education_value` | 0.4052 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_amount` | 0.3998 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `monthly_payment` | 0.3817 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `current_balance` | 0.3788 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.3640 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `down_payment` | 0.2665 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `payment_to_income_ratio` | 0.1802 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `debt_to_income_ratio` | 0.1705 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `loan_progress_pct` | 0.1092 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `total_payments_made` | -0.1073 | 📉 Negative (Low) | Higher values decrease component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `education_value` (loading: 0.405)
- `loan_amount` (loading: 0.400)
- `monthly_payment` (loading: 0.382)

**Negative Drivers:** Features that decrease this component:
- `total_payments_made` (loading: -0.107)

**Component Statistics:**
- Maximum loading magnitude: 0.4052
- Average loading magnitude: 0.2763
- Loading standard deviation: 0.1239

---

### PC3 (8.23% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `loan_progress_pct` | 0.2979 | 📈 Positive (High) | Higher values increase component score |
| 2 | `days_to_maturity` | -0.2928 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `program_type_encoded` | -0.2555 | 📉 Negative (Medium) | Higher values decrease component score |
| 4 | `loan_age_days` | 0.2420 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `days_since_disbursement` | 0.2293 | 📈 Positive (Low) | Higher values increase component score |
| 6 | `loan_term_months` | -0.2036 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `loan_term_years` | -0.2036 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `total_amount_paid` | -0.2003 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `employment_status_encoded` | -0.1939 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `annual_income_cad` | 0.1888 | 📈 Positive (Low) | Higher values increase component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `loan_progress_pct` (loading: 0.298)
- `loan_age_days` (loading: 0.242)
- `days_since_disbursement` (loading: 0.229)

**Negative Drivers:** Features that decrease this component:
- `days_to_maturity` (loading: -0.293)
- `program_type_encoded` (loading: -0.256)
- `loan_term_months` (loading: -0.204)

**Component Statistics:**
- Maximum loading magnitude: 0.2979
- Average loading magnitude: 0.2308
- Loading standard deviation: 0.0403

---

### PC4 (7.41% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.4062 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.3774 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `debt_to_income_ratio` | 0.3533 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `payment_to_income_ratio` | 0.3531 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `days_to_maturity` | -0.1897 | 📉 Negative (Low) | Higher values decrease component score |
| 6 | `typical_tuition_cad` | 0.1851 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `education_roi` | -0.1844 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `current_balance` | -0.1716 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `loan_term_months` | -0.1683 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `loan_term_years` | -0.1683 | 📉 Negative (Low) | Higher values decrease component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.406)
- `debt_to_income_ratio` (loading: 0.353)
- `payment_to_income_ratio` (loading: 0.353)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.377)
- `days_to_maturity` (loading: -0.190)
- `education_roi` (loading: -0.184)

**Component Statistics:**
- Maximum loading magnitude: 0.4062
- Average loading magnitude: 0.2557
- Loading standard deviation: 0.1018

---

### PC5 (7.06% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `typical_tuition_cad` | 0.4165 | 📈 Positive (High) | Higher values increase component score |
| 2 | `program_difficulty` | 0.3662 | 📈 Positive (High) | Higher values increase component score |
| 3 | `average_starting_salary` | 0.3550 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `education_roi` | -0.3321 | 📉 Negative (Medium) | Higher values decrease component score |
| 5 | `missed_payments` | 0.2304 | 📈 Positive (Low) | Higher values increase component score |
| 6 | `delinquency_rate` | 0.2241 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `avg_late_fee_per_payment` | 0.2241 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `pos_duration` | 0.2010 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `payment_to_income_ratio` | -0.2000 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `debt_to_income_ratio` | -0.1894 | 📉 Negative (Low) | Higher values decrease component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `typical_tuition_cad` (loading: 0.417)
- `program_difficulty` (loading: 0.366)
- `average_starting_salary` (loading: 0.355)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.332)
- `payment_to_income_ratio` (loading: -0.200)
- `debt_to_income_ratio` (loading: -0.189)

**Component Statistics:**
- Maximum loading magnitude: 0.4165
- Average loading magnitude: 0.2739
- Loading standard deviation: 0.0841

---



## 📈 Generated Visualizations

All interactive charts and reports have been saved to the `C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\static\eda_outputs` directory:

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
