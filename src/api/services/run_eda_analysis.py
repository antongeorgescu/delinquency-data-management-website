#!/usr/bin/env python3
"""
Student Loan EDA Runner
Run comprehensive exploratory data analysis with PCA on student loan data.

This script provides a user-friendly interface to perform:
- Principal Component Analysis (PCA) dimensionality reduction
- Interactive visualizations and charts
- Feature correlation analysis  
- Risk distribution analysis
- K-means clustering on PCA components
- Comprehensive reporting

Example usage:
    python run_eda_analysis.py
    python run_eda_analysis.py --db_path my_data.db --n_clusters 4
    python run_eda_analysis.py --output_dir custom_eda_outputs
"""

import sys
import os
import argparse
from pathlib import Path

def main():
    """Main entry point for EDA analysis."""
    
    parser = argparse.ArgumentParser(
        description='Student Loan Exploratory Data Analysis with PCA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_eda_analysis.py                                    # Basic EDA with defaults
  python run_eda_analysis.py --db_path custom_data.db          # Custom database
  python run_eda_analysis.py --n_clusters 5                    # 5 clusters for K-means
  python run_eda_analysis.py --output_dir my_eda_results       # Custom output directory
  python run_eda_analysis.py --n_components 10                 # Limit PCA components
        """
    )
    
    # Database path is fixed - always in the shared directory
    # parser.add_argument(
    #     '--db_path', 
    #     default='student_loan_data.db',
    #     help='Path to SQLite database file (default: student_loan_data.db)'
    # )
    
    parser.add_argument(
        '--output_dir', 
        default='eda_outputs',
        help='Output directory for charts and reports (default: eda_outputs)'
    )
    
    parser.add_argument(
        '--n_components', 
        type=int, 
        default=None,
        help='Number of PCA components to extract (default: auto-determine)'
    )
    
    parser.add_argument(
        '--n_clusters', 
        type=int, 
        default=3,
        help='Number of clusters for K-means analysis (default: 3)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Database path is automatically determined - always in the shared directory
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared', 'student_loan_data.db'))
    
    # Validate database file exists
    if not os.path.exists(db_path):
        print(f"ERROR: Database file '{db_path}' not found!")
        print("TIP: Run 'python run_data_generation.py' first to create the database.")
        return 1
    
    try:
        # Import the EDA module
        from delinquency_analysis.exploratory_data_analysis import ExploratoryDataAnalysis
        
        print("Starting Exploratory Data Analysis with PCA...")
        print(f"Database: {db_path}")
        print(f"Output directory: {args.output_dir}")
        print(f"K-means clusters: {args.n_clusters}")
        if args.n_components:
            print(f"PCA components: {args.n_components}")
        else:
            print(f"PCA components: Auto-determined")
        
        # Initialize EDA
        eda = ExploratoryDataAnalysis(db_path, args.output_dir)
        
        # Step 1: Load and process data
        print("\\n" + "="*60)
        print("STEP 1: DATA LOADING AND PROCESSING")
        print("="*60)
        eda.load_and_process_data()
        
        # Step 2: Perform PCA analysis
        print("\\n" + "="*60)
        print("STEP 2: PRINCIPAL COMPONENT ANALYSIS")
        print("="*60)
        eda.perform_pca_analysis(args.n_components)
        
        # Step 3: Create visualizations
        print("\\n" + "="*60)
        print("STEP 3: CREATING VISUALIZATIONS")
        print("="*60)
        
        print("Creating scree plot...")
        eda.create_scree_plot()
        
        print("Creating PCA scatter plot...")
        eda.create_pca_scatter_plot()
        
        print("Creating PCA biplot...")
        eda.create_biplot()
        
        print("Analyzing feature contributions...")
        eda.analyze_feature_contributions()
        
        print("Creating correlation heatmap...")
        eda.create_correlation_heatmap()
        
        # Step 4: Clustering analysis
        print("\\n" + "="*60)
        print("STEP 4: CLUSTERING ANALYSIS")
        print("="*60)
        eda.perform_clustering_analysis(args.n_clusters)
        
        # Step 5: Generate comprehensive report
        print("\\n" + "="*60)
        print("STEP 5: GENERATING REPORTS")
        print("="*60)
        markdown_report = eda.generate_comprehensive_report()
        
        # Convert to HTML
        eda.convert_markdown_to_html(markdown_report)
        
        print("\\n" + "="*60)
        print("ANALYSIS COMPLETE!")
        print("="*60)
        print(f"All visualizations and reports saved to: {args.output_dir}/")
        print("\nGenerated Files:")
        print("  - 6 Interactive HTML charts")
        print("  - 1 Comprehensive markdown report (eda_comprehensive_report.md)")
        print("  - 1 Styled HTML report (eda_comprehensive_report.html)")
        print("\nTIP: Open the HTML files in your browser to explore the interactive charts and reports.")
        
        return 0
        
    except ImportError as e:
        print(f"IMPORT ERROR: {e}")
        print("TIP: Make sure you have installed all required packages:")
        print("   pip install -r requirements.txt")
        return 1
        
    except FileNotFoundError as e:
        print(f"FILE ERROR: {e}")
        print("TIP: Make sure the database file exists and is accessible.")
        return 1
        
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        print("TIP: Check the error details above and ensure data integrity.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)