"""
Flask API server for delinquency data management
"""
import sys
import os
import json
import math
from datetime import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

# Add the shared and services directories to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from database import DatabaseManager
from run_data_generation import generate_complete_dataset
from explore_database import explore_database

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

def sanitize_json_data(obj):
    """
    Recursively sanitize data to ensure JSON compatibility
    Converts None, NaN, inf, -inf to null or appropriate values
    """
    if obj is None:
        return None
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None  # Convert NaN and infinite values to null
        return obj
    elif isinstance(obj, dict):
        return {key: sanitize_json_data(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_json_data(item) for item in obj]
    else:
        return obj

@app.route('/api/generate-data', methods=['POST'])
def generate_data():
    """
    Generate synthetic data for all entities using the data generation service
    """
    try:
        # Get parameters from POST request body
        data = request.get_json() or {}
        
        # Extract parameters with defaults
        num_payers = data.get('num_payers', 50)
        start_date = data.get('start_date', '2023-01-01')
        end_date = data.get('end_date', '2024-12-31')
        validate = data.get('validate', False)
        
        # Database path for the current database
        db_path = os.path.join(os.path.dirname(__file__), 'shared', 'student_loan_data.db')
        
        # Ensure the shared directory exists
        shared_dir = os.path.join(os.path.dirname(__file__), 'shared')
        os.makedirs(shared_dir, exist_ok=True)
        
        # Call the data generation service
        print(f"Generating data for {num_payers} payers from {start_date} to {end_date}")
        df_profiles, df_programs, df_loans, df_payments = generate_complete_dataset(
            num_payers=num_payers,
            start_date_str=start_date,
            end_date_str=end_date,
            db_path=db_path,
            validate=validate
        )
        
        # Return success response with generation statistics
        response_data = {
            "success": True,
            "message": "Synthetic data generated successfully using data generation service",
            "parameters": {
                "num_payers": num_payers,
                "start_date": start_date,
                "end_date": end_date,
                "validate": validate
            },
            "statistics": {
                "user_profiles": len(df_profiles),
                "loan_info": len(df_loans),
                "programs_of_study": len(df_programs),
                "loan_payments": len(df_payments)
            }
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to generate synthetic data"
        }
        
        return jsonify(error_response), 500

@app.route('/api/get-user-profiles', methods=['GET'])
def get_user_profiles():
    """
    Get user profiles with pagination
    """
    try:
        db_manager = DatabaseManager()
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 30))
        offset = (page - 1) * per_page
        
        # Get total count
        count_query = "SELECT COUNT(*) as total FROM user_profile"
        count_result = db_manager.execute_query(count_query)
        total_count = count_result[0]['total'] if count_result else 0
        
        # Get paginated data with all fields from user_profile table
        query = """
            SELECT payer_id, first_name, last_name, date_of_birth, age, 
                   address, city, province, employment_status, 
                   annual_income_cad, marital_status
            FROM user_profile
            ORDER BY payer_id ASC
            LIMIT ? OFFSET ?
        """
        
        user_profiles = db_manager.execute_query(query, (per_page, offset))
        
        response_data = {
            "success": True,
            "data": user_profiles,
            "count": len(user_profiles),
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve user profiles"
        }
        
        return jsonify(error_response), 500

@app.route('/api/get-loans', methods=['GET'])
def get_loans():
    """
    Get paginated loan information with borrower details
    """
    try:
        db_manager = DatabaseManager()
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 30))
        offset = (page - 1) * per_page
        
        # Get total count
        count_query = "SELECT COUNT(*) as total FROM loan_info"
        count_result = db_manager.execute_query(count_query)
        total_count = count_result[0]['total'] if count_result else 0
        
        # Get paginated loan data with all fields including borrower names
        query = """
            SELECT l.loan_id, l.payer_id, l.program_id, l.loan_amount, l.interest_rate,
                   l.loan_term_years, l.loan_term_months, l.loan_type, l.institution_name,
                   l.institution_city, l.institution_province, l.education_value,
                   l.down_payment, l.ltv_ratio, l.origination_date, l.disbursement_date,
                   l.maturity_date, l.current_balance, l.loan_status, l.lender,
                   l.program_duration_years, l.monthly_payment, l.grace_period_months,
                   l.delinquency_risk, u.first_name, u.last_name
            FROM loan_info l
            LEFT JOIN user_profile u ON l.payer_id = u.payer_id
            ORDER BY l.loan_id ASC
            LIMIT ? OFFSET ?
        """
        
        loans = db_manager.execute_query(query, (per_page, offset))
        
        response_data = {
            "success": True,
            "data": loans,
            "count": len(loans),
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve loan information"
        }
        
        return jsonify(error_response), 500

