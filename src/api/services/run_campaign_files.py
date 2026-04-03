#!/usr/bin/env python3
"""
Campaign Files Generator
========================

This script generates targeted marketing campaign files by extracting borrowers
based on their ML-calculated delinquency risk levels.

Usage:
    python run_campaign_files.py
    
Example:
    python run_campaign_files.py
    
Outputs:
    - campaigns/high_risk_users.csv (Risk level 2)
    - campaigns/medium_risk_users.csv (Risk level 1)
    
Database connection is handled automatically through the centralized DatabaseManager.
"""

import pandas as pd
import sys
import os
import argparse
from datetime import datetime

# Add the shared directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from database import DatabaseManager

def create_campaigns_folder():
    """
    Create campaigns folder if it doesn't exist.
    """
    campaigns_dir = "campaigns"
    if not os.path.exists(campaigns_dir):
        os.makedirs(campaigns_dir)
        print(f"✓ Created '{campaigns_dir}' folder")
    else:
        print(f"✓ Using existing '{campaigns_dir}' folder")
    return campaigns_dir

def extract_campaign_data(risk_level, risk_label):
    """
    Extract campaign data for a specific risk level using centralized database methods.
    
    Args:
        risk_level: Integer risk level (1 or 2)
        risk_label: String label for the risk level
    
    Returns:
        DataFrame with campaign data
    """
    db_manager = DatabaseManager()
    
    # Get comprehensive loan data using centralized method
    data = db_manager.get_comprehensive_loan_data()
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    if df.empty:
        print(f"Warning: No data found in database")
        return pd.DataFrame()
    
    # Filter by risk level
    filtered_df = df[df['delinquency_risk'] == risk_level].copy()
    
    if filtered_df.empty:
        print(f"Warning: No users found with {risk_label} (risk level {risk_level})")
        return pd.DataFrame()
    
    # Add calculated fields for campaign use
    filtered_df['income_category'] = filtered_df['annual_income_cad'].apply(
        lambda x: 'Low Income' if x < 40000 else 'Medium Income' if x < 70000 else 'High Income'
    )
    
    filtered_df['age_group'] = filtered_df['age'].apply(
        lambda x: 'Young Adult (18-24)' if x < 25 else 
                  'Young Professional (25-34)' if x < 35 else 
                  'Mid-Career (35-49)' if x < 50 else 
                  'Senior (50+)'
    )
    
    # Calculate remaining balance percentage
    filtered_df['remaining_balance_pct'] = (
        (filtered_df['current_balance'] / filtered_df['loan_amount']) * 100
    ).round(2)
    
    # Calculate payment to income ratio
    filtered_df['payment_to_income_ratio_pct'] = (
        (filtered_df['monthly_payment'] * 12 / filtered_df['annual_income_cad']) * 100
    ).round(2)
    
    # Add contact strategy flags
    filtered_df['campaign_priority'] = filtered_df['delinquency_risk'].apply(
        lambda x: 'Immediate Intervention' if x == 2 else 'Proactive Monitoring'
    )
    
    # Add program difficulty labels for summary reporting
    if 'program_difficulty' in filtered_df.columns:
        filtered_df['program_difficulty_label'] = filtered_df['program_difficulty'].apply(
            lambda x: 'Low Difficulty' if x == 1 else 'Medium Difficulty' if x == 2 else 'High Difficulty' if x == 3 else f'Difficulty {x}'
        )
    
    return filtered_df

def generate_campaign_summary(df, risk_label):
    """
    Generate summary statistics for campaign data.
    """
    if len(df) == 0:
        print(f"⚠️  No {risk_label} borrowers found")
        return
    
    print(f"\n📊 {risk_label.upper()} BORROWERS CAMPAIGN SUMMARY:")
    print(f"   Total Borrowers: {len(df):,}")
    print(f"   Average Age: {df['age'].mean():.1f} years")
    print(f"   Average Income: ${df['annual_income_cad'].mean():,.0f}")
    print(f"   Average Loan Amount: ${df['loan_amount'].mean():,.0f}")
    print(f"   Average Monthly Payment: ${df['monthly_payment'].mean():.0f}")
    
    # Geographic distribution
    print(f"\n📍 Geographic Distribution:")
    province_dist = df['province'].value_counts().head(5)
    for province, count in province_dist.items():
        pct = (count / len(df)) * 100
        print(f"   {province}: {count:,} ({pct:.1f}%)")
    
    # Program difficulty distribution (if available)
    if 'program_difficulty_label' in df.columns:
        print(f"\n🎓 Program Difficulty Distribution:")
        difficulty_dist = df['program_difficulty_label'].value_counts()
        for difficulty, count in difficulty_dist.items():
            pct = (count / len(df)) * 100
            print(f"   {difficulty}: {count:,} ({pct:.1f}%)")
    elif 'program_difficulty' in df.columns:
        print(f"\n🎓 Program Difficulty Distribution:")
        difficulty_dist = df['program_difficulty'].value_counts()
        for difficulty, count in difficulty_dist.items():
            pct = (count / len(df)) * 100
            print(f"   Difficulty Level {difficulty}: {count:,} ({pct:.1f}%)")
    
    # Income categories
    print(f"\n💰 Income Categories:")
    income_dist = df['income_category'].value_counts()
    for category, count in income_dist.items():
        pct = (count / len(df)) * 100
        print(f"   {category}: {count:,} ({pct:.1f}%)")

