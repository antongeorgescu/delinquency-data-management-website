# Delinquency Website - ML-Powered Student Loan Analytics Platform

A comprehensive full-stack application for synthetic student loan delinquency analysis, featuring advanced machine learning risk prediction with 9 algorithms, exploratory data analysis (EDA), and interactive performance visualizations. Built with Angular 17 frontend and Flask ML backend.

## 🚀 Key Features

- 🎲 **Synthetic Data Generation**: Generate comprehensive mock student loan datasets (100-5,000 borrowers)
- 🤖 **ML-Powered Risk Analysis**: 9 advanced algorithms including Random Forest, Gradient Boosting, Neural Networks
- 📊 **Interactive EDA**: Principal Component Analysis with Plotly visualizations and K-means clustering
- 📈 **Campaign Management**: Generate targeted marketing campaigns for high-risk borrowers
- 💻 **Modern Web Interface**: Responsive Angular SPA with Bootstrap 5 and performance metrics tooltips
- 🎯 **Individual Algorithm Training**: Each algorithm trains independently for optimized performance
- 📄 **Enhanced Performance Display**: AUC scores, cross-validation metrics, and detailed algorithm insights

## 📋 Technology Stack

- **Frontend**: Angular 17, TypeScript, Bootstrap 5, Bootstrap Icons
- **Backend**: Flask 3.1.3, Python 3.9+
- **Machine Learning**: scikit-learn, NumPy 2.2.6, Pandas 3.0.2  
- **Database**: SQLite with comprehensive schema design
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Development**: Node.js 18+, pip virtual environments

## 🤖 Machine Learning Algorithms

### Classification Algorithms (6)
1. **Random Forest** - Ensemble method with decision trees, excellent for general purpose
2. **Gradient Boosting** - Sequential ensemble learning, high accuracy for complex patterns
3. **Logistic Regression** - Linear statistical model, interpretable probability estimation
4. **Neural Network** - Multi-layer perceptron, complex pattern recognition
5. **Support Vector Machine (SVM)** - Kernel-based classification with optimal boundaries
6. **K-Nearest Neighbors (KNN)** - Instance-based learning using neighbor similarity

### Statistical Methods (3)
7. **Percentile Algorithm** - Risk based on 60th/90th percentile distribution
8. **Threshold Algorithm** - Fixed cutoffs at 0.6/0.9 risk score thresholds  
9. **K-Means Clustering** - Unsupervised clustering for risk segmentation

## 🎯 Risk Classification System

**Updated Threshold Values:**
- **Low Risk**: < 0.6 (60%)
- **Medium Risk**: 0.6 - 0.9 (60-90%)  
- **High Risk**: > 0.9 (90%+)

**Performance Metrics:**
- **AUC Scores**: 90-100% (Excellent), 80-89% (Good), 70-79% (Fair), <70% (Poor)
- **Cross-Validation**: Mean ± standard deviation across data splits
- **Performance Ratings**: Automated assessment with color-coded indicators

## 📊 Enhanced UI Features

### Performance Metrics Display
- **Information Tooltips**: Detailed explanations for AUC Score, Performance Rating, and CV Mean
- **Algorithm Details**: Descriptions, strengths, parameters, and best use cases
- **Visual Indicators**: Color-coded performance ratings and interactive charts
- **Responsive Design**: Bootstrap 5 grid with mobile optimization

### Interactive Panels
- **Risk Estimation Results**: Comprehensive performance metrics for Classification Algorithms
- **EDA Analysis Results**: File metadata, download links, and statistical summaries  
- **Campaign Generation**: Risk-based borrower segmentation and CSV exports
- **Persistent State**: LocalStorage-based panel state across browser sessions

## 📁 Project Structure

