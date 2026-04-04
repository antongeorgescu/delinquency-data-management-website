# Student Loan Analytics Documentation

## Overview

The student loan analytics system provides comprehensive data analysis capabilities through two primary components:
1. **Delinquency Risk Analysis**: Machine learning-based risk prediction and scoring
2. **Exploratory Data Analysis (EDA)**: Interactive visualizations and statistical insights

Both systems integrate data from all four database tables to provide actionable insights for loan portfolio management.

## System Architecture

The analytics system follows a modular pipeline architecture supporting multiple analysis types:

```mermaid
flowchart TB
    subgraph data_layer[📊 Data Layer]
        A[(User Profile)]
        B[(Program of Study)]
        C[(Loan Information)]
        D[(Loan Payments)]
    end
    
    subgraph analysis_engines[🤖 Analysis Engines]
        E[Risk Analysis ML Pipeline]
        F[EDA Visualization Engine]
        G[Campaign Generator]
    end
    
    subgraph output_layer[📋 Output Layer]
        H[Updated Database]
        I[Interactive Visualizations]
        J[Campaign Files]
        K[Analysis Reports]
    end
    
    subgraph web_interface[🌐 Web Interface]
        L[Angular SPA]
        M[Results Panels]
        N[File Management]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    A --> F
    B --> F
    C --> F
    D --> F
    
    E --> H
    F --> I
    E --> J
    F --> K
    
    H --> L
    I --> M
    J --> N
    K --> N
```

## 🎯 Core Analytics Components

### 1. Delinquency Risk Analysis Pipeline

**Purpose**: Advanced machine learning system for predicting loan delinquency risk with multiple algorithms and comprehensive feature engineering.

#### Architecture Overview
```mermaid
flowchart TD
    A[Start Risk Analysis] --> B[Load Comprehensive Dataset]
    B --> C[Feature Engineering Pipeline]
    C --> D[ML Data Preparation]
    D --> E[Multi-Model Training]
    E --> F[Best Model Selection]
    F --> G[Feature Importance Analysis]
    G --> H[Risk Score Calculation]
    H --> I[Database Updates]
    I --> J[Performance Reporting]
    J --> K[End]
    
    B --> B1[Join 4 Tables with<br/>Payment Aggregation]
    C --> C1[60+ Engineered Features<br/>- Time-based<br/>- Financial Ratios<br/>- Risk Indicators<br/>- Behavioral Metrics]
    E --> E1[Random Forest<br/>Gradient Boosting<br/>Logistic Regression]
    H --> H1[5 Risk Algorithms<br/>- Percentile (Default)<br/>- Threshold<br/>- K-Means<br/>- SVM<br/>- KNN]
```

#### Feature Engineering Categories

**Time-based Features**:
- `loan_age_days`: Loan maturity tracking
- `days_since_disbursement`: Payment timeline analysis
- `loan_progress_pct`: Completion percentage

**Financial Stress Indicators**:
- `debt_to_income_ratio`: Leverage analysis
- `payment_to_income_ratio`: Affordability metrics
- `education_roi`: Investment return calculation

**Payment Behavior Analysis**:
- `delinquency_rate`: Historical performance
- `payment_consistency`: Reliability scoring
- `avg_late_fee_per_payment`: Penalty analysis

**Binary Risk Flags**:
- `high_ltv_risk`, `low_income_risk`, `young_borrower_risk`
- `long_term_loan_risk`, `poor_job_outlook`

#### ML Model Performance
- **Random Forest**: AUC 0.75-0.85, excellent feature importance
- **Gradient Boosting**: AUC 0.78-0.88, complex pattern capture  
- **Logistic Regression**: AUC 0.70-0.80, interpretable baseline

### 2. Exploratory Data Analysis (EDA) Engine

**Purpose**: Comprehensive statistical analysis with interactive visualizations using Principal Component Analysis and clustering techniques.

#### EDA Pipeline Architecture
```mermaid
flowchart TD
    A[Start EDA Analysis] --> B[Load & Process Data]
    B --> C[Feature Standardization] 
    C --> D[PCA Analysis]
    D --> E[Visualization Generation]
    E --> F[Clustering Analysis]
    F --> G[Statistical Reporting]
    G --> H[File Generation & Serving]
    H --> I[End]
    
    D --> D1[Configurable Components<br/>n_components: 2-50<br/>Variance Analysis<br/>Scree Plotting]
    E --> E1[Interactive Charts<br/>- Scatter Plots<br/>- Biplots<br/>- Heatmaps<br/>- Feature Contributions]
    F --> F1[K-means Clustering<br/>n_clusters: 1-20<br/>Risk-based Coloring<br/>Cluster Statistics]
    H --> H1[8 Generated Files<br/>- HTML Visualizations<br/>- CSV Data<br/>- MD Reports]
```

#### Generated EDA Files

