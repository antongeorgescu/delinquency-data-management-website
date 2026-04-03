"""
Flask API server for delinquency data management
"""
import sys
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add the shared directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))

from database import DatabaseManager
from mock_data import MockDataGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route('/api/generate-data', methods=['POST'])
def generate_data():
    """
    Generate synthetic data for all entities
    """
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Clear existing data
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM loan_payments")
        cursor.execute("DELETE FROM loan_info")
        cursor.execute("DELETE FROM user_profile")
        cursor.execute("DELETE FROM programs_of_study")
        conn.commit()
        conn.close()
        
        # Generate user profiles
        user_profiles = MockDataGenerator.generate_user_profiles(50)
        user_query = """
            INSERT INTO user_profile (id, first_name, last_name, email, created_at)
            VALUES (?, ?, ?, ?, ?)
        """
        db_manager.execute_many(user_query, user_profiles)
        
        # Get user IDs for foreign key relationships
        user_ids = [profile[0] for profile in user_profiles]
        
        # Generate loan information
        loan_info = MockDataGenerator.generate_loan_info(user_ids, 2)
        loan_query = """
            INSERT INTO loan_info (id, user_id, loan_amount, interest_rate, loan_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        db_manager.execute_many(loan_query, loan_info)
        
        # Get loan IDs for payment history
        loan_ids = [loan[0] for loan in loan_info]
        
        # Generate programs of study
        programs = MockDataGenerator.generate_programs_of_study(20)
        program_query = """
            INSERT INTO programs_of_study (id, program_name, degree_level, duration_months)
            VALUES (?, ?, ?, ?)
        """
        db_manager.execute_many(program_query, programs)
        
        # Generate loan payments
        loan_payments = MockDataGenerator.generate_loan_payments(loan_ids, 12)
        payment_query = """
            INSERT INTO loan_payments (id, loan_id, payment_amount, payment_date, status)
            VALUES (?, ?, ?, ?, ?)
        """
        db_manager.execute_many(payment_query, loan_payments)
        
        # Return success response with generation statistics
        response_data = {
            "success": True,
            "message": "Synthetic data generated successfully",
            "statistics": {
                "user_profile": len(user_profiles),
                "loan_info": len(loan_info),
                "programs_of_study": len(programs),
                "loan_payments": len(loan_payments)
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

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Delinquency API is running"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)