```
delinquency-website/
├── README.md                          # This comprehensive documentation
├── DELINQUENCY_ANALYSIS.md           # Technical ML pipeline analysis
├── student_loan_data.db              # SQLite database (auto-created)
├── start.bat                         # Windows batch startup script
├── start.ps1                         # PowerShell startup script
├── minimal_flask.py                  # Minimal Flask test server
├── database_exports/                 # CSV data exports
│   ├── loan_info_*.csv
│   ├── loan_payments_*.csv
│   ├── program_of_study_*.csv
│   └── user_profile_*.csv
├── eda_outputs/                      # Generated EDA analysis files
│   ├── *.html                        # Interactive Plotly visualizations
│   ├── *.csv                         # Statistical summaries
│   └── *.md                          # Analysis reports
├── src/
│   ├── api/                          # Flask Backend (Python)
│   │   ├── app.py                    # Main Flask application with API endpoints
│   │   ├── requirements.txt          # Python dependencies (Flask, scikit-learn, etc.)
│   │   ├── shared/                   # Core database and utilities
│   │   │   └── database.py           # SQLite database management
│   │   ├── services/                 # ML and analysis services
│   │   │   ├── algorithms.json       # 9 algorithm configurations
│   │   │   ├── run_risk_estimation.py # Individual algorithm training
│   │   │   ├── run_eda_analysis.py   # EDA analysis execution
│   │   │   ├── generate_campaign_files.py # Campaign CSV generation
│   │   │   ├── delinquency_analysis/ # ML pipeline core
│   │   │   │   ├── delinquency_analysis.py # Risk analysis algorithms
│   │   │   │   └── exploratory_data_analysis.py # PCA and clustering
│   │   │   ├── synthetic_data/       # Data generation modules  
│   │   │   │   ├── generate_user_profiles.py
│   │   │   │   ├── generate_loans.py
│   │   │   │   ├── generate_payments.py
│   │   │   │   └── generate_programs.py
│   │   │   ├── campaigns/            # Generated campaign files
│   │   │   ├── eda_outputs/          # EDA visualization files
│   │   │   └── database_exports/     # CSV data exports
│   │   └── static/                   # Static file serving
│   │       └── eda_outputs/          # Public EDA files
│   └── web/                          # Angular Frontend (TypeScript)
│       ├── package.json              # Node.js dependencies
│       ├── angular.json              # Angular CLI configuration
│       ├── tsconfig.json             # TypeScript compiler settings
│       └── src/
│           ├── index.html            # Main HTML template
│           ├── main.ts               # Angular bootstrap
│           ├── styles.css            # Global styles
│           └── app/
│               ├── app.component.*   # Root Angular component
│               ├── components/       # UI Components
│               │   └── home/         # Main dashboard component
│               │       ├── home.component.html # UI template with tooltips
│               │       ├── home.component.ts # Component logic + tooltip handling
│               │       └── home.component.css # Component styles
│               ├── services/         # HTTP services
│               │   └── data.service.ts # API communication service
│               └── interfaces/       # TypeScript interfaces
│                   └── data.interface.ts # API response types
```

## 💾 Database Schema

### Core Tables
```sql
-- Borrower demographics and employment information
user_profile (
    id INTEGER PRIMARY KEY,
    first_name TEXT, last_name TEXT, email TEXT,
    phone TEXT, address TEXT, city TEXT, state TEXT, zip_code TEXT,
    date_of_birth DATE, ssn TEXT,
    employment_status TEXT, annual_income REAL,
    credit_score INTEGER, created_at TIMESTAMP
);

-- Loan details with ML-generated risk scores  
loan_info (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES user_profile(id),
    program_id INTEGER REFERENCES program_of_study(id), 
    loan_amount REAL, interest_rate REAL,
    loan_term_months INTEGER, origination_date DATE,
    loan_status TEXT, risk_score REAL,
    created_at TIMESTAMP
);

-- Academic program information
program_of_study (
    id INTEGER PRIMARY KEY,
    program_name TEXT, degree_level TEXT,
    field_of_study TEXT, program_length_months INTEGER,
    average_salary REAL, employment_rate REAL,
    created_at TIMESTAMP  
);

-- Payment history and delinquency tracking
loan_payments (
    id INTEGER PRIMARY KEY,
    loan_id INTEGER REFERENCES loan_info(id),
    payment_date DATE, amount_due REAL, amount_paid REAL,
    days_late INTEGER, payment_status TEXT,
    created_at TIMESTAMP
);
```

### Data Relationships
- **1:N User → Loans**: One borrower can have multiple loans
- **1:N Program → Loans**: One program can have many borrower loans  
- **1:N Loan → Payments**: One loan has multiple payment records
- **Referential Integrity**: Foreign key constraints maintained

## 📊 Generated Analysis Files

