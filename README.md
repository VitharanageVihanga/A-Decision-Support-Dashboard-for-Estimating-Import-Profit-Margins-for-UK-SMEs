# A Decision Support Dashboard for Estimating Import Profit Margins for UK SMEs

**BSc (Hons) Data Science and Analytics - Final Year Project**  
**Student:** Vitharanage Vihanga Sathsara  
**Institution:** University of Westminster

---

## Overview

This project is an interactive web dashboard that helps UK small and medium-sized enterprises (SMEs) and their accountants estimate the profitability of importing goods. The system calculates landed costs, profit margins, and financial risks by integrating official UK government data (HMRC, ONS, Bank of England).

Instead of predicting future market conditions, the dashboard focuses on scenario-based analysis - allowing users to explore "what if" questions about exchange rates, shipping costs, and tariffs.

---

## Key Features

- **Landed Cost Calculation** - Incorporates foreign exchange rates, shipping, insurance, and tariffs
- **Real-time Profit & Margin Updates** - Results update as users adjust parameters
- **Risk Classification** - Assesses financial risk based on data quality and profit margins
- **Sensitivity Analysis** - Shows how changes in FX rates and costs impact profitability
- **Data Coverage Transparency** - Clearly indicates where data is reliable or limited

---

## Data Sources

All data is publicly available from UK government sources:

- **HM Revenue & Customs (HMRC)** - UK import values by commodity (HS codes)
- **Office for National Statistics (ONS)** - Trade statistics by commodity (SITC codes)
- **Bank of England** - Historical exchange rate data

The project harmonises HMRC's HS classification system with ONS's SITC system to enable integrated analysis.

---

## How It Works

### 1. Data Processing

The system processes and merges HMRC and ONS datasets:

```python
# Extract commodity codes and country data
# Map HS codes to SITC sections
# Calculate data coverage for each commodity
# Output: merged datasets with coverage classifications
```

### 2. Cost Calculation

Landed cost is calculated using:

```
Goods Cost = Import Value × (1 + FX Shock %)
Landed Cost = Goods Cost + Shipping + Insurance + Tariff
Profit = Revenue - Landed Cost
Margin (%) = (Profit / Revenue) × 100
```

### 3. Risk Assessment

Risk is classified based on:
- Data coverage (High/Partial/Low/No coverage)
- Profit margin levels
- Economic uncertainty factors

---

## Installation & Usage

### Requirements

- Python 3.9 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/VitharanageVihanga/A-Decision-Support-Dashboard-for-Estimating-Import-Profit-Margins-for-UK-SMEs.git
cd A-Decision-Support-Dashboard-for-Estimating-Import-Profit-Margins-for-UK-SMEs

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## Project Structure

```
fyp-project/
│
├── app.py                          # Main Streamlit application
│
├── scripts/
│   ├── margin_model.py             # Cost and margin calculations
│   ├── scenario_runner.py          # Sensitivity analysis
│   ├── risk_label.py               # Risk classification
│   ├── data_merge.py               # Data harmonisation pipeline
│   └── ...                         # Other calculation modules
│
├── data/
│   ├── raw/                        # Original HMRC and ONS datasets
│   ├── processed/                  # Cleaned datasets
│   └── output/                     # Merged outputs
│
└── requirements.txt                # Python dependencies
```

---

## Example Use Case

**Scenario:** Importing machinery from Germany

**Inputs:**
- Import value: £50,000
- Revenue target: £70,000
- FX shock: +5%
- Shipping: 8%
- Insurance: 2%
- Tariff: 3%

**Results:**
- Landed cost: £59,325
- Profit: £10,675
- Margin: 15.25%
- Risk: Medium

---

## Technologies Used

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical calculations
- **Plotly** - Interactive visualizations

---

## Limitations

- Uses static datasets (no real-time API integration)
- Simplified cost model (doesn't account for volume discounts, customs delays, etc.)
- Single transaction analysis (not portfolio-level)
- Some commodity categories have limited historical data

---

## Future Enhancements

- Automated data updates via government APIs
- Advanced analytics (trend analysis, forecasting, Value-at-Risk)
- Multi-currency support
- PDF report generation
- Portfolio-level analysis

---

## License

This project is available under the MIT License.

---

## Contact

**GitHub:** [@VitharanageVihanga](https://github.com/VitharanageVihanga)  
**Repository:** [A-Decision-Support-Dashboard-for-Estimating-Import-Profit-Margins-for-UK-SMEs](https://github.com/VitharanageVihanga/A-Decision-Support-Dashboard-for-Estimating-Import-Profit-Margins-for-UK-SMEs)

---

**University of Westminster - BSc Data Science and Analytics Final Year Project**