def save_campaign_file(df, campaigns_dir, filename, risk_label):
    """
    Save campaign data to CSV file.
    """
    if len(df) == 0:
        print(f"⚠️  Skipping {filename} - no data to export")
        return
    
    filepath = os.path.join(campaigns_dir, filename)
    
    # Sort by recommended priority (higher risk score first, then by loan amount)
    df_sorted = df.sort_values(['delinquency_risk', 'loan_amount'], ascending=[False, False])
    
    # Save to CSV
    df_sorted.to_csv(filepath, index=False)
    
    print(f"✅ Saved {len(df):,} {risk_label} borrowers to: {filepath}")

def generate_campaign_files():
    """
    Main function to generate all campaign files using centralized database methods.
    """
    print("🎯 GENERATING CAMPAIGN FILES")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    db_manager = DatabaseManager()
    
    # Create campaigns folder
    campaigns_dir = create_campaigns_folder()
    
    # Check if delinquency risk scores exist using centralized method
    try:
        total_with_risk = db_manager.get_delinquency_risk_count()
        
        if total_with_risk == 0:
            print("❌ Error: No delinquency risk scores found in database.")
            print("Please run 'python run_delinquency_analysis.py' first to calculate risk scores.")
            return False
            
        # Check risk distribution using centralized method
        risk_dist_data = db_manager.get_delinquency_risk_distribution()
        
        print(f"\n📊 Risk Score Distribution:")
        risk_labels = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
        for row in risk_dist_data:
            risk_level = row['delinquency_risk']
            count = row['count']
            if risk_level is not None:
                label = risk_labels.get(risk_level, f"Risk {risk_level}")
                pct = (count / total_with_risk) * 100
                print(f"   {label} ({risk_level}): {count:,} borrowers ({pct:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
        return False
    
    # Generate files for medium and high risk borrowers
    campaign_configs = [
        (1, "Medium Risk", "medium_risk_users.csv"),
        (2, "High Risk", "high_risk_users.csv")
    ]
    
    for risk_level, risk_label, filename in campaign_configs:
        print(f"\n🔄 Processing {risk_label} Borrowers...")
        
        # Extract data using centralized method
        df = extract_campaign_data(risk_level, risk_label)
        
        # Generate summary
        generate_campaign_summary(df, risk_label)
        
        # Save file
        save_campaign_file(df, campaigns_dir, filename, risk_label)
    
    print(f"\n🎉 CAMPAIGN FILES GENERATION COMPLETE!")
    print(f"📁 Files saved in: {os.path.abspath(campaigns_dir)}")
    print(f"🕒 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

def main():
    """
    Main entry point for campaign files generation.
    """
    parser = argparse.ArgumentParser(
        description="Generate targeted marketing campaign files based on delinquency risk levels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_campaign_files.py
  
The script generates two campaign files:
  - high_risk_users.csv (delinquency_risk = 2)
  - medium_risk_users.csv (delinquency_risk = 1)
  
Each file contains comprehensive borrower information for targeted campaigns.
Database connection is handled automatically through the centralized DatabaseManager.
        """
    )
    
    args = parser.parse_args()
    
    try:
        success = generate_campaign_files()
        if not success:
            exit(1)
            
    except Exception as e:
        print(f"❌ Error generating campaign files: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Ensure the database exists and has been populated")
        print("2. Run delinquency analysis first to calculate risk scores")
        print("3. Check database permissions and available disk space")
        exit(1)

if __name__ == "__main__":
    main()