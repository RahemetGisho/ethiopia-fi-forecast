# 🇪🇹 Ethiopia Financial Inclusion Forecasting

Forecasting Ethiopia's financial inclusion progress (2025–2027) using time series analysis, event-impact modeling, and an interactive Streamlit dashboard. This project was completed as part of the 10 Academy Artificial Intelligence Mastery Program.

---

# Business Problem

Ethiopia is experiencing rapid growth in digital financial services through initiatives such as Telebirr, M-Pesa, and the National Financial Inclusion Strategy (NFIS-II). Despite this expansion, account ownership increased by only three percentage points between 2021 and 2024.

Financial institutions, policymakers, and development partners need a data-driven system that can:

- Understand the factors driving financial inclusion
- Quantify the impact of policies, infrastructure, and product launches
- Forecast future financial inclusion trends
- Support evidence-based policy and investment decisions

---

# Overview

This project develops an end-to-end financial inclusion forecasting system that:

- Explores and enriches Ethiopia's financial inclusion dataset
- Performs exploratory data analysis to identify trends and gaps
- Models the effects of policy changes, infrastructure investments, and digital financial product launches
- Forecasts financial inclusion indicators for 2025–2027
- Presents findings through an interactive Streamlit dashboard

The forecasting system combines trend regression with an event-impact model calibrated using Ethiopia-specific historical data.

---

# Features

- Financial inclusion data enrichment
- Exploratory data analysis (EDA)
- Event-impact modeling
- Scenario-based forecasting
- Interactive Streamlit dashboard
- Downloadable forecast datasets
- Policy target tracking
- Interactive visualizations

---

# Dashboard Pages

### Overview

- Financial inclusion KPI cards
- Growth rate summaries
- P2P vs ATM transaction comparison
- Mobile money activity metrics

### Trends

- Interactive time-series visualization
- Date range filtering
- Event overlays
- Channel comparison charts

### Forecasts

- Forecasts for 2025–2027
- Trend-only vs event-adjusted models
- Confidence intervals
- Scenario analysis

### Inclusion Projections

- Progress toward financial inclusion targets
- Scenario planning
- Policy insights
- Key recommendations

---

# Dataset

The project uses a unified financial inclusion dataset containing:

- Financial inclusion observations
- Policy and market events
- Event-indicator relationships
- National policy targets

### Data Sources

- World Bank Global Findex
- IMF Financial Access Survey
- National Bank of Ethiopia
- EthSwitch
- Telebirr
- Safaricom M-Pesa Ethiopia
- GSMA
- ITU
- World Bank Open Data

---

# Methodology

## 1. Data Enrichment

Additional indicators were collected from official sources, including:

- Mobile money adoption
- Infrastructure indicators
- Internet penetration
- Electricity access
- Literacy
- Gender gap metrics

---

## 2. Exploratory Data Analysis

Performed:

- Trend analysis
- Growth rate analysis
- Infrastructure analysis
- Correlation analysis
- Data quality assessment
- Event timeline analysis

---

## 3. Event Impact Modeling

Built an event-indicator association model that estimates the influence of:

- Policy reforms
- Product launches
- Infrastructure investments
- Market liberalization

Historical observations were used to calibrate event effects.

---

## 4. Forecasting

Forecasts were generated for:

- Account Ownership Rate (Access)
- Digital Payment Usage (Usage)

Three scenarios were evaluated:

- Optimistic
- Base
- Pessimistic

Forecast horizon:

- 2025
- 2026
- 2027

---

# Technologies Used

- Python
- Pandas
- NumPy
- SciPy
- Plotly
- Streamlit
- Scikit-learn
- Git
- Jupyter Notebook

---

# Project Structure

```text
ethiopia-fi-forecast/
│
├── dashboard/
├── data/
├── models/
├── notebooks/
├── reports/
├── src/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Quick Start

## Clone the repository

```bash
git clone https://github.com/RahemetGisho/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast
```

## Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the dashboard

```bash
streamlit run dashboard/app.py
```

---

# Results

The project provides:

- Financial inclusion trend analysis
- Event impact estimates
- Scenario-based forecasts for 2025–2027
- Interactive policy dashboard
- Downloadable forecast tables
- Evidence-based policy insights

---

# Future Improvements

- Incorporate quarterly financial inclusion data
- Integrate macroeconomic indicators
- Explore advanced forecasting models (Prophet, LSTM)
- Automate data updates from official APIs
- Improve uncertainty estimation
- Add regional-level forecasting

---

# Author

**Rahemet Hussen**

- LinkedIn: https://www.linkedin.com/in/rahemethussen/
- GitHub: https://github.com/RahemetGisho
- Email: gishorahemeth@gmail.com

---

# License

This project was developed for educational purposes as part of the **10 Academy Artificial Intelligence Mastery Program**.
