# Client Wealth Dashboard

Advisor-focused KPI dashboard for net worth monitoring, liquidity analysis, and scenario comparison.

## Features
- KPI snapshot: net worth, liquidity runway, debt-to-asset ratio, savings rate
- Asset mix visualization
- Scenario projection (base vs alternative)
- Net worth delta analysis

## Setup
```bash
git clone https://github.com/john-stromberg/client-wealth-dashboard.git
cd client-wealth-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure
- `app.py` - Streamlit UI
- `calculators/kpis.py` - KPI calculations
- `calculators/scenarios.py` - scenario projection and comparison

## Notes
This MVP is intended for advisory workflow prototyping with mock/simplified assumptions.