@app.route('/api/get-programs', methods=['GET'])
def get_programs():
    """
    Get paginated programs of study
    """
    try:
        db_manager = DatabaseManager()
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 30))
        offset = (page - 1) * per_page
        
        # Get total count
        count_query = "SELECT COUNT(*) as total FROM program_of_study"
        count_result = db_manager.execute_query(count_query)
        total_count = count_result[0]['total'] if count_result else 0
        
        # Get paginated programs data with all fields
        query = """
            SELECT program_id, program_name, program_type, field_of_study,
                   program_difficulty, duration_years, typical_tuition_cad,
                   employment_rate_percent, avg_starting_salary_cad,
                   accreditation_body, institution_type, university_name,
                   requires_licensing, job_market_outlook
            FROM program_of_study
            ORDER BY program_id ASC
            LIMIT ? OFFSET ?
        """
        
        programs = db_manager.execute_query(query, (per_page, offset))
        
        response_data = {
            "success": True,
            "data": programs,
            "count": len(programs),
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve programs of study"
        }
        
        return jsonify(error_response), 500

@app.route('/api/risk-models', methods=['GET'])
def get_risk_models():
    """
    Get available risk analysis models/algorithms
    """
    try:
        algorithms = [
            {
                'id': 'percentile',
                'name': 'Percentile Based',
                'short_name': 'Percentile',
                'description': 'Bottom 60% = Low(0), Next 30% = Medium(1), Top 10% = High(2)',
                'type': 'Statistical Distribution'
            },
            {
                'id': 'threshold',
                'name': 'Fixed Threshold',
                'short_name': 'Threshold',
                'description': 'Fixed probability thresholds: <0.6=Low, 0.6-0.9=Medium, >0.9=High',
                'type': 'Statistical Distribution'
            },
            {
                'id': 'random_forest',
                'name': 'Random Forest Classifier',
                'short_name': 'Random Forest',
                'description': 'Ensemble classifier with balanced classes and feature importance analysis',
                'type': 'Classification Algorithm'
            },
            {
                'id': 'gradient_boosting',
                'name': 'Gradient Boosting Classifier',
                'short_name': 'Gradient Boosting',
                'description': 'Gradient Boosting classifier for complex patterns and high accuracy',
                'type': 'Classification Algorithm'
            },
            {
                'id': 'logistic_regression',
                'name': 'Logistic Regression Classifier',
                'short_name': 'Logistic Regression',
                'description': 'Linear classifier with L2 regularization and balanced class handling',
                'type': 'Classification Algorithm'
            },
            {
                'id': 'neural_network',
                'name': 'Neural Network (MLP)',
                'short_name': 'Neural Network',
                'description': 'Multi-layer Perceptron with adaptive learning for complex pattern detection',
                'type': 'Classification Algorithm'
            },
            {
                'id': 'svm',
                'name': 'Support Vector Machine',
                'short_name': 'SVM',
                'description': 'Support Vector Machine classifier trained on probability-based risk labels',
                'type': 'Classification Algorithm'
            },
            {
                'id': 'knn',
                'name': 'K-Nearest Neighbors',
                'short_name': 'KNN',
                'description': 'K-Nearest Neighbors classifier with optimal k and distance weighting',
                'type': 'Classification Algorithm'
            },
            {
                'id': 'kmeans',
                'name': 'K-Means Clustering',
                'short_name': 'K-Means',
                'description': 'Clustering algorithm adapted for risk classification - groups borrowers into distinct risk categories',
                'type': 'Clustering Algorithm'
            }
        ]
        
        response_data = {
            'models': algorithms
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve risk models"
        }
        
        return jsonify(error_response), 500

