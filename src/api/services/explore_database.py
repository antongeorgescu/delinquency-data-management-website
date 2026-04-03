import sys
import os
import pandas as pd

# Add the shared directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from database import DatabaseManager

def explore_database():
    """
    Explore the database structure and return sample data using centralized database methods
    """
    db_manager = DatabaseManager()
    
    result = {
        "database_structure": {},
        "sample_user_profiles": [],
        "employment_income_analysis": [],
        "provincial_analysis": [],
        "loan_amount_analysis": [],
        "program_analysis": [],
        "payment_status_analysis": [],
        "payment_trends_analysis": [],
        "summary": {}
    }
    
    try:
        # Get table names using centralized method
        tables = db_manager.get_table_names()
        
        for table_name in tables:
            # For now, we'll keep the column inspection logic as it's schema-specific
            # This could be moved to DatabaseManager if needed
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            # Validate table name to prevent SQL injection
            if not table_name.replace('_', '').replace('-', '').isalnum():
                raise ValueError(f"Invalid table name: {table_name}")
            cursor.execute('PRAGMA table_info("{}")'.format(table_name))
            columns = cursor.fetchall()
            conn.close()
            
            table_info = []
            for col in columns:
                column_info = {
                    "name": col[1],
                    "type": col[2],
                    "primary_key": bool(col[5])
                }
                table_info.append(column_info)
            
            result["database_structure"][table_name] = table_info
        
        # Use centralized method for sample user profiles
        profiles = db_manager.get_sample_user_profiles(10)
        if profiles:
            df = pd.DataFrame(profiles)
            # Replace NaN values with None (null in JSON) to ensure valid JSON
            df = df.where(pd.notna(df), None)
            result["sample_user_profiles"] = df.to_dict('records')
        
        # Use centralized method for employment analysis
        employment_data = db_manager.get_employment_income_analysis()
        if employment_data:
            df = pd.DataFrame(employment_data)
            # Replace NaN values with None (null in JSON) to ensure valid JSON
            df = df.where(pd.notna(df), None)
            result["employment_income_analysis"] = df.to_dict('records')
        
        # Use centralized method for province analysis
        province_data = db_manager.get_province_analysis()
        if province_data:
            df = pd.DataFrame(province_data)
            # Replace NaN values with None (null in JSON) to ensure valid JSON
            df = df.where(pd.notna(df), None)
            result["provincial_analysis"] = df.to_dict('records')
        
        # Use centralized method for loan analysis
        loan_data = db_manager.get_loan_amount_analysis()
        if loan_data:
            df = pd.DataFrame(loan_data)
            # Replace NaN values with None (null in JSON) to ensure valid JSON
            df = df.where(pd.notna(df), None)
            result["loan_amount_analysis"] = df.to_dict('records')
        
        # Use centralized method for program analysis
        program_data = db_manager.get_program_analysis()
        if program_data:
            df = pd.DataFrame(program_data)
            # Replace NaN values with None (null in JSON) to ensure valid JSON
            df = df.where(pd.notna(df), None)
            result["program_analysis"] = df.to_dict('records')
        
        # Use centralized method for payment status analysis
        payment_status_data = db_manager.get_payment_status_analysis()
        if payment_status_data:
            df = pd.DataFrame(payment_status_data)
            # Replace NaN values with None (null in JSON) to ensure valid JSON
            df = df.where(pd.notna(df), None)
            result["payment_status_analysis"] = df.to_dict('records')
        
        # Use centralized method for payment trends analysis
        payment_trends_data = db_manager.get_payment_trends_analysis()
        if payment_trends_data:
            df = pd.DataFrame(payment_trends_data)
            # Replace NaN values with None (null in JSON) to ensure valid JSON
            df = df.where(pd.notna(df), None)
            result["payment_trends_analysis"] = df.head(20).to_dict('records')  # Limit to 20 records
        
        # Add summary information
        result["summary"] = {
            "total_tables": len(tables),
            "tables_analyzed": len([k for k, v in result.items() if k != "database_structure" and k != "summary" and v]),
            "analysis_complete": True
        }
        
    except Exception as e:
        result["error"] = str(e)
        result["summary"] = {
            "analysis_complete": False,
            "error_message": str(e)
        }
    
    return result