| File Type | Description | Technology | Typical Size |
|-----------|------------|------------|-------------|
| **HTML Interactive Charts** | Plotly-based visualizations | JavaScript/D3.js | 4-5 MB |
| `pca_scree_plot.html` | Variance explained analysis | Interactive line chart | 4.4 MB |
| `pca_scatter_plot.html` | PC1 vs PC2 colored by risk | Interactive scatter | 4.4 MB |
| `pca_biplot_pc1_vs_pc2.html` | Feature loading vectors | Biplot visualization | 4.4 MB |
| `pca_feature_contributions.html` | Feature importance heatmap | Interactive heatmap | 4.4 MB |
| `feature_correlation_heatmap.html` | Original feature correlations | Correlation matrix | 4.4 MB |
| `pca_clustering_k{n}.html` | K-means cluster visualization | Clustered scatter plot | 4.4 MB |
| **Data Exports** | Statistical summaries | CSV/Markdown | < 10 KB |
| `cluster_analysis_summary.csv` | Cluster statistics | Tabular data | 400 B |
| `eda_comprehensive_report.md` | Complete analysis report | Formatted report | 2.4 KB |

#### EDA Configuration Parameters

**PCA Configuration**:
```python
n_components = {
    'range': (2, 50),
    'default': 10,
    'description': 'Number of principal components to extract'
}
```

**Clustering Configuration**:
```python
n_clusters = {
    'range': (1, 20), 
    'default': 5,
    'description': 'K-means cluster count for analysis'
}
```

### 3. Campaign Generation System

**Purpose**: Risk-based borrower segmentation for targeted marketing and intervention campaigns.

#### Campaign Types
- **Medium Risk Campaigns**: Early intervention strategies
- **High Risk Campaigns**: Intensive support and retention efforts
- **Custom Risk Combinations**: Flexible borrower targeting

#### Generated Files
```csv
# Example: high_risk_borrowers_campaign.csv
payer_id,first_name,last_name,email,phone,delinquency_risk,risk_probability
1001,John,Doe,john.doe@email.com,555-0123,2,0.87
```

## 📊 Technical Implementation

### Database Integration

#### Core Database Schema
```sql  
-- Enhanced loan_info table with ML predictions
CREATE TABLE loan_info (
    loan_id INTEGER PRIMARY KEY,
    payer_id INTEGER,
    loan_amount DECIMAL(10,2),
    interest_rate DECIMAL(5,2),
    delinquency_risk INTEGER DEFAULT 0,  -- ML-generated: 0=Low, 1=Medium, 2=High  
    risk_probability DECIMAL(5,4),       -- ML confidence score
    FOREIGN KEY (payer_id) REFERENCES user_profile(payer_id)
);
```

#### Comprehensive Data Joins
```sql
-- Multi-table analysis query foundation
SELECT 
    up.*, li.*, pos.*, 
    lp_agg.total_payments, lp_agg.missed_payments,
    lp_agg.total_late_fees, lp_agg.avg_days_late
FROM user_profile up
LEFT JOIN loan_info li ON up.payer_id = li.payer_id  
LEFT JOIN program_of_study pos ON li.program_id = pos.program_id
LEFT JOIN (
    SELECT loan_id,
           COUNT(*) as total_payments,
           SUM(CASE WHEN status = 'missed' THEN 1 ELSE 0 END) as missed_payments,
           SUM(late_fee) as total_late_fees,
           AVG(days_late) as avg_days_late
    FROM loan_payments
    GROUP BY loan_id
) lp_agg ON li.loan_id = lp_agg.loan_id;
```

### API Endpoint Architecture

#### Risk Analysis Endpoints
```python
# POST /api/risk-estimation
{
    "algorithm": "percentile",  # Risk scoring algorithm
    "parameters": {
        "test_size": 0.2,
        "cv_folds": 5
    }
}

# Response
{
    "success": True,
    "algorithm": "percentile", 
    "statistics": {
        "total_borrowers": 1000,
        "delinquent_borrowers": 156,
        "overall_delinquency_rate": 0.156
    },
    "risk_distribution": {
        "low_risk": {"count": 600, "percentage": 60.0},
        "medium_risk": {"count": 300, "percentage": 30.0}, 
        "high_risk": {"count": 100, "percentage": 10.0}
    },
    "model_performance": {
        "best_model": "RandomForest",
        "auc_score": 0.847,
        "cv_scores": [0.834, 0.851, 0.849, 0.845, 0.856]
    }
}
```

