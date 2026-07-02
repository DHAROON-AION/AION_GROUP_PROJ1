"""Sector economic signal tool for risk monitoring."""

from typing import Any

SECTOR_SIGNALS: dict[str, dict[str, Any]] = {
    "retail": {
        "sector": "Retail",
        "outlook": "deteriorating",
        "signal_score": 0.72,
        "key_risk": "Declining consumer spending and rising inventory costs",
        "provision_recommendation": "review",
    },
    "construction": {
        "sector": "Construction",
        "outlook": "stable",
        "signal_score": 0.45,
        "key_risk": "Material cost volatility",
        "provision_recommendation": "maintain",
    },
    "hospitality": {
        "sector": "Hospitality",
        "outlook": "improving",
        "signal_score": 0.28,
        "key_risk": "Seasonal revenue concentration",
        "provision_recommendation": "maintain",
    },
    "manufacturing": {
        "sector": "Manufacturing",
        "outlook": "deteriorating",
        "signal_score": 0.68,
        "key_risk": "Supply chain disruption and export demand slowdown",
        "provision_recommendation": "increase_monitoring",
    },
    "technology": {
        "sector": "Technology",
        "outlook": "stable",
        "signal_score": 0.38,
        "key_risk": "Competitive pricing pressure",
        "provision_recommendation": "maintain",
    },
}


def get_sector_signal(sector: str) -> dict[str, Any]:
    """Return macro sector deterioration signal for SME risk assessment."""
    key = sector.lower().strip()
    signal = SECTOR_SIGNALS.get(key)
    if not signal:
        return {
            "sector": sector,
            "found": False,
            "message": f"No sector signal available for '{sector}'.",
            "available_sectors": list(SECTOR_SIGNALS.keys()),
        }
    return {"found": True, **signal}


SECTOR_SIGNAL_TOOL_SCHEMA = {
    "name": "get_sector_signal",
    "description": "Get economic deterioration signal and risk outlook for a business sector.",
    "parameters": {
        "type": "object",
        "properties": {
            "sector": {
                "type": "string",
                "description": "Business sector: retail, construction, hospitality, manufacturing, technology",
            },
        },
        "required": ["sector"],
    },
}