### EDA Visualization Files (Interactive HTML)
| File | Size | Description |
|------|------|-------------|
| `pca_scree_plot.html` | ~4.4 MB | Variance explained by each Principal Component |
| `pca_scatter_plot.html` | ~4.4 MB | PC1 vs PC2 scatter plot colored by risk level |
| `pca_biplot_pc1_vs_pc2.html` | ~4.4 MB | Feature contribution vectors and data points |
| `pca_feature_contributions.html` | ~4.4 MB | Feature loading analysis for all components |
| `feature_correlation_heatmap.html` | ~4.4 MB | Correlation matrix heatmap with clustering |
| `pca_clustering_k{n}.html` | ~4.4 MB | K-means clustering results on PCA space |

### Statistical Summary Files
| File | Size | Description |
|------|------|-------------|
| `cluster_analysis_summary.csv` | ~400 B | Statistical summary of K-means clusters |
| `eda_comprehensive_report.md` | ~2.4 KB | Detailed analysis report with insights |

### Campaign Files (Generated)
| File | Description |
|------|-------------|
| `high_risk_users.csv` | High-risk borrowers for intervention campaigns |
| `medium_risk_users.csv` | Medium-risk borrowers for monitoring programs |

## 🔐 Security & Best Practices

### Input Validation & Sanitization
- **Parameter Validation**: All API endpoints validate input parameters
- **SQL Injection Prevention**: Parameterized queries throughout application
- **Path Traversal Protection**: Secure file serving with path validation
- **Error Handling**: Sanitized error messages without sensitive data exposure

### CORS Configuration
- **Development**: Configured for localhost:4200 ↔ localhost:5000
- **Production**: Configurable origins through environment variables
- **Preflight Handling**: Proper OPTIONS request support

### Data Privacy
- **Synthetic Data Only**: No real borrower information stored or processed
- **Local Storage**: All data stored locally, no external transmission
- **Session Management**: Frontend state stored in browser localStorage only

## 🚀 Performance Guidelines

### Recommended Dataset Sizes
- **Testing/Development**: 100-500 borrowers (fast processing)
- **Demo/Presentation**: 1,000 borrowers (standard performance) 
- **Analysis/Research**: 2,000-5,000 borrowers (comprehensive dataset)
- **Maximum**: 10,000 borrowers (performance limitations apply)

### Algorithm Performance Tiers
- **Fastest**: Percentile, Threshold (~5 seconds)
- **Fast**: Logistic Regression, KNN (~10-15 seconds)  
- **Medium**: Random Forest, SVM (~15-30 seconds)
- **Slower**: Gradient Boosting, Neural Network (~30-60 seconds)

### System Requirements
- **RAM**: 4GB minimum, 8GB+ recommended for large datasets
- **CPU**: Multi-core processor recommended for ML training
- **Storage**: 100MB+ free space for database and EDA files
- **Network**: Not required (fully local development)

## 🛠 API Endpoints

Base URL: `http://localhost:5000/api`

### Core Data Operations
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/generate-data` | POST | Generate synthetic loan data | `num_payers`, `start_date`, `end_date` |
| `/get-user-profiles` | GET | Retrieve borrower profiles | - |
| `/get-loan-info` | GET | Retrieve loan information | - |
| `/get-programs` | GET | Retrieve programs of study | - |
| `/get-loan-payments` | GET | Retrieve payment history | - |

### Machine Learning & Analytics
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/risk-estimation` | POST | Run ML risk analysis with selected algorithm | `algorithm` (algorithm_id) |
| `/risk-models` | GET | Get all 9 available algorithms with details | - |
| `/eda-reports` | POST | Generate EDA with PCA and clustering | `n_clusters`, `n_components` |

### Enhanced Risk Analysis Response
```json
{
  "success": true,
  "algorithm_used": "random_forest",
  "execution_time": 12.34,
  "risk_distribution": {
    "low_risk": {"count": 600, "percentage": 60.0},
    "medium_risk": {"count": 300, "percentage": 30.0}, 
    "high_risk": {"count": 100, "percentage": 10.0}
  },
  "model_performance": {
    "algorithm_category": "Classification Algorithm",
    "algorithm_details": {
      "name": "Random Forest",
      "type": "Ensemble Learning",
      "description": "Uses multiple decision trees...",
      "strengths": ["Handles missing values", "Feature importance"],
      "parameters": {"n_estimators": 100, "max_depth": 10},
      "best_for": "General purpose classification with high accuracy"
    },
    "performance_summary": {
      "auc_score": 0.95,
      "performance_rating": "Excellent",
      "cross_validation_mean": 0.94,
      "cross_validation_std": 0.02
    }
  }
}
```

