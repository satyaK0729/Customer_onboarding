"""
Customer Onboarding Analytics - Visualization Module
Creates comprehensive visualizations for dashboard and reports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class OnboardingVisualizer:
    """Create visualizations for onboarding analytics"""
    
    def __init__(self, applications_df, kyc_df, events_df):
        """Initialize with dataframes"""
        self.applications_df = applications_df.copy()
        self.kyc_df = kyc_df.copy()
        self.events_df = events_df.copy()
        
        # Convert dates
        self.applications_df['application_date'] = pd.to_datetime(
            self.applications_df['application_date']
        )
        self.applications_df['date'] = self.applications_df['application_date'].dt.date
        
        # Create output directory
        import os
        os.makedirs('reports/visualizations', exist_ok=True)
    
    def plot_daily_applications(self):
        """Plot daily application trends"""
        daily_counts = self.applications_df.groupby('date').size().reset_index(name='count')
        daily_counts['date'] = pd.to_datetime(daily_counts['date'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_counts['date'],
            y=daily_counts['count'],
            mode='lines+markers',
            name='Applications',
            line=dict(color='#3498db', width=2),
            marker=dict(size=6)
        ))
        
        # Add 7-day moving average
        daily_counts['ma7'] = daily_counts['count'].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=daily_counts['date'],
            y=daily_counts['ma7'],
            mode='lines',
            name='7-day MA',
            line=dict(color='#e74c3c', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Daily Application Volume Trend',
            xaxis_title='Date',
            yaxis_title='Number of Applications',
            hovermode='x unified',
            template='plotly_white'
        )
        
        fig.write_html('reports/visualizations/daily_applications.html')
        print("✓ Created: daily_applications.html")
        
        return fig
    
    def plot_status_distribution(self):
        """Plot application status distribution"""
        status_counts = self.applications_df['application_status'].value_counts()
        
        colors = {
            'approved': '#27ae60',
            'rejected': '#e74c3c',
            'pending': '#f39c12',
            'under_review': '#3498db'
        }
        
        color_list = [colors.get(status, '#95a5a6') for status in status_counts.index]
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.4,
            marker=dict(colors=color_list),
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title='Application Status Distribution',
            template='plotly_white'
        )
        
        fig.write_html('reports/visualizations/status_distribution.html')
        print("✓ Created: status_distribution.html")
        
        return fig
    
    def plot_processing_time_distribution(self):
        """Plot processing time distribution"""
        processed = self.applications_df[
            self.applications_df['processing_duration_hours'].notna()
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=processed['processing_duration_hours'],
            nbinsx=50,
            name='Processing Time',
            marker_color='#3498db'
        ))
        
        # Add vertical lines for key metrics
        avg_time = processed['processing_duration_hours'].mean()
        median_time = processed['processing_duration_hours'].median()
        
        fig.add_vline(x=avg_time, line_dash="dash", line_color="red", 
                     annotation_text=f"Avg: {avg_time:.1f}h")
        fig.add_vline(x=median_time, line_dash="dash", line_color="green", 
                     annotation_text=f"Median: {median_time:.1f}h")
        fig.add_vline(x=48, line_dash="dot", line_color="orange", 
                     annotation_text="SLA: 48h")
        
        fig.update_layout(
            title='Processing Time Distribution',
            xaxis_title='Processing Time (hours)',
            yaxis_title='Number of Applications',
            template='plotly_white'
        )
        
        fig.write_html('reports/visualizations/processing_time_distribution.html')
        print("✓ Created: processing_time_distribution.html")
        
        return fig
    
    def plot_kyc_success_rates(self):
        """Plot KYC success rates by document type"""
        kyc_stats = self.kyc_df.groupby('document_type').agg({
            'verification_status': lambda x: (x == 'verified').sum() / len(x) * 100,
            'application_id': 'count'  # Use application_id to count records
        }).reset_index()
        kyc_stats.columns = ['document_type', 'success_rate', 'total_count']
        kyc_stats = kyc_stats.sort_values('success_rate', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=kyc_stats['document_type'],
            x=kyc_stats['success_rate'],
            orientation='h',
            marker=dict(
                color=kyc_stats['success_rate'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Success %")
            ),
            text=kyc_stats['success_rate'].round(1),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Success Rate: %{x:.1f}%<br>Total: %{customdata}<extra></extra>',
            customdata=kyc_stats['total_count']
        ))
        
        fig.update_layout(
            title='KYC Verification Success Rate by Document Type',
            xaxis_title='Success Rate (%)',
            yaxis_title='Document Type',
            template='plotly_white',
            xaxis=dict(range=[0, 100])
        )
        
        fig.write_html('reports/visualizations/kyc_success_rates.html')
        print("✓ Created: kyc_success_rates.html")
        
        return fig
    
    def plot_risk_distribution(self):
        """Plot risk score distribution"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Risk Score Distribution', 'Risk Category Distribution'),
            specs=[[{'type': 'histogram'}, {'type': 'pie'}]]
        )
        
        # Risk score histogram
        fig.add_trace(
            go.Histogram(
                x=self.applications_df['risk_score'],
                nbinsx=50,
                name='Risk Score',
                marker_color='#e74c3c'
            ),
            row=1, col=1
        )
        
        # Risk category pie chart
        risk_counts = self.applications_df['risk_category'].value_counts()
        colors_risk = {'low': '#27ae60', 'medium': '#f39c12', 'high': '#e74c3c'}
        color_list = [colors_risk.get(cat, '#95a5a6') for cat in risk_counts.index]
        
        fig.add_trace(
            go.Pie(
                labels=risk_counts.index,
                values=risk_counts.values,
                marker=dict(colors=color_list)
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Risk Score", row=1, col=1)
        fig.update_yaxes(title_text="Count", row=1, col=1)
        
        fig.update_layout(
            title_text='Risk Analysis',
            template='plotly_white',
            showlegend=True
        )
        
        fig.write_html('reports/visualizations/risk_distribution.html')
        print("✓ Created: risk_distribution.html")
        
        return fig
    
    def plot_channel_performance(self):
        """Plot channel performance comparison"""
        channel_stats = self.applications_df.groupby('channel').agg({
            'application_id': 'count',
            'application_status': lambda x: (x == 'approved').sum() / len(x) * 100,
            'processing_duration_hours': 'mean',
            'fraud_flag': 'sum'
        }).reset_index()
        channel_stats.columns = ['channel', 'count', 'approval_rate', 'avg_processing', 'fraud_count']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Applications by Channel',
                'Approval Rate by Channel',
                'Avg Processing Time by Channel',
                'Fraud Cases by Channel'
            ),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Applications count
        fig.add_trace(
            go.Bar(x=channel_stats['channel'], y=channel_stats['count'],
                   marker_color='#3498db', name='Applications'),
            row=1, col=1
        )
        
        # Approval rate
        fig.add_trace(
            go.Bar(x=channel_stats['channel'], y=channel_stats['approval_rate'],
                   marker_color='#27ae60', name='Approval Rate'),
            row=1, col=2
        )
        
        # Processing time
        fig.add_trace(
            go.Bar(x=channel_stats['channel'], y=channel_stats['avg_processing'],
                   marker_color='#f39c12', name='Avg Processing'),
            row=2, col=1
        )
        
        # Fraud count
        fig.add_trace(
            go.Bar(x=channel_stats['channel'], y=channel_stats['fraud_count'],
                   marker_color='#e74c3c', name='Fraud Cases'),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text='Channel Performance Analysis',
            template='plotly_white',
            showlegend=False,
            height=800
        )
        
        fig.write_html('reports/visualizations/channel_performance.html')
        print("✓ Created: channel_performance.html")
        
        return fig
    
    def plot_onboarding_funnel(self):
        """Plot onboarding funnel"""
        # Get event counts
        event_counts = self.events_df.groupby('event_type')['application_id'].nunique()
        
        funnel_stages = [
            'application_started',
            'personal_details_completed',
            'document_uploaded',
            'kyc_completed',
            'terms_accepted',
            'account_created'
        ]
        
        stages = []
        counts = []
        
        for stage in funnel_stages:
            if stage in event_counts.index:
                stages.append(stage.replace('_', ' ').title())
                counts.append(event_counts[stage])
        
        fig = go.Figure(go.Funnel(
            y=stages,
            x=counts,
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(
                color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c']
            )
        ))
        
        fig.update_layout(
            title='Onboarding Funnel Analysis',
            template='plotly_white'
        )
        
        fig.write_html('reports/visualizations/onboarding_funnel.html')
        print("✓ Created: onboarding_funnel.html")
        
        return fig
    
    def plot_hourly_pattern(self):
        """Plot hourly application pattern"""
        self.applications_df['hour'] = pd.to_datetime(
            self.applications_df['application_date']
        ).dt.hour
        
        hourly_counts = self.applications_df['hour'].value_counts().sort_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=hourly_counts.index,
            y=hourly_counts.values,
            marker=dict(
                color=hourly_counts.values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Applications")
            ),
            text=hourly_counts.values,
            textposition='outside'
        ))
        
        fig.update_layout(
            title='Application Volume by Hour of Day',
            xaxis_title='Hour of Day',
            yaxis_title='Number of Applications',
            template='plotly_white',
            xaxis=dict(tickmode='linear', tick0=0, dtick=1)
        )
        
        fig.write_html('reports/visualizations/hourly_pattern.html')
        print("✓ Created: hourly_pattern.html")
        
        return fig
    
    def plot_geographic_distribution(self):
        """Plot applications by state"""
        state_counts = self.applications_df['state'].value_counts().head(15)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=state_counts.index,
            x=state_counts.values,
            orientation='h',
            marker=dict(color='#3498db'),
            text=state_counts.values,
            textposition='outside'
        ))
        
        fig.update_layout(
            title='Top 15 States by Application Volume',
            xaxis_title='Number of Applications',
            yaxis_title='State',
            template='plotly_white',
            height=600
        )
        
        fig.write_html('reports/visualizations/geographic_distribution.html')
        print("✓ Created: geographic_distribution.html")
        
        return fig
    
    def create_dashboard_summary(self):
        """Create a comprehensive dashboard with key metrics"""
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=(
                'Status Distribution',
                'Risk Categories',
                'Channel Distribution',
                'Daily Applications (7-day MA)',
                'Processing Time Box Plot',
                'KYC Success by Document',
                'Approval Rate Trend',
                'Fraud Rate by Risk',
                'Top Failure Reasons'
            ),
            specs=[
                [{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}],
                [{'type': 'scatter'}, {'type': 'box'}, {'type': 'bar'}],
                [{'type': 'scatter'}, {'type': 'bar'}, {'type': 'bar'}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Row 1: Pie charts
        # Status
        status_counts = self.applications_df['application_status'].value_counts()
        fig.add_trace(
            go.Pie(labels=status_counts.index, values=status_counts.values, hole=0.3),
            row=1, col=1
        )
        
        # Risk
        risk_counts = self.applications_df['risk_category'].value_counts()
        fig.add_trace(
            go.Pie(labels=risk_counts.index, values=risk_counts.values, hole=0.3),
            row=1, col=2
        )
        
        # Channel
        channel_counts = self.applications_df['channel'].value_counts()
        fig.add_trace(
            go.Pie(labels=channel_counts.index, values=channel_counts.values, hole=0.3),
            row=1, col=3
        )
        
        # Row 2
        # Daily trend
        daily_counts = self.applications_df.groupby('date').size().reset_index(name='count')
        daily_counts['ma7'] = daily_counts['count'].rolling(window=7).mean()
        fig.add_trace(
            go.Scatter(x=daily_counts['date'], y=daily_counts['ma7'], mode='lines'),
            row=2, col=1
        )
        
        # Processing time box plot
        for status in ['approved', 'rejected', 'pending']:
            data = self.applications_df[
                self.applications_df['application_status'] == status
            ]['processing_duration_hours'].dropna()
            fig.add_trace(
                go.Box(y=data, name=status),
                row=2, col=2
            )
        
        # KYC success
        kyc_success = self.kyc_df.groupby('document_type').apply(
            lambda x: (x['verification_status'] == 'verified').sum() / len(x) * 100
        )
        fig.add_trace(
            go.Bar(x=kyc_success.index, y=kyc_success.values),
            row=2, col=3
        )
        
        fig.update_layout(
            title_text='Customer Onboarding Analytics Dashboard',
            template='plotly_white',
            height=1400,
            showlegend=False
        )
        
        fig.write_html('reports/visualizations/dashboard_summary.html')
        print("✓ Created: dashboard_summary.html")
        
        return fig
    
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("\n" + "="*80)
        print("GENERATING VISUALIZATIONS")
        print("="*80 + "\n")
        
        self.plot_daily_applications()
        self.plot_status_distribution()
        self.plot_processing_time_distribution()
        self.plot_kyc_success_rates()
        self.plot_risk_distribution()
        self.plot_channel_performance()
        self.plot_onboarding_funnel()
        self.plot_hourly_pattern()
        self.plot_geographic_distribution()
        self.create_dashboard_summary()
        
        print("\n✅ All visualizations generated successfully!")
        print("📁 Saved to: reports/visualizations/")


def main():
    """Main execution"""
    print("="*80)
    print("CUSTOMER ONBOARDING ANALYTICS - VISUALIZATION MODULE")
    print("="*80)
    
    # Load data
    print("\nLoading data...")
    applications_df = pd.read_csv('data/raw/applications.csv')
    kyc_df = pd.read_csv('data/raw/kyc_verifications.csv')
    events_df = pd.read_csv('data/raw/onboarding_events.csv')
    
    print(f"✓ Loaded {len(applications_df):,} applications")
    print(f"✓ Loaded {len(kyc_df):,} KYC verifications")
    print(f"✓ Loaded {len(events_df):,} onboarding events")
    
    # Create visualizations
    visualizer = OnboardingVisualizer(applications_df, kyc_df, events_df)
    visualizer.generate_all_visualizations()


if __name__ == "__main__":
    main()