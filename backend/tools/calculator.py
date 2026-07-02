"""Banking ratio calculator tool."""

from typing import Any


def calculate_ratios(
    revenue: float,
    net_income: float,
    total_debt: float,
    current_assets: float,
    current_liabilities: float,
    interest_expense: float,
) -> dict[str, Any]:
    """
    Compute key SME credit ratios from financial inputs.

    Returns ratio values with interpretation flags for risk monitoring.
    """
    current_ratio = current_assets / current_liabilities if current_liabilities else 0.0
    debt_service_coverage = (
        net_income / interest_expense if interest_expense else 0.0
    )
    profit_margin = (net_income / revenue * 100) if revenue else 0.0
    debt_to_income = (total_debt / net_income) if net_income else 0.0

    flags: list[str] = []
    if current_ratio < 1.0:
        flags.append("low_liquidity")
    if debt_service_coverage < 1.25:
        flags.append("weak_debt_service")
    if profit_margin < 5.0:
        flags.append("thin_margins")

    return {
        "current_ratio": round(current_ratio, 2),
        "debt_service_coverage": round(debt_service_coverage, 2),
        "profit_margin_pct": round(profit_margin, 2),
        "debt_to_income": round(debt_to_income, 2),
        "risk_flags": flags,
        "risk_level": "high" if len(flags) >= 2 else "medium" if flags else "low",
    }


CALCULATOR_TOOL_SCHEMA = {
    "name": "calculate_ratios",
    "description": (
        "Calculate SME banking ratios: current ratio, debt service coverage, "
        "profit margin, and debt-to-income from financial inputs."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "revenue": {"type": "number", "description": "Annual revenue"},
            "net_income": {"type": "number", "description": "Net income"},
            "total_debt": {"type": "number", "description": "Total outstanding debt"},
            "current_assets": {"type": "number", "description": "Current assets"},
            "current_liabilities": {"type": "number", "description": "Current liabilities"},
            "interest_expense": {"type": "number", "description": "Annual interest expense"},
        },
        "required": [
            "revenue",
            "net_income",
            "total_debt",
            "current_assets",
            "current_liabilities",
            "interest_expense",
        ],
    },
}