#### EDA Analysis Endpoints
```python
# POST /api/eda-reports  
{
    "n_clusters": 5,
    "n_components": 10
}

# Response
{
    "success": True,
    "parameters": {
        "n_clusters": 5,
        "n_components": 10
    },
    "files": [
        {
            "filename": "pca_scree_plot.html",
            "description": "Variance explained by each principal component",
            "url": "http://127.0.0.1:5000/api/static/eda_outputs/pca_scree_plot.html",
            "size": 4568046,
            "size_formatted": "4.4 MB",
            "creation_date": "2026-04-04 14:07:08",
            "exists": True
        }
    ],
    "files_count": 8,
    "data_overview": {
        "total_records": 1000,
        "total_features": 34,
        "data_completeness": 0.97
    },
    "analysis_summary": {
        "pca_variance_explained": 0.78,
        "optimal_clusters": 5,
        "risk_separation_quality": 0.85
    }
}
```

### Frontend Integration

#### Angular Service Architecture
```typescript
// data.service.ts - API Integration
@Injectable({
    providedIn: 'root'
})
export class DataService {
    
    runRiskEstimation(algorithm: string): Observable<RiskAnalysisResponse> {
        return this.http.post<RiskAnalysisResponse>(
            `${this.baseUrl}/risk-estimation`,
            { algorithm }
        );
    }
    
    runEDAReports(nClusters: number, nComponents: number): Observable<EdaResponse> {
        return this.http.post<EdaResponse>(
            `${this.baseUrl}/eda-reports`, 
            { n_clusters: nClusters, n_components: nComponents }
        );
    }
}
```

#### Results Panel Management
```typescript
// home.component.ts - State Management
export class HomeComponent implements OnInit {
    
    // Panel State Management
    showRiskResults = false;
    showEdaResults = false; 
    riskEstimationResults: any = null;
    edaResults: any = null;
    
    // Persistent State in LocalStorage
    saveEdaResults(): void {
        if (this.edaResults) {
            localStorage.setItem('edaResults', JSON.stringify(this.edaResults));
        }
    }
    
    loadPersistedPanels(): void {
        const savedEdaResults = localStorage.getItem('edaResults');
        if (savedEdaResults) {
            this.edaResults = JSON.parse(savedEdaResults);
            this.showEdaResults = true;
        }
    }
}
```

## 🔬 Advanced Analytics Features

### Statistical Analysis Capabilities

#### PCA Analysis Details
```python
# Principal Component Analysis Configuration
pca_analysis = {
    'components': 'auto-determined or user-configured',
    'variance_threshold': 0.95,  # Capture 95% of variance
    'feature_scaling': 'StandardScaler normalization',
    'interpretation': 'Biplot visualization with loading vectors'
}
```

#### Clustering Analysis
```python
# K-means Configuration
clustering = {
    'algorithm': 'K-means++',
    'init_method': 'k-means++',
    'n_init': 10,
    'max_iter': 300,
    'evaluation_metrics': ['silhouette_score', 'inertia', 'calinski_harabasz']
}
```

### Visualization Technology Stack

#### Interactive Chart Libraries
- **Plotly.js**: Primary visualization engine for interactive charts
- **D3.js**: Underlying technology for advanced customizations
- **Bootstrap**: Responsive design and styling framework
- **Bootstrap Icons**: Consistent iconography throughout interface

#### Chart Specifications
```javascript
// Example Plotly Configuration
plotly_config = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToAdd: ['downloadPlotAsJson'],
    toImageButtonOptions: {
        format: 'png',
        filename: 'eda_analysis',
        height: 800,
        width: 1200,
        scale: 2
    }
}
```

### Performance Optimization

#### Backend Optimizations
- **Vectorized Operations**: NumPy/Pandas for efficient computation
- **Memory Management**: Batch processing for large datasets  
- **Caching Strategy**: File-based caching for generated visualizations
- **Database Optimization**: Indexed queries and connection pooling

#### Frontend Optimizations  
- **Lazy Loading**: Components loaded on demand
- **State Management**: Efficient Angular change detection
- **Bundle Optimization**: Tree shaking and compression
- **Static Asset Caching**: Browser caching for generated files

## 🔧 Configuration & Deployment

### Environment Configuration

#### Development Settings
```python
# Flask Development Configuration
FLASK_CONFIG = {
    'DEBUG': True,
    'TESTING': False,
    'DATABASE_URI': 'sqlite:///student_loan_data.db',
    'CORS_ORIGINS': ['http://localhost:4200'],
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024  # 16MB file size limit
}
```

#### Production Considerations
```python
# Production Deployment Settings
PRODUCTION_CONFIG = {
    'DEBUG': False,
    'DATABASE_URI': 'postgresql://user:pass@host:port/db',
    'STATIC_FILE_STORAGE': 'AWS_S3',  # For EDA file hosting
    'REDIS_CACHE': 'redis://localhost:6379/0',  # Analysis caching
    'WORKER_PROCESSES': 4  # Parallel analysis processing
}
```

### Security Implementation

#### Input Validation
```python
# Parameter validation for EDA endpoints
def validate_eda_parameters(data):
    n_clusters = data.get('n_clusters', 5)
    n_components = data.get('n_components', 10)
    
    if not isinstance(n_clusters, int) or not (1 <= n_clusters <= 20):
        raise ValueError("n_clusters must be integer between 1-20")
    
    if not isinstance(n_components, int) or not (2 <= n_components <= 50):
        raise ValueError("n_components must be integer between 2-50")
        
    return n_clusters, n_components
```

