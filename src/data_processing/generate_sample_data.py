"""
Generate synthetic customer onboarding data for analytics
This creates realistic test data matching Signzy's digital KYC onboarding scenario
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class OnboardingDataGenerator:
    """Generate synthetic customer onboarding data"""
    
    def __init__(self, num_records=10000, start_date='2023-01-01', end_date='2024-12-31'):
        self.num_records = num_records
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        
        # Indian names for realistic data
        self.first_names = ['Rajesh', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 
                            'Rahul', 'Pooja', 'Arjun', 'Divya', 'Karan', 'Neha',
                            'Sanjay', 'Kavya', 'Rohan', 'Swati', 'Arun', 'Meera']
        
        self.last_names = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Nair',
                          'Gupta', 'Shah', 'Agarwal', 'Joshi', 'Mehta', 'Verma']
        
        self.cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 
                      'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
        
        self.states = ['Maharashtra', 'Delhi', 'Karnataka', 'Telangana', 'Tamil Nadu',
                      'West Bengal', 'Maharashtra', 'Gujarat', 'Rajasthan', 'Uttar Pradesh']
        
        self.occupations = ['Software Engineer', 'Teacher', 'Doctor', 'Business Owner',
                           'Consultant', 'Manager', 'Accountant', 'Sales Executive',
                           'Government Employee', 'Student', 'Self Employed']
        
        self.document_types = ['aadhaar', 'pan', 'passport', 'driving_license', 'voter_id']
        
        self.channels = ['mobile', 'web', 'branch']
        self.device_types = ['android', 'ios', 'desktop', 'tablet']
        
        self.application_types = ['savings', 'current', 'credit_card', 'loan']
        
        self.failure_reasons = [
            'Poor image quality',
            'Document not readable',
            'Details mismatch',
            'Expired document',
            'Photo mismatch',
            'Address verification failed',
            'Duplicate application',
            'Incomplete information'
        ]
        
    def generate_dates(self):
        """Generate random dates between start and end date"""
        date_range = (self.end_date - self.start_date).days
        random_days = np.random.randint(0, date_range, self.num_records)
        
        # Add time of day with realistic distribution (peak hours)
        # Using random.choices with weights instead of np.random.choice with probabilities
        # This avoids floating point precision issues
        hour_weights = [1, 1, 1, 1, 1, 2, 3, 4, 5, 8,   # 0-9
                       10, 11, 10, 9, 8, 7, 6, 5, 4, 3,   # 10-19
                       2, 1, 1, 1]                        # 20-23
        
        hours = random.choices(range(24), weights=hour_weights, k=self.num_records)
        
        dates = [self.start_date + timedelta(days=int(d), hours=int(h)) 
                for d, h in zip(random_days, hours)]
        
        return dates
    
    def generate_customers(self):
        """Generate customer data"""
        customers = []
        
        for i in range(self.num_records):
            customer = {
                'customer_id': i + 1,
                'email': f"{self.first_names[i % len(self.first_names)].lower()}.{self.last_names[i % len(self.last_names)].lower()}{i}@example.com",
                'phone': f"+91{random.randint(7000000000, 9999999999)}"
            }
            customers.append(customer)
        
        return pd.DataFrame(customers)
    
    def generate_applications(self, application_dates):
        """Generate application data"""
        applications = []
        
        for i, app_date in enumerate(application_dates):
            # Generate status with realistic distribution
            status_prob = random.random()
            if status_prob < 0.65:  # 65% approved
                status = 'approved'
            elif status_prob < 0.85:  # 20% rejected
                status = 'rejected'
            elif status_prob < 0.95:  # 10% pending
                status = 'pending'
            else:  # 5% under review
                status = 'under_review'
            
            # Channel and device
            channel = np.random.choice(self.channels, p=[0.50, 0.35, 0.15])
            if channel == 'mobile':
                device_type = np.random.choice(['android', 'ios'], p=[0.65, 0.35])
            elif channel == 'web':
                device_type = np.random.choice(['desktop', 'tablet'], p=[0.80, 0.20])
            else:
                device_type = 'desktop'
            
            # Processing time (in hours)
            if status == 'approved':
                processing_hours = np.random.exponential(12) + 1  # Average 13 hours
            elif status == 'rejected':
                processing_hours = np.random.exponential(8) + 1  # Faster rejection
            else:
                processing_hours = None
            
            # Risk score (higher for rejected applications)
            if status == 'rejected':
                risk_score = np.random.beta(8, 2)  # Skewed towards high risk
            elif status == 'approved':
                risk_score = np.random.beta(2, 8)  # Skewed towards low risk
            else:
                risk_score = np.random.beta(5, 5)  # Uniform
            
            # Risk category
            if risk_score < 0.3:
                risk_category = 'low'
            elif risk_score < 0.7:
                risk_category = 'medium'
            else:
                risk_category = 'high'
            
            # Fraud flag (3% of applications)
            fraud_flag = random.random() < 0.03
            
            # Age and income
            age = random.randint(21, 65)
            annual_income = random.randint(200000, 5000000)
            
            application = {
                'application_id': i + 1,
                'customer_id': i + 1,
                'application_date': app_date,
                'application_status': status,
                'application_type': random.choice(self.application_types),
                'channel': channel,
                'device_type': device_type,
                'referral_source': random.choice(['organic', 'google_ads', 'facebook', 'referral', 'branch']),
                'full_name': f"{random.choice(self.first_names)} {random.choice(self.last_names)}",
                'date_of_birth': datetime(1960 + age - 21, random.randint(1, 12), random.randint(1, 28)),
                'gender': random.choice(['Male', 'Female']),
                'nationality': 'Indian',
                'city': random.choice(self.cities),
                'state': random.choice(self.states),
                'pincode': f"{random.randint(100000, 999999)}",
                'country': 'India',
                'occupation': random.choice(self.occupations),
                'annual_income': annual_income,
                'employment_type': random.choice(['salaried', 'self_employed', 'business']),
                'assigned_to': f"agent_{random.randint(1, 20):03d}",
                'processing_start_time': app_date + timedelta(minutes=random.randint(5, 120)),
                'processing_end_time': app_date + timedelta(hours=processing_hours) if processing_hours else None,
                'processing_duration_hours': processing_hours,
                'approval_date': app_date + timedelta(hours=processing_hours) if status == 'approved' and processing_hours else None,
                'rejection_date': app_date + timedelta(hours=processing_hours) if status == 'rejected' and processing_hours else None,
                'rejection_reason': random.choice(self.failure_reasons) if status == 'rejected' else None,
                'risk_score': round(risk_score, 3),
                'risk_category': risk_category,
                'fraud_flag': fraud_flag,
                'compliance_score': round(random.uniform(0.7, 1.0), 3),
                'regulatory_check_status': 'passed' if status != 'rejected' else random.choice(['passed', 'failed']),
                'aml_check_passed': status != 'rejected' or random.random() > 0.3
            }
            
            applications.append(application)
        
        return pd.DataFrame(applications)
    
    def generate_kyc_verifications(self, num_applications):
        """Generate KYC verification data"""
        verifications = []
        
        for app_id in range(1, num_applications + 1):
            # Each application has 2-3 document verifications
            num_docs = random.randint(2, 3)
            
            for _ in range(num_docs):
                doc_type = random.choice(self.document_types)
                
                # Verification status
                status_prob = random.random()
                if status_prob < 0.85:  # 85% verified
                    ver_status = 'verified'
                elif status_prob < 0.92:  # 7% failed
                    ver_status = 'failed'
                elif status_prob < 0.97:  # 5% pending
                    ver_status = 'pending'
                else:  # 3% rejected
                    ver_status = 'rejected'
                
                # Document quality scores
                if ver_status == 'verified':
                    quality_score = np.random.beta(8, 2)
                    ocr_score = np.random.beta(9, 2)
                    face_match = np.random.beta(8, 2)
                    attempts = random.randint(1, 2)
                else:
                    quality_score = np.random.beta(3, 5)
                    ocr_score = np.random.beta(3, 5)
                    face_match = np.random.beta(3, 5)
                    attempts = random.randint(2, 5)
                
                verification = {
                    'application_id': app_id,
                    'document_type': doc_type,
                    'document_number': f"{doc_type.upper()}{random.randint(100000000, 999999999)}",
                    'verification_status': ver_status,
                    'verification_method': random.choice(['automated', 'manual', 'hybrid']),
                    'document_uploaded': True,
                    'document_quality_score': round(quality_score, 3),
                    'ocr_confidence_score': round(ocr_score, 3),
                    'face_match_score': round(face_match, 3),
                    'liveness_check_passed': ver_status in ['verified', 'pending'],
                    'address_verification_status': random.choice(['verified', 'pending', 'failed']),
                    'verification_attempts': attempts,
                    'retry_count': attempts - 1,
                    'failure_reason': random.choice(self.failure_reasons) if ver_status in ['failed', 'rejected'] else None,
                    'manual_review_required': ver_status == 'rejected' or (ver_status == 'failed' and random.random() < 0.3)
                }
                
                verifications.append(verification)
        
        return pd.DataFrame(verifications)
    
    def generate_onboarding_events(self, num_applications):
        """Generate onboarding event data for funnel analysis"""
        events = []
        event_id = 1
        
        event_types = [
            'application_started',
            'personal_details_completed',
            'document_uploaded',
            'kyc_initiated',
            'kyc_completed',
            'terms_accepted',
            'account_created',
            'first_transaction'
        ]
        
        for app_id in range(1, num_applications + 1):
            # Simulate funnel drop-off
            num_events = random.choices(
                range(1, len(event_types) + 1),
                weights=[5, 10, 15, 15, 15, 15, 15, 10],
                k=1
            )[0]
            
            base_time = datetime.now() - timedelta(days=random.randint(1, 365))
            
            for i in range(num_events):
                event = {
                    'event_id': event_id,
                    'application_id': app_id,
                    'event_type': event_types[i],
                    'event_timestamp': base_time + timedelta(minutes=random.randint(1, 60) * i),
                    'session_id': f"session_{app_id}_{random.randint(1000, 9999)}",
                    'time_spent_seconds': random.randint(30, 600)
                }
                
                events.append(event)
                event_id += 1
        
        return pd.DataFrame(events)
    
    def generate_all_data(self):
        """Generate all datasets"""
        print(f"Generating {self.num_records} customer onboarding records...")
        
        # Generate application dates
        application_dates = self.generate_dates()
        
        # Generate all datasets
        print("Generating customers...")
        customers_df = self.generate_customers()
        
        print("Generating applications...")
        applications_df = self.generate_applications(application_dates)
        
        print("Generating KYC verifications...")
        kyc_df = self.generate_kyc_verifications(self.num_records)
        
        print("Generating onboarding events...")
        events_df = self.generate_onboarding_events(self.num_records)
        
        return customers_df, applications_df, kyc_df, events_df
    
    def save_to_csv(self, customers_df, applications_df, kyc_df, events_df):
        """Save datasets to CSV files"""
        print("\nSaving datasets to CSV files...")
        
        customers_df.to_csv('data/raw/customers.csv', index=False)
        print("✓ Saved customers.csv")
        
        applications_df.to_csv('data/raw/applications.csv', index=False)
        print("✓ Saved applications.csv")
        
        kyc_df.to_csv('data/raw/kyc_verifications.csv', index=False)
        print("✓ Saved kyc_verifications.csv")
        
        events_df.to_csv('data/raw/onboarding_events.csv', index=False)
        print("✓ Saved onboarding_events.csv")
        
        print("\n✅ All datasets generated successfully!")
        print(f"\nDataset Summary:")
        print(f"- Customers: {len(customers_df):,}")
        print(f"- Applications: {len(applications_df):,}")
        print(f"- KYC Verifications: {len(kyc_df):,}")
        print(f"- Onboarding Events: {len(events_df):,}")


def main():
    """Main execution function"""
    # Initialize generator
    generator = OnboardingDataGenerator(
        num_records=10000,
        start_date='2023-01-01',
        end_date='2024-12-31'
    )
    
    # Generate data
    customers_df, applications_df, kyc_df, events_df = generator.generate_all_data()
    
    # Save to CSV
    generator.save_to_csv(customers_df, applications_df, kyc_df, events_df)
    
    # Display sample data
    print("\n" + "="*80)
    print("SAMPLE DATA")
    print("="*80)
    
    print("\n📋 Applications Sample:")
    print(applications_df.head())
    
    print("\n📄 KYC Verifications Sample:")
    print(kyc_df.head())
    
    print("\n📊 Quick Statistics:")
    print(f"\nApplication Status Distribution:")
    print(applications_df['application_status'].value_counts())
    
    print(f"\nRisk Category Distribution:")
    print(applications_df['risk_category'].value_counts())
    
    print(f"\nChannel Distribution:")
    print(applications_df['channel'].value_counts())


if __name__ == "__main__":
    main()