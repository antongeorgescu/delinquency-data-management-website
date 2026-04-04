
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-04 16:34:13
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 1,000
- **Total Features:** 47 (engineered)
- **Delinquency Rate:** 4.00%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 14.60% of total variance
- **PC2:** 11.41% of total variance
- **PC3:** 7.92% of total variance
- **First 5 PCs:** 48.17% of total variance
- **Components for 80% variance:** 13
- **Components for 95% variance:** 22

### Key Insights from PCA

1. **Dimensionality Reduction:** The dataset's 47 features can be effectively 
   reduced to a smaller number of components while retaining most variance.

2. **Feature Relationships:** PCA reveals underlying relationships between different risk factors
   and borrower characteristics.

3. **Risk Patterns:** The principal components help identify natural groupings of borrowers
   based on their risk profiles.


## 🔍 Feature Importance Analysis

This section identifies the most important features for each principal component based on their loadings. Features with higher absolute loadings have more influence on the component.

### PC1 (14.60% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3359 | 📈 Positive (High) | Higher values increase component score |
| 2 | `total_payments_made` | 0.3095 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `days_since_last_payment` | -0.3091 | 📉 Negative (Medium) | Higher values decrease component score |
| 4 | `on_time_payments` | 0.3085 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `payment_consistency` | 0.3081 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `total_amount_paid` | 0.2706 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `days_since_disbursement` | 0.2498 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `loan_age_days` | 0.2385 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `loan_progress_pct` | 0.2295 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `program_type_encoded` | 0.1997 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.336)
- `total_payments_made` (loading: 0.309)
- `on_time_payments` (loading: 0.309)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.309)

**Component Statistics:**
- Maximum loading magnitude: 0.3359
- Average loading magnitude: 0.2759
- Loading standard deviation: 0.0447

---

### PC2 (11.41% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `loan_amount` | 0.3670 | 📈 Positive (High) | Higher values increase component score |
| 2 | `education_value` | 0.3669 | 📈 Positive (High) | Higher values increase component score |
| 3 | `current_balance` | 0.3650 | 📈 Positive (High) | Higher values increase component score |
| 4 | `monthly_payment` | 0.3429 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.3204 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `down_payment` | 0.2332 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `payment_to_income_ratio` | 0.2283 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `debt_to_income_ratio` | 0.2258 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `total_payments_made` | -0.1754 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `on_time_payments` | -0.1754 | 📉 Negative (Low) | Higher values decrease component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `loan_amount` (loading: 0.367)
- `education_value` (loading: 0.367)
- `current_balance` (loading: 0.365)

**Negative Drivers:** Features that decrease this component:
- `total_payments_made` (loading: -0.175)
- `on_time_payments` (loading: -0.175)

**Component Statistics:**
- Maximum loading magnitude: 0.3670
- Average loading magnitude: 0.2800
- Loading standard deviation: 0.0800

---

### PC3 (7.92% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `days_to_maturity` | 0.4209 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_term_months` | 0.3652 | 📈 Positive (High) | Higher values increase component score |
| 3 | `loan_term_years` | 0.3652 | 📈 Positive (High) | Higher values increase component score |
| 4 | `loan_progress_pct` | -0.3007 | 📉 Negative (Medium) | Higher values decrease component score |
| 5 | `typical_tuition_cad` | -0.2289 | 📉 Negative (Low) | Higher values decrease component score |
| 6 | `average_starting_salary` | -0.2025 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `program_difficulty` | -0.1969 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `loan_age_days` | -0.1956 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `education_roi` | 0.1767 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `days_since_disbursement` | -0.1732 | 📉 Negative (Low) | Higher values decrease component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `days_to_maturity` (loading: 0.421)
- `loan_term_months` (loading: 0.365)
- `loan_term_years` (loading: 0.365)

**Negative Drivers:** Features that decrease this component:
- `loan_progress_pct` (loading: -0.301)
- `typical_tuition_cad` (loading: -0.229)
- `average_starting_salary` (loading: -0.202)

**Component Statistics:**
- Maximum loading magnitude: 0.4209
- Average loading magnitude: 0.2626
- Loading standard deviation: 0.0922

---

### PC4 (7.49% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `typical_tuition_cad` | 0.3678 | 📈 Positive (High) | Higher values increase component score |
| 2 | `average_starting_salary` | 0.3173 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `program_difficulty` | 0.2952 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `employment_status_encoded` | 0.2756 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `education_roi` | -0.2626 | 📉 Negative (Low) | Higher values decrease component score |
| 6 | `annual_income_cad` | -0.2572 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `program_type_encoded` | 0.2530 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `debt_to_income_ratio` | 0.2435 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `payment_to_income_ratio` | 0.2381 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `total_amount_paid` | 0.1657 | 📈 Positive (Low) | Higher values increase component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `typical_tuition_cad` (loading: 0.368)
- `average_starting_salary` (loading: 0.317)
- `program_difficulty` (loading: 0.295)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.263)
- `annual_income_cad` (loading: -0.257)

**Component Statistics:**
- Maximum loading magnitude: 0.3678
- Average loading magnitude: 0.2676
- Loading standard deviation: 0.0533

---

### PC5 (6.75% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.4302 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.4085 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `debt_to_income_ratio` | 0.3396 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `payment_to_income_ratio` | 0.3375 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `average_starting_salary` | -0.2315 | 📉 Negative (Low) | Higher values decrease component score |
| 6 | `typical_tuition_cad` | -0.2260 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `program_difficulty` | -0.2074 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `delinquency_rate` | 0.1905 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `avg_late_fee_per_payment` | 0.1905 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `missed_payments` | 0.1821 | 📈 Positive (Low) | Higher values increase component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.430)
- `debt_to_income_ratio` (loading: 0.340)
- `payment_to_income_ratio` (loading: 0.338)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.408)
- `average_starting_salary` (loading: -0.232)
- `typical_tuition_cad` (loading: -0.226)

**Component Statistics:**
- Maximum loading magnitude: 0.4302
- Average loading magnitude: 0.2744
- Loading standard deviation: 0.0953

---



## 📈 Generated Visualizations

All interactive charts and reports have been saved to the `eda_outputs` directory:

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