#### File Security  
```python
# Static file serving with security checks
def secure_filename_check(filename):
    if '..' in filename or filename.startswith('/'):
        raise SecurityError("Invalid filename detected")
    
    allowed_extensions = {'.html', '.csv', '.md', '.png', '.jpg'}
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise SecurityError("File type not permitted")
```

## 📈 Performance Metrics & Monitoring

### Analysis Performance Benchmarks

#### EDA Generation Times (1000 records)
- **Data Loading & Processing**: 5-10 seconds
- **PCA Analysis**: 3-5 seconds  
- **Visualization Generation**: 15-25 seconds
- **File Writing & Optimization**: 5-10 seconds
- **Total EDA Runtime**: 30-60 seconds

#### Risk Analysis Performance
- **Feature Engineering**: 5-8 seconds
- **Model Training (3 algorithms)**: 10-15 seconds
- **Cross-validation**: 5-10 seconds  
- **Risk Score Calculation**: 2-3 seconds
- **Database Updates**: 1-2 seconds
- **Total Risk Analysis Runtime**: 25-40 seconds

### File Size Management

#### Generated File Sizes
```yaml
HTML_Files:
  size_range: "4.0 - 5.0 MB"
  compression: "gzip recommended"
  format: "Plotly JSON embedded"
  
CSV_Files:
  size_range: "< 1 KB - 10 KB" 
  compression: "minimal benefit"
  format: "standard CSV"
  
Markdown_Files:
  size_range: "1 - 5 KB"
  compression: "minimal benefit"  
  format: "GitHub Flavored Markdown"
```

## 🚀 Future Enhancement Roadmap

### Advanced ML Capabilities
1. **Deep Learning Models**: Neural networks for complex pattern recognition
2. **Time Series Analysis**: Temporal delinquency pattern identification  
3. **Ensemble Methods**: Advanced model combination strategies
4. **AutoML Integration**: Automated hyperparameter optimization

### Enhanced Visualizations
1. **3D Visualizations**: Three-dimensional PCA exploration
2. **Animation Support**: Time-based trend animations
3. **Interactive Dashboards**: Real-time analytics dashboards  
4. **Custom Chart Builder**: User-defined visualization creation

### Operational Enhancements  
1. **Real-time Analysis**: Streaming data processing
2. **Automated Reporting**: Scheduled analysis generation
3. **API Rate Limiting**: Performance and security controls
4. **Multi-tenant Support**: Organization-based data isolation

## 🔍 Troubleshooting & Diagnostics

### Common Analysis Issues

#### EDA Generation Failures
```bash
# Check database connectivity
python -c "from shared.database import DatabaseManager; dm = DatabaseManager(); print('DB OK')"

# Verify data completeness  
python -c "import pandas as pd; from services.run_eda_analysis_json import run_eda_analysis_json; print('EDA OK')"

# Test matplotlib/seaborn imports
python -c "import matplotlib.pyplot as plt; import seaborn as sns; print('Visualization libs OK')"
```

#### File Serving Issues
```bash  
# Check static file permissions
ls -la src/api/static/eda_outputs/

# Test direct file access
curl -I http://127.0.0.1:5000/api/static/eda_outputs/pca_scree_plot.html

# Verify CORS headers
curl -H "Origin: http://localhost:4200" -I http://127.0.0.1:5000/api/static/eda_outputs/pca_scree_plot.html
```