@app.route('/api/risk-estimator', methods=['POST'])
def run_risk_estimator():
    """
    Run delinquency risk estimation analysis with specified algorithm
    """
    try:
        # Get parameters from POST request body
        data = request.get_json() or {}
        
        # Extract algorithm parameter with default
        algorithm = data.get('algorithm', 'random_forest')
        
        # Validate algorithm - include all supported algorithms
        valid_algorithms = ['percentile', 'threshold', 'random_forest', 'gradient_boosting', 'logistic_regression', 'neural_network', 'svm', 'knn', 'kmeans']
        if algorithm not in valid_algorithms:
            return jsonify({
                "success": False,
                "error": f"Invalid algorithm '{algorithm}'. Must be one of: {', '.join(valid_algorithms)}",
                "message": "Invalid algorithm specified"
            }), 400
        
        # Import and run the JSON-compatible risk estimation
        from services.run_risk_estimation import run_risk_estimation_json
        
        # Run the analysis and get JSON results
        results = run_risk_estimation_json(algorithm=algorithm)
        
        # Return results
        if results["success"]:
            return jsonify(results), 200
        else:
            return jsonify(results), 500
        
    except Exception as e:
        import traceback
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to run risk estimation analysis",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "traceback": traceback.format_exc()
        }
        
        # Log the error for debugging
        print(f"Risk estimation error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        return jsonify(error_response), 500

@app.route('/api/generate-campaign-files', methods=['POST'])
def generate_campaign_files_endpoint():
    """
    Generate targeted marketing campaign files based on delinquency risk levels
    """
    try:
        # Import and run the JSON-compatible campaign file generation
        from services.generate_campaign_files import generate_campaign_files_json
        
        # Run the campaign file generation and get JSON results
        results = generate_campaign_files_json()
        
        # Return results
        if results["success"]:
            return jsonify(results), 200
        else:
            return jsonify(results), 500
        
    except Exception as e:
        import traceback
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to generate campaign files",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "traceback": traceback.format_exc()
        }
        
        # Log the error for debugging
        print(f"Campaign generation error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        return jsonify(error_response), 500

@app.route('/api/download-campaign-file/<filename>', methods=['GET'])
def download_campaign_file(filename):
    """
    Download generated campaign files
    """
    try:
        # Define the campaigns directory path
        campaigns_dir = os.path.join(os.path.dirname(__file__), 'services', 'campaigns')
        
        # Validate filename for security
        allowed_files = ['medium_risk_users.csv', 'high_risk_users.csv']
        if filename not in allowed_files:
            return jsonify({
                "success": False,
                "error": "Invalid filename",
                "message": "File not found or access denied"
            }), 404
        
        file_path = os.path.join(campaigns_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "error": "File not found",
                "message": f"Campaign file '{filename}' does not exist. Please generate campaign files first."
            }), 404
        
        # Return the file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to download campaign file"
        }
        
        return jsonify(error_response), 500

@app.route('/api/get-payments', methods=['GET'])
def get_payments():
    """
    Get paginated loan payments with all fields
    """
    try:
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 30))
        offset = (page - 1) * per_page
        
        db_manager = DatabaseManager()
        
        # Get total count
        count_query = "SELECT COUNT(*) as total FROM loan_payments"
        count_result = db_manager.execute_query(count_query)
        total = count_result[0]['total'] if count_result else 0
        
        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page
        
        # Get data with pagination
        query = f"""
            SELECT 
                lp.payment_id,
                up.first_name,
                up.last_name,
                lp.due_date,
                lp.paid_date,
                lp.payment_due,
                lp.amount_paid,
                lp.principal_payment,
                lp.interest_payment,
                lp.escrow_payment,
                lp.late_fee,
                lp.total_amount_due,
                lp.remaining_balance,
                lp.status,
                lp.days_late,
                lp.payment_method,
                lp.payment_processor,
                lp.transaction_id,
                lp.confirmation_number,
                lp.payment_type
            FROM loan_payments lp
            LEFT JOIN user_profile up ON lp.payer_id = up.payer_id
            ORDER BY lp.payment_id ASC
            LIMIT {per_page} OFFSET {offset}
        """
        
        payments = db_manager.execute_query(query)
        
        response_data = {
            "success": True,
            "data": payments,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Error in get_payments: {str(e)}")
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve payments"
        }
        
        return jsonify(error_response), 500

