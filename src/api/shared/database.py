"""
Database utilities for SQLite operations in local development
"""
import os
import sqlite3
import json
from typing import List, Dict, Any


class DatabaseManager:
    def __init__(self):
        self.db_filename = "delinquency_data.db"
        
    def get_connection(self) -> sqlite3.Connection:
        """Get SQLite connection"""
        # Check if database exists, if not create it
        if not os.path.exists(self.db_filename):
            self.create_database()
        
        return sqlite3.connect(self.db_filename)
    
    def create_database(self):
        """Create initial database schema"""
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loan_info (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                loan_amount REAL NOT NULL,
                interest_rate REAL NOT NULL,
                loan_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profile (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS programs_of_study (
                id TEXT PRIMARY KEY,
                program_name TEXT NOT NULL,
                degree_level TEXT NOT NULL,
                duration_months INTEGER NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loan_payments (
                id TEXT PRIMARY KEY,
                loan_id TEXT NOT NULL,
                payment_amount REAL NOT NULL,
                payment_date TIMESTAMP NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (loan_id) REFERENCES loan_info (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        result = [dict(row) for row in rows]
        conn.close()
        
        return result
    
    def execute_insert(self, query: str, params: tuple = ()):
        """Execute an INSERT query"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        conn.commit()
        conn.close()
    
    def execute_many(self, query: str, data: List[tuple]):
        """Execute multiple INSERT queries"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.executemany(query, data)
        conn.commit()
        conn.close()