#### Performance Diagnostics
```python
# Profile EDA generation
import cProfile
cProfile.run('run_eda_analysis_json(n_clusters=5, n_components=10)')

# Memory usage monitoring
import psutil
process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

## 📋 API Reference Summary

### Complete Endpoint Catalog

#### Data Management
- `POST /api/generate-data` - Synthetic data generation
- `GET /api/get-user-profiles` - User profile retrieval
- `GET /api/get-loan-info` - Loan information access
- `GET /api/get-programs` - Program catalog
- `GET /api/get-loan-payments` - Payment history

#### Analytics & ML  
- `POST /api/risk-estimation` - ML risk analysis
- `GET /api/risk-models` - Available algorithms  
- `POST /api/eda-reports` - EDA generation
- `POST /api/campaign-files` - Campaign creation

#### File & Static Assets
- `GET /api/static/eda_outputs/<filename>` - EDA file serving
- `GET /api/health` - System health check

This comprehensive student loan analytics platform provides enterprise-grade capabilities for risk assessment, data exploration, and campaign management through an intuitive web interface backed by robust machine learning and statistical analysis engines.

## Core Components Analysis

### 1. Data Loading and Integration (`load_comprehensive_dataset`)

**Purpose**: Creates a unified dataset by joining all four database tables with comprehensive feature extraction.

**Key Operations**:
- **Multi-table JOIN**: Combines `user_profile`, `loan_info`, `program_of_study`, and `loan_payments`
- **Feature Aggregation**: Calculates payment behavior metrics (total payments, missed payments, late fees)
- **Target Variable Creation**: Defines delinquency as any borrower with missed payments
- **Data Validation**: Reports dataset size and delinquency rate

**SQL Logic**: Uses LEFT JOIN to preserve all borrowers even without payment history, with GROUP BY to aggregate payment statistics per borrower.

### 2. Feature Engineering (`engineer_features`)

**Purpose**: Creates advanced predictive features from raw data to improve model performance.

**Feature Categories**:

**Time-based Features**:
- `loan_age_days`: Days since loan origination
- `days_since_disbursement`: Days since funds were disbursed  
- `days_to_maturity`: Remaining days until loan maturity
- `loan_progress_pct`: Percentage of loan term completed

**Financial Ratios**:
- `debt_to_income_ratio`: Loan amount relative to annual income
- `payment_to_income_ratio`: Annual payment burden as % of income
- `education_roi`: Expected salary return on education investment
- `loan_to_education_value_ratio`: Loan coverage of education costs

**Payment Behavior Metrics**:
- `delinquency_rate`: Percentage of payments missed
- `payment_consistency`: Percentage of successful payments
- `avg_late_fee_per_payment`: Average penalty per payment

**Binary Risk Indicators**:
- `high_ltv_risk`: Loan-to-value ratio > 80%
- `low_income_risk`: Annual income < $40,000
- `young_borrower_risk`: Age < 26 years
- `long_term_loan_risk`: Loan term > 15 years
- `high_difficulty_program`: Program difficulty level 3
- `low_employment_rate`: Employment rate < 80%
- `poor_job_outlook`: Program has challenging job market

### 3. Machine Learning Preparation (`prepare_ml_features`)

**Purpose**: Transforms raw features into ML-ready format through encoding and preprocessing.

**Key Operations**:
- **Categorical Encoding**: Label encoding for 14 categorical features
- **Feature Selection**: Automatically selects numerical and encoded features
- **Missing Value Handling**: Imputes missing values with column means
- **Infinite Value Cleanup**: Replaces infinite values with finite equivalents
- **Data Type Consistency**: Ensures all features are numerical for ML algorithms

**Encoded Categories**: Employment status, marital status, provinces, loan types, lenders, program types, fields of study, accreditation bodies, institutions, licensing requirements, job market outlook, and loan status.

### 4. Model Training Pipeline (`train_delinquency_models`)

**Purpose**: Trains and evaluates multiple ML models to select the best performer for delinquency prediction.

**Model Architecture**:
1. **Random Forest**: 100 trees, max depth 10, excellent for feature importance
2. **Gradient Boosting**: 100 estimators, max depth 6, captures complex patterns
3. **Logistic Regression**: Linear model with L2 regularization, interpretable coefficients

**Evaluation Process**:
- **Train/Test Split**: 80/20 stratified split maintaining class balance
- **Feature Scaling**: StandardScaler for Logistic Regression only
- **Cross-Validation**: 5-fold CV with AUC scoring for robust evaluation
- **Metrics Calculation**: AUC-ROC scores, classification reports, confusion matrices
- **Model Selection**: Highest AUC score determines best model

### 5. Feature Importance Analysis (`analyze_feature_importance`)

**Purpose**: Identifies and ranks the most influential features for delinquency prediction.

**Analysis Components**:
- **Importance Extraction**: Uses `feature_importances_` for tree models, `coef_` for linear models
- **Feature Ranking**: Sorts features by importance scores descending
- **Top Features Report**: Displays top 20 most influential features
- **Category Analysis**: Groups features by data source (User Profile, Loan Info, Program, Payment Behavior)
- **Source Contribution**: Calculates total importance contribution by table source

**Output**: Comprehensive feature importance ranking with categorical breakdown showing which data sources drive delinquency predictions.

### 6. Risk Score Calculation (`calculate_risk_scores`)

**Purpose**: Converts ML probability predictions into discrete risk levels (0=Low, 1=Medium, 2=High) using multiple algorithms.

**Risk Scoring Algorithms**:

**Percentile Algorithm** (Default):
- Low Risk (0): Bottom 60% of probability scores
- Medium Risk (1): Next 30% of probability scores  
- High Risk (2): Top 10% of probability scores

**Threshold Algorithm**:
- Low Risk (0): Probability < 0.3
- Medium Risk (1): Probability 0.3-0.6
- High Risk (2): Probability > 0.6

**K-Means Clustering**:
- Clusters probability scores into 3 groups
- Maps clusters to risk levels based on cluster centers
- Data-driven risk boundaries

**SVM Classification**:
- Trains secondary SVM classifier on probability-based labels
- Uses RBF kernel with balanced class weighting
- Handles class imbalance with adaptive percentile splits

**KNN Classification**:
- K-Nearest Neighbors with optimal k selection
- Distance-weighted predictions for better accuracy
- Cross-validation for hyperparameter tuning

### 7. Database Update (`update_loan_info_table`)

**Purpose**: Persists calculated risk scores back to the database for operational use.

**Operations**:
- **Schema Alteration**: Adds `delinquency_risk INTEGER` column if not exists
- **Score Updates**: Batch updates all borrower risk scores
- **Data Validation**: Verifies update counts and provides distribution statistics
- **Error Handling**: Manages duplicate column scenarios gracefully

### 8. Analysis Reporting (`generate_analysis_report`)

**Purpose**: Creates comprehensive summary of analysis results and model performance.

**Report Components**:
- **Dataset Statistics**: Total borrowers, feature counts, delinquency rates
- **Model Performance**: AUC scores, cross-validation results for all models
- **Feature Importance**: Top influential features driving predictions
- **Risk Distribution**: Count and percentage breakdown by risk level
- **Sample Analysis**: Example borrowers from each risk category
- **Validation Metrics**: Actual vs. predicted delinquency rates by risk level

## Files Added

### 1. `delinquency_analysis.py`
Main analysis script with 8 core functions implementing the complete ML pipeline from data loading through risk score calculation and database updates.

### 2. `run_risk_estimation.py`
Simple runner script with error checking and user-friendly interface.

### 3. Updated Database Schema
The `loan_info` table now includes:
- `delinquency_risk INTEGER DEFAULT 0` - Discrete risk levels (0=Low, 1=Medium, 2=High)

## Usage

### Basic Usage
```bash
# Run analysis with default settings
python run_risk_estimation.py