### Campaign & File Management  
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/campaign-files` | POST | Generate targeted campaign CSV files | - |
| `/static/eda_outputs/<filename>` | GET | Serve generated EDA visualization files | `filename` |

### System Health
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/health` | GET | Application health check | - |

## 🏠 Local Deployment Guide

### Prerequisites
- **Python 3.9+** with pip package manager
- **Node.js 18+** with npm
- **Git** (optional, for cloning)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)

### Step-by-Step Setup

#### 1. Clone or Download Project
```bash
# Option A: Clone with Git
git clone <repository-url>
cd delinquency-website

# Option B: Download and extract ZIP file
# Extract to desired directory and navigate to it
```

#### 2. Backend Setup (Flask API)
```bash
# Navigate to API directory
cd src/api

# Create Python virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start Flask development server
python app.py

# ✅ Backend running at: http://localhost:5000
# ✅ API accessible at: http://localhost:5000/api
```

#### 3. Frontend Setup (Angular SPA)
```bash
# Open new terminal/command prompt
# Navigate to web directory  
cd src/web

# Install Node.js dependencies (this may take a few minutes)
npm install

# Start Angular development server
npm start

# ✅ Frontend running at: http://localhost:4200
# ✅ Application accessible in browser
```

#### 4. Verify Installation
1. Open browser to `http://localhost:4200`
2. Check that both servers are running:
   - Backend: API requests should complete successfully
   - Frontend: Interface should load without errors
3. Test basic functionality:
   - Generate sample data (100 borrowers recommended for testing)
   - Run risk estimation with any algorithm
   - View performance metrics with tooltips

### Quick Start Commands
```bash
# Terminal 1 - Start Backend
cd src/api
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Terminal 2 - Start Frontend  
cd src/web
npm install
npm start

# Access application at http://localhost:4200
```

### Development Environment Verification
```bash
# Check Python version
python --version  # Should be 3.9+

# Check Node.js version  
node --version     # Should be 18+
npm --version      # Should be 8+

# Test API health endpoint
curl http://localhost:5000/api/health

# Check database creation (after first data generation)
ls -la *.db  # Should show student_loan_data.db
```

### Production Deployment Options

#### Docker Containerization
```dockerfile
# Backend Dockerfile (src/api/Dockerfile)
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]

# Frontend Dockerfile (src/web/Dockerfile)  
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install && npm run build
EXPOSE 4200
CMD ["npm", "run", "serve:static"]
```

#### Cloud Platform Deployment
- **Heroku**: Deploy backend as Python app, frontend as static site
- **DigitalOcean App Platform**: Multi-component app with Python + static site
- **AWS**: Elastic Beanstalk + S3 for static assets
- **Azure**: App Service + Static Web Apps
- **Vercel/Netlify**: Frontend deployment with serverless backend

### Environment Configuration
```env
# Backend (.env file in src/api/)
FLASK_ENV=development
DATABASE_URL=sqlite:///student_loan_data.db
CORS_ORIGINS=http://localhost:4200

# Frontend (src/web/src/environments/)
API_BASE_URL=http://localhost:5000/api
PRODUCTION=false
```
|----------|--------|-------------|------------|
| `/risk-estimation` | POST | Run ML delinquency analysis | `algorithm` |
| `/risk-models` | GET | Get available risk algorithms | - |
| `/eda-reports` | POST | Generate EDA with visualizations | `n_clusters`, `n_components` |

### File Management
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/campaign-files` | POST | Generate campaign CSV files | `risk_levels[]` |
| `/static/eda_outputs/<filename>` | GET | Serve generated EDA files | `filename` |

### System
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/health` | GET | Health check endpoint | - |

## 💾 Database Schema

### Tables
- **user_profile**: Borrower demographics and employment
- **loan_info**: Loan details with ML-generated risk scores
- **program_of_study**: Academic program information
- **loan_payments**: Payment history and delinquency tracking

