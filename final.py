import numpy as np
import pandas as pd
import random
import plotly.graph_objects as go
import scipy.stats as stats

# --- DATA LOADING & CLEANING ---

spot_file = r"C:\Users\Vince\OneDrive\Desktop\Finance\Dauphine\International Finance\ASSIGNEMENT\spot_rates.xls"
df_spot = pd.read_excel(spot_file, skiprows=1).set_index("Code")

fwd_file = r"C:\Users\Vince\OneDrive\Desktop\Finance\Dauphine\International Finance\ASSIGNEMENT\fwd_rates.xlsx"
df_fwd = pd.read_excel(fwd_file, skiprows=1).set_index("Code")

mapping_spot_forward = {
    "AUSTDOL(ER)": "TDAUD1M(ER)", "CNDOLLR(ER)": "BBCAD1F(ER)",
    "USEURSP(ER)": "TDEUR1M(ER)", "HUNFORT(ER)": "USHUF1F(ER)",
    "INDRUPE(ER)": "USINR1F(ER)", "JAPAYEN(ER)": "TDJPY1M(ER)",
    "MEXPESO(ER)": "USMXN1F(ER)", "NZDOLLR(ER)": "TDNZD1M(ER)",
    "NORKRON(ER)": "TDNOK1M(ER)", "PHILPES(ER)": "USPHP1F(ER)",
    "POLZLOT(ER)": "TDPLN1M(ER)", "SINGDOL(ER)": "BBSGD1F(ER)",
    "COMRAND(ER)": "TDZAR1M(ER)", "SWEKRON(ER)": "TDSEK1M(ER)",
    "SWISSFR(ER)": "TDCHF1M(ER)", "THABAHT(ER)": "USTHB1F(ER)",
    "GBPOUND(ER)": "TDGBP1M(ER)", "CZECHCM(ER)": "TDCZK1M(ER)"
}

# Currency Conversion to USD Terms
gbp_cols = [col for col in df_spot.columns if (col != 'GBPOUND(ER)' and col != 'USEURSP(ER)')]
for col in gbp_cols:
    df_spot[col] = df_spot[col] / df_spot['GBPOUND(ER)']
df_spot['USEURSP(ER)'] = 1 / df_spot['USEURSP(ER)']
df_spot['GBPOUND(ER)'] = 1 / df_spot['GBPOUND(ER)']

df_fwd['TDAUD1M(ER)'] = 1 / df_fwd['TDAUD1M(ER)']
df_fwd['TDEUR1M(ER)'] = 1 / df_fwd['TDEUR1M(ER)']
df_fwd['TDNZD1M(ER)'] = 1 / df_fwd['TDNZD1M(ER)']
df_fwd['TDGBP1M(ER)'] = 1 / df_fwd['TDGBP1M(ER)']

df_fwd.index = pd.to_datetime(df_fwd.index)
monthly_dates = df_fwd.index
df_spot_monthly = df_spot.reindex(monthly_dates, method='ffill')

all_available = [k for k, v in mapping_spot_forward.items() if v is not None]

# BACKTEST FUNCTION

def backtest_portfolio(currencies):
    n = len(currencies)
    sig_list = []
    
    # 1. Monthly Rebalancing with 4-day looking back signal
    for i in range(1, len(monthly_dates)):
        current_date = monthly_dates[i]
        # Momentum: 4-day window strictly before the rebalancing date
        spot_history = df_spot[df_spot.index < current_date].tail(5)
        if len(spot_history) < 5: continue
        
        row = {'Date': current_date}
        for c in currencies:
            mom = np.log(spot_history[c].iloc[-1] / spot_history[c].iloc[0])
            row[c] = -mom
        sig_list.append(row)
    
    df_sig = pd.DataFrame(sig_list).set_index('Date')
    
    # 2. Performance Calculation (1-month holding period)
    pnl_list = []
    sig_dates = df_sig.index
    for i in range(len(sig_dates) - 1):
        d_start, d_end = sig_dates[i], sig_dates[i+1]
        month_ret = 0
        for c in currencies:
            pos = np.sign(df_sig.loc[d_start, c])
            s_0, s_1 = df_spot_monthly.loc[d_start, c], df_spot_monthly.loc[d_end, c]
            f_0 = df_fwd.loc[d_start, mapping_spot_forward[c]]
            
            # Total Return = Spot Return + Forward Premium (Carry)
            ret = pos * (-np.log(s_1 / s_0) + (np.log(f_0) - np.log(s_0)))
            month_ret += (ret / n)
        pnl_list.append(month_ret)
    
    returns = pd.Series(pnl_list, index=sig_dates[:-1])
    
    # 3. Annualized Metrics
    ann_return = returns.mean() * 12
    ann_vol = returns.std() * np.sqrt(12)
    sharpe = ann_return / ann_vol if ann_vol != 0 else 0
    skew = returns.skew()
    kurt = returns.kurtosis() # Excess Kurtosis
    
    # 4. Sub-samples Analysis
    def sub_perf(series):
        if len(series) < 6: return 0.0
        return round((series.mean() * 12) * 100, 2) # Annualized Return %

    pre_08 = returns[returns.index < '2008-01-01']
    gfc = returns[(returns.index >= '2008-01-01') & (returns.index <= '2012-12-31')]
    post_12 = returns[returns.index > '2012-12-31']
    
    clean_names = [c.replace("(ER)", "") for c in currencies]
    
    return {
        "Return_Ann_%": round(ann_return * 100, 2),
        "Vol_Ann_%": round(ann_vol * 100, 2),
        "Sharpe": round(sharpe, 3),
        "Skewness": round(skew, 3),
        "Kurtosis": round(kurt, 3),
        "Ret_Pre08_%": sub_perf(pre_08),
        "Ret_GFC_%": sub_perf(gfc),
        "Ret_Post12_%": sub_perf(post_12),
        "History": np.exp(returns.cumsum()),
        "Monthly_Returns": returns,
        "Currencies": ", ".join(clean_names)
    }

