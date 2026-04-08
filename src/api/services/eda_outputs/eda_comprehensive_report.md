
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-08 13:36:01
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 1,000
- **Total Features:** 54 (engineered)
- **Delinquency Rate:** 48.90%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 13.72% of total variance
- **PC2:** 9.84% of total variance
- **PC3:** 7.97% of total variance
- **First 5 PCs:** 45.77% of total variance
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

### PC1 (13.72% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3249 | 📈 Positive (High) | Higher values increase component score |
| 2 | `total_payments_made` | 0.3082 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `late_payments` | 0.3038 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `on_time_payments` | 0.2997 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `days_since_last_payment` | -0.2785 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `total_amount_paid` | 0.2779 | 📈 Positive (Medium) | Higher values increase component score |
| 7 | `payment_consistency` | 0.2199 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `days_since_disbursement` | 0.2173 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `loan_progress_pct` | 0.2140 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `loan_age_days` | 0.2049 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.325)
- `total_payments_made` (loading: 0.308)
- `late_payments` (loading: 0.304)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.279)

**Component Statistics:**
- Maximum loading magnitude: 0.3249
- Average loading magnitude: 0.2649
- Loading standard deviation: 0.0460

---

### PC2 (9.84% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `loan_amount` | 0.3225 | 📈 Positive (Medium) | Higher values increase component score |
| 2 | `education_value` | 0.3207 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `monthly_payment` | 0.3098 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `current_balance` | 0.3096 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.2918 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `payment_to_income_ratio` | 0.2784 | 📈 Positive (Medium) | Higher values increase component score |
| 7 | `debt_to_income_ratio` | 0.2727 | 📈 Positive (Medium) | Higher values increase component score |
| 8 | `down_payment` | 0.2014 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `employment_status_encoded` | 0.1975 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `annual_income_cad` | -0.1861 | 📉 Negative (Low) | Higher values decrease component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `loan_amount` (loading: 0.322)
- `education_value` (loading: 0.321)
- `monthly_payment` (loading: 0.310)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.186)

**Component Statistics:**
- Maximum loading magnitude: 0.3225
- Average loading magnitude: 0.2691
- Loading standard deviation: 0.0538

---

### PC3 (7.97% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `days_to_maturity` | 0.3697 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_term_years` | 0.3420 | 📈 Positive (High) | Higher values increase component score |
| 3 | `loan_term_months` | 0.3420 | 📈 Positive (High) | Higher values increase component score |
| 4 | `long_term_loan_risk` | 0.3240 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `loan_progress_pct` | -0.2572 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `current_balance` | 0.2524 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `loan_amount` | 0.1880 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `loan_age_days` | -0.1581 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `days_since_disbursement` | -0.1547 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `education_value` | 0.1530 | 📈 Positive (Low) | Higher values increase component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `days_to_maturity` (loading: 0.370)
- `loan_term_years` (loading: 0.342)
- `loan_term_months` (loading: 0.342)

**Negative Drivers:** Features that decrease this component:
- `loan_progress_pct` (loading: -0.257)
- `loan_age_days` (loading: -0.158)
- `days_since_disbursement` (loading: -0.155)

**Component Statistics:**
- Maximum loading magnitude: 0.3697
- Average loading magnitude: 0.2541
- Loading standard deviation: 0.0866

---

### PC4 (7.44% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `typical_tuition_cad` | 0.4184 | 📈 Positive (High) | Higher values increase component score |
| 2 | `program_difficulty` | 0.3904 | 📈 Positive (High) | Higher values increase component score |
| 3 | `average_starting_salary` | 0.3638 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `high_difficulty_program` | 0.3577 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `education_roi` | -0.3217 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `pos_duration` | 0.1750 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `loan_term_years` | 0.1639 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `loan_term_months` | 0.1639 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `long_term_loan_risk` | 0.1487 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `employment_status_encoded` | -0.1396 | 📉 Negative (Low) | Higher values decrease component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `typical_tuition_cad` (loading: 0.418)
- `program_difficulty` (loading: 0.390)
- `average_starting_salary` (loading: 0.364)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.322)
- `employment_status_encoded` (loading: -0.140)

**Component Statistics:**
- Maximum loading magnitude: 0.4184
- Average loading magnitude: 0.2643
- Loading standard deviation: 0.1148

---

### PC5 (6.80% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.4244 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.4106 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `low_income_risk` | 0.3739 | 📈 Positive (High) | Higher values increase component score |
| 4 | `debt_to_income_ratio` | 0.2975 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `payment_to_income_ratio` | 0.2793 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `education_value` | -0.1812 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `down_payment` | -0.1730 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `program_duration_years` | -0.1716 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `monthly_payment` | -0.1619 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `loan_amount` | -0.1542 | 📉 Negative (Low) | Higher values decrease component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.424)
- `low_income_risk` (loading: 0.374)
- `debt_to_income_ratio` (loading: 0.298)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.411)
- `education_value` (loading: -0.181)
- `down_payment` (loading: -0.173)

**Component Statistics:**
- Maximum loading magnitude: 0.4244
- Average loading magnitude: 0.2628
- Loading standard deviation: 0.1089

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
