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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)