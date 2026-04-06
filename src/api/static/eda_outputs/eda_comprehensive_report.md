
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-06 09:20:43
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 1,000
- **Total Features:** 54 (engineered)
- **Delinquency Rate:** 74.40%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 13.05% of total variance
- **PC2:** 9.71% of total variance
- **PC3:** 7.85% of total variance
- **First 5 PCs:** 44.49% of total variance
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

### PC1 (13.05% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3277 | 📈 Positive (High) | Higher values increase component score |
| 2 | `total_payments_made` | 0.3175 | 📈 Positive (High) | Higher values increase component score |
| 3 | `late_payments` | 0.3098 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `on_time_payments` | 0.3073 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `total_amount_paid` | 0.2790 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `days_since_last_payment` | -0.2682 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `loan_progress_pct` | 0.2570 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `days_since_disbursement` | 0.2543 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `loan_age_days` | 0.2501 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `payment_consistency` | 0.2162 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.328)
- `total_payments_made` (loading: 0.318)
- `late_payments` (loading: 0.310)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.268)

**Component Statistics:**
- Maximum loading magnitude: 0.3277
- Average loading magnitude: 0.2787
- Loading standard deviation: 0.0359

---

### PC2 (9.71% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `current_balance` | 0.3845 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_amount` | 0.3716 | 📈 Positive (High) | Higher values increase component score |
| 3 | `education_value` | 0.3631 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `monthly_payment` | 0.3402 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.3170 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `payment_to_income_ratio` | 0.2496 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `debt_to_income_ratio` | 0.2466 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `down_payment` | 0.2087 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `employment_status_encoded` | 0.1538 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `late_payments` | -0.1414 | 📉 Negative (Low) | Higher values decrease component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `current_balance` (loading: 0.384)
- `loan_amount` (loading: 0.372)
- `education_value` (loading: 0.363)

**Negative Drivers:** Features that decrease this component:
- `late_payments` (loading: -0.141)

**Component Statistics:**
- Maximum loading magnitude: 0.3845
- Average loading magnitude: 0.2776
- Loading standard deviation: 0.0903

---

### PC3 (7.85% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `days_to_maturity` | 0.3100 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_term_months` | 0.2797 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `loan_term_years` | 0.2797 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `long_term_loan_risk` | 0.2587 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `employment_status_encoded` | 0.2365 | 📈 Positive (Low) | Higher values increase component score |
| 6 | `annual_income_cad` | -0.2338 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `loan_progress_pct` | -0.2050 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `low_income_risk` | 0.2044 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `debt_to_income_ratio` | 0.1839 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `program_type_encoded` | 0.1810 | 📈 Positive (Low) | Higher values increase component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `days_to_maturity` (loading: 0.310)
- `loan_term_months` (loading: 0.280)
- `loan_term_years` (loading: 0.280)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.234)
- `loan_progress_pct` (loading: -0.205)

**Component Statistics:**
- Maximum loading magnitude: 0.3100
- Average loading magnitude: 0.2373
- Loading standard deviation: 0.0441

---

### PC4 (7.05% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `typical_tuition_cad` | 0.4491 | 📈 Positive (High) | Higher values increase component score |
| 2 | `program_difficulty` | 0.4091 | 📈 Positive (High) | Higher values increase component score |
| 3 | `average_starting_salary` | 0.3848 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `high_difficulty_program` | 0.3816 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `education_roi` | -0.3075 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `loan_term_years` | 0.1863 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `loan_term_months` | 0.1863 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `long_term_loan_risk` | 0.1822 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `days_to_maturity` | 0.1790 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `program_type_encoded` | 0.1752 | 📈 Positive (Low) | Higher values increase component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `typical_tuition_cad` (loading: 0.449)
- `program_difficulty` (loading: 0.409)
- `average_starting_salary` (loading: 0.385)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.307)

**Component Statistics:**
- Maximum loading magnitude: 0.4491
- Average loading magnitude: 0.2841
- Loading standard deviation: 0.1133

---

### PC5 (6.83% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.4060 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.3920 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `low_income_risk` | 0.3570 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `payment_to_income_ratio` | 0.2830 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `debt_to_income_ratio` | 0.2824 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `current_balance` | -0.1985 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `loan_term_months` | -0.1810 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `loan_term_years` | -0.1810 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `loan_amount` | -0.1774 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `long_term_loan_risk` | -0.1750 | 📉 Negative (Low) | Higher values decrease component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.406)
- `low_income_risk` (loading: 0.357)
- `payment_to_income_ratio` (loading: 0.283)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.392)
- `current_balance` (loading: -0.198)
- `loan_term_months` (loading: -0.181)

**Component Statistics:**
- Maximum loading magnitude: 0.4060
- Average loading magnitude: 0.2633
- Loading standard deviation: 0.0939

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
