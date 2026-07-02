"""
Synthetic Banking Dataset Generator

This script generates synthetic banking documents for the AION AI Factory
project. The generated documents are used to populate the RAG knowledge base
for testing retrieval, semantic search, and question answering.

Author: AION Team
"""

import os
import random

OUTPUT_DIR = "documents"

# -------------------------------------------------------------------
# Synthetic Bank Profile
# -------------------------------------------------------------------

BANK = {
    "name": "AION Bank",
    "country": "Pakistan",
    "currency": "PKR",
    "regulator": "State Bank of Pakistan (SBP)",
    "website": "www.aionbank.pk",
    "customer_care": "111-111-111",
    "email": "support@aionbank.pk",
}

# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------

def clear_category(category: str):
    """
    Deletes all generated documents from a category.
    """

    folder = os.path.join(OUTPUT_DIR, category)

    if not os.path.exists(folder):
        return

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            os.remove(os.path.join(folder, file))

    print(f"Cleaned: {folder}")


def save_document(category: str, filename: str, content: str):
    output_path = os.path.join(OUTPUT_DIR, category, filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content.strip())

    print(f"Generated: {output_path}")


# -------------------------------------------------------------------
# CBS Generator
# -------------------------------------------------------------------

def generate_cbs_documents(count: int):

    document_types = [
        "Savings Account Policy",
        "Current Account Policy",
        "Dormant Account Policy",
        "Joint Account Policy",
        "Minimum Balance Policy",
        "Cheque Book Policy",
        "KYC Verification Policy",
        "Account Opening Guidelines",
        "Account Closure Policy",
        "Nomination Facility Policy",
    ]

    for i in range(1, count + 1):

        title = random.choice(document_types)

        minimum_balance = random.choice([5000, 10000, 25000])
        interest_rate = random.choice([8.5, 9.0, 9.5, 10.0])
        atm_limit = random.choice([50000, 75000, 100000])

        content = f"""
Title: {title}

Bank:
{BANK['name']}

Country:
{BANK['country']}

Currency:
{BANK['currency']}

Regulator:
{BANK['regulator']}

Purpose:
This document defines the operational procedures and customer policies related to {title.lower()}.

Minimum Initial Deposit:
PKR {minimum_balance}

Minimum Monthly Balance:
PKR {minimum_balance}

Annual Profit Rate:
{interest_rate}%

ATM Withdrawal Limit:
PKR {atm_limit} per day

Customer Care:
{BANK['customer_care']}

Email:
{BANK['email']}

Website:
{BANK['website']}
"""

        filename = (
            title.lower()
            .replace(" ", "_")
            .replace("/", "")
            + f"_{i}.txt"
        )

        save_document("cbs", filename, content)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main():

    print("=" * 60)
    print(f"Generating synthetic dataset for {BANK['name']}")
    print("=" * 60)

    clear_category("cbs")

    generate_cbs_documents(10)

    print("\nDataset generation completed successfully.")


if __name__ == "__main__":
    main()