### Key Relationships
```sql
user_profile (1) → (many) loan_info
program_of_study (1) → (many) loan_info  
loan_info (1) → (many) loan_payments
```

## 🎨 UI Features

### Interactive Panels
- **Risk Estimation Results**: Risk distribution, statistics, and model performance
- **EDA Analysis Results**: File table with metadata, download links, and analysis summary
- **Campaign Generation**: Targeted borrower list creation and download

### Enhanced UX
- **Persistent State**: Panel states saved in localStorage
- **Responsive Design**: Bootstrap 5 responsive grid system
- **Icon Integration**: Bootstrap Icons for visual enhancement
- **Loading States**: Spinner indicators for long-running operations
- **Error Handling**: Comprehensive error messages and troubleshooting

## 🚀 Development Setup

### Prerequisites
- **Node.js 18+** with npm
- **Python 3.9+** with pip
- **Git** (recommended)

### Backend Setup
```bash
# Navigate to API directory
cd src/api

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start Flask development server
python app.py
# API available at: http://localhost:5000
```

### Frontend Setup
```bash  
# Navigate to web directory
cd src/web

# Install Node.js dependencies
npm install

# Start Angular development server
npm start
# Frontend available at: http://localhost:4200
```

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd delinquency-website

# Start both servers in separate terminals
# Terminal 1 - Backend
cd src/api && python app.py

# Terminal 2 - Frontend  
cd src/web && npm start

# Access application at http://localhost:4200
```

## 📊 EDA Analysis Files

When running EDA analysis, the following files are generated:

| File | Type | Size | Description |
|------|------|------|-------------|
| `pca_scree_plot.html` | Interactive Chart | ~4.4 MB | Variance explained by each PC |
| `pca_scatter_plot.html` | Interactive Chart | ~4.4 MB | PC1 vs PC2 colored by risk |
| `pca_biplot_pc1_vs_pc2.html` | Interactive Chart | ~4.4 MB | Feature contribution vectors |
| `pca_feature_contributions.html` | Interactive Chart | ~4.4 MB | Feature loadings analysis |
| `feature_correlation_heatmap.html` | Interactive Chart | ~4.4 MB | Correlation matrix heatmap |
| `pca_clustering_k{n}.html` | Interactive Chart | ~4.4 MB | K-means clustering results |
| `cluster_analysis_summary.csv` | Data Export | ~400 B | Statistical cluster summary |
| `eda_comprehensive_report.md` | Report | ~2.4 KB | Complete analysis report |

## 🔧 Configuration Options

### EDA Parameters
- **n_clusters**: Number of K-means clusters (1-20, default: 5)
- **n_components**: Number of PCA components (2-50, default: 10)

### Risk Analysis Algorithms
The system now supports 9 comprehensive algorithms:

```json
{
  "classification_algorithms": [
    {
      "id": "random_forest",
      "name": "Random Forest Classifier", 
      "category": "Classification Algorithm",
      "performance_tier": "Excellent (95%+ AUC)",
      "best_for": "General purpose with feature importance"
    },
    {
      "id": "gradient_boosting",
      "name": "Gradient Boosting Classifier",
      "category": "Classification Algorithm", 
      "performance_tier": "Excellent (95%+ AUC)",
      "best_for": "Complex patterns and high accuracy"
    },
    {
      "id": "logistic_regression", 
      "name": "Logistic Regression",
      "category": "Classification Algorithm",
      "performance_tier": "Good (85%+ AUC)",
      "best_for": "Interpretable probability estimation"
    },
    {
      "id": "neural_network",
      "name": "Neural Network (MLP)",
      "category": "Classification Algorithm",
      "performance_tier": "Excellent (95%+ AUC)", 
      "best_for": "Complex pattern recognition"
    },
    {
      "id": "svm",
      "name": "Support Vector Machine",
      "category": "Classification Algorithm",
      "performance_tier": "Good (85%+ AUC)",
      "best_for": "High-dimensional data with clear margins"
    },
    {
      "id": "knn", 
      "name": "K-Nearest Neighbors",
      "category": "Classification Algorithm",
      "performance_tier": "Fair (75%+ AUC)",
      "best_for": "Instance-based learning and local patterns"
    }
  ],
  "statistical_methods": [
    {
      "id": "percentile",
      "name": "Percentile Algorithm", 
      "category": "Statistical Distribution",
      "thresholds": "60th/90th percentiles",
      "best_for": "Distribution-based risk segmentation"
    },
    {
      "id": "threshold",
      "name": "Threshold Algorithm",
      "category": "Statistical Distribution", 
      "thresholds": "Fixed 0.6/0.9 cutoffs",
      "best_for": "Simple rule-based classification"
    },
    {
      "id": "kmeans",
      "name": "K-Means Clustering",
      "category": "Unsupervised Learning",
      "clusters": "3 risk-based clusters", 
      "best_for": "Unsupervised risk pattern discovery"
    }
  ]
}
```

### Data Generation Parameters
```typescript
interface DataGenerationParams {
  num_payers: number;     // 100-5000 borrowers (1000 recommended)
  start_date: string;     // Loan origination start (e.g., '2020-01-01')
  end_date: string;       // Loan origination end (e.g., '2023-12-31')
}
```

### EDA Configuration
```typescript 
interface EDAParams {
  n_clusters: number;     // K-means clusters (1-20, default: 5)
  n_components: number;   // PCA components (2-50, default: 10)
}
```

## 🔐 Security Features

- **Input Validation**: Comprehensive parameter validation on all endpoints
- **CORS Configuration**: Proper cross-origin configuration for development  
- **Path Traversal Protection**: Security checks for file serving
- **SQL Injection Prevention**: Parameterized queries throughout
- **Error Sanitization**: Safe error message exposure

## 🚀 Production Deployment

### Environment Variables
```env
# Flask Configuration
FLASK_ENV=production
DATABASE_URL=sqlite:///production.db