# --- EXECUTION & PLOTTING ---

# Note: These portfolios were generated randomly as described in the methodology.
# We explicitly define this specific draw here to ensure that running this script
# reproduces the exact tables, figures, and statistical analysis presented in the report.

fixed_draw = [
    ['JAPAYEN(ER)', 'SINGDOL(ER)', 'HUNFORT(ER)', 'NORKRON(ER)', 'CZECHCM(ER)'],
    ['AUSTDOL(ER)', 'USEURSP(ER)', 'MEXPESO(ER)', 'THABAHT(ER)', 'SWEKRON(ER)'],
    ['GBPOUND(ER)', 'INDRUPE(ER)', 'POLZLOT(ER)', 'COMRAND(ER)', 'NZDOLLR(ER)'],
    ['CNDOLLR(ER)', 'PHILPES(ER)', 'SWISSFR(ER)', 'USEURSP(ER)', 'JAPAYEN(ER)'],
    ['THABAHT(ER)', 'SINGDOL(ER)', 'MEXPESO(ER)', 'COMRAND(ER)', 'SWEKRON(ER)']
]

random.seed(None)
results_table = []
fig = go.Figure()

for i, currencies in enumerate(fixed_draw):
    p_name = f"Portfolio {i+1}"
    # Using the fixed draw for reproducibility
    res = backtest_portfolio(currencies) 
    res["Portfolio"] = p_name
    results_table.append(res)
    fig.add_trace(go.Scatter(x=res["History"].index, y=res["History"].values, name=p_name))

# Shading GFC period
fig.add_vrect(x0="2008-01-01", x1="2012-12-31", fillcolor="gray", opacity=0.2, line_width=0,
             annotation_text="GFC & Euro Crisis", annotation_position="top left")

# Shading COVID period
fig.add_vrect(x0="2020-01-01", x1="2021-12-31", fillcolor="grey", opacity=0.15, line_width=0,
             annotation_text="COVID-19 Crisis", annotation_position="top right")

fig.update_layout(title="Strategy Performance Across Portfolios", template="plotly_white",
                  xaxis_title="Year", yaxis_title="Cumulative Return (Log scale)")
fig.show()

# --- DISTRIBUTION PLOT ---

fig_dist = go.Figure()

for res in results_table:
    monthly_rets = res["Monthly_Returns"] 
    
    fig_dist.add_trace(go.Histogram(
        x=monthly_rets,
        name=res["Portfolio"],
        opacity=0.6,
        nbinsx=50,
        histnorm='probability density'
    ))

fig_dist.update_layout(
    title="Return Distributions (Skewness and Kurtosis Analysis)",
    xaxis_title="Monthly Log Returns",
    yaxis_title="Probability Density",
    barmode='overlay',
    template="plotly_white",
    legend=dict(orientation="h", y=-0.2)
)

fig_dist.add_vline(x=0, line_dash="dash", line_color="black")
fig_dist.show()

# Final Dataframe
df_results = pd.DataFrame(results_table).sort_values(by="Sharpe", ascending=False)
cols = ["Portfolio", "Return_Ann_%", "Vol_Ann_%", "Sharpe", "Skewness", "Kurtosis", 
        "Ret_Pre08_%", "Ret_GFC_%", "Ret_Post12_%", "Currencies"]

print(df_results[cols].to_string(index=False))