# Use specific algorithm
python run_risk_estimation.py --algorithm svm

# Custom database path
python run_risk_estimation.py --db_path my_database.db --algorithm kmeans
```

### Available Risk Algorithms
- `percentile`: Percentile-based thresholds (60%-30%-10% split)
- `threshold`: Fixed probability thresholds (0.3, 0.6)
- `kmeans`: K-means clustering of probabilities
- `svm`: Support Vector Machine classification
- `knn`: K-Nearest Neighbors classification

## Machine Learning Approach

### Models Used
1. **Random Forest Classifier** - Ensemble of 100 trees, excellent feature importance, handles mixed data types
2. **Gradient Boosting Classifier** - Sequential boosting, captures complex non-linear patterns  
3. **Logistic Regression** - Linear model with regularization, provides probability calibration

### Model Selection Criteria
- **Primary Metric**: AUC-ROC score for handling class imbalance
- **Validation**: 5-fold cross-validation for robust performance estimation
- **Final Selection**: Best AUC score across test set evaluations

### Feature Engineering Strategy
The analysis creates 60+ features from the source tables:

#### User Profile Features
- Demographics: Age, income, employment status, marital status, location
- Risk indicators: Young borrower risk, low income risk flags

#### Loan Information Features  
- Financial metrics: Loan amount, interest rate, term, monthly payment
- Ratios: LTV ratio, debt-to-income, payment-to-income ratios
- Timeline: Origination date, disbursement date, loan maturity
- Risk flags: High LTV risk, long-term loan risk indicators

#### Program of Study Features
- Academic details: Program type, field of study, difficulty level
- Employment prospects: Employment rate, starting salary, job outlook
- Institution characteristics: Type, accreditation, licensing requirements
- ROI calculations: Education return on investment metrics

#### Payment Behavior Features (Aggregated)
- Payment history: Total payments, missed payments, successful payments
- Timing metrics: Average days late, maximum days late
- Financial impact: Total late fees, average payment amounts
- Performance ratios: Delinquency rate, payment consistency scores

## Data Flow and Processing Pipeline

```mermaid
flowchart LR
    subgraph DB[Database Tables]
        UP[User Profile<br/>Demographics]
        LI[Loan Info<br/>Financial Terms]
        PS[Program Study<br/>Academic Data]  
        LP[Loan Payments<br/>Payment History]
    end
    
    subgraph FE[Feature Engineering]
        TF[Time Features<br/>Loan Age, Progress]
        FR[Financial Ratios<br/>DTI, PTI, ROI]
        RF[Risk Flags<br/>Binary Indicators]
        PB[Payment Behavior<br/>Aggregated Metrics]
    end
    
    subgraph ML[Machine Learning]
        RF_MODEL[Random Forest<br/>n_estimators=100]
        GB_MODEL[Gradient Boosting<br/>n_estimators=100]  
        LR_MODEL[Logistic Regression<br/>L2 Regularization]
    end
    
    subgraph RS[Risk Scoring]
        PERC[Percentile<br/>60-30-10 Split]
        THRESH[Threshold<br/>0.3, 0.6 Cutoffs]
        KMEANS[K-Means<br/>3 Clusters]
        SVM[SVM Classifier<br/>RBF Kernel]
        KNN[KNN Classifier<br/>Optimal K]
    end
    
    subgraph OUT[Output]
        RISK[Risk Scores<br/>0=Low, 1=Med, 2=High]
        DB_UPDATE[Database Update<br/>loan_info.delinquency_risk]
        REPORT[Analysis Report<br/>Feature Importance]
    end
    
    UP --> FE
    LI --> FE
    PS --> FE
    LP --> FE
    
    FE --> TF
    FE --> FR  
    FE --> RF
    FE --> PB
    
    TF --> ML
    FR --> ML
    RF --> ML
    PB --> ML
    
    ML --> RF_MODEL
    ML --> GB_MODEL
    ML --> LR_MODEL
    
    ML --> RS
    
    RS --> PERC
    RS --> THRESH
    RS --> KMEANS
    RS --> SVM
    RS --> KNN
    
    RS --> OUT
    OUT --> RISK
    OUT --> DB_UPDATE
    OUT --> REPORT