# Angular Configuration  
API_BASE_URL=https://your-api.com/api
```

### Docker Deployment
```dockerfile
# Backend Container
FROM python:3.9-slim
WORKDIR /app
COPY src/api/ .
RUN pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Frontend Container
FROM node:18-alpine
WORKDIR /app
COPY src/web/ .
RUN npm install && npm run build
CMD ["npm", "run", "serve:prod"]
```

### Cloud Platforms
- **AWS**: EB + S3 for static files
- **Azure**: App Service + Blob Storage
- **Heroku**: Web dyno + Heroku Postgres
- **DigitalOcean**: App Platform + Spaces

## 🔍 Troubleshooting

### Common Issues & Solutions

#### **Port Conflicts**
```bash
# Check if ports are in use
netstat -ano | findstr :4200  # Frontend port
netstat -ano | findstr :5000  # Backend port

# Kill processes using ports (Windows)
taskkill /PID <process_id> /F

# Use alternative ports
ng serve --port 4201     # Frontend
# Modify app.py for backend: app.run(port=5001)
```

#### **CORS (Cross-Origin) Errors**
```bash  
# Ensure Flask-CORS is installed
pip install flask-cors

# Check browser console for CORS errors
# Verify both servers are running on correct ports
# Frontend: http://localhost:4200
# Backend: http://localhost:5000
```

#### **NumPy Compatibility Issues**
```bash
# Install compatible NumPy version
pip install numpy==2.2.6

# If scikit-learn conflicts occur:
pip install --upgrade scikit-learn numpy pandas

# Clear pip cache if needed
pip cache purge
```

#### **Database Connection Issues**
```bash
# Check if database file exists (created after first data generation)
ls -la student_loan_data.db

# Test database connection
python -c "from shared.database import DatabaseManager; dm = DatabaseManager(); print('Database OK')"

# If database is corrupted, delete and regenerate
rm student_loan_data.db
# Then regenerate data through the web interface
```

#### **Frontend Build/Runtime Errors**
```bash
# Clear Node.js cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Check for TypeScript errors
npm run build

# Verify Angular CLI version
ng version
```

#### **ML Algorithm Training Failures**
```bash
# Check Python dependencies
pip install scikit-learn==1.8.0 numpy==2.2.6 pandas==3.0.2

# Validate data exists before running risk estimation
curl http://localhost:5000/api/get-user-profiles

