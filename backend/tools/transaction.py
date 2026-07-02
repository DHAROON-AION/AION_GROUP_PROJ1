"""Synthetic SME transaction data tool."""

from typing import Any

# Synthetic transaction data for demo — no real customer data
SME_TRANSACTIONS: dict[str, list[dict[str, Any]]] = {
    "SME-1042": [
        {"date": "2026-06-01", "type": "credit", "amount": 45200, "description": "Customer payment"},
        {"date": "2026-06-05", "type": "debit", "amount": 12800, "description": "Supplier payment"},
        {"date": "2026-06-12", "type": "debit", "amount": 8900, "description": "Payroll"},
        {"date": "2026-06-18", "type": "credit", "amount": 22100, "description": "Customer payment"},
        {"date": "2026-06-22", "type": "debit", "amount": 15600, "description": "Equipment lease"},
        {"date": "2026-06-28", "type": "debit", "amount": 4200, "description": "Utilities"},
    ],
    "SME-2087": [
        {"date": "2026-06-03", "type": "credit", "amount": 18500, "description": "Invoice settlement"},
        {"date": "2026-06-10", "type": "debit", "amount": 9200, "description": "Inventory purchase"},
        {"date": "2026-06-15", "type": "debit", "amount": 3100, "description": "Insurance premium"},
        {"date": "2026-06-20", "type": "debit", "amount": 7800, "description": "Loan repayment"},
        {"date": "2026-06-25", "type": "credit", "amount": 11200, "description": "Customer payment"},
    ],
}


def get_transactions(customer_id: str, months: int = 3) -> dict[str, Any]:
    """
    Retrieve synthetic transaction history for an SME borrower.

    Returns transaction list with cash-flow summary indicators.
    """
    transactions = SME_TRANSACTIONS.get(customer_id, [])
    if not transactions:
        return {
            "customer_id": customer_id,
            "found": False,
            "message": f"No transaction records found for {customer_id}.",
            "transactions": [],
        }

    credits = sum(t["amount"] for t in transactions if t["type"] == "credit")
    debits = sum(t["amount"] for t in transactions if t["type"] == "debit")
    net_flow = credits - debits

    deterioration = net_flow < 0 or (debits / credits > 0.85 if credits else True)

    return {
        "customer_id": customer_id,
        "found": True,
        "period_months": months,
        "transaction_count": len(transactions),
        "total_credits": credits,
        "total_debits": debits,
        "net_cash_flow": net_flow,
        "cash_flow_deteriorating": deterioration,
        "transactions": transactions,
    }


TRANSACTION_TOOL_SCHEMA = {
    "name": "get_transactions",
    "description": "Retrieve synthetic transaction history and cash-flow summary for an SME customer.",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_id": {"type": "string", "description": "SME customer ID e.g. SME-1042"},
            "months": {"type": "integer", "description": "Lookback period in months", "default": 3},
        },
        "required": ["customer_id"],
    },
}