```

## Performance and Validation

### Model Evaluation Metrics
- **Primary Metric**: AUC-ROC Score (Area Under Receiver Operating Characteristic)
- **Cross-Validation**: 5-fold stratified CV maintaining class distribution
- **Secondary Metrics**: Precision, recall, F1-score for each class
- **Confusion Matrix**: Classification accuracy breakdown

### Expected Performance Ranges
- **Random Forest**: Typically achieves 0.75-0.85 AUC
- **Gradient Boosting**: Generally 0.78-0.88 AUC with proper tuning
- **Logistic Regression**: Usually 0.70-0.80 AUC as baseline

### Risk Score Validation
Each risk algorithm is validated by:
- **Distribution Analysis**: Ensuring appropriate risk level distributions
- **Actual vs Predicted**: Comparing delinquency rates within each risk tier
- **Business Logic**: Verifying high-risk borrowers have higher actual delinquency
- **Stability Testing**: Cross-validation performance across different data splits

## Key Insights and Feature Importance

Based on typical delinquency analysis, the most influential factors usually include:

1. **Payment History Metrics** (Highest Impact)
   - Historical delinquency rate
   - Payment consistency scores
   - Average days late on payments

2. **Financial Stress Indicators**
   - Debt-to-income ratio
   - Payment-to-income burden
   - Low income risk flags

3. **Loan Characteristics**
   - Loan-to-value ratio
   - Interest rate levels
   - Loan term length

4. **Demographic Risk Factors**
   - Age-related risk (very young borrowers)
   - Employment status stability
   - Geographic risk factors

5. **Educational Program Factors**
   - Program difficulty level
   - Job market outlook
   - Expected ROI on education

## Error Handling and Robustness

### Data Quality Management
- **Missing Value Imputation**: Mean imputation for numerical features
- **Infinite Value Handling**: Replacement with finite approximations
- **Categorical Encoding**: Robust label encoding with 'Unknown' fallbacks
- **Data Type Consistency**: Automatic conversion to appropriate ML formats

### Model Stability Features
- **Stratified Sampling**: Maintains class balance in train/test splits
- **Cross-Validation**: 5-fold CV reduces overfitting risk
- **Multiple Algorithms**: Ensemble approach reduces single-model bias
- **Hyperparameter Consistency**: Fixed random seeds ensure reproducibility

### Database Robustness
- **Schema Flexibility**: Graceful handling of existing columns
- **Transaction Safety**: Commit-based updates with rollback capability
- **Validation Checks**: Verification of update counts and distributions
- **Error Recovery**: Informative error messages and suggested corrections

## Technical Implementation Details

### Dependencies and Requirements
- **Core ML**: scikit-learn for all machine learning algorithms  
- **Data Processing**: pandas for data manipulation, numpy for numerical operations
- **Database**: sqlite3 for database connectivity and SQL operations
- **Utilities**: argparse for command-line interface

### Configuration Parameters
- **Random State**: Fixed at 42 for reproducibility across runs
- **Test Size**: 20% held out for final model evaluation
- **Cross-Validation Folds**: 5-fold stratified for robust validation
- **Model Hyperparameters**: Optimized for balance between performance and interpretability

### Scalability Considerations
- **Memory Efficiency**: Processes data in single batch (suitable for datasets up to 100K records)
- **Computation Speed**: Optimized algorithms with reasonable default parameters
- **Database Updates**: Batch processing for efficient database operations
- **Feature Engineering**: Vectorized operations using pandas/numpy for speed

## Future Enhancements

### Potential Model Improvements
1. **Advanced Algorithms**: XGBoost, LightGBM, or Neural Networks
2. **Hyperparameter Tuning**: Grid search or Bayesian optimization
3. **Feature Selection**: Automated feature selection algorithms
4. **Ensemble Methods**: Voting classifiers combining multiple algorithms

### Additional Risk Factors
1. **External Data Integration**: Credit scores, economic indicators
2. **Temporal Features**: Seasonal patterns, economic cycles
3. **Social Network Analysis**: Peer group risk factors
4. **Alternative Data**: Social media, spending patterns

### Operational Enhancements
1. **Real-time Scoring**: API endpoint for live risk assessment
2. **Model Monitoring**: Performance drift detection and alerts
3. **Automated Retraining**: Scheduled model updates with new data
4. **Business Rules Integration**: Combining ML scores with policy rules

## Conclusion

The delinquency analysis system provides a comprehensive, production-ready machine learning solution for loan risk assessment. It combines robust data engineering, multiple ML algorithms, and flexible risk scoring to deliver actionable insights for loan portfolio management. The modular design allows for easy maintenance, enhancement, and integration with existing loan origination and servicing systems.
- Age, income, employment status, marital status, location
- Risk categories: low_income_risk, young_borrower_risk

#### Loan Info Features  
- Loan amount, interest rate, term, LTV ratio
- Financial ratios: debt_to_income_ratio, payment_to_income_ratio
- Time-based: loan_age_days, days_to_maturity

#### Program Features
- Difficulty level, employment rate, starting salary
- Education ROI, program type, university prestige

#### Payment Behavior Features
- Missed payments, late fees, payment consistency
- Average days late, delinquency rate

### Target Variable
Binary classification based on whether a borrower has any missed payments in their history.

## Output

### Risk Scores
- **Range**: 1% to 100%
- **Interpretation**: Higher percentages indicate greater delinquency risk
- **Storage**: Updated in `loan_info.delinquency_risk` column

### Feature Importance Analysis
The analysis identifies the most influential attributes across all tables:

**Expected Top Risk Factors:**
1. Payment behavior metrics (missed_payments, delinquency_rate)
2. Financial ratios (debt_to_income_ratio, payment_to_income_ratio)
3. Demographics (age, annual_income_cad)
4. Program characteristics (program_difficulty, employment_rate_percent)
5. Loan characteristics (loan_amount, interest_rate, days_to_maturity)

### Model Performance
- **Cross-validation** ensures robust results
- **AUC scores** measure predictive accuracy
- **Feature importance rankings** show which attributes matter most

## Integration with Existing System

### Database Updates
- Automatically adds `delinquency_risk` column if it doesn't exist
- Updates risk scores for all borrowers
- Maintains existing table structure and relationships

### Enhanced Reporting
The `explore_database.py` script now includes:
- ML-based risk score distribution analysis
- Top highest-risk borrowers identification
- Model validation comparing predicted vs actual delinquency

### CSV Exports
Risk scores are automatically included in loan_info CSV exports via `run_data_generation.py --export_csv` in the database_exports folder.

## Requirements

### Python Packages
```bash
pip install pandas numpy scikit-learn
```

### Data Requirements
- Minimum 100+ borrowers for reliable ML training
- Complete data across all 4 tables
- Payment history data for target variable creation

## Interpretation Guide

### Risk Score Ranges
- **1-5%**: Very Low Risk - Excellent payment history, strong financials
- **5-10%**: Low Risk - Good payment behavior, stable income
- **10-15%**: Moderate Risk - Some risk factors present
- **15-25%**: High Risk - Multiple risk factors, requires monitoring
- **25-50%**: Very High Risk - Significant delinquency indicators
- **50%+**: Extreme Risk - Multiple severe risk factors

### Business Applications
1. **Loan Origination**: Screen new applicants using risk model
2. **Portfolio Management**: Monitor existing loans by risk tier
3. **Collection Strategy**: Prioritize outreach to high-risk borrowers
4. **Pricing**: Risk-based interest rate adjustments
5. **Regulatory Reporting**: Comprehensive risk assessment documentation

## Validation

The system includes automatic validation:
- **Cross-validation** during training ensures model stability
- **Holdout testing** measures real-world performance
- **Correlation analysis** between predicted risk and actual delinquency
- **Distribution analysis** shows realistic risk score ranges

## Troubleshooting

### Common Issues
1. **Insufficient data**: Need minimum 100+ borrowers with payment history
2. **Missing tables**: Ensure all 4 tables are populated
3. **Package errors**: Install required Python packages
4. **Database locks**: Close other database connections

### Performance Optimization
- Analysis typically takes 30-60 seconds for 1000+ borrowers
- Memory usage scales with dataset size
- Consider sampling for very large datasets (10,000+ borrowers)

## Future Enhancements

Potential improvements:
1. **Real-time scoring**: API endpoint for instant risk assessment
2. **Model updates**: Periodic retraining with new data
3. **Advanced features**: Economic indicators, seasonality effects
4. **Ensemble methods**: Combining multiple model predictions
5. **Explainable AI**: Individual prediction explanations