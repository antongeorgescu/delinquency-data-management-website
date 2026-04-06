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
import numpy as np

def main():
    """
    Main entry point for running delinquency analysis.
    """
    parser = argparse.ArgumentParser(
        description="Run comprehensive delinquency analysis and update loan risk scores",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Risk Scoring Algorithms:
  random_forest      - Random Forest classifier with balanced classes (default)
  gradient_boosting  - Gradient Boosting classifier for complex patterns
  logistic_regression - Linear classifier with L2 regularization
  neural_network     - Multi-layer Perceptron with adaptive learning
  svm                - Support Vector Machine with RBF kernel
  knn                - K-Nearest Neighbors with distance weighting
  kmeans             - K-means clustering for unsupervised segmentation

Examples:
  python run_risk_estimation.py
  python run_risk_estimation.py --algorithm gradient_boosting
  python run_risk_estimation.py --algorithm svm --db_path my_database.db
        """
    )
    
    parser.add_argument(
        "--algorithm",
        choices=['random_forest', 'gradient_boosting', 'logistic_regression', 'neural_network', 'svm', 'knn', 'kmeans'],
        default='random_forest',
        help="Risk scoring algorithm to use (default: random_forest)"
    )
    
    parser.add_argument(
        "--db_path", 
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared', 'student_loan_data.db')),
        help="Path to the SQLite database file (default: auto-detected absolute path)"
    )
    
    args = parser.parse_args()
    
    # Check if database exists
    if not os.path.exists(args.db_path):
        print(f"Error: Database file '{args.db_path}' not found.")
        print(f"Expected location: {os.path.abspath(args.db_path)}")
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
        sys.argv = ['delinquency_analysis.py', '--algorithm', args.algorithm]
        
        from delinquency_analysis import main as run_analysis
        
        # Run the analysis
        run_analysis()
        
        print("=" * 60)
        print("✅ Risk estimation analysis completed successfully!")
        print(f"📊 The database '{args.db_path}' has been updated with ML-based risk scores.")
        print(f"🤖 Algorithm used: {args.algorithm} (Classification-based)")
        print(f"📈 Risk levels: 0 (Low), 1 (Medium), 2 (High)")
        print("📈 You can now explore the enhanced data using:")
        print(f"   python explore_database.py --db_path {args.db_path}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Ensure the database has been populated with data")
        print("2. Check that all required tables exist (user_profile, loan_info, program_of_study, loan_payments)")
        print("3. Verify you have sufficient data for machine learning (recommended: 100+ borrowers)")
        print("4. For advanced algorithms (SVM/Neural Network), ensure you have sufficient data for training")
        print(f"5. Try a different algorithm if '{args.algorithm}' fails (e.g., --algorithm random_forest)")
        sys.exit(1)

def run_risk_estimation_json(algorithm='random_forest'):
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
        
        # Initialize session logging for web interface calls
        # Add the delinquency_analysis directory to the Python path
        analysis_dir = os.path.join(os.path.dirname(__file__), 'delinquency_analysis')
        if analysis_dir not in sys.path:
            sys.path.insert(0, analysis_dir)
            
        try:
            from delinquency_analysis import init_session_logging, finalize_session_logging
            # Initialize logging for web interface calls
            init_session_logging()
        except ImportError:
            # Logging modules not available - continue without logging
            pass
        
        # Set up arguments for the analysis script
        sys.argv = ['delinquency_analysis.py', '--algorithm', algorithm]
        
        # Add the delinquency_analysis directory to the Python path
        analysis_dir = os.path.join(os.path.dirname(__file__), 'delinquency_analysis')
        if analysis_dir not in sys.path:
            sys.path.insert(0, analysis_dir)
        
        # Import and run the analysis with result capture
        try:
            from delinquency_analysis import (
                load_comprehensive_dataset, engineer_features, prepare_ml_features,
                train_delinquency_models, train_single_algorithm, analyze_feature_importance, calculate_risk_scores,
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
        
        # Train models based on selected algorithm
        if algorithm in ['percentile', 'threshold', 'kmeans']:
            # For statistical algorithms, train all models and use best for probability generation
            best_model, model_results, scaler = train_delinquency_models(X, y)
            best_model_name = max(model_results.keys(), key=lambda x: model_results[x]['auc_score'])
            feature_importance_df = analyze_feature_importance(best_model, feature_columns, best_model_name)
        else:
            # For specific ML algorithms, train only the selected algorithm
            best_model, model_results, scaler, best_model_name = train_single_algorithm(X, y, algorithm)
            feature_importance_df = analyze_feature_importance(best_model, feature_columns, best_model_name)
        
        # Calculate risk scores using the selected algorithm
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
        
        # Model performance with enhanced details for Classification Algorithms
        classification_algorithms = ['random_forest', 'gradient_boosting', 'logistic_regression', 'neural_network', 'svm', 'knn']
        
        results["model_performance"] = {
            "best_model": best_model_name,
            "algorithm_category": "Classification Algorithm" if algorithm in classification_algorithms else "Statistical Distribution",
            "algorithm_used": algorithm,
            "models": {}
        }
        
        # Add detailed metrics for Classification Algorithms
        if algorithm in classification_algorithms:
            results["model_performance"]["algorithm_details"] = get_algorithm_details(algorithm)
            
            # Get CV metrics with fallback to handle both old and new dictionary structures
            best_model_data = model_results[best_model_name]
            cv_mean = best_model_data.get('cv_auc_mean', best_model_data.get('cv_mean', 0.0))
            cv_std = best_model_data.get('cv_auc_std', best_model_data.get('cv_std', 0.0))
            
            results["model_performance"]["performance_summary"] = {
                "auc_score": float(best_model_data['auc_score']),
                "accuracy": float(best_model_data.get('accuracy', 0.0)),
                "precision": float(best_model_data.get('precision', 0.0)),
                "recall": float(best_model_data.get('recall', 0.0)),
                "f1_score": float(best_model_data.get('f1_score', 0.0)),
                "cross_validation_auc_mean": float(cv_mean),
                "cross_validation_auc_std": float(cv_std),
                "cross_validation_accuracy_mean": float(best_model_data.get('cv_accuracy_mean', 0.0)),
                "cross_validation_accuracy_std": float(best_model_data.get('cv_accuracy_std', 0.0)),
                "performance_rating": get_performance_rating(best_model_data['auc_score'])
            }
        else:
            results["model_performance"]["algorithm_details"] = get_statistical_algorithm_description(algorithm)
        
        for name, model_data in model_results.items():
            # Handle both old and new dictionary structures
            cv_mean = model_data.get('cv_auc_mean', model_data.get('cv_mean', 0.0))
            cv_std = model_data.get('cv_auc_std', model_data.get('cv_std', 0.0))
            
            results["model_performance"]["models"][name] = {
                "auc_score": float(model_data['auc_score']),
                "accuracy": float(model_data.get('accuracy', 0.0)),
                "precision": float(model_data.get('precision', 0.0)),
                "recall": float(model_data.get('recall', 0.0)),
                "f1_score": float(model_data.get('f1_score', 0.0)),
                "cv_auc_mean": float(cv_mean),
                "cv_auc_std": float(cv_std),
                "cv_accuracy_mean": float(model_data.get('cv_accuracy_mean', 0.0)),
                "cv_accuracy_std": float(model_data.get('cv_accuracy_std', 0.0))
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
        
        # Add detailed classification metrics for web display
        results["detailed_classification_metrics"] = get_detailed_classification_display(model_results, algorithm)
        
        # Finalize session logging for web interface calls
        try:
            from delinquency_analysis import finalize_session_logging
            md_file, html_file = finalize_session_logging()
            if md_file and html_file:
                results["session_log"] = {
                    "markdown_file": md_file,
                    "html_file": html_file
                }
        except (ImportError, NameError):
            # Logging modules not available - continue without logging
            pass
        
        # Restore original sys.argv
        sys.argv = original_argv
        
        return results
        
    except Exception as e:
        # Restore original sys.argv in case of error
        if 'original_argv' in locals():
            sys.argv = original_argv
        
        # Finalize session logging even in case of error
        try:
            from delinquency_analysis import finalize_session_logging
            md_file, html_file = finalize_session_logging()
            if md_file and html_file:
                results["session_log"] = {
                    "markdown_file": md_file,
                    "html_file": html_file
                }
        except (ImportError, NameError):
            # Logging modules not available - continue without logging
            pass
        
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

def get_detailed_classification_display(model_results, algorithm):
    """
    Generate detailed classification metrics display for web interface.
    """
    classification_display = {
        "algorithm_used": algorithm,
        "models": {}
    }
    
    for model_name, metrics in model_results.items():
        # Format test set performance
        test_performance = {
            "accuracy": f"{metrics.get('accuracy', 0.0):.4f}",
            "precision": f"{metrics.get('precision', 0.0):.4f}",
            "recall": f"{metrics.get('recall', 0.0):.4f}",
            "f1_score": f"{metrics.get('f1_score', 0.0):.4f}",
            "auc_score": f"{metrics['auc_score']:.4f}"
        }
        
        # Format cross-validation performance  
        cv_accuracy_mean = metrics.get('cv_accuracy_mean', 0.0)
        cv_accuracy_std = metrics.get('cv_accuracy_std', 0.0)
        cv_precision_mean = metrics.get('cv_precision_mean', 0.0)
        cv_precision_std = metrics.get('cv_precision_std', 0.0)
        cv_recall_mean = metrics.get('cv_recall_mean', 0.0)
        cv_recall_std = metrics.get('cv_recall_std', 0.0)
        cv_f1_mean = metrics.get('cv_f1_mean', 0.0)
        cv_f1_std = metrics.get('cv_f1_std', 0.0)
        cv_auc_mean = metrics.get('cv_auc_mean', metrics.get('cv_mean', 0.0))
        cv_auc_std = metrics.get('cv_auc_std', metrics.get('cv_std', 0.0))
        
        cv_performance = {
            "accuracy": f"{cv_accuracy_mean:.4f} (+/- {cv_accuracy_std * 2:.4f})",
            "precision": f"{cv_precision_mean:.4f} (+/- {cv_precision_std * 2:.4f})",
            "recall": f"{cv_recall_mean:.4f} (+/- {cv_recall_std * 2:.4f})",
            "f1_score": f"{cv_f1_mean:.4f} (+/- {cv_f1_std * 2:.4f})",
            "auc_score": f"{cv_auc_mean:.4f} (+/- {cv_auc_std * 2:.4f})"
        }
        
        classification_display["models"][model_name] = {
            "test_set_performance": test_performance,
            "cross_validation_performance": cv_performance,
            "summary": {
                "best_metric": "auc_score",
                "best_value": f"{metrics['auc_score']:.4f}",
                "performance_rating": get_performance_rating(metrics['auc_score'])
            }
        }
    
    return classification_display

def get_performance_rating(auc_score):
    """Generate a performance rating based on AUC score."""
    if auc_score >= 0.95:
        return "Excellent"
    elif auc_score >= 0.90:
        return "Very Good" 
    elif auc_score >= 0.80:
        return "Good"
    elif auc_score >= 0.70:
        return "Fair"
    else:
        return "Poor"

def get_algorithm_details(algorithm):
    """
    Get detailed information about classification algorithms.
    """
    algorithm_details = {
        'random_forest': {
            'name': 'Random Forest Classifier',
            'type': 'Ensemble Learning',
            'description': 'Combines multiple decision trees using bootstrap aggregating (bagging)',
            'strengths': ['Reduces overfitting', 'Handles missing values', 'Provides feature importance', 'Works well with categorical and numerical features'],
            'parameters': {'n_estimators': 100, 'max_depth': 10, 'class_weight': 'balanced'},
            'best_for': 'Complex datasets with mixed feature types and potential overfitting concerns'
        },
        'gradient_boosting': {
            'name': 'Gradient Boosting Classifier', 
            'type': 'Sequential Ensemble Learning',
            'description': 'Builds models sequentially, each correcting errors of the previous',
            'strengths': ['High predictive accuracy', 'Handles complex patterns', 'Feature importance', 'Robust to outliers'],
            'parameters': {'n_estimators': 100, 'max_depth': 6, 'learning_rate': 0.1},
            'best_for': 'High-accuracy requirements with structured/tabular data'
        },
        'logistic_regression': {
            'name': 'Logistic Regression',
            'type': 'Linear Classification',
            'description': 'Uses logistic function to model probability of binary outcomes',
            'strengths': ['Interpretable coefficients', 'Fast training', 'No hyperparameter tuning needed', 'Probabilistic output'],
            'parameters': {'C': 1.0, 'max_iter': 1000, 'class_weight': 'balanced'},
            'best_for': 'Linear relationships and when model interpretability is important'
        },
        'neural_network': {
            'name': 'Multi-layer Perceptron (MLP)',
            'type': 'Deep Learning',
            'description': 'Neural network with hidden layers for complex pattern recognition',
            'strengths': ['Captures non-linear patterns', 'Universal approximator', 'Adaptive learning', 'Flexible architecture'],
            'parameters': {'hidden_layers': '100, 50', 'activation': 'relu', 'max_iter': 500},
            'best_for': 'Complex non-linear relationships and large datasets'
        },
        'svm': {
            'name': 'Support Vector Machine',
            'type': 'Kernel-based Classification',
            'description': 'Finds optimal hyperplane using support vectors and kernel tricks',
            'strengths': ['Effective in high dimensions', 'Memory efficient', 'Versatile kernels', 'Works with small datasets'],
            'parameters': {'kernel': 'rbf', 'C': 10.0, 'class_weight': 'balanced'},
            'best_for': 'High-dimensional data and when clear margin separation exists'
        },
        'knn': {
            'name': 'K-Nearest Neighbors',
            'type': 'Instance-based Learning',
            'description': 'Classifies based on similarity to k nearest training samples',
            'strengths': ['Simple to understand', 'No assumptions about data', 'Naturally handles multi-class', 'Local decision boundaries'],
            'parameters': {'n_neighbors': 5, 'weights': 'distance', 'algorithm': 'auto'},
            'best_for': 'Datasets with clear local patterns and sufficient training data'
        }
    }
    
    return algorithm_details.get(algorithm, {'name': 'Unknown Algorithm', 'description': 'Algorithm details not available'})

def get_statistical_algorithm_description(algorithm):
    """
    Get description for statistical algorithms.
    """
    descriptions = {
        'percentile': {
            'name': 'Percentile-based Classification',
            'type': 'Statistical Distribution',
            'description': 'Divides borrowers based on probability percentiles: Bottom 60% = Low, Next 30% = Medium, Top 10% = High',
            'thresholds': 'Dynamic based on 60th and 90th percentiles of risk probabilities'
        },
        'threshold': {
            'name': 'Fixed Threshold Classification',
            'type': 'Statistical Distribution', 
            'description': 'Uses fixed probability thresholds for risk classification',
            'thresholds': 'Low < 0.6, Medium = 0.6-0.9, High > 0.9'
        },
        'kmeans': {
            'name': 'K-Means Clustering',
            'type': 'Unsupervised Learning',
            'description': 'Groups borrowers into 3 clusters based on feature similarity, then maps to risk levels',
            'clusters': 3
        }
    }
    
    return descriptions.get(algorithm, {'name': 'Unknown Algorithm', 'description': 'Algorithm details not available'})

def get_performance_rating(auc_score):
    """
    Get performance rating based on AUC score.
    """
    if auc_score >= 0.9:
        return "Excellent"
    elif auc_score >= 0.8:
        return "Good"
    elif auc_score >= 0.7:
        return "Fair" 
    elif auc_score >= 0.6:
        return "Poor"
    else:
        return "Very Poor"

if __name__ == "__main__":
    main()