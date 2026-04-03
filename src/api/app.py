"""
Flask API server for delinquency data management
"""
import sys
import os
import json
import math
from flask import Flask, jsonify, request
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
    Get all user profiles
    """
    try:
        db_manager = DatabaseManager()
        
        query = """
            SELECT id, first_name, last_name, email, created_at
            FROM user_profile
            ORDER BY created_at DESC
        """
        
        user_profiles = db_manager.execute_query(query)
        
        response_data = {
            "success": True,
            "data": user_profiles,
            "count": len(user_profiles)
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve user profiles"
        }
        
        return jsonify(error_response), 500

@app.route('/api/get-loan-info', methods=['GET'])
def get_loan_info():
    """
    Get all loan information with user details
    """
    try:
        db_manager = DatabaseManager()
        
        query = """
            SELECT 
                l.id, 
                l.user_id,
                l.loan_amount,
                l.interest_rate,
                l.loan_type,
                l.created_at,
                u.first_name,
                u.last_name,
                u.email
            FROM loan_info l
            JOIN user_profile u ON l.user_id = u.id
            ORDER BY l.created_at DESC
        """
        
        loan_info = db_manager.execute_query(query)
        
        response_data = {
            "success": True,
            "data": loan_info,
            "count": len(loan_info)
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
    Get all programs of study
    """
    try:
        db_manager = DatabaseManager()
        
        query = """
            SELECT id, program_name, degree_level, duration_months
            FROM programs_of_study
            ORDER BY degree_level, program_name
        """
        
        programs = db_manager.execute_query(query)
        
        response_data = {
            "success": True,
            "data": programs,
            "count": len(programs)
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve programs of study"
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)