@app.route('/api/get-loan-payments', methods=['GET'])  
def get_loan_payments():
    """
    Get all loan payments with loan and user details
    """
    try:
        db_manager = DatabaseManager()
        
        query = """
            SELECT 
                p.id,
                p.loan_id,
                p.payment_amount,
                p.payment_date,
                p.status,
                l.loan_amount,
                l.loan_type,
                u.first_name,
                u.last_name,
                u.email
            FROM loan_payments p
            JOIN loan_info l ON p.loan_id = l.id
            JOIN user_profile u ON l.user_id = u.id
            ORDER BY p.payment_date DESC
        """
        
        loan_payments = db_manager.execute_query(query)
        
        response_data = {
            "success": True,
            "data": loan_payments,
            "count": len(loan_payments)
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve loan payments"
        }
        
        return jsonify(error_response), 500

@app.route('/api/explore-database', methods=['GET'])
def explore_database_api():
    """
    Explore database structure and return comprehensive analysis in JSON format
    """
    try:
        # Get the database analysis result
        analysis_result = explore_database()
        
        # Sanitize the data to ensure proper JSON serialization
        analysis_result = sanitize_json_data(analysis_result)
        
        # Return success response with database analysis
        if "error" in analysis_result:
            error_response = {
                "success": False,
                "error": analysis_result["error"],
                "message": "Failed to explore database"
            }
            return jsonify(error_response), 500
        
        response_data = {
            "success": True,
            "message": "Database exploration completed successfully",
            "data": analysis_result
        }
        
        # Sanitize the entire response
        response_data = sanitize_json_data(response_data)
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to explore database"
        }
        
        return jsonify(error_response), 500

