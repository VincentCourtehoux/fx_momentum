# FX Momentum Strategy Backtest 📉🚀

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Finance](https://img.shields.io/badge/Finance-Quant-green) ![Status](https://img.shields.io/badge/Status-Completed-success)

## Project Overview
This project implements and backtests a Momentum Strategy on the Foreign Exchange (FX) market using Python. The study focuses on a basket of 18 currencies against the USD over a period spanning from 1998 to 2024.

The core objective is to analyze the "Momentum Anomaly" in currency markets and evaluate its robustness across different market regimes, specifically analyzing the structural break caused by the 2008 Global Financial Crisis (GFC).

## Key Features
* **Signal Generation:** Implementation of a 4-day lookback log-return signal (Short-term Momentum).
* **Dynamic Portfolio Construction:** Simulation of 5 distinct currency portfolios.
* **Backtesting Engine:** Monthly rebalancing logic.
* **Regime Analysis:** Comparative performance analysis across three eras:
    * *Pre-2008* 
    * *GFC & Euro Crisis* 
    * *Post-2012* 
* **Statistical Metrics:** Calculation of Sharpe Ratio, Skewness (Crash Risk), and Kurtosis (Fat Tails).

## Repository Structure
```text
├── data/
│   ├── spot_rates.xls       # Historical Spot Rates
│   └── fwd_rates.xlsx       # Historical Forward Rates
├── FX_Momentum_Report.pdf         # Full Academic Report (December 2025)
├── main.py                        # Python Script (Backtest & Visualization)
└── README.md                      # Project Documentation
```

## Key Findings
The analysis reveals a significant decay in raw momentum profitability in the modern era:

* **Pre-2008:** Strong positive returns across all portfolios (Annualized returns ~3-6%).
* **Post-2012:** Structural deterioration of the strategy (Negative returns), highlighting the impact of Central Bank interventions on FX trends.
* **Risk Profile:** The strategy exhibits positive skewness in most baskets, contrasting with the negative skewness typically found in Carry Trades.

## 🛠️ Tech Stack
* **Python** (NumPy, Pandas, SciPy)
* **Visualization:** Plotly (Interactive financial charts)
* **Statistics:** Moments analysis (Skew/Kurtosis), Financial Ratios.

## 👥 Authors
*Project for Université Paris Dauphine - PSL (Master in Finance)*

* Vincent Courtehoux
* Alys Hingant
* Ariles Hireche
* Gianmarco Zuccaroli
* Mehdi Boisdur
