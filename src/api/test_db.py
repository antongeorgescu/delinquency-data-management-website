#!/usr/bin/env python3
"""
Test database connectivity and data availability
"""
import sys
import os

# Add paths
sys.path.append('.')
sys.path.append('shared')

from database import DatabaseManager

try:
    # Test database connection
    db = DatabaseManager()
    print("✅ Database connected successfully")
    
    # Get connection and check tables
    conn = db.get_connection()
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"📊 Tables found: {[t[0] for t in tables]}")
    
    # Check record counts
    for table in ['loan_info', 'user_profile', 'loan_payments', 'program_of_study']:
        try:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"📋 {table}: {count} records")
        except Exception as e:
            print(f"❌ Error checking {table}: {str(e)}")
    
    # Test comprehensive data method
    print("\n🔍 Testing comprehensive loan data method...")
    loan_data = db.get_comprehensive_loan_data()
    print(f"📈 Comprehensive loan data: {len(loan_data)} records")
    
    if loan_data:
        sample = loan_data[0]
        print(f"📝 Sample record keys: {list(sample.keys())[:10]}...")
        
        # Check for delinquency risk scores
        risk_scores = [r.get('delinquency_risk') for r in loan_data if r.get('delinquency_risk') is not None]
        print(f"🎯 Records with risk scores: {len(risk_scores)}")
        
    print("\n✅ Database check completed successfully!")
    
except Exception as e:
    print(f"❌ Database test failed: {str(e)}")
    import traceback
    traceback.print_exc()