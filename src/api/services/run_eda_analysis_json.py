#!/usr/bin/env python3
"""
Simple EDA analysis function that returns JSON results
Bypasses the complex EDA script to avoid Unicode issues
"""

import sys
import os
import json
from datetime import datetime

# Add the shared directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from database import DatabaseManager

def run_eda_analysis_json(n_clusters=5, n_components=10):
    """
    Run simple EDA analysis and return results as JSON-compatible dictionary.
    
    Args:
        n_clusters: Number of clusters for analysis
        n_components: Number of PCA components
        
    Returns:
        dict: JSON-compatible results with analysis statistics and status
    """
    results = {
        "success": False,
        "message": "",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "parameters": {
            "n_clusters": n_clusters,
            "n_components": n_components
        },
        "analysis_summary": {},
        "data_overview": {},
        "feature_summary": {}
    }
    
    try:
        # Hardcode database path - always look in the shared folder relative to this script
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared', 'student_loan_data.db'))
        
        # Check if database exists
        if not os.path.exists(db_path):
            results["message"] = f"Database file '{db_path}' not found. Please run data generation first."
            return results
        
        # Check if database is not empty
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM user_profile")
            count = cursor.fetchone()[0]
            conn.close()
            
            if count == 0:
                results["message"] = f"Database '{db_path}' is empty. Please run data generation first."
                return results
        except Exception as db_check_error:
            results["message"] = f"Error reading database '{db_path}': {str(db_check_error)}. Please ensure data is generated first."
            return results
        
        # Get basic data overview using DatabaseManager
        db_manager = DatabaseManager()
        
        # Get comprehensive data for analysis
        loan_data = db_manager.get_comprehensive_loan_data()
        
        if not loan_data:
            results["message"] = "No loan data found in database for EDA analysis."
            return results
        
        # Basic data statistics
        total_records = len(loan_data)
        
        # Analyze key metrics
        loan_amounts = [record.get('loan_amount', 0) for record in loan_data if record.get('loan_amount')]
        ages = [record.get('age', 0) for record in loan_data if record.get('age')]
        incomes = [record.get('annual_income_cad', 0) for record in loan_data if record.get('annual_income_cad')]
        
        # Risk distribution
        risk_distribution = {}
        risk_scores = [record.get('delinquency_risk') for record in loan_data if record.get('delinquency_risk') is not None]
        
        if risk_scores:
            for level in [0, 1, 2]:
                count = sum(1 for score in risk_scores if int(score) == level)
                risk_distribution[str(level)] = {
                    "count": count,
                    "percentage": round((count / len(risk_scores)) * 100, 1) if risk_scores else 0
                }
        
        # Feature analysis
        features_with_data = []
        feature_completeness = {}
        
        sample_record = loan_data[0] if loan_data else {}
        for key, value in sample_record.items():
            if value is not None:
                features_with_data.append(key)
                non_null_count = sum(1 for record in loan_data if record.get(key) is not None)
                feature_completeness[key] = {
                    "completeness_percentage": round((non_null_count / total_records) * 100, 1),
                    "non_null_count": non_null_count
                }
        
        # Build results
        results["data_overview"] = {
            "total_records": total_records,
            "total_features": len(features_with_data),
            "features_with_delinquency_risk": len(risk_scores),
            "risk_distribution": risk_distribution
        }
        
        if loan_amounts:
            results["analysis_summary"]["loan_statistics"] = {
                "average_loan_amount": round(sum(loan_amounts) / len(loan_amounts), 2),
                "min_loan_amount": min(loan_amounts),
                "max_loan_amount": max(loan_amounts),
                "total_loans_analyzed": len(loan_amounts)
            }
        
        if ages:
            results["analysis_summary"]["demographic_statistics"] = {
                "average_age": round(sum(ages) / len(ages), 1),
                "min_age": min(ages),
                "max_age": max(ages)
            }
        
        if incomes:
            results["analysis_summary"]["income_statistics"] = {
                "average_income": round(sum(incomes) / len(incomes), 2),
                "min_income": min(incomes),
                "max_income": max(incomes)
            }
        
        results["feature_summary"] = {
            "total_features_available": len(features_with_data),
            "feature_completeness": feature_completeness,
            "key_features": features_with_data[:10]  # Top 10 features
        }
        
        results["success"] = True
        results["message"] = f"EDA analysis completed successfully with {total_records} records using {n_clusters} clusters and {n_components} PCA components."
        
        return results
        
    except Exception as e:
        import traceback
        results["message"] = f"Error during EDA analysis: {str(e)}"
        results["error_details"] = {
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        return results

if __name__ == "__main__":
    # Test the function
    result = run_eda_analysis_json(5, 10)
    print(json.dumps(result, indent=2))