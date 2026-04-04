# Delinquency Website - Student Loan Analytics Platform

A comprehensive full-stack local development application for synthetic student loan delinquency analysis, featuring advanced machine learning analytics, exploratory data analysis (EDA), and interactive visualizations. Built with Angular 17 frontend and Flask backend.

## 🚀 Key Features

- 🎲 **Synthetic Data Generation**: Generate comprehensive mock student loan data
- 🤖 **ML-Powered Risk Analysis**: Advanced delinquency risk prediction with multiple algorithms
- 📊 **Interactive EDA**: Principal Component Analysis with interactive Plotly visualizations
- 📈 **Campaign Management**: Generate targeted marketing campaign files
- 💻 **Modern Web Interface**: Responsive Angular SPA with Bootstrap styling
- 📄 **File Management**: Static file serving with detailed metadata
- 💾 **Persistent State**: LocalStorage-based panel state management

## 📋 Architecture

- **Frontend**: Angular 17 SPA with TypeScript, Bootstrap 5, and Bootstrap Icons
- **Backend**: Flask REST API with Python ML pipeline
- **Database**: SQLite with comprehensive schema design
- **Analytics**: scikit-learn, pandas, matplotlib, seaborn, plotly
- **Visualization**: Interactive charts with file download capabilities

## 🎯 Core Features

### 1. 🎲 Data Generation
- **Comprehensive Dataset**: 1000+ borrower records with realistic distributions
- **Multi-table Schema**: User profiles, loan information, programs of study, payment history
- **Configurable Parameters**: Customizable date ranges and borrower counts
- **Data Integrity**: Foreign key relationships and referential integrity

### 2. 🤖 Delinquency Risk Analysis
- **ML Pipeline**: Random Forest, Gradient Boosting, and Logistic Regression models
- **Feature Engineering**: 60+ engineered features from raw data
- **Risk Algorithms**: 5 different scoring algorithms (Percentile, Threshold, K-Means, SVM, KNN)
- **Performance Metrics**: AUC-ROC scoring with cross-validation
- **Interactive Results**: Risk distribution analysis with detailed statistics

### 3. 📊 Exploratory Data Analysis (EDA)
- **Principal Component Analysis**: Configurable PCA with variance analysis
- **Interactive Visualizations**: 8 different chart types with Plotly integration
- **K-means Clustering**: Customizable cluster analysis on PCA components  
- **Generated Files**: HTML charts, CSV summaries, and comprehensive MD reports
- **File Metadata**: Size, creation date, and description for each analysis file

### 4. 📈 Campaign Generation
- **Targeted Lists**: Medium and high-risk borrower campaigns
- **Export Formats**: CSV files with borrower contact information
- **Risk-based Segmentation**: Automatic filtering by delinquency risk levels

## 📁 Project Structure

```
delinquency-website/
├── src/
│   ├── api/                           # Flask Backend
│   │   ├── shared/                    # Database & Utilities
│   │   │   ├── database.py           # SQLite database management
│   │   │   └── mock_data.py          # Synthetic data generation
│   │   ├── services/                  # Analysis Services
│   │   │   ├── delinquency_analysis/  # ML Pipeline
│   │   │   │   ├── delinquency_analysis.py
│   │   │   │   └── exploratory_data_analysis.py
│   │   │   ├── run_risk_estimation.py
│   │   │   ├── run_eda_analysis.py
│   │   │   ├── run_eda_analysis_json.py
│   │   │   └── generate_campaign_files.py
│   │   ├── static/                    # Static File Serving
│   │   │   └── eda_outputs/          # Generated EDA files
│   │   ├── app.py                     # Main Flask application
│   │   └── requirements.txt           # Python dependencies
│   └── web/                          # Angular Frontend
│       ├── src/app/                  # Angular Application
│       │   ├── components/           # UI Components
│       │   │   └── home/            # Main dashboard
│       │   ├── services/            # HTTP Services
│       │   │   └── data.service.ts  # API communication
│       │   └── interfaces/          # TypeScript interfaces
│       ├── package.json             # Node.js dependencies
│       ├── angular.json             # Angular CLI config
│       └── tsconfig.json            # TypeScript config
├── student_loan_data.db             # SQLite database (auto-created)
├── README.md                        # This documentation
└── DELINQUENCY_ANALYSIS.md         # Technical analysis guide
```

## 🛠 API Endpoints

Base URL: `http://localhost:5000/api`

### Core Data Operations
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/generate-data` | POST | Generate synthetic data | `num_payers`, `start_date`, `end_date` |
| `/get-user-profiles` | GET | Retrieve user profiles | - |
| `/get-loan-info` | GET | Retrieve loan information | - |
| `/get-programs` | GET | Retrieve programs of study | - |
| `/get-loan-payments` | GET | Retrieve payment history | - |

### Analytics & ML
| Endpoint | Method | Description | Parameters |
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
```python
algorithms = [
    'percentile',  # 60%-30%-10% split (default)
    'threshold',   # Fixed 0.3/0.6 thresholds
    'kmeans',      # K-means clustering  
    'svm',         # Support Vector Machine
    'knn'          # K-Nearest Neighbors
]
```

### Data Generation Parameters
```typescript
parameters = {
    num_payers: 1000,           // Number of borrowers (100-10000)
    start_date: '2020-01-01',   // Loan origination start
    end_date: '2023-12-31'      // Loan origination end
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

### Common Issues

**CORS Errors**
```bash
# Ensure Flask-CORS is installed
pip install flask-cors

# Check CORS headers in browser dev tools
```

**Port Conflicts**
```bash
# Check port usage
netstat -ano | findstr :4200
netstat -ano | findstr :5000

# Use alternative ports
ng serve --port 4201
```

**Database Issues**
```bash  
# Verify database creation
ls -la student_loan_data.db

# Check database integrity
python -c "from shared.database import DatabaseManager; dm = DatabaseManager(); print('DB OK')"
```

**Missing Dependencies**
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies  
npm install

# Clear cache if needed
npm cache clean --force
```

### Debug Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Test data generation
curl -X POST http://localhost:5000/api/generate-data \
  -H "Content-Type: application/json" \
  -d '{"num_payers": 100}'
```

## 📝 Development Notes

### File Size Optimization
- EDA HTML files are large (~4 MB) due to embedded Plotly data
- Consider implementing data compression for production
- Static file caching recommended for better performance

### Browser Compatibility  
- Modern browsers required for ES2020+ features
- Interactive charts require JavaScript enabled
- File downloads may be blocked by popup blockers

### Performance Considerations
- EDA generation takes 30-60 seconds for 1000 records
- Risk analysis completes in 10-20 seconds
- Consider implementing progress indicators for long operations

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 Additional Documentation

- **Technical Analysis**: See `DELINQUENCY_ANALYSIS.md` for ML pipeline details
- **API Reference**: Endpoint documentation with request/response examples
- **Database Schema**: Complete ERD with relationship documentation
   python app.py
   ```
   
   **Frontend (Angular)**:
   ```bash
   cd src/web
   npm start
   ```

5. **Access the application**:
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:5000/api
   - Database: `delinquency_data.db` (created automatically)

## Production Deployment

For production deployment, you can:

1. **Deploy to any cloud platform** (Heroku, DigitalOcean, AWS, etc.)
2. **Containerize with Docker**:
   ```dockerfile
   # Backend Dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY src/api/ .
   RUN pip install -r requirements.txt
   CMD ["python", "app.py"]
   ```
3. **Serve Angular build** with any static file server
4. **Use PostgreSQL or MySQL** for production database

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