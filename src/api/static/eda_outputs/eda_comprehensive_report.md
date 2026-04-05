
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-05 16:57:58
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 1,000
- **Total Features:** 54 (engineered)
- **Delinquency Rate:** 5.30%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 12.98% of total variance
- **PC2:** 9.37% of total variance
- **PC3:** 8.33% of total variance
- **First 5 PCs:** 45.16% of total variance
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

### PC1 (12.98% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3288 | 📈 Positive (High) | Higher values increase component score |
| 2 | `days_since_last_payment` | -0.3026 | 📉 Negative (Medium) | Higher values decrease component score |
| 3 | `payment_consistency` | 0.3011 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `total_payments_made` | 0.2800 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `on_time_payments` | 0.2786 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `total_amount_paid` | 0.2460 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `days_since_disbursement` | 0.2385 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `loan_progress_pct` | 0.2351 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `loan_age_days` | 0.2347 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `education_value` | 0.1882 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.329)
- `payment_consistency` (loading: 0.301)
- `total_payments_made` (loading: 0.280)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.303)

**Component Statistics:**
- Maximum loading magnitude: 0.3288
- Average loading magnitude: 0.2634
- Loading standard deviation: 0.0421

---

### PC2 (9.37% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `education_value` | 0.3469 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_amount` | 0.3424 | 📈 Positive (High) | Higher values increase component score |
| 3 | `current_balance` | 0.3419 | 📈 Positive (High) | Higher values increase component score |
| 4 | `monthly_payment` | 0.3236 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.3066 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `down_payment` | 0.2259 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `on_time_payments` | -0.2240 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `total_payments_made` | -0.2235 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `total_amount_paid` | -0.2001 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `debt_to_income_ratio` | 0.1822 | 📈 Positive (Low) | Higher values increase component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `education_value` (loading: 0.347)
- `loan_amount` (loading: 0.342)
- `current_balance` (loading: 0.342)

**Negative Drivers:** Features that decrease this component:
- `on_time_payments` (loading: -0.224)
- `total_payments_made` (loading: -0.223)
- `total_amount_paid` (loading: -0.200)

**Component Statistics:**
- Maximum loading magnitude: 0.3469
- Average loading magnitude: 0.2717
- Loading standard deviation: 0.0661

---

### PC3 (8.33% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `days_to_maturity` | 0.3704 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_term_months` | 0.3304 | 📈 Positive (High) | Higher values increase component score |
| 3 | `loan_term_years` | 0.3304 | 📈 Positive (High) | Higher values increase component score |
| 4 | `long_term_loan_risk` | 0.3088 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `loan_progress_pct` | -0.2699 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `employment_status_encoded` | 0.1975 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `annual_income_cad` | -0.1960 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `debt_to_income_ratio` | 0.1818 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `low_income_risk` | 0.1811 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `program_type_encoded` | 0.1786 | 📈 Positive (Low) | Higher values increase component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `days_to_maturity` (loading: 0.370)
- `loan_term_months` (loading: 0.330)
- `loan_term_years` (loading: 0.330)

**Negative Drivers:** Features that decrease this component:
- `loan_progress_pct` (loading: -0.270)
- `annual_income_cad` (loading: -0.196)

**Component Statistics:**
- Maximum loading magnitude: 0.3704
- Average loading magnitude: 0.2545
- Loading standard deviation: 0.0755

---

### PC4 (7.52% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.4078 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.3930 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `low_income_risk` | 0.3518 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `debt_to_income_ratio` | 0.3059 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `payment_to_income_ratio` | 0.3044 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `high_difficulty_program` | 0.1846 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `program_difficulty` | 0.1782 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `typical_tuition_cad` | 0.1644 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `current_balance` | -0.1606 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `loan_to_education_value_ratio` | -0.1506 | 📉 Negative (Low) | Higher values decrease component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.408)
- `low_income_risk` (loading: 0.352)
- `debt_to_income_ratio` (loading: 0.306)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.393)
- `current_balance` (loading: -0.161)
- `loan_to_education_value_ratio` (loading: -0.151)

**Component Statistics:**
- Maximum loading magnitude: 0.4078
- Average loading magnitude: 0.2601
- Loading standard deviation: 0.1030

---

### PC5 (6.97% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `typical_tuition_cad` | 0.4362 | 📈 Positive (High) | Higher values increase component score |
| 2 | `program_difficulty` | 0.3925 | 📈 Positive (High) | Higher values increase component score |
| 3 | `average_starting_salary` | 0.3893 | 📈 Positive (High) | Higher values increase component score |
| 4 | `high_difficulty_program` | 0.3630 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `education_roi` | -0.2989 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `ltv_ratio` | 0.2083 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `loan_to_education_value_ratio` | 0.2083 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `high_ltv_risk` | 0.1832 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `pos_duration` | 0.1666 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `current_balance` | 0.1309 | 📈 Positive (Low) | Higher values increase component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `typical_tuition_cad` (loading: 0.436)
- `program_difficulty` (loading: 0.392)
- `average_starting_salary` (loading: 0.389)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.299)

**Component Statistics:**
- Maximum loading magnitude: 0.4362
- Average loading magnitude: 0.2777
- Loading standard deviation: 0.1110

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
