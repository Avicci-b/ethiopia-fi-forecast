# ethiopia-fi-forecast
 A financial inclusion forecasting system
# Ethiopia Financial Inclusion Forecasting

## Project Overview
Forecasting financial inclusion in Ethiopia using time series methods and event impact modeling.

## Project Structure
- `data/raw/`: Original, immutable data
- `data/processed/`: Cleaned, analysis-ready data  
- `notebooks/`: Jupyter notebooks for exploration and analysis
- `src/`: Source code for Python modules
- `dashboard/`: Interactive Streamlit dashboard
- `tests/`: Unit tests
- `models/`: Trained model artifacts
- `reports/figures/`: Generated graphs and visualization

Task 1 is successfully finished with all the enrichment phasese completed. It might be a small sata that I have found and added but all the added data follow the schema perfectly.

# Ethiopia Financial Inclusion Forecasting Dashboard

## 📊 Project Overview
This project develops an interactive dashboard for forecasting Ethiopia's financial inclusion trends, supporting the National Financial Inclusion Strategy (NFIS II) goal of 60% financial inclusion by 2027. The dashboard enables stakeholders to explore historical data, understand event impacts, and view forecasts through an intuitive interface.

## 🎯 Project Requirements (KAIM Task 5)

### **Task 5: Dashboard Development**
**Objective:** Create an interactive dashboard that enables stakeholders to explore the data, understand event impacts, and view forecasts.

#### **1. Dashboard Setup**
- ✅ Built with Streamlit
- ✅ Created dashboard/app.py
- ✅ Clear instructions in README for running locally

#### **2. Dashboard Sections**
- **Overview Page:**
  - Key metrics summary cards (current values, trends)
  - P2P/ATM Crossover Ratio indicator
  - Growth rate highlights
  
- **Trends Page:**
  - Interactive time series plots
  - Date range selector
  - Channel comparison view
  
- **Forecasts Page:**
  - Forecast visualizations with confidence intervals
  - Model selection option
  - Key projected milestones
  
- **Inclusion Projections Page:**
  - Financial inclusion rate projections
  - Progress toward 60% target visualization
  - Scenario selector (optimistic/base/pessimistic)
  - Answers to consortium's key questions

#### **3. Technical Requirements**
- ✅ At least 4 interactive visualizations
- ✅ Clear labels and explanations
- ✅ Data download functionality (ready for implementation)

#### **4. Git Workflow Requirements**
- ✅ Merge branches from task-3 into main using PR
- ✅ Create branch "task-4"
- ✅ Commit work with descriptive commit messages
- ✅ Create working Streamlit application

## 🚀 Quick Start Guide

### **Prerequisites**
- Python 3.8+
- Git
- 4GB RAM minimum
- Modern web browser (Chrome, Firefox, Edge)

### **Installation Steps**

#### **1. Clone the Repository**
```bash
git clone https://github.com/[YOUR_USERNAME]/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast
```

#### **2. Set Up Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

#### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **4. Prepare Data Files**
Ensure your data files are in the correct structure:
```
ethiopia-fi-forecast/
├── data/processed/
│   ├── ethiopia_fi_enriched_combined.csv
│   ├── ethiopia_fi_enriched_sheet1.csv
│   └── ethiopia_fi_enriched_sheet2.csv
└── forecasts/
    ├── account_ownership_forecasts.csv
    └── forecast_summary.csv
```

#### **5. Run the Dashboard**
```bash
streamlit run dashboard/app.py
```

#### **6. Access the Dashboard**
- Open your web browser
- Navigate to: `http://localhost:8501`
- The dashboard will load automatically

## 📱 Dashboard Features

### **1. Overview Page**
- **Key Metrics Cards:** Current account ownership (46%), target (60%), projected growth
- **Historical Trends:** Account ownership over time with target line
- **Growth Analysis:** Annual growth rates and key milestones
- **Insights Panel:** Key findings and recommendations

### **2. Trends Page**
- **Interactive Time Series:** Select indicators, pillars, and gender filters
- **Date Range Selector:** Customize historical analysis period
- **Channel Comparison:** Compare financial service channels
- **Data Table:** View filtered data with sorting options

### **3. Forecasts Page**
- **Multi-Scenario Forecasts:** Base, optimistic, and pessimistic scenarios
- **Confidence Intervals:** 95% confidence bands for predictions
- **Model Comparison:** Compare different forecasting approaches
- **Milestone Tracker:** Key projected milestones and status

### **4. Inclusion Projections Page**
- **Target Progress:** Visual progress toward 60% inclusion target
- **Scenario Analysis:** Toggle between optimistic/base/pessimistic scenarios
- **Gap Analysis:** Years remaining and required growth rates
- **Q&A Section:** Answers to consortium's key questions

## 🛠️ Technical Specifications