# Check algorithm availability
curl http://localhost:5000/api/risk-models
```

### Performance Optimization

#### **Large Dataset Handling**
- **Recommended**: Start with 1000 borrowers for testing
- **Performance**: 5000+ borrowers may take 2-3 minutes for ML training
- **Memory**: Gradient Boosting and Neural Networks require more RAM

#### **EDA Generation Speed**
- **PCA Components**: Reduce from 10 to 5 for faster processing
- **Clusters**: Use 3-5 clusters to balance insight vs performance
- **File Size**: EDA HTML files are 4MB+ due to embedded Plotly data

#### **Browser Performance**
- **Chrome/Edge**: Best performance for interactive visualizations
- **Memory**: Close unused tabs when running large analyses  
- **JavaScript**: Ensure JavaScript is enabled for tooltips and charts

### Debug Endpoints & Testing

#### **Health Checks**
```bash
# Backend health
curl http://localhost:5000/api/health

# Check available algorithms 
curl http://localhost:5000/api/risk-models

# Test data generation (small dataset)
curl -X POST http://localhost:5000/api/generate-data \
  -H "Content-Type: application/json" \
  -d '{"num_payers": 100, "start_date": "2023-01-01", "end_date": "2023-12-31"}'
```

#### **Frontend Debug Mode**
```bash
# Run Angular in development mode with detailed logging
ng serve --verbose

