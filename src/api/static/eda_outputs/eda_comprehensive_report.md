
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-06 18:50:35
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 1,000
- **Total Features:** 54 (engineered)
- **Delinquency Rate:** 50.90%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 13.52% of total variance
- **PC2:** 9.98% of total variance
- **PC3:** 7.64% of total variance
- **First 5 PCs:** 45.41% of total variance
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

### PC1 (13.52% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3300 | 📈 Positive (High) | Higher values increase component score |
| 2 | `total_payments_made` | 0.3196 | 📈 Positive (High) | Higher values increase component score |
| 3 | `late_payments` | 0.3145 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `on_time_payments` | 0.3062 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `total_amount_paid` | 0.2892 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `days_since_last_payment` | -0.2843 | 📉 Negative (Medium) | Higher values decrease component score |
| 7 | `payment_consistency` | 0.2360 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `loan_age_days` | 0.2291 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `loan_progress_pct` | 0.2220 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `days_since_disbursement` | 0.2201 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.330)
- `total_payments_made` (loading: 0.320)
- `late_payments` (loading: 0.315)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.284)

**Component Statistics:**
- Maximum loading magnitude: 0.3300
- Average loading magnitude: 0.2751
- Loading standard deviation: 0.0438

---

### PC2 (9.98% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `loan_amount` | 0.3346 | 📈 Positive (High) | Higher values increase component score |
| 2 | `education_value` | 0.3262 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `monthly_payment` | 0.3237 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `current_balance` | 0.3171 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.2734 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `payment_to_income_ratio` | 0.2500 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `debt_to_income_ratio` | 0.2463 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `down_payment` | 0.1852 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `employment_status_encoded` | 0.1725 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `annual_income_cad` | -0.1600 | 📉 Negative (Low) | Higher values decrease component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `loan_amount` (loading: 0.335)
- `education_value` (loading: 0.326)
- `monthly_payment` (loading: 0.324)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.160)

**Component Statistics:**
- Maximum loading magnitude: 0.3346
- Average loading magnitude: 0.2589
- Loading standard deviation: 0.0675

---

### PC3 (7.64% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `days_to_maturity` | 0.4199 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_term_years` | 0.4065 | 📈 Positive (High) | Higher values increase component score |
| 3 | `loan_term_months` | 0.4065 | 📈 Positive (High) | Higher values increase component score |
| 4 | `long_term_loan_risk` | 0.3733 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `loan_progress_pct` | -0.2542 | 📉 Negative (Low) | Higher values decrease component score |
| 6 | `current_balance` | 0.2490 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `education_value` | 0.1873 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `loan_amount` | 0.1804 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `program_duration_years` | 0.1526 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `days_since_disbursement` | -0.1367 | 📉 Negative (Low) | Higher values decrease component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `days_to_maturity` (loading: 0.420)
- `loan_term_years` (loading: 0.406)
- `loan_term_months` (loading: 0.406)

**Negative Drivers:** Features that decrease this component:
- `loan_progress_pct` (loading: -0.254)
- `days_since_disbursement` (loading: -0.137)

**Component Statistics:**
- Maximum loading magnitude: 0.4199
- Average loading magnitude: 0.2766
- Loading standard deviation: 0.1140

---

### PC4 (7.36% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `typical_tuition_cad` | 0.4670 | 📈 Positive (High) | Higher values increase component score |
| 2 | `program_difficulty` | 0.4306 | 📈 Positive (High) | Higher values increase component score |
| 3 | `average_starting_salary` | 0.4215 | 📈 Positive (High) | Higher values increase component score |
| 4 | `high_difficulty_program` | 0.3850 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `education_roi` | -0.3022 | 📉 Negative (Medium) | Higher values decrease component score |
| 6 | `program_type_encoded` | 0.1859 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `poor_job_outlook` | 0.1536 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `employment_rate` | 0.1325 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `job_market_outlook_encoded` | -0.1153 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `pos_duration` | 0.1087 | 📈 Positive (Low) | Higher values increase component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `typical_tuition_cad` (loading: 0.467)
- `program_difficulty` (loading: 0.431)
- `average_starting_salary` (loading: 0.422)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.302)
- `job_market_outlook_encoded` (loading: -0.115)

**Component Statistics:**
- Maximum loading magnitude: 0.4670
- Average loading magnitude: 0.2702
- Loading standard deviation: 0.1458

---

### PC5 (6.92% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.4585 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.4482 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `low_income_risk` | 0.3968 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `debt_to_income_ratio` | 0.3209 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `payment_to_income_ratio` | 0.3079 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `monthly_payment` | -0.1743 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `loan_amount` | -0.1673 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `current_balance` | -0.1547 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `education_value` | -0.1481 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `program_duration_years` | -0.1455 | 📉 Negative (Low) | Higher values decrease component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.458)
- `low_income_risk` (loading: 0.397)
- `debt_to_income_ratio` (loading: 0.321)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.448)
- `monthly_payment` (loading: -0.174)
- `loan_amount` (loading: -0.167)

**Component Statistics:**
- Maximum loading magnitude: 0.4585
- Average loading magnitude: 0.2722
- Loading standard deviation: 0.1294

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