### **Architecture**
```
Frontend: Streamlit (Python framework)
Visualization: Plotly (interactive charts)
Data Processing: Pandas, NumPy
Caching: Streamlit caching for performance
```

### **Interactive Visualizations (4+ Required)**
1. **Time Series Plot** with date filtering and hover details
2. **Forecast Chart** with confidence intervals and scenario toggles
3. **Progress Chart** toward 60% target with gap visualization
4. **Comparison Bar Chart** of financial channels
5. **Metric Cards** with dynamic updates



### **Performance Features**
- Data caching with `@st.cache_data`
- Lazy loading of visualizations
- Optimized DataFrame operations
- Responsive design for different screen sizes

## 📁 Project Structure

```
ethiopia-fi-forecast/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── dashboard/                          # Dashboard application
│   ├── app.py                         # Main dashboard application
│   └── assets/                        # Static assets (optional)
├── data/                              # Data directory
│   ├── processed/                     # Processed data files
│   │   ├── ethiopia_fi_enriched_combined.csv
│   │   ├── ethiopia_fi_enriched_sheet1.csv
│   │   └── ethiopia_fi_enriched_sheet2.csv
│   └── raw/                           # Raw data files (gitignored)
├── forecasts/                         # Forecast results
│   ├── account_ownership_forecasts.csv
│   └── forecast_summary.csv
├── notebooks/                         # Jupyter notebooks for analysis
├── src/                               # Source code modules
├── tests/                             # Test files
├── .gitignore                         # Git ignore rules
└── data_enrichment_log.md             # Data processing documentation
```

## 🔧 Troubleshooting

### **Common Issues**

#### **1. "File not found" errors**
```bash
# Check file locations
ls data/processed/
# Ensure CSV files exist in correct locations
```

#### **2. Module import errors**
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

#### **3. Dashboard won't start**
```bash
# Check if port 8501 is in use
lsof -i :8501  # macOS/Linux
# netstat -ano | findstr :8501  # Windows

# Try different port
streamlit run dashboard/app.py --server.port 8502
```

#### **4. No data displayed**
- Check CSV file encoding (should be UTF-8)
- Verify column names match those in app.py
- Check data types in CSV files

### **Debug Mode**
Run with verbose output:
```bash
streamlit run dashboard/app.py --logger.level=debug
```

## 📈 Key Metrics Tracked

### **Primary Indicators**
- Account Ownership Rate (ACC_OWNERSHIP)
- Mobile Money Account Rate
- P2P Transaction Count
- ATM/POS Penetration Rates
- Digital Payment Adoption

### **Forecast Period**
- Historical: 2014-2021
- Forecast: 2025-2027
- Target: 60% by 2027

### **Impact Events Modeled**
- Telebirr mobile money launch (2021)
- Regulatory policy changes
- Digital infrastructure investments
- Financial literacy programs

## 🤝 Contributing

### **Branch Strategy**
1. Main branch: production-ready code
2. Task branches: `task-1`, `task-2`, `task-3`, `task-4`,`dashboard`
3. Feature branches: `feature/[description]`

### **Browser Compatibility**
- ✅ Google Chrome 90+
- ✅ Mozilla Firefox 88+
- ✅ Microsoft Edge 90+
- ✅ Safari 14+

## 📄 Documentation

### **Data Sources**
- Global Findex Database (World Bank)
- National Bank of Ethiopia
- Commercial Bank Reports
- Mobile Network Operator Data

## 🎓 KAIM Project Compliance

### **Completed Requirements**
- [x] Streamlit dashboard with 4 sections
- [x] 4+ interactive visualizations
- [x] Clear labels and explanations
- [x] Data loading and caching
- [x] Interactive controls and filters
- [x] Scenario analysis implementation
- [x] Progress toward target visualization
- [x] Clear run instructions in README
- [x] Proper Git workflow with task-4 branch

### **Next Steps for Enhancement**
1. Add user authentication
2. Implement advanced filtering
3. Add export functionality
4. Include geographic mapping
5. Add real-time data updates

## 📞 Support

### **Project Team**
- **KAIM Trainee:** [Biniyam Mitiku]

### **Technical Support**
For technical issues:
1. Check troubleshooting section
2. Review error messages in terminal
3. Verify file paths and permissions
4. Ensure all dependencies are installed

### **Contact**
- Email: [binattamit@gmail.com]
- KAIM Platform: [https://kaimtenx.10academy.org/trainee/dashboard]

---

**Last Updated:** February 2024  
**Dashboard Version:** 1.0  
**KAIM Task:** Task 5 - Dashboard Development  
**Status:** ✅ Complete & Ready for Review  

---

*This dashboard was developed as part of the KAIM (Knowledge Analytics and Interactive Modeling) project for forecasting Ethiopia's financial inclusion trends. All data is for educational and analytical purposes.*