# Check browser console for errors (F12 Developer Tools)
# Network tab shows API request/response details
```

### Known Limitations

#### **Browser Compatibility**
- **Modern Browsers Required**: ES2020+ features used (Chrome 88+, Firefox 78+, Safari 14+)
- **Internet Explorer**: Not supported
- **Mobile Browsers**: Limited functionality on small screens

#### **Dataset Constraints**  
- **Maximum Borrowers**: 10,000 (performance limitations)
- **Date Range**: 2020-2024 recommended for realistic data patterns
- **Database Size**: SQLite file grows ~1MB per 1000 borrowers

#### **Algorithm Performance**
- **Training Time**: Neural Networks take 30-60 seconds to train
- **Memory Usage**: Gradient Boosting requires 2GB+ RAM for large datasets
- **Cross-Validation**: May timeout on slower systems with 5000+ records

### Getting Help

#### **Error Reporting**
1. Check browser console (F12) for JavaScript errors
2. Check terminal/command prompt for Python backend errors
3. Verify both servers are running and accessible
4. Test with smaller dataset (100 borrowers) first

#### **Performance Issues**
1. Close unnecessary applications to free RAM
2. Use smaller datasets for testing (100-500 borrowers)
3. Clear browser cache and restart both servers
4. Check system resources with Task Manager/Activity Monitor

## � Additional Resources

### Technical Documentation
- **`DELINQUENCY_ANALYSIS.md`**: Comprehensive ML pipeline analysis, feature engineering details, and algorithm performance comparisons
- **API Documentation**: In-depth endpoint documentation with request/response examples
- **Database ERD**: Complete entity-relationship diagram with field descriptions
- **Algorithm Performance Report**: Detailed analysis of all 9 algorithms with benchmarks

### Learning Resources
- **Machine Learning**: scikit-learn documentation for algorithm details
- **Angular Development**: Angular 17 official guide and TypeScript handbook
- **Flask API Development**: Flask documentation and REST API best practices
- **Data Visualization**: Plotly documentation for interactive charts

### Development Tools
- **VS Code Extensions**: Angular Language Service, Python, REST Client
- **Browser DevTools**: Network tab for API debugging, Console for frontend errors
- **Database Tools**: DB Browser for SQLite for database inspection

## 🚦 Version History

### v2.0.0 - Current (ML-Enhanced)
- ✅ 9 comprehensive ML algorithms (6 Classification + 3 Statistical)
- ✅ Individual algorithm training for optimized performance
- ✅ Enhanced UI with performance metrics tooltips
- ✅ Updated risk thresholds (0.6/0.9) with comprehensive explanations
- ✅ Bootstrap 5 responsive design with accessibility features
- ✅ Detailed algorithm descriptions and performance ratings

### v1.0.0 - Initial Release
- Basic risk analysis with 5 algorithms
- Simple UI without performance metrics
- Original threshold system (0.3/0.6)
- Basic EDA functionality

## 🤝 Contributing

### Development Workflow
1. **Fork** the repository to your GitHub account
2. **Clone** your fork locally: `git clone <your-fork-url>`
3. **Create feature branch**: `git checkout -b feature/amazing-feature`
4. **Make changes** following the coding standards below
5. **Test thoroughly** with different algorithms and datasets
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open Pull Request** with detailed description of changes

### Coding Standards
- **Python**: Follow PEP 8, use type hints, comprehensive docstrings
- **TypeScript**: Use strict mode, proper interfaces, JSDoc comments  
- **HTML/CSS**: Semantic HTML5, accessible design, responsive layouts
- **API Design**: RESTful endpoints, consistent error handling, JSON responses

### Testing Guidelines
- **Unit Tests**: Test all new algorithm implementations
- **Integration Tests**: Verify API endpoints with various parameters
- **UI Testing**: Test responsive design across browsers and devices
- **Performance Testing**: Validate with different dataset sizes (100-5000 records)

### Feature Requests & Bug Reports
- **Use GitHub Issues** with detailed descriptions
- **Include reproduction steps** for bugs
- **Provide example data** when applicable
- **Label appropriately**: bug, enhancement, documentation, etc.

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for full details.

### MIT License Summary
- ✅ **Commercial Use**: Use in commercial projects
- ✅ **Modification**: Modify the source code  
- ✅ **Distribution**: Distribute original or modified versions
- ✅ **Private Use**: Use privately without restriction
- ❗ **Liability**: Software provided "as-is" without warranty
- ❗ **Attribution**: Include original license in distributions

## 🎯 Roadmap & Future Enhancements

### Planned Features (v2.1)
- **Model Persistence**: Save trained models for reuse across sessions
- **Feature Selection**: Automated feature importance analysis and selection
- **A/B Testing**: Compare multiple algorithms simultaneously  
- **Export Capabilities**: PDF reports and Excel-compatible analysis files

### Advanced Analytics (v3.0)
- **Time Series Analysis**: Payment pattern trends over time
- **Ensemble Methods**: Combine multiple algorithms for improved accuracy
- **Explainable AI**: SHAP values and LIME explanations for predictions
- **Real-time Scoring**: API endpoints for live risk assessment

### UI/UX Improvements
- **Dark Mode**: Toggle between light and dark themes
- **Mobile App**: React Native or Progressive Web App version
- **Advanced Filtering**: Multi-criteria borrower search and filtering
- **Dashboard Customization**: Drag-and-drop widget arrangement

## 💬 Support & Community

### Getting Help
1. **Check Documentation**: README, troubleshooting, and API docs
2. **Search Issues**: Existing GitHub issues may have solutions
3. **Create Issue**: Provide detailed description with reproduction steps
4. **Community Discussion**: GitHub Discussions for questions and ideas

### Contact Information
- **Technical Issues**: Create GitHub issue with error details
- **Feature Requests**: GitHub issues with enhancement label  
- **Security Concerns**: Contact maintainers directly
- **General Questions**: GitHub Discussions forum

---

**🏆 Comprehensive ML-Powered Student Loan Delinquency Analysis Platform**

*Built with Angular 17, Flask, scikit-learn, and modern web technologies for comprehensive local development and analysis capabilities.*

## Configuration

### Environment Variables

**Flask API** (optional):
- `FLASK_ENV`: `development` or `production`
- `DATABASE_URL`: Custom database connection (defaults to local SQLite)

**Angular Frontend**:
- API base URL is hardcoded to `http://localhost:5000/api` for local development

## Development Features

- **Hot Reload**: Both frontend and backend support hot reload during development
- **CORS Enabled**: Cross-origin requests configured for local development
- **Error Handling**: Comprehensive error handling and logging
- **SQLite Database**: Lightweight database perfect for development and small deployments

## Security

- Input validation on all API endpoints
- CORS configuration for frontend-backend communication
- SQL injection protection with parameterized queries
- Error message sanitization

## Cost

**Local Development**: Free! No cloud costs.
**Production Deployment**: Varies by hosting provider (typically $5-20/month for small applications)

## Troubleshooting

### Common Issues

1. **CORS errors**: Ensure Flask-CORS is installed and configured
2. **Database not found**: Database file will be created automatically on first run
3. **Port conflicts**: Ensure ports 4200 and 5000 are available
4. **Module not found**: Check that you're in the correct directory when running commands

### Logs and Diagnostics

```bash
# Check if Flask API is running
curl http://localhost:5000/api/health

# View Flask logs in the terminal where you started the API
# View Angular logs in the terminal where you started ng serve
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is licensed under the MIT License.