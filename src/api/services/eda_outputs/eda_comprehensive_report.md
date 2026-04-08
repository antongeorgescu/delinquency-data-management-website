
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** 2026-04-07 20:19:05
**Database:** C:\Users\ag4488\OneDrive - Finastra\Visual Studio 2022\Projects\delinquency-website\src\api\shared\student_loan_data.db

## Dataset Overview

- **Total Borrowers:** 1,000
- **Total Features:** 54 (engineered)
- **Delinquency Rate:** 50.40%
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** 13.55% of total variance
- **PC2:** 9.87% of total variance
- **PC3:** 7.70% of total variance
- **First 5 PCs:** 45.21% of total variance
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

### PC1 (13.55% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `avg_payment_amount` | 0.3285 | 📈 Positive (High) | Higher values increase component score |
| 2 | `total_payments_made` | 0.3114 | 📈 Positive (Medium) | Higher values increase component score |
| 3 | `late_payments` | 0.3067 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `on_time_payments` | 0.3007 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `total_amount_paid` | 0.2880 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `days_since_last_payment` | -0.2753 | 📉 Negative (Medium) | Higher values decrease component score |
| 7 | `program_type_encoded` | 0.2201 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `payment_consistency` | 0.2164 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `days_since_disbursement` | 0.2103 | 📈 Positive (Low) | Higher values increase component score |
| 10 | `loan_progress_pct` | 0.2060 | 📈 Positive (Low) | Higher values increase component score |

#### PC1 Interpretation:

**Positive Drivers:** Features that increase this component:
- `avg_payment_amount` (loading: 0.328)
- `total_payments_made` (loading: 0.311)
- `late_payments` (loading: 0.307)

**Negative Drivers:** Features that decrease this component:
- `days_since_last_payment` (loading: -0.275)

**Component Statistics:**
- Maximum loading magnitude: 0.3285
- Average loading magnitude: 0.2663
- Loading standard deviation: 0.0479

---

### PC2 (9.87% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `loan_amount` | 0.3294 | 📈 Positive (High) | Higher values increase component score |
| 2 | `education_value` | 0.3276 | 📈 Positive (High) | Higher values increase component score |
| 3 | `monthly_payment` | 0.3217 | 📈 Positive (High) | Higher values increase component score |
| 4 | `current_balance` | 0.3128 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `program_duration_years` | 0.2922 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `payment_to_income_ratio` | 0.2180 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `debt_to_income_ratio` | 0.2096 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `down_payment` | 0.2065 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `program_type_encoded` | -0.1882 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `total_payments_made` | -0.1820 | 📉 Negative (Low) | Higher values decrease component score |

#### PC2 Interpretation:

**Positive Drivers:** Features that increase this component:
- `loan_amount` (loading: 0.329)
- `education_value` (loading: 0.328)
- `monthly_payment` (loading: 0.322)

**Negative Drivers:** Features that decrease this component:
- `program_type_encoded` (loading: -0.188)
- `total_payments_made` (loading: -0.182)

**Component Statistics:**
- Maximum loading magnitude: 0.3294
- Average loading magnitude: 0.2588
- Loading standard deviation: 0.0627

---

### PC3 (7.70% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.3122 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.2973 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `debt_to_income_ratio` | 0.2722 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `low_income_risk` | 0.2643 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `payment_to_income_ratio` | 0.2547 | 📈 Positive (Low) | Higher values increase component score |
| 6 | `typical_tuition_cad` | -0.2476 | 📉 Negative (Low) | Higher values decrease component score |
| 7 | `high_difficulty_program` | -0.2434 | 📉 Negative (Low) | Higher values decrease component score |
| 8 | `days_to_maturity` | 0.2359 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `program_difficulty` | -0.2248 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `average_starting_salary` | -0.2019 | 📉 Negative (Low) | Higher values decrease component score |

#### PC3 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.312)
- `debt_to_income_ratio` (loading: 0.272)
- `low_income_risk` (loading: 0.264)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.297)
- `typical_tuition_cad` (loading: -0.248)
- `high_difficulty_program` (loading: -0.243)

**Component Statistics:**
- Maximum loading magnitude: 0.3122
- Average loading magnitude: 0.2554
- Loading standard deviation: 0.0329

---

### PC4 (7.23% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `loan_term_years` | 0.3581 | 📈 Positive (High) | Higher values increase component score |
| 2 | `loan_term_months` | 0.3581 | 📈 Positive (High) | Higher values increase component score |
| 3 | `long_term_loan_risk` | 0.3385 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `days_to_maturity` | 0.3304 | 📈 Positive (Medium) | Higher values increase component score |
| 5 | `typical_tuition_cad` | 0.3069 | 📈 Positive (Medium) | Higher values increase component score |
| 6 | `program_difficulty` | 0.2918 | 📈 Positive (Medium) | Higher values increase component score |
| 7 | `high_difficulty_program` | 0.2636 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `average_starting_salary` | 0.2545 | 📈 Positive (Low) | Higher values increase component score |
| 9 | `education_roi` | -0.2483 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `pos_duration` | 0.1619 | 📈 Positive (Low) | Higher values increase component score |

#### PC4 Interpretation:

**Positive Drivers:** Features that increase this component:
- `loan_term_years` (loading: 0.358)
- `loan_term_months` (loading: 0.358)
- `long_term_loan_risk` (loading: 0.338)

**Negative Drivers:** Features that decrease this component:
- `education_roi` (loading: -0.248)

**Component Statistics:**
- Maximum loading magnitude: 0.3581
- Average loading magnitude: 0.2912
- Loading standard deviation: 0.0611

---

### PC5 (6.85% variance explained)

#### Most Influential Features:

| Rank | Feature | Loading | Impact | Description |
|------|---------|---------|--------|-------------|
| 1 | `employment_status_encoded` | 0.3582 | 📈 Positive (High) | Higher values increase component score |
| 2 | `annual_income_cad` | -0.3518 | 📉 Negative (High) | Higher values decrease component score |
| 3 | `low_income_risk` | 0.3088 | 📈 Positive (Medium) | Higher values increase component score |
| 4 | `debt_to_income_ratio` | 0.2494 | 📈 Positive (Low) | Higher values increase component score |
| 5 | `payment_to_income_ratio` | 0.2466 | 📈 Positive (Low) | Higher values increase component score |
| 6 | `typical_tuition_cad` | 0.2424 | 📈 Positive (Low) | Higher values increase component score |
| 7 | `program_difficulty` | 0.2225 | 📈 Positive (Low) | Higher values increase component score |
| 8 | `current_balance` | -0.2109 | 📉 Negative (Low) | Higher values decrease component score |
| 9 | `education_roi` | -0.2030 | 📉 Negative (Low) | Higher values decrease component score |
| 10 | `high_difficulty_program` | 0.1979 | 📈 Positive (Low) | Higher values increase component score |

#### PC5 Interpretation:

**Positive Drivers:** Features that increase this component:
- `employment_status_encoded` (loading: 0.358)
- `low_income_risk` (loading: 0.309)
- `debt_to_income_ratio` (loading: 0.249)

**Negative Drivers:** Features that decrease this component:
- `annual_income_cad` (loading: -0.352)
- `current_balance` (loading: -0.211)
- `education_roi` (loading: -0.203)

**Component Statistics:**
- Maximum loading magnitude: 0.3582
- Average loading magnitude: 0.2591
- Loading standard deviation: 0.0596

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
