"""
KPI calculations for client wealth dashboard.
"""


def net_worth(total_assets: float, total_liabilities: float) -> float:
    return total_assets - total_liabilities


def liquidity_runway(liquid_assets: float, monthly_spend: float) -> float:
    if monthly_spend <= 0:
        return 0.0
    return liquid_assets / monthly_spend


def debt_to_asset_ratio(total_liabilities: float, total_assets: float) -> float:
    if total_assets <= 0:
        return 0.0
    return total_liabilities / total_assets


def savings_rate(monthly_income: float, monthly_contributions: float) -> float:
    if monthly_income <= 0:
        return 0.0
    return monthly_contributions / monthly_income


def asset_mix(total_assets: float, equities: float, fixed_income: float, alternatives: float, cash: float):
    if total_assets <= 0:
        return {
            "equities": 0.0,
            "fixed_income": 0.0,
            "alternatives": 0.0,
            "cash": 0.0,
        }

    return {
        "equities": equities / total_assets,
        "fixed_income": fixed_income / total_assets,
        "alternatives": alternatives / total_assets,
        "cash": cash / total_assets,
    }
