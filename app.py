"""
Client Wealth Dashboard - Advisor KPI and scenario tool.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from calculators.kpis import (
    asset_mix,
    debt_to_asset_ratio,
    liquidity_runway,
    net_worth,
    savings_rate,
)
from calculators.scenarios import scenario_delta, scenario_projection

st.set_page_config(page_title="Client Wealth Dashboard", page_icon="📊", layout="wide")

st.title("📊 Client Wealth Dashboard")
st.markdown("Advisor-focused KPI monitoring and what-if scenario planning.")

st.sidebar.header("Client Snapshot")

total_assets = st.sidebar.number_input("Total Assets ($)", min_value=0, max_value=100000000, value=2500000, step=50000)
total_liabilities = st.sidebar.number_input("Total Liabilities ($)", min_value=0, max_value=100000000, value=750000, step=25000)
liquid_assets = st.sidebar.number_input("Liquid Assets ($)", min_value=0, max_value=100000000, value=300000, step=10000)
monthly_spend = st.sidebar.number_input("Monthly Spend ($)", min_value=0, max_value=1000000, value=15000, step=500)
monthly_income = st.sidebar.number_input("Monthly Income ($)", min_value=0, max_value=1000000, value=25000, step=500)
monthly_contrib = st.sidebar.number_input("Monthly Contributions ($)", min_value=0, max_value=1000000, value=6000, step=500)

st.sidebar.subheader("Asset Mix Inputs")
equities = st.sidebar.number_input("Equities ($)", min_value=0, max_value=100000000, value=1400000, step=25000)
fixed_income = st.sidebar.number_input("Fixed Income ($)", min_value=0, max_value=100000000, value=700000, step=25000)
alternatives = st.sidebar.number_input("Alternatives ($)", min_value=0, max_value=100000000, value=250000, step=25000)
cash = st.sidebar.number_input("Cash ($)", min_value=0, max_value=100000000, value=150000, step=10000)

if st.sidebar.button("Refresh Dashboard", use_container_width=True):
    nw = net_worth(total_assets, total_liabilities)
    runway = liquidity_runway(liquid_assets, monthly_spend)
    dta = debt_to_asset_ratio(total_liabilities, total_assets)
    sr = savings_rate(monthly_income, monthly_contrib)
    mix = asset_mix(total_assets, equities, fixed_income, alternatives, cash)

    st.session_state.kpis = {
        "net_worth": nw,
        "runway": runway,
        "dta": dta,
        "savings_rate": sr,
        "mix": mix,
    }

if "kpis" in st.session_state:
    k = st.session_state.kpis

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Net Worth", f"${k['net_worth']:,.0f}")
    c2.metric("Liquidity Runway", f"{k['runway']:.1f} months")
    c3.metric("Debt-to-Asset", f"{k['dta']*100:.1f}%")
    c4.metric("Savings Rate", f"{k['savings_rate']*100:.1f}%")

    st.subheader("Asset Allocation Mix")
    mix_df = pd.DataFrame(
        {
            "Bucket": ["Equities", "Fixed Income", "Alternatives", "Cash"],
            "Percent": [
                k["mix"]["equities"] * 100,
                k["mix"]["fixed_income"] * 100,
                k["mix"]["alternatives"] * 100,
                k["mix"]["cash"] * 100,
            ],
        }
    )

    fig = px.pie(mix_df, names="Bucket", values="Percent", title="Portfolio Mix")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Scenario Comparison")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Base Scenario**")
        base_contrib = st.number_input("Base Annual Contribution ($)", min_value=0, max_value=5000000, value=monthly_contrib * 12, step=5000)
        base_return = st.number_input("Base Expected Return (%)", min_value=-20.0, max_value=25.0, value=6.0, step=0.5)
        base_paydown = st.number_input("Base Annual Liability Paydown ($)", min_value=0, max_value=5000000, value=60000, step=5000)

    with col_b:
        st.markdown("**Alternative Scenario**")
        alt_contrib = st.number_input("Alt Annual Contribution ($)", min_value=0, max_value=5000000, value=base_contrib + 12000, step=5000)
        alt_return = st.number_input("Alt Expected Return (%)", min_value=-20.0, max_value=25.0, value=6.5, step=0.5)
        alt_paydown = st.number_input("Alt Annual Liability Paydown ($)", min_value=0, max_value=5000000, value=70000, step=5000)

    years = st.slider("Projection Horizon (Years)", min_value=1, max_value=30, value=10, step=1)

    if st.button("Run Scenario Analysis"):
        base = scenario_projection(
            current_assets=total_assets,
            current_liabilities=total_liabilities,
            annual_contribution=base_contrib,
            expected_return_pct=base_return,
            years=years,
            annual_liability_paydown=base_paydown,
        )

        alt = scenario_projection(
            current_assets=total_assets,
            current_liabilities=total_liabilities,
            annual_contribution=alt_contrib,
            expected_return_pct=alt_return,
            years=years,
            annual_liability_paydown=alt_paydown,
        )

        delta = scenario_delta(base, alt)

        comp_df = pd.DataFrame(
            {
                "Metric": ["Projected Assets", "Projected Liabilities", "Projected Net Worth"],
                "Base": [base["projected_assets"], base["projected_liabilities"], base["projected_net_worth"]],
                "Alternative": [alt["projected_assets"], alt["projected_liabilities"], alt["projected_net_worth"]],
                "Delta (Alt - Base)": [delta["assets_delta"], delta["liabilities_delta"], delta["net_worth_delta"]],
            }
        )

        for col in ["Base", "Alternative", "Delta (Alt - Base)"]:
            comp_df[col] = comp_df[col].map(lambda x: f"${x:,.0f}")

        st.dataframe(comp_df, use_container_width=True)
else:
    st.info("Set inputs and click Refresh Dashboard.")

st.divider()
st.caption("MVP dashboard for advisor workflow prototyping. Not investment advice.")