@app.route('/api/test', methods=['GET'])
def test():
    """Simple test endpoint to verify Angular-Flask communication"""
    return jsonify({
        "success": True,
        "message": "Flask API is working correctly",
        "timestamp": "2026-04-03",
        "data": {
            "test_array": [1, 2, 3, 4, 5],
            "test_object": {"name": "test", "value": "success"}
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Delinquency API is running"
    }), 200

@app.route('/api/eda-reports', methods=['POST'])
def run_eda_reports():
    """
    Run comprehensive exploratory data analysis with specified parameters and generate files
    """
    try:
        # Get parameters from POST request body
        data = request.get_json() or {}
        
        # Extract parameters with defaults
        n_clusters = data.get('n_clusters', 5)
        n_components = data.get('n_components', 10)
        
        # Validate parameters
        try:
            n_clusters = int(n_clusters)
            n_components = int(n_components)
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Invalid parameter values. Both n_clusters and n_components must be integers.",
                "message": "Invalid parameters"
            }), 400
        
        if n_clusters < 1 or n_clusters > 20:
            return jsonify({
                "success": False,
                "error": "n_clusters must be between 1 and 20",
                "message": "Invalid n_clusters value"
            }), 400
        
        if n_components < 2 or n_components > 50:
            return jsonify({
                "success": False,
                "error": "n_components must be between 2 and 50",
                "message": "Invalid n_components value"
            }), 400
        
        # Database path for the current database
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shared', 'student_loan_data.db'))
        
        # Check if database exists
        if not os.path.exists(db_path):
            return jsonify({
                "success": False,
                "error": "Database not found. Please generate data first.",
                "message": "Database not found"
            }), 404
        
        # Set up output directory for EDA files
        output_dir = os.path.join(os.path.dirname(__file__), 'services', 'eda_outputs')
        os.makedirs(output_dir, exist_ok=True)
        
        # Run full EDA analysis with file generation
        import subprocess
        import sys
        
        # Run the full EDA script
        script_path = os.path.join(os.path.dirname(__file__), 'services', 'run_eda_analysis.py')
        
        # Use virtual environment Python executable instead of sys.executable
        # Get the project root (go up from src/api to project root)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        venv_python = os.path.join(project_root, '.venv', 'Scripts', 'python.exe')
        
        cmd = [
            venv_python, script_path,
            '--output_dir', output_dir,
            '--n_clusters', str(n_clusters),
            '--n_components', str(n_components)
        ]
        
        # Execute EDA script
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode != 0:
            return jsonify({
                "success": False,
                "error": f"EDA script failed: {result.stderr}",
                "stdout": result.stdout,
                "message": "EDA script execution failed"
            }), 500
        
        # Get analysis summary using JSON function
        from services.run_eda_analysis_json import run_eda_analysis_json
        json_results = run_eda_analysis_json(n_clusters=n_clusters, n_components=n_components)
        
        # Define the generated files with descriptions
        files_info = [
            {
                "filename": "pca_scree_plot.html",
                "description": "Variance explained by each principal component",
                "url": f"http://127.0.0.1:5000/api/services/eda_outputs/pca_scree_plot.html"
            },
            {
                "filename": "pca_scatter_plot.html", 
                "description": "PC1 vs PC2 scatter plot colored by delinquency risk",
                "url": f"http://127.0.0.1:5000/api/services/eda_outputs/pca_scatter_plot.html"
            },
            {
                "filename": f"pca_biplot_pc1_vs_pc2.html",
                "description": "Biplot showing feature contribution vectors",
                "url": f"http://127.0.0.1:5000/api/services/eda_outputs/pca_biplot_pc1_vs_pc2.html"
            },
            {
                "filename": "pca_feature_contributions.html",
                "description": "Feature contributions to each principal component",
                "url": f"http://127.0.0.1:5000/api/services/eda_outputs/pca_feature_contributions.html"
            },
            {
                "filename": "feature_correlation_heatmap.html",
                "description": "Correlation matrix heatmap of original features",
                "url": f"http://127.0.0.1:5000/api/services/eda_outputs/feature_correlation_heatmap.html"
            },
            {
                "filename": f"pca_clustering_k{n_clusters}.html",
                "description": f"K-means clustering results (k={n_clusters}) on PCA components",
                "url": f"http://127.0.0.1:5000/api/services/eda_outputs/pca_clustering_k{n_clusters}.html"
            },
            {
                "filename": "cluster_analysis_summary.csv",
                "description": "Statistical summary of cluster analysis",
                "url": f"http://127.0.0.1:5000/api/services/eda_outputs/cluster_analysis_summary.csv"
            },
            {
                "filename": "eda_comprehensive_report.md",
                "description": "Comprehensive analysis report with insights",
                "url": f"http://127.0.0.1:5000/api/services/eda_outputs/eda_comprehensive_report.md"
            },
            {
                "filename": "eda_comprehensive_report.html",
                "description": "Comprehensive analysis report (HTML format)",
                "url": f"http://127.0.0.1:5000/api/services/eda_outputs/eda_comprehensive_report.html"
            }
        ]
        
        # Verify files exist and add file size info
        existing_files = []
        for file_info in files_info:
            file_path = os.path.join(output_dir, file_info["filename"])
            if os.path.exists(file_path):
                file_stats = os.stat(file_path)
                file_size = file_stats.st_size
                file_mtime = file_stats.st_mtime
                
                # Convert file size to human-readable format
                if file_size < 1024:
                    size_str = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                elif file_size < 1024 * 1024 * 1024:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                else:
                    size_str = f"{file_size / (1024 * 1024 * 1024):.1f} GB"
                
                # Format creation date
                from datetime import datetime
                creation_date = datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                file_info["size"] = file_size
                file_info["size_formatted"] = size_str
                file_info["creation_date"] = creation_date
                file_info["exists"] = True
                existing_files.append(file_info)
            else:
                file_info["exists"] = False
        
        # Prepare response with analysis summary and file information
        response = {
            "success": True,
            "parameters": {
                "n_clusters": n_clusters,
                "n_components": n_components
            },
            "files": existing_files,
            "files_count": len(existing_files),
            "analysis_summary": json_results.get("analysis_summary", {}),
            "data_overview": json_results.get("data_overview", {}),
            "feature_summary": json_results.get("feature_summary", {}),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "message": f"EDA analysis completed successfully. Generated {len(existing_files)} files."
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        error_response = {
            "success": False,  
            "error": str(e),
            "message": "Failed to run EDA analysis",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "traceback": traceback.format_exc()
        }
        
        # Log the error for debugging
        print(f"EDA analysis error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        return jsonify(error_response), 500

@app.route('/api/services/eda_outputs/<path:filename>')
def serve_eda_files(filename):
    """
    Serve EDA output files (HTML, CSV, MD)
    """
    try:
        # Define the services directory for EDA outputs
        eda_outputs_dir = os.path.join(os.path.dirname(__file__), 'services', 'eda_outputs')
        
        # Security check: ensure filename doesn't contain path traversal
        if '..' in filename or filename.startswith('/'):
            return jsonify({"error": "Invalid filename"}), 400
            
        # Check if file exists
        file_path = os.path.join(eda_outputs_dir, filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        # Determine content type based on file extension
        if filename.endswith('.html'):
            mimetype = 'text/html'
        elif filename.endswith('.csv'):
            mimetype = 'text/csv'
        elif filename.endswith('.md'):
            mimetype = 'text/markdown'
        else:
            mimetype = 'application/octet-stream'
        
        # Send the file with CORS headers
        from flask import send_file, make_response
        response = make_response(send_file(file_path, mimetype=mimetype))
        
        # Add CORS headers for frontend access
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        
        return response
        
    except Exception as e:
        return jsonify({"error": f"Failed to serve file: {str(e)}"}), 500

@app.route('/api/services/eda_outputs/<path:filename>', methods=['OPTIONS'])
def serve_eda_files_options(filename):
    """
    Handle CORS preflight requests for EDA files
    """
    from flask import make_response
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/risk-report/<filename>', methods=['GET'])
def get_risk_report(filename):
    """
    Serve risk estimation report files (markdown and HTML)
    """
    try:
        # Define the risk report directory path
        reports_dir = os.path.join(os.path.dirname(__file__), 'services', 'risk_estimate_outputs')
        
        # Validate filename to prevent directory traversal attacks
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({
                "success": False,
                "error": "Invalid filename",
                "message": "File not found or access denied"
            }), 404
        
        file_path = os.path.join(reports_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "error": "File not found",
                "message": f"Report file '{filename}' does not exist. Please run risk estimation first."
            }), 404
        
        # Determine mimetype based on file extension
        if filename.endswith('.html'):
            mimetype = 'text/html'
        elif filename.endswith('.md'):
            mimetype = 'text/markdown'
        else:
            mimetype = 'text/plain'
        
        # Return the file for viewing (not as download)
        from flask import send_file, make_response
        response = make_response(send_file(file_path, mimetype=mimetype))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to serve report file"
        }
        
        return jsonify(error_response), 500

@app.route('/api/services/risk_estimate_outputs/<filename>', methods=['GET'])
def get_risk_estimate_output(filename):
    """
    Serve risk estimation output files (text, markdown and HTML)
    """
    try:
        # Define the risk estimate outputs directory path
        outputs_dir = os.path.join(os.path.dirname(__file__), 'services', 'risk_estimate_outputs')
        
        # Validate filename to prevent directory traversal attacks
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({
                "success": False,
                "error": "Invalid filename",
                "message": "File not found or access denied"
            }), 404
        
        file_path = os.path.join(outputs_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "error": "File not found",
                "message": f"Output file '{filename}' does not exist. Please run risk estimation first."
            }), 404
        
        # Determine mimetype based on file extension
        if filename.endswith('.html'):
            mimetype = 'text/html'
        elif filename.endswith('.md'):
            mimetype = 'text/markdown'
        elif filename.endswith('.txt'):
            mimetype = 'text/plain'
        else:
            mimetype = 'application/octet-stream'
        
        # Return the file for viewing (not as download)
        from flask import send_file, make_response
        response = make_response(send_file(file_path, mimetype=mimetype))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to serve output file"
        }
        
        return jsonify(error_response), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)