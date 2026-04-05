
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-05 11:48:54
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 1,000
- **Total Features:** 47 (engineered)
- **Delinquency Rate:** 4.70%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 14.72% of total variance
- **PC2:** 11.23% of total variance
- **PC3:** 8.07% of total variance
- **First 5 PCs:** 47.81% of total variance
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

### PC1 (14.72% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3206 | 📈 Positive (High) | Higher values increase component score |
| 2 | `days_since_last_payment` | -0.2932 | 📉 Negative (Medium) | Higher values decrease component score |
| 3 | `payment_consistency` | 0.2925 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `total_payments_made` | 0.2707 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `on_time_payments` | 0.2693 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `loan_progress_pct` | 0.2527 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `loan_age_days` | 0.2504 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `days_since_disbursement` | 0.2459 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `total_amount_paid` | 0.2340 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `education_value` | 0.2071 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.321)
- `payment_consistency` (loading: 0.292)
- `total_payments_made` (loading: 0.271)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.293)

**Component Statistics:**
- Maximum loading magnitude: 0.3206
- Average loading magnitude: 0.2636
- Loading standard deviation: 0.0329

---

### PC2 (11.23% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `current_balance` | 0.3270 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_amount` | 0.3263 | 📈 Positive (High) | Higher values increase component score |
| 3 | `education_value` | 0.3198 | 📈 Positive (High) | Higher values increase component score |
| 4 | `monthly_payment` | 0.3035 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.2810 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `on_time_payments` | -0.2456 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `total_payments_made` | -0.2448 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `total_amount_paid` | -0.2254 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `program_type_encoded` | -0.2137 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `payment_to_income_ratio` | 0.2004 | 📈 Positive (Low) | Higher values increase component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `current_balance` (loading: 0.327)
- `loan_amount` (loading: 0.326)
- `education_value` (loading: 0.320)

**Negative Drivers:** Features that decrease this component:
- `on_time_payments` (loading: -0.246)
- `total_payments_made` (loading: -0.245)
- `total_amount_paid` (loading: -0.225)

**Component Statistics:**
- Maximum loading magnitude: 0.3270
- Average loading magnitude: 0.2688
- Loading standard deviation: 0.0487

---

### PC3 (8.07% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `days_to_maturity` | 0.3405 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_progress_pct` | -0.3129 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `loan_term_months` | 0.2602 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `loan_term_years` | 0.2602 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `loan_age_days` | -0.2403 | 📉 Negative (Low) | Higher values decrease component score |
| 6 | `days_since_disbursement` | -0.2402 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `program_type_encoded` | 0.2225 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `total_amount_paid` | 0.2095 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `avg_late_fee_per_payment` | -0.1972 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `delinquency_rate` | -0.1972 | 📉 Negative (Low) | Higher values decrease component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `days_to_maturity` (loading: 0.341)
- `loan_term_months` (loading: 0.260)
- `loan_term_years` (loading: 0.260)

**Negative Drivers:** Features that decrease this component:
- `loan_progress_pct` (loading: -0.313)
- `loan_age_days` (loading: -0.240)
- `days_since_disbursement` (loading: -0.240)

**Component Statistics:**
- Maximum loading magnitude: 0.3405
- Average loading magnitude: 0.2481
- Loading standard deviation: 0.0477

---

### PC4 (7.04% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.4342 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.4054 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `payment_to_income_ratio` | 0.3683 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `debt_to_income_ratio` | 0.3668 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `down_payment` | -0.2661 | 📉 Negative (Low) | Higher values decrease component score |
| 6 | `education_value` | -0.1919 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `program_duration_years` | -0.1868 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `ltv_ratio` | 0.1835 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `loan_to_education_value_ratio` | 0.1835 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `current_balance` | -0.1334 | 📉 Negative (Low) | Higher values decrease component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.434)
- `payment_to_income_ratio` (loading: 0.368)
- `debt_to_income_ratio` (loading: 0.367)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.405)
- `down_payment` (loading: -0.266)
- `education_value` (loading: -0.192)

**Component Statistics:**
- Maximum loading magnitude: 0.4342
- Average loading magnitude: 0.2720
- Loading standard deviation: 0.1110

---

### PC5 (6.75% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `typical_tuition_cad` | 0.5264 | 📈 Positive (High) | Higher values increase component score |
| 2 | `average_starting_salary` | 0.4644 | 📈 Positive (High) | Higher values increase component score |
| 3 | `program_difficulty` | 0.4423 | 📈 Positive (High) | Higher values increase component score |
| 4 | `education_roi` | -0.3724 | 📉 Negative (Medium) | Higher values decrease component score |
| 5 | `pos_duration` | 0.2061 | 📈 Positive (Low) | Higher values increase component score |
| 6 | `employment_rate` | 0.1354 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `down_payment` | 0.1126 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `field_of_study_encoded` | -0.1039 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `ltv_ratio` | -0.0988 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `loan_to_education_value_ratio` | -0.0988 | 📉 Negative (Low) | Higher values decrease component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `typical_tuition_cad` (loading: 0.526)
- `average_starting_salary` (loading: 0.464)
- `program_difficulty` (loading: 0.442)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.372)
- `field_of_study_encoded` (loading: -0.104)
- `ltv_ratio` (loading: -0.099)

**Component Statistics:**
- Maximum loading magnitude: 0.5264
- Average loading magnitude: 0.2561
- Loading standard deviation: 0.1748

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
