"""
Scenario analysis helpers for simple what-if planning.
"""


def scenario_projection(
    current_assets: float,
    current_liabilities: float,
    annual_contribution: float,
    expected_return_pct: float,
    years: int,
    annual_liability_paydown: float,
):
    assets = current_assets
    liabilities = current_liabilities

    for _ in range(max(0, years)):
        assets = assets * (1 + expected_return_pct / 100.0) + annual_contribution
        liabilities = max(0.0, liabilities - annual_liability_paydown)

    return {
        "projected_assets": assets,
        "projected_liabilities": liabilities,
        "projected_net_worth": assets - liabilities,
    }


def scenario_delta(base: dict, alt: dict):
    return {
        "assets_delta": alt["projected_assets"] - base["projected_assets"],
        "liabilities_delta": alt["projected_liabilities"] - base["projected_liabilities"],
        "net_worth_delta": alt["projected_net_worth"] - base["projected_net_worth"],
    }
