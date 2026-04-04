#!/usr/bin/env python3
"""
Risk Estimation Runner Script
=============================

This script provides a simple interface to run the comprehensive delinquency analysis
and update the database with ML-based risk scores.

Usage:
    python run_risk_estimation.py [--db_path path_to_database]
    
Example:
    python run_risk_estimation.py --db_path student_loan_data.db
"""

import argparse
import sys
import os
from datetime import datetime
import json

def main():
    """
    Main entry point for running delinquency analysis.
    """
    parser = argparse.ArgumentParser(
        description="Run comprehensive delinquency analysis and update loan risk scores",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Risk Scoring Algorithms:
  percentile  - Bottom 60% = Low(0), Next 30% = Medium(1), Top 10% = High(2)
  threshold   - Fixed probability thresholds: <0.3=Low, 0.3-0.6=Medium, >0.6=High
  kmeans      - K-means clustering of probabilities into 3 risk groups
  svm         - Support Vector Machine classifier trained on probability-based risk labels
  knn         - K-Nearest Neighbors classifier with optimal k and distance weighting

Examples:
  python run_risk_estimation.py
  python run_risk_estimation.py --algorithm svm
  python run_risk_estimation.py --algorithm knn --db_path my_database.db
        """
    )
    
    parser.add_argument(
        "--algorithm",
        choices=['percentile', 'threshold', 'kmeans', 'svm', 'knn'],
        default='percentile',
        help="Risk scoring algorithm to use (default: percentile)"
    )
    
    parser.add_argument(
        "--db_path", 
        default="student_loan_data.db",
        help="Path to the SQLite database file (default: student_loan_data.db)"
    )
    
    args = parser.parse_args()
    
    # Check if database exists
    if not os.path.exists(args.db_path):
        print(f"Error: Database file '{args.db_path}' not found.")
        print(f"Please run 'python run_data_generation.py' first to create the database.")
        sys.exit(1)
    
    # Check if required Python packages are available
    try:
        import pandas as pd
        import numpy as np
        import sklearn
        print("✓ Required packages (pandas, numpy, scikit-learn) are available")
    except ImportError as e:
        print(f"Error: Required package not found - {e}")
        print("Please install required packages:")
        print("  pip install pandas numpy scikit-learn")
        sys.exit(1)
    
    print(f"🚀 Starting Risk Estimation Analysis")
    print(f"   Database: {args.db_path}")
    print(f"   Algorithm: {args.algorithm}")
    print(f"   Risk Levels: 0 (Low), 1 (Medium), 2 (High)")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Import and run the analysis
        # Set up arguments for the main analysis script
        sys.argv = ['delinquency_analysis.py', '--algorithm', args.algorithm, '--db_path', args.db_path]
        
        from delinquency_analysis import main as run_analysis
        
        # Run the analysis
        run_analysis()
        
        print("=" * 60)
        print("✅ Risk estimation analysis completed successfully!")
        print(f"📊 The database '{args.db_path}' has been updated with ML-based risk scores.")
        print(f"🤖 Algorithm used: {args.algorithm}")
        print(f"📈 Risk levels: 0 (Low), 1 (Medium), 2 (High)")
        print("📈 You can now explore the enhanced data using:")
        print(f"   python explore_database.py --db_path {args.db_path}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Ensure the database has been populated with data")
        print("2. Check that all required tables exist (user_profile, loan_info, program_of_study, loan_payments)")
        print("3. Verify you have sufficient data for machine learning (recommended: 100+ borrowers)")
        print("4. For SVM/KNN algorithms, ensure you have enough diverse data for training")
        print(f"5. Try a different algorithm if '{args.algorithm}' fails (e.g., --algorithm percentile)")
        sys.exit(1)

def run_risk_estimation_json(algorithm='percentile'):
    """
    Run risk estimation analysis and return results as JSON-compatible dictionary.
    
    Args:
        algorithm: Risk scoring algorithm to use
        
    Returns:
        dict: JSON-compatible results with analysis statistics and status
    """
    # Hardcode database path - always look in the shared folder relative to this script
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared', 'student_loan_data.db'))
    
    results = {
        "success": False,
        "message": "",
        "algorithm": algorithm,
        "db_path": db_path,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "risk_levels": {"0": "Low Risk", "1": "Medium Risk", "2": "High Risk"},
        "statistics": {},
        "model_performance": {},
        "risk_distribution": {},
        "validation_metrics": {},
        "feature_importance": []
    }
    
    try:
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
        
        # Check if required packages are available
        try:
            import pandas as pd
            import numpy as np
            import sklearn
        except ImportError as e:
            results["message"] = f"Required package not found: {e}"
            return results
        
        # Store original sys.argv to restore later
        original_argv = sys.argv.copy()
        
        # Set up arguments for the analysis script
        sys.argv = ['delinquency_analysis.py', '--algorithm', algorithm, '--db_path', db_path]
        
        # Add the delinquency_analysis directory to the Python path
        analysis_dir = os.path.join(os.path.dirname(__file__), 'delinquency_analysis')
        if analysis_dir not in sys.path:
            sys.path.insert(0, analysis_dir)
        
        # Import and run the analysis with result capture
        try:
            from delinquency_analysis import (
                load_comprehensive_dataset, engineer_features, prepare_ml_features,
                train_delinquency_models, analyze_feature_importance, calculate_risk_scores,
                update_loan_info_table
            )
        except ImportError as import_error:
            # Restore original sys.argv
            sys.argv = original_argv
            results["message"] = f"Failed to import analysis modules: {str(import_error)}"
            return results
        
        # Load and prepare data
        df = load_comprehensive_dataset()
        if df.empty:
            results["message"] = "No data found in database for analysis"
            return results
        
        df = engineer_features(df)
        X, y, feature_columns, label_encoders = prepare_ml_features(df)
        
        # Train models and get results
        best_model, model_results, scaler = train_delinquency_models(X, y)
        best_model_name = max(model_results.keys(), key=lambda x: model_results[x]['auc_score'])
        
        # Get feature importance
        feature_importance_df = analyze_feature_importance(best_model, feature_columns, best_model_name)
        
        # Calculate risk scores
        risk_scores = calculate_risk_scores(best_model, X, scaler, best_model_name, algorithm)
        
        # Update database
        update_loan_info_table(df, risk_scores)
        
        # Populate results dictionary
        results["success"] = True
        results["message"] = "Risk estimation analysis completed successfully"
        
        # Dataset statistics
        results["statistics"] = {
            "total_borrowers": len(df),
            "delinquent_borrowers": int(df['is_delinquent'].sum()),
            "overall_delinquency_rate": float(df['is_delinquent'].mean()),
            "features_analyzed": len(feature_columns),
            "records_updated": len(risk_scores)
        }
        
        # Model performance
        results["model_performance"] = {
            "best_model": best_model_name,
            "models": {}
        }
        
        for name, model_data in model_results.items():
            results["model_performance"]["models"][name] = {
                "auc_score": float(model_data['auc_score']),
                "cv_mean": float(model_data['cv_mean']),
                "cv_std": float(model_data['cv_std'])
            }
        
        # Risk distribution
        low_risk = int(np.sum(risk_scores == 0))
        medium_risk = int(np.sum(risk_scores == 1))
        high_risk = int(np.sum(risk_scores == 2))
        total_scores = len(risk_scores)
        
        results["risk_distribution"] = {
            "low_risk": {
                "count": low_risk,
                "percentage": round(low_risk / total_scores * 100, 1)
            },
            "medium_risk": {
                "count": medium_risk,
                "percentage": round(medium_risk / total_scores * 100, 1)
            },
            "high_risk": {
                "count": high_risk,
                "percentage": round(high_risk / total_scores * 100, 1)
            }
        }
        
        # Validation metrics (actual delinquency rates by risk level)
        df_with_risk = df.copy()
        df_with_risk['calculated_risk'] = risk_scores
        
        validation_metrics = {}
        for risk_level in [0, 1, 2]:
            level_data = df_with_risk[df_with_risk['calculated_risk'] == risk_level]
            if len(level_data) > 0:
                actual_delinq_rate = float(level_data['is_delinquent'].mean())
                validation_metrics[str(risk_level)] = {
                    "actual_delinquency_rate": round(actual_delinq_rate * 100, 1),
                    "borrower_count": len(level_data)
                }
        
        results["validation_metrics"] = validation_metrics
        
        # Top feature importance (limit to top 15 for JSON response)
        if feature_importance_df is not None:
            top_features = feature_importance_df.head(15)
            results["feature_importance"] = [
                {
                    "feature": row['feature'],
                    "importance": round(float(row['importance']), 4),
                    "rank": i + 1
                }
                for i, (_, row) in enumerate(top_features.iterrows())
            ]
        
        # Restore original sys.argv
        sys.argv = original_argv
        
        return results
        
    except Exception as e:
        # Restore original sys.argv in case of error
        if 'original_argv' in locals():
            sys.argv = original_argv
        
        # Get more detailed error information
        import traceback
        error_traceback = traceback.format_exc()
        
        results["message"] = f"Error during analysis: {str(e)}"
        results["error_details"] = {
            "error_type": type(e).__name__,
            "traceback": error_traceback,
            "troubleshooting_tips": [
                "Ensure the database has been populated with data",
                "Check that all required tables exist",
                "Verify you have sufficient data for machine learning (100+ borrowers recommended)",
                f"Try a different algorithm if '{algorithm}' fails"
            ]
        }
        
        # Also print to console for debugging
        print(f"Risk estimation error: {str(e)}")
        print(f"Full traceback: {error_traceback}")
        
        return results

if __name__ == "__main__":
    main()