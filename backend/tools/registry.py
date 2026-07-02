"""Tool registry — exposes banking tools for agent frameworks and MCP."""

import json
from typing import Any, Callable

from backend.tools.calculator import calculate_ratios
from backend.tools.sector_signal import get_sector_signal
from backend.tools.transaction import get_transactions

ToolFn = Callable[..., dict[str, Any]]

TOOL_REGISTRY: dict[str, ToolFn] = {
    "calculate_ratios": calculate_ratios,
    "get_transactions": get_transactions,
    "get_sector_signal": get_sector_signal,
}

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "calculate_ratios",
        "description": (
            "Calculate SME banking ratios: current ratio, debt service coverage, "
            "profit margin, and debt-to-income."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "revenue": {"type": "number"},
                "net_income": {"type": "number"},
                "total_debt": {"type": "number"},
                "current_assets": {"type": "number"},
                "current_liabilities": {"type": "number"},
                "interest_expense": {"type": "number"},
            },
            "required": [
                "revenue", "net_income", "total_debt",
                "current_assets", "current_liabilities", "interest_expense",
            ],
        },
    },
    {
        "name": "get_transactions",
        "description": "Retrieve synthetic SME transaction history and cash-flow summary.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "months": {"type": "integer", "default": 3},
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "get_sector_signal",
        "description": "Get sector economic deterioration signal for risk assessment.",
        "parameters": {
            "type": "object",
            "properties": {"sector": {"type": "string"}},
            "required": ["sector"],
        },
    },
]


def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Execute a registered tool by name with JSON-serializable arguments."""
    fn = TOOL_REGISTRY.get(name)
    if not fn:
        return {"error": f"Unknown tool: {name}"}
    try:
        return fn(**arguments)
    except Exception as exc:
        return {"error": str(exc)}


def list_tools() -> list[dict[str, Any]]:
    """Return tool schemas for agent binding."""
    return TOOL_SCHEMAS


def tools_as_mcp_manifest() -> dict[str, Any]:
    """MCP-compatible tool manifest for protocol integration."""
    return {
        "protocol": "mcp",
        "version": "1.0",
        "tools": [
            {"name": s["name"], "description": s["description"], "inputSchema": s["parameters"]}
            for s in TOOL_SCHEMAS
        ],
    }


def format_tool_result(name: str, result: dict[str, Any]) -> str:
    """Format tool output for LLM context injection."""
    return f"[Tool: {name}]\n{json.dumps(result, indent=2)}"
