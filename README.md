# Delinquency Website - Local Development Application

A full-stack local development application for managing and analyzing synthetic delinquency data, built with Angular frontend and Flask backend.

## Architecture

- **Frontend**: Angular 17 SPA running on development server
- **Backend**: Flask REST API with Python
- **Database**: Local SQLite database

## Features

- 🎲 **Synthetic Data Generation**: Generate mock data for all entity types
- 👥 **User Profiles**: Manage user profile information
- 💰 **Loan Information**: Track loan details with user relationships
- 📚 **Programs of Study**: Catalog of academic programs
- 💳 **Loan Payments**: Payment history with delinquency tracking

## Project Structure

```
delinquency-website/
├── src/
│   ├── api/                    # Flask API (Python)
│   │   ├── shared/            # Shared utilities
│   │   │   ├── database.py    # Database management
│   │   │   └── mock_data.py   # Data generation modules
│   │   ├── app.py             # Main Flask application
│   │   └── requirements.txt   # Python dependencies
│   └── web/                   # Angular frontend
│       ├── src/app/          # Angular application
│       │   ├── components/   # UI components
│       │   ├── services/     # Data services
│       │   └── interfaces/   # TypeScript interfaces
│       ├── package.json      # Node.js dependencies
│       ├── angular.json      # Angular CLI configuration
│       └── tsconfig.json     # TypeScript configuration
├── delinquency_data.db       # SQLite database (created automatically)
└── README.md                 # This file
```

## API Endpoints

All endpoints run on `http://localhost:5000`

| Endpoint | Method | Description |
|----------|--------|-----------|
| `/api/generate-data` | POST | Generate all synthetic data |
| `/api/get-user-profiles` | GET | Retrieve user profiles |
| `/api/get-loan-info` | GET | Retrieve loan information |
| `/api/get-programs` | GET | Retrieve programs of study |
| `/api/get-loan-payments` | GET | Retrieve loan payments |
| `/api/health` | GET | Health check endpoint |

## Data Model

### User Profiles
- ID, first name, last name, email, created date

### Loan Information  
- ID, user ID, loan amount, interest rate, loan type, created date

### Programs of Study
- ID, program name, degree level, duration in months

### Loan Payments
- ID, loan ID, payment amount, payment date, status

## Development Setup

### Prerequisites
- [Node.js 18+](https://nodejs.org/)
- [Python 3.9+](https://www.python.org/)
- [Git](https://git-scm.com/) (optional)

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd delinquency-website
   ```

2. **Install backend dependencies**:
   ```bash
   cd src/api
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**:
   ```bash
   cd src/web
   npm install
   ```

4. **Start development servers**:
   
   **Backend (Flask API)**:
   ```bash
   cd src/api
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