def explore_database_console():
    """
    Console version of explore_database that prints results (for backward compatibility)
    """
    result = explore_database()
    
    if "error" in result:
        print(f"❌ Error exploring database: {result['error']}")
        return result  # Return the same error structure as the JSON version
    
    print("=== DATABASE STRUCTURE ===")
    for table_name, columns in result["database_structure"].items():
        print(f"\nTable: {table_name}")
        print("Columns:")
        for col in columns:
            primary_key_text = " PRIMARY KEY" if col["primary_key"] else ""
            print(f"  - {col['name']} ({col['type']}){primary_key_text}")
    
    print("\n" + "="*50)
    print("SAMPLE USER PROFILES")
    print("="*50)
    if result["sample_user_profiles"]:
        df = pd.DataFrame(result["sample_user_profiles"])
        print(df.to_string(index=False))
    else:
        print("No user profile data found.")
    
    print("\n" + "="*50)
    print("EMPLOYMENT AND INCOME ANALYSIS")
    print("="*50)
    if result["employment_income_analysis"]:
        df = pd.DataFrame(result["employment_income_analysis"])
        print(df.to_string(index=False))
    else:
        print("No employment data found.")
    
    print("\n" + "="*50)
    print("PROVINCIAL ANALYSIS")
    print("="*50)
    if result["provincial_analysis"]:
        df = pd.DataFrame(result["provincial_analysis"])
        print(df.to_string(index=False))
    else:
        print("No provincial data found.")
    
    print("\n" + "="*50)
    print("LOAN AMOUNT ANALYSIS")
    print("="*50)
    if result["loan_amount_analysis"]:
        df = pd.DataFrame(result["loan_amount_analysis"])
        print(df.to_string(index=False))
    else:
        print("No loan data found.")
    
    print("\n" + "="*50)
    print("PROGRAM OF STUDY ANALYSIS")
    print("="*50)
    if result["program_analysis"]:
        df = pd.DataFrame(result["program_analysis"])
        print(df.to_string(index=False))
    else:
        print("No program data found.")
    
    print("\n" + "="*50)
    print("PAYMENT STATUS ANALYSIS")
    print("="*50)
    if result["payment_status_analysis"]:
        df = pd.DataFrame(result["payment_status_analysis"])
        print(df.to_string(index=False))
    else:
        print("No payment status data found.")
    
    print("\n" + "="*50)
    print("PAYMENT TRENDS ANALYSIS")
    print("="*50)
    if result["payment_trends_analysis"]:
        df = pd.DataFrame(result["payment_trends_analysis"])
        print(df.to_string(index=False, max_rows=20))
    else:
        print("No payment trends data found.")
    
    # Display summary information to match the JSON version
    print("\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    if "summary" in result:
        summary = result["summary"]
        print(f"Total Tables: {summary.get('total_tables', 'N/A')}")
        print(f"Tables Analyzed: {summary.get('tables_analyzed', 'N/A')}")
        print(f"Analysis Complete: {summary.get('analysis_complete', 'N/A')}")
    
    return result  # Return the same data structure for consistency

def main():
    """
    Main entry point for database exploration (console version).
    """
    try:
        result = explore_database_console()
        if "error" in result:
            print("\n🔍 Troubleshooting tips:")
            print("1. Ensure the database exists and has been populated")
            print("2. Check database permissions")
            print("3. Verify all required dependencies are installed")
        else:
            print(f"\n🎉 Database exploration completed successfully!")
    except Exception as e:
        print(f"❌ Error exploring database: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Ensure the database exists and has been populated")
        print("2. Check database permissions")
        print("3. Verify all required dependencies are installed")

if __name__ == "__main__":
    main()