"""
Customer Onboarding Analytics - Metrics Calculator
Calculates key metrics and KPIs for customer onboarding process
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class OnboardingMetricsCalculator:
    """Calculate comprehensive onboarding metrics"""
    
    def __init__(self, applications_df, kyc_df, events_df):
        """
        Initialize with dataframes
        
        Args:
            applications_df: Applications data
            kyc_df: KYC verifications data
            events_df: Onboarding events data
        """
        self.applications_df = applications_df.copy()
        self.kyc_df = kyc_df.copy()
        self.events_df = events_df.copy()
        
        # Convert date columns
        date_columns = ['application_date', 'processing_start_time', 
                       'processing_end_time', 'approval_date', 'rejection_date']
        for col in date_columns:
            if col in self.applications_df.columns:
                self.applications_df[col] = pd.to_datetime(self.applications_df[col])
        
        if 'event_timestamp' in self.events_df.columns:
            self.events_df['event_timestamp'] = pd.to_datetime(self.events_df['event_timestamp'])
    
    def calculate_operational_metrics(self):
        """Calculate operational KPIs"""
        print("\n" + "="*80)
        print("OPERATIONAL METRICS")
        print("="*80)
        
        metrics = {}
        
        # Total applications
        metrics['total_applications'] = len(self.applications_df)
        
        # Status breakdown
        status_counts = self.applications_df['application_status'].value_counts()
        metrics['approved'] = status_counts.get('approved', 0)
        metrics['rejected'] = status_counts.get('rejected', 0)
        metrics['pending'] = status_counts.get('pending', 0)
        metrics['under_review'] = status_counts.get('under_review', 0)
        
        # Approval rate
        processed = metrics['approved'] + metrics['rejected']
        metrics['approval_rate'] = (metrics['approved'] / processed * 100) if processed > 0 else 0
        
        # Processing time statistics
        processed_apps = self.applications_df[
            self.applications_df['processing_duration_hours'].notna()
        ]
        
        if len(processed_apps) > 0:
            metrics['avg_processing_hours'] = processed_apps['processing_duration_hours'].mean()
            metrics['median_processing_hours'] = processed_apps['processing_duration_hours'].median()
            metrics['p95_processing_hours'] = processed_apps['processing_duration_hours'].quantile(0.95)
            
            # SLA compliance (assuming 48 hours SLA)
            metrics['sla_compliance_rate'] = (
                (processed_apps['processing_duration_hours'] <= 48).sum() / 
                len(processed_apps) * 100
            )
        
        # Daily application trends
        self.applications_df['date'] = self.applications_df['application_date'].dt.date
        daily_apps = self.applications_df.groupby('date').size()
        metrics['avg_daily_applications'] = daily_apps.mean()
        metrics['peak_daily_applications'] = daily_apps.max()
        
        # Print metrics
        print(f"\n📊 Application Volume:")
        print(f"   Total Applications: {metrics['total_applications']:,}")
        print(f"   Approved: {metrics['approved']:,} ({metrics['approved']/metrics['total_applications']*100:.1f}%)")
        print(f"   Rejected: {metrics['rejected']:,} ({metrics['rejected']/metrics['total_applications']*100:.1f}%)")
        print(f"   Pending: {metrics['pending']:,}")
        print(f"   Under Review: {metrics['under_review']:,}")
        
        print(f"\n⏱️  Processing Time:")
        if 'avg_processing_hours' in metrics:
            print(f"   Average: {metrics['avg_processing_hours']:.1f} hours")
            print(f"   Median: {metrics['median_processing_hours']:.1f} hours")
            print(f"   95th Percentile: {metrics['p95_processing_hours']:.1f} hours")
            print(f"   SLA Compliance (48h): {metrics['sla_compliance_rate']:.1f}%")
        
        print(f"\n📈 Volume Trends:")
        print(f"   Average Daily: {metrics['avg_daily_applications']:.0f} applications")
        print(f"   Peak Daily: {metrics['peak_daily_applications']:.0f} applications")
        
        return metrics
    
    def calculate_kyc_metrics(self):
        """Calculate KYC verification metrics"""
        print("\n" + "="*80)
        print("KYC COMPLIANCE METRICS")
        print("="*80)
        
        metrics = {}
        
        # Overall KYC success rate
        total_verifications = len(self.kyc_df)
        verified = (self.kyc_df['verification_status'] == 'verified').sum()
        metrics['overall_success_rate'] = (verified / total_verifications * 100) if total_verifications > 0 else 0
        
        # Success rate by document type
        doc_success = self.kyc_df.groupby('document_type').apply(
            lambda x: (x['verification_status'] == 'verified').sum() / len(x) * 100
        ).to_dict()
        metrics['success_by_document'] = doc_success
        
        # Average quality scores
        metrics['avg_document_quality'] = self.kyc_df['document_quality_score'].mean()
        metrics['avg_ocr_confidence'] = self.kyc_df['ocr_confidence_score'].mean()
        metrics['avg_face_match'] = self.kyc_df['face_match_score'].mean()
        
        # Verification attempts
        metrics['avg_attempts'] = self.kyc_df['verification_attempts'].mean()
        
        # Manual review requirements
        manual_review = (self.kyc_df['manual_review_required'] == True).sum()
        metrics['manual_review_rate'] = (manual_review / total_verifications * 100) if total_verifications > 0 else 0
        
        # Failure reasons
        failed_kyc = self.kyc_df[self.kyc_df['verification_status'].isin(['failed', 'rejected'])]
        failure_reasons = failed_kyc['failure_reason'].value_counts().head(5).to_dict()
        metrics['top_failure_reasons'] = failure_reasons
        
        # Print metrics
        print(f"\n✅ Verification Success:")
        print(f"   Overall Success Rate: {metrics['overall_success_rate']:.1f}%")
        print(f"   Total Verifications: {total_verifications:,}")
        print(f"   Successful: {verified:,}")
        
        print(f"\n📄 Success Rate by Document Type:")
        for doc_type, rate in doc_success.items():
            print(f"   {doc_type.upper()}: {rate:.1f}%")
        
        print(f"\n🎯 Quality Scores:")
        print(f"   Document Quality: {metrics['avg_document_quality']:.3f}")
        print(f"   OCR Confidence: {metrics['avg_ocr_confidence']:.3f}")
        print(f"   Face Match: {metrics['avg_face_match']:.3f}")
        
        print(f"\n🔄 Processing:")
        print(f"   Average Attempts: {metrics['avg_attempts']:.1f}")
        print(f"   Manual Review Required: {metrics['manual_review_rate']:.1f}%")
        
        print(f"\n❌ Top Failure Reasons:")
        for reason, count in list(failure_reasons.items())[:5]:
            print(f"   {reason}: {count:,} ({count/len(failed_kyc)*100:.1f}%)")
        
        return metrics
    
    def calculate_risk_metrics(self):
        """Calculate risk and fraud metrics"""
        print("\n" + "="*80)
        print("RISK & FRAUD METRICS")
        print("="*80)
        
        metrics = {}
        
        # Risk distribution
        risk_dist = self.applications_df['risk_category'].value_counts().to_dict()
        metrics['risk_distribution'] = risk_dist
        
        # Average risk score
        metrics['avg_risk_score'] = self.applications_df['risk_score'].mean()
        
        # Fraud statistics
        fraud_count = self.applications_df['fraud_flag'].sum()
        metrics['fraud_cases'] = fraud_count
        metrics['fraud_rate'] = (fraud_count / len(self.applications_df) * 100)
        
        # Risk vs approval rate
        risk_approval = self.applications_df.groupby('risk_category').apply(
            lambda x: (x['application_status'] == 'approved').sum() / len(x) * 100
        ).to_dict()
        metrics['approval_by_risk'] = risk_approval
        
        # High risk characteristics
        high_risk = self.applications_df[self.applications_df['risk_category'] == 'high']
        if len(high_risk) > 0:
            metrics['high_risk_fraud_rate'] = (high_risk['fraud_flag'].sum() / len(high_risk) * 100)
            metrics['high_risk_rejection_rate'] = (
                (high_risk['application_status'] == 'rejected').sum() / len(high_risk) * 100
            )
        
        # Print metrics
        print(f"\n⚠️  Risk Distribution:")
        total_apps = len(self.applications_df)
        for category in ['low', 'medium', 'high']:
            count = risk_dist.get(category, 0)
            print(f"   {category.capitalize()} Risk: {count:,} ({count/total_apps*100:.1f}%)")
        
        print(f"\n📊 Risk Scores:")
        print(f"   Average Risk Score: {metrics['avg_risk_score']:.3f}")
        
        print(f"\n🚨 Fraud Detection:")
        print(f"   Fraud Cases: {fraud_count:,}")
        print(f"   Fraud Rate: {metrics['fraud_rate']:.2f}%")
        
        print(f"\n✓ Approval Rate by Risk Category:")
        for category, rate in risk_approval.items():
            print(f"   {category.capitalize()}: {rate:.1f}%")
        
        if 'high_risk_fraud_rate' in metrics:
            print(f"\n⚡ High Risk Analysis:")
            print(f"   Fraud Rate in High Risk: {metrics['high_risk_fraud_rate']:.1f}%")
            print(f"   Rejection Rate: {metrics['high_risk_rejection_rate']:.1f}%")
        
        return metrics
    
    def calculate_channel_metrics(self):
        """Calculate channel and device performance metrics"""
        print("\n" + "="*80)
        print("CHANNEL & DEVICE METRICS")
        print("="*80)
        
        metrics = {}
        
        # Channel distribution
        channel_dist = self.applications_df['channel'].value_counts().to_dict()
        metrics['channel_distribution'] = channel_dist
        
        # Performance by channel
        channel_perf = self.applications_df.groupby('channel').agg({
            'application_id': 'count',
            'application_status': lambda x: (x == 'approved').sum() / len(x) * 100,
            'processing_duration_hours': 'mean',
            'fraud_flag': 'sum'
        }).round(2)
        channel_perf.columns = ['applications', 'approval_rate', 'avg_processing_hours', 'fraud_count']
        metrics['channel_performance'] = channel_perf.to_dict()
        
        # Device type analysis
        device_dist = self.applications_df['device_type'].value_counts().to_dict()
        metrics['device_distribution'] = device_dist
        
        # Mobile vs Web comparison
        mobile_apps = self.applications_df[self.applications_df['device_type'].isin(['android', 'ios'])]
        web_apps = self.applications_df[self.applications_df['device_type'] == 'desktop']
        
        if len(mobile_apps) > 0 and len(web_apps) > 0:
            metrics['mobile_approval_rate'] = (
                (mobile_apps['application_status'] == 'approved').sum() / len(mobile_apps) * 100
            )
            metrics['web_approval_rate'] = (
                (web_apps['application_status'] == 'approved').sum() / len(web_apps) * 100
            )
        
        # Print metrics
        print(f"\n📱 Channel Distribution:")
        total = len(self.applications_df)
        for channel, count in channel_dist.items():
            print(f"   {channel.capitalize()}: {count:,} ({count/total*100:.1f}%)")
        
        print(f"\n📊 Channel Performance:")
        print(channel_perf.to_string())
        
        print(f"\n💻 Device Distribution:")
        for device, count in device_dist.items():
            print(f"   {device.capitalize()}: {count:,} ({count/total*100:.1f}%)")
        
        if 'mobile_approval_rate' in metrics:
            print(f"\n📲 Mobile vs Web:")
            print(f"   Mobile Approval Rate: {metrics['mobile_approval_rate']:.1f}%")
            print(f"   Web Approval Rate: {metrics['web_approval_rate']:.1f}%")
        
        return metrics
    
    def calculate_funnel_metrics(self):
        """Calculate onboarding funnel metrics"""
        print("\n" + "="*80)
        print("ONBOARDING FUNNEL ANALYSIS")
        print("="*80)
        
        # Get unique applications with each event
        event_pivot = self.events_df.pivot_table(
            index='application_id',
            columns='event_type',
            values='event_timestamp',
            aggfunc='first'
        ).notna()
        
        funnel_stages = [
            'application_started',
            'personal_details_completed',
            'document_uploaded',
            'kyc_completed',
            'terms_accepted',
            'account_created'
        ]
        
        funnel_data = []
        prev_count = None
        
        for stage in funnel_stages:
            if stage in event_pivot.columns:
                count = event_pivot[stage].sum()
                if prev_count is not None:
                    conversion = (count / prev_count * 100) if prev_count > 0 else 0
                    drop_off = 100 - conversion
                else:
                    conversion = 100.0
                    drop_off = 0.0
                
                funnel_data.append({
                    'stage': stage.replace('_', ' ').title(),
                    'count': count,
                    'conversion_rate': conversion,
                    'drop_off_rate': drop_off
                })
                prev_count = count
        
        funnel_df = pd.DataFrame(funnel_data)
        
        print(f"\n🎯 Conversion Funnel:")
        print(funnel_df.to_string(index=False))
        
        # Calculate overall conversion rate
        if len(funnel_data) > 0:
            overall_conversion = (funnel_data[-1]['count'] / funnel_data[0]['count'] * 100)
            print(f"\n📈 Overall Conversion Rate: {overall_conversion:.1f}%")
        
        return funnel_df.to_dict()
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n" + "="*80)
        print("EXECUTIVE SUMMARY")
        print("="*80)
        
        # Key metrics
        total_apps = len(self.applications_df)
        approved = (self.applications_df['application_status'] == 'approved').sum()
        approval_rate = (approved / total_apps * 100) if total_apps > 0 else 0
        
        processed = self.applications_df[self.applications_df['processing_duration_hours'].notna()]
        avg_processing = processed['processing_duration_hours'].mean() if len(processed) > 0 else 0
        
        kyc_success = (self.kyc_df['verification_status'] == 'verified').sum() / len(self.kyc_df) * 100
        
        fraud_rate = (self.applications_df['fraud_flag'].sum() / total_apps * 100)
        
        print(f"\n🎯 KEY PERFORMANCE INDICATORS:")
        print(f"   • Total Applications: {total_apps:,}")
        print(f"   • Approval Rate: {approval_rate:.1f}%")
        print(f"   • Average Processing Time: {avg_processing:.1f} hours")
        print(f"   • KYC Success Rate: {kyc_success:.1f}%")
        print(f"   • Fraud Detection Rate: {fraud_rate:.2f}%")
        
        print(f"\n💡 INSIGHTS:")
        
        # Top channel
        top_channel = self.applications_df['channel'].value_counts().index[0]
        print(f"   • Most popular channel: {top_channel.capitalize()}")
        
        # Best performing day
        self.applications_df['dayofweek'] = pd.to_datetime(
            self.applications_df['application_date']
        ).dt.day_name()
        top_day = self.applications_df['dayofweek'].value_counts().index[0]
        print(f"   • Highest application volume: {top_day}")
        
        # Risk distribution
        high_risk_pct = (
            (self.applications_df['risk_category'] == 'high').sum() / total_apps * 100
        )
        print(f"   • High-risk applications: {high_risk_pct:.1f}%")
        
        # Processing efficiency
        sla_compliance = (processed['processing_duration_hours'] <= 48).sum() / len(processed) * 100
        print(f"   • SLA Compliance (48h): {sla_compliance:.1f}%")


def main():
    """Main execution"""
    print("="*80)
    print("CUSTOMER ONBOARDING ANALYTICS - METRICS CALCULATOR")
    print("="*80)
    
    # Load data
    print("\nLoading data...")
    applications_df = pd.read_csv('data/raw/applications.csv')
    kyc_df = pd.read_csv('data/raw/kyc_verifications.csv')
    events_df = pd.read_csv('data/raw/onboarding_events.csv')
    
    print(f"✓ Loaded {len(applications_df):,} applications")
    print(f"✓ Loaded {len(kyc_df):,} KYC verifications")
    print(f"✓ Loaded {len(events_df):,} onboarding events")
    
    # Initialize calculator
    calculator = OnboardingMetricsCalculator(applications_df, kyc_df, events_df)
    
    # Calculate all metrics
    operational_metrics = calculator.calculate_operational_metrics()
    kyc_metrics = calculator.calculate_kyc_metrics()
    risk_metrics = calculator.calculate_risk_metrics()
    channel_metrics = calculator.calculate_channel_metrics()
    funnel_metrics = calculator.calculate_funnel_metrics()
    
    # Generate summary
    calculator.generate_summary_report()
    
    print("\n" + "="*80)
    print("✅ Analysis Complete!")
    print("="*80)


if __name__ == "__main__":
    main()