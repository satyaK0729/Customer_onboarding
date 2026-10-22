# Automated Customer Onboarding Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-316192)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end analytics solution for monitoring and optimizing digital customer onboarding processes in financial institutions, with focus on KYC compliance, fraud detection, and user experience metrics.

## 🎯 Project Overview

This project implements a comprehensive analytics dashboard for tracking customer onboarding metrics in digital banking and fintech platforms. Built specifically for regulatory compliance and operational efficiency monitoring, it processes large-scale onboarding data to provide actionable insights.

### Key Features

- **Real-time Onboarding Metrics**: Track application status, approval rates, and processing times
- **KYC Compliance Analytics**: Monitor document verification success rates and compliance scores
- **Fraud Risk Assessment**: Identify high-risk applications using ML-based scoring
- **Customer Journey Analysis**: Funnel analysis from application start to account activation
- **Automated Reporting**: Daily/weekly reports with key performance indicators
- **Interactive Dashboards**: Power BI/Tableau visualizations for stakeholder insights

## 🏗️ Architecture

```
┌─────────────────┐
│  Data Sources   │
│  (SQL Database) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ETL Pipeline    │
│ (Python/SQL)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Processing │
│ & Analysis      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Visualization  │
│  Dashboard      │
└─────────────────┘
```

## 📊 Metrics Tracked

### Operational Metrics
- Total applications received
- Applications in progress
- Approval/rejection rates
- Average processing time
- Daily/weekly application trends

### Compliance Metrics
- KYC verification success rate
- Document quality scores
- Regulatory compliance percentage
- Audit trail completeness

### Risk Metrics
- Fraud risk score distribution
- High-risk application flagging
- Identity verification failure reasons
- Duplicate/repeat application detection

### User Experience Metrics
- Drop-off rates by stage
- Time spent per onboarding step
- Mobile vs web completion rates
- Customer satisfaction scores

## 🛠️ Technology Stack

- **Languages**: Python 3.8+, SQL
- **Data Processing**: Pandas, NumPy
- **Statistical Analysis**: SciPy, Statsmodels
- **Machine Learning**: Scikit-learn
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Dashboard**: Power BI / Tableau
- **Database**: PostgreSQL
- **Version Control**: Git

## 📁 Project Structure

```
customer-onboarding-analytics/
│
├── data/
│   ├── raw/                    # Raw data files
│   └── processed/              # Cleaned and processed data
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_statistical_analysis.ipynb
│   ├── 04_risk_modeling.ipynb
│   └── 05_visualization.ipynb
│
├── src/
│   ├── data_processing/
│   │   ├── data_loader.py
│   │   ├── data_cleaner.py
│   │   └── feature_engineering.py
│   ├── analysis/
│   │   ├── metrics_calculator.py
│   │   ├── statistical_tests.py
│   │   └── risk_scorer.py
│   └── visualization/
│       ├── dashboard_builder.py
│       └── report_generator.py
│
├── sql/
│   ├── schema.sql
│   ├── data_extraction.sql
│   └── aggregation_queries.sql
│
├── dashboard/
│   ├── power_bi_dashboard.pbix
│   └── tableau_workbook.twb
│
├── tests/
│   └── test_data_processing.py
│
├── docs/
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── insights_report.pdf
│
├── requirements.txt
├── config.yaml
└── README.md
```

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8 or higher
PostgreSQL 12+
Power BI Desktop / Tableau Desktop
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/customer-onboarding-analytics.git
cd customer-onboarding-analytics
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up database:
```bash
psql -U postgres -f sql/schema.sql
```

5. Configure settings:
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your database credentials
```

### Running the Analysis

1. **Generate Synthetic Data** (for demonstration):
```bash
python src/data_processing/generate_sample_data.py
```

2. **Run ETL Pipeline**:
```bash
python src/data_processing/data_loader.py
python src/data_processing/data_cleaner.py
```

3. **Execute Analysis**:
```bash
python src/analysis/metrics_calculator.py
python src/analysis/risk_scorer.py
```

4. **Generate Reports**:
```bash
python src/visualization/report_generator.py
```

5. **Launch Dashboard**:
- Open `dashboard/power_bi_dashboard.pbix` in Power BI Desktop
- Or open `dashboard/tableau_workbook.twb` in Tableau

## 📈 Sample Insights

### Key Findings from Analysis

1. **Onboarding Efficiency**
   - Average processing time reduced from 5 days to 2.3 days
   - 78% of applications completed within 24 hours
   - Peak application times: 10 AM - 2 PM IST

2. **KYC Compliance**
   - 94% document verification success rate
   - Aadhaar verification: 98% success, PAN: 96% success
   - Top rejection reasons: Poor image quality (45%), Mismatch in details (32%)

3. **Fraud Detection**
   - 3.2% applications flagged as high-risk
   - 87% accuracy in fraud prediction model
   - Common fraud patterns identified and documented

4. **User Experience**
   - 15% drop-off rate at document upload stage
   - Mobile completion rate: 82%, Web: 76%
   - Average user satisfaction: 4.2/5

## 🔍 SQL Queries Used

Key analytical queries include:

- Daily onboarding funnel analysis
- Time-based cohort analysis
- KYC verification success rates by document type
- Risk score distribution analysis
- Geographic distribution of applications
- Device and channel performance metrics

See `sql/` directory for complete query documentation.

## 📊 Dashboard Screenshots

### Main Overview Dashboard
![Dashboard Overview](docs/screenshots/overview_dashboard.png)

### KYC Compliance Metrics
![KYC Metrics](docs/screenshots/kyc_metrics.png)

### Risk Analysis View
![Risk Analysis](docs/screenshots/risk_analysis.png)

## 🧪 Testing

Run tests using pytest:

```bash
pytest tests/ -v
```

## 📚 Documentation

Detailed documentation available in the `docs/` directory:

- **Data Dictionary**: Complete field definitions and data types
- **Methodology**: Statistical methods and analytical approaches
- **Insights Report**: Comprehensive findings and recommendations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Inspired by real-world fintech onboarding challenges
- Built for demonstrating data analytics capabilities in financial services
- Designed with Signzy's digital KYC compliance use cases in mind

## 📞 Contact

For questions or feedback, please open an issue or reach out via email.

---

**Note**: This project uses synthetic data for demonstration purposes. All metrics and insights are illustrative examples.