
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-07 13:02:29
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 5,000
- **Total Features:** 54 (engineered)
- **Delinquency Rate:** 48.76%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 13.26% of total variance
- **PC2:** 9.55% of total variance
- **PC3:** 7.73% of total variance
- **First 5 PCs:** 44.69% of total variance
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

### PC1 (13.26% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3338 | 📈 Positive (High) | Higher values increase component score |
| 2 | `total_payments_made` | 0.3262 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `late_payments` | 0.3199 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `on_time_payments` | 0.3163 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `total_amount_paid` | 0.2985 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `days_since_last_payment` | -0.2784 | 📉 Negative (Medium) | Higher values decrease component score |
| 7 | `payment_consistency` | 0.2268 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `program_type_encoded` | 0.2141 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `days_since_disbursement` | 0.2032 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `job_market_outlook_encoded` | 0.1991 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.334)
- `total_payments_made` (loading: 0.326)
- `late_payments` (loading: 0.320)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.278)

**Component Statistics:**
- Maximum loading magnitude: 0.3338
- Average loading magnitude: 0.2716
- Loading standard deviation: 0.0550

---

### PC2 (9.55% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `loan_amount` | 0.3643 | 📈 Positive (High) | Higher values increase component score |
| 2 | `education_value` | 0.3588 | 📈 Positive (High) | Higher values increase component score |
| 3 | `monthly_payment` | 0.3469 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `current_balance` | 0.3409 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.3168 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `down_payment` | 0.2071 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `payment_to_income_ratio` | 0.1949 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `debt_to_income_ratio` | 0.1875 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `total_payments_made` | -0.1637 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `late_payments` | -0.1625 | 📉 Negative (Low) | Higher values decrease component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `loan_amount` (loading: 0.364)
- `education_value` (loading: 0.359)
- `monthly_payment` (loading: 0.347)

**Negative Drivers:** Features that decrease this component:
- `total_payments_made` (loading: -0.164)
- `late_payments` (loading: -0.162)

**Component Statistics:**
- Maximum loading magnitude: 0.3643
- Average loading magnitude: 0.2643
- Loading standard deviation: 0.0875

---

### PC3 (7.73% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `days_to_maturity` | 0.3771 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_term_months` | 0.3366 | 📈 Positive (High) | Higher values increase component score |
| 3 | `loan_term_years` | 0.3366 | 📈 Positive (High) | Higher values increase component score |
| 4 | `long_term_loan_risk` | 0.3104 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `loan_progress_pct` | -0.2701 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `debt_to_income_ratio` | 0.2298 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `employment_status_encoded` | 0.2215 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `annual_income_cad` | -0.2096 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `payment_to_income_ratio` | 0.2027 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `low_income_risk` | 0.1754 | 📈 Positive (Low) | Higher values increase component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `days_to_maturity` (loading: 0.377)
- `loan_term_months` (loading: 0.337)
- `loan_term_years` (loading: 0.337)

**Negative Drivers:** Features that decrease this component:
- `loan_progress_pct` (loading: -0.270)
- `annual_income_cad` (loading: -0.210)

**Component Statistics:**
- Maximum loading magnitude: 0.3771
- Average loading magnitude: 0.2670
- Loading standard deviation: 0.0691

---

### PC4 (7.34% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.3784 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.3675 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `low_income_risk` | 0.3294 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `payment_to_income_ratio` | 0.2763 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `debt_to_income_ratio` | 0.2712 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `loan_term_months` | -0.1997 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `loan_term_years` | -0.1997 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `long_term_loan_risk` | -0.1884 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `current_balance` | -0.1874 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `days_to_maturity` | -0.1832 | 📉 Negative (Low) | Higher values decrease component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.378)
- `low_income_risk` (loading: 0.329)
- `payment_to_income_ratio` (loading: 0.276)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.367)
- `loan_term_months` (loading: -0.200)
- `loan_term_years` (loading: -0.200)

**Component Statistics:**
- Maximum loading magnitude: 0.3784
- Average loading magnitude: 0.2581
- Loading standard deviation: 0.0777

---

### PC5 (6.81% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `typical_tuition_cad` | 0.4390 | 📈 Positive (High) | Higher values increase component score |
| 2 | `program_difficulty` | 0.4134 | 📈 Positive (High) | Higher values increase component score |
| 3 | `high_difficulty_program` | 0.3818 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `average_starting_salary` | 0.3701 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `education_roi` | -0.3138 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `employment_status_encoded` | 0.1973 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `annual_income_cad` | -0.1911 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `low_income_risk` | 0.1768 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `pos_duration` | 0.1729 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `program_type_encoded` | 0.1384 | 📈 Positive (Low) | Higher values increase component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `typical_tuition_cad` (loading: 0.439)
- `program_difficulty` (loading: 0.413)
- `high_difficulty_program` (loading: 0.382)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.314)
- `annual_income_cad` (loading: -0.191)

**Component Statistics:**
- Maximum loading magnitude: 0.4390
- Average loading magnitude: 0.2794
- Loading standard deviation: 0.1153

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
