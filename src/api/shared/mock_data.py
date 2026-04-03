"""
Mock data generation modules for synthetic data creation
"""
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from typing import List, Dict, Any

fake = Faker()

class MockDataGenerator:
    """Mock data generator for all entity types"""
    
    @staticmethod
    def generate_user_profiles(count: int = 50) -> List[tuple]:
        """Generate mock user profiles"""
        profiles = []
        for _ in range(count):
            profile = (
                str(uuid.uuid4()),
                fake.first_name(),
                fake.last_name(),
                fake.email(),
                fake.date_time_between(start_date='-2y', end_date='now').isoformat()
            )
            profiles.append(profile)
        return profiles
    
    @staticmethod
    def generate_loan_info(user_ids: List[str], count_per_user: int = 2) -> List[tuple]:
        """Generate mock loan information"""
        loans = []
        loan_types = ['Federal Subsidized', 'Federal Unsubsidized', 'Private', 'PLUS']
        
        for user_id in user_ids:
            for _ in range(random.randint(1, count_per_user)):
                loan = (
                    str(uuid.uuid4()),
                    user_id,
                    round(random.uniform(5000, 50000), 2),
                    round(random.uniform(3.5, 8.5), 2),
                    random.choice(loan_types),
                    fake.date_time_between(start_date='-2y', end_date='now').isoformat()
                )
                loans.append(loan)
        return loans
    
    @staticmethod
    def generate_programs_of_study(count: int = 20) -> List[tuple]:
        """Generate mock programs of study"""
        programs = []
        degree_levels = ['Associate', 'Bachelor', 'Master', 'Doctorate']
        program_names = [
            'Computer Science', 'Business Administration', 'Engineering', 
            'Nursing', 'Education', 'Psychology', 'Biology', 'Chemistry',
            'Mathematics', 'English Literature', 'History', 'Political Science',
            'Economics', 'Art', 'Music', 'Physics', 'Communications',
            'Criminal Justice', 'Social Work', 'Marketing'
        ]
        
        for _ in range(count):
            degree_level = random.choice(degree_levels)
            duration_map = {
                'Associate': random.randint(18, 24),
                'Bachelor': random.randint(36, 48),
                'Master': random.randint(18, 30),
                'Doctorate': random.randint(48, 84)
            }
            
            program = (
                str(uuid.uuid4()),
                random.choice(program_names),
                degree_level,
                duration_map[degree_level]
            )
            programs.append(program)
        return programs
    
    @staticmethod
    def generate_loan_payments(loan_ids: List[str], payments_per_loan: int = 12) -> List[tuple]:
        """Generate mock loan payment history"""
        payments = []
        statuses = ['Paid', 'Late', 'Delinquent', 'Default']
        
        for loan_id in loan_ids:
            start_date = fake.date_time_between(start_date='-1y', end_date='-6m')
            for i in range(random.randint(1, payments_per_loan)):
                payment_date = start_date + timedelta(days=30 * i)
                # Most payments are on time, some are late/delinquent
                status_weights = [0.7, 0.2, 0.08, 0.02]
                status = random.choices(statuses, weights=status_weights)[0]
                
                payment = (
                    str(uuid.uuid4()),
                    loan_id,
                    round(random.uniform(200, 800), 2),
                    payment_date.isoformat(),
                    status
                )
                payments.append(payment)
        return payments