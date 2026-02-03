# A-Decision-Support-Dashboard-for-Estimating-Import-Profit-Margins-for-UK-SMEs
Decision-support dashboard for estimating import profit margins and cost risk for UK SMEs using official HMRC and ONS data.
Project Overview

This project develops an interactive decision-support dashboard designed to help UK small and medium-sized enterprises (SMEs) estimate the profitability of importing goods under uncertain economic conditions. The primary users of the system are accountants, who support SMEs by evaluating import costs, profit margins, and financial risk before purchase decisions are made.

The dashboard enables users to explore how changes in foreign exchange (FX) rates, shipping costs, insurance, and tariffs impact landed costs and profit margins. Rather than attempting to predict future market movements, the system focuses on scenario-based analysis, transparency, and explainability.

Key Features

Landed cost calculation incorporating FX, shipping, insurance, and tariffs

Real-time profit and margin updates based on user inputs

Risk classification with uncertainty awareness

Sensitivity analysis for FX and shipping cost changes

Interactive web-based interface built with Streamlit

Explicit handling of data coverage and reliability

Data Sources

The project integrates official UK government datasets:

HM Revenue & Customs (HMRC) – UK import values by HS commodity codes

Office for National Statistics (ONS) – Trade statistics and commodity coverage data

Bank of England – Exchange rate data (used for simulation scenarios)

All data used in the project is publicly available.

Methodology Summary

Data cleaning and preprocessing using Python

Harmonisation of HS and SITC commodity classification systems

Coverage-based classification to reflect data reliability

Modular implementation of cost, margin, and risk logic

Visualisation and interaction delivered via Streamlit

Repository Structure
fyp-project/
├── app.py                    # Main Streamlit application
├── scripts/                  # Core calculation and data processing modules
├── data/
│   ├── raw/                  # Original HMRC and ONS datasets
│   ├── processed/            # Cleaned and harmonised datasets
│   └── output/               # Aggregated and derived data
├── README.md                 # Project documentation

Running the Application
Requirements

Python 3.9+

streamlit

pandas

numpy

plotly

Setup
pip install -r requirements.txt

Launch
streamlit run app.py


The application will launch locally in your web browser.

Project Status

This repository contains a working prototype developed as part of a BSc (Hons) Data Science and Analytics final year project. Advanced analytics and automated data updates are considered future enhancements and are not required for the current prototype.

Author

Vitharanage Vihanga Sathsara
BSc (Hons) Data Science and Analytics
University of Westminster
