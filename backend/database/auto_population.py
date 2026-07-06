import os


mock_data = {
    "data/policies": {
        "aml_kyc_policy_2026.txt": """
Document ID: POL-AML-004
Title: Anti-Money Laundering (AML) & Know Your Customer (KYC) Compliance Policy
Effective Date: January 1, 2026

1. Purpose
The purpose of this policy is to establish the minimum standards for preventing the bank's products and services from being used for money laundering or terrorist financing. This policy aligns with the FATF recommendations and local Central Bank regulatory frameworks.

2. Customer Due Diligence (CDD)
All new retail and corporate accounts must undergo strict CDD procedures prior to activation. 
- Retail Customers: Must provide a valid National ID, proof of address (utility bill within the last 3 months), and a declaration of the source of funds.
- Corporate Customers: Must provide a valid Commercial Registration (CR), Memorandum of Association, and identification for all Ultimate Beneficial Owners (UBOs) holding more than 10% equity.

3. Enhanced Due Diligence (EDD)
EDD is required for Politically Exposed Persons (PEPs) and cross-border correspondent banking relationships. EDD requires approval from the Chief Risk Officer (CRO). Transactions exceeding 10,000 BHD (or equivalent in foreign currency) require automated flagging and manual review by the compliance team within 24 hours.
""".strip(),
        
        "corporate_lending_policy.txt": """
Document ID: POL-CRED-012
Title: Commercial & Business Lending Policy Framework
Effective Date: March 15, 2026

1. Objective & Scope
This framework dictates the credit underwriting standards for Small and Medium Enterprises (SMEs) and Corporate clients seeking commercial financing. All facilities must align with the risk appetite set by the Board Risk Committee.

2. Eligibility Criteria for Business Loans
To qualify for a term loan or working capital facility, the applicant business must meet the following baseline conditions:
- Operational History: Minimum of 3 consecutive years of audited financial statements.
- Registration: Must possess an active Commercial Registration (CR) from the Ministry of Industry and Commerce.
- Debt Service Coverage Ratio (DSCR): A minimum historic and projected DSCR of 1.25x.
- Leverage Ratio: Total Debt to Equity ratio must not exceed 3.0x post-financing.

3. Collateral Requirements
- Real Estate: First-degree mortgage on commercial or residential property, valued by an independent bank-approved appraiser at a minimum Loan-to-Value (LTV) of 70%.
- Cash Cover / Fixed Deposits: 100% lien mark on funds held within the bank.
- Personal/Corporate Guarantees: Unconditional and irrevocable joint and several guarantees are mandatory from all partners holding a 20% or greater stake in the legal entity.
""".strip(),
        
        "data_privacy_guidelines.txt": """
All customer interactions via the AI assistant must comply with local data protection laws. PII (Personally Identifiable Information) must be masked before being logged in the PostgreSQL database.
""".strip()
    },
    "data/complaints": {
        "dispute_ticket_88392.txt": """
Ticket ID: TKT-88392
Date: July 2, 2026
Customer: Ahmed Al-Farsi
Account Ending In: 4092
Category: Transaction Dispute

Message:
I am writing to formally dispute an unauthorized charge on my Platinum Credit Card. On June 30th, a charge of 450 BHD was processed by a merchant named "TechStore Online", which I did not authorize. I was traveling and my card was in my possession the entire time. I immediately froze the card via the mobile app, but the transaction still went through from pending to posted. 

I expect a provisional credit to be applied to my account while this is investigated, as per the standard customer protection guidelines. Please contact me at my registered mobile number between 4 PM and 6 PM to resolve this.
""".strip()
    },
    "data/faqs": {
        "retail_faq_q3.txt": """
Category: Retail Banking & Personal Finance FAQs

Q: What are the eligibility requirements for the Sharia-compliant Murabaha Auto Finance?
A: To be eligible for the Murabaha Auto Finance, applicants must be at least 21 years old, have a minimum monthly salary of 800 BHD, and have been employed at their current company for a minimum of 6 months. The maximum financing tenure is 72 months.

Q: How do I update my registered mobile number?
A: For security reasons, updating your registered mobile number cannot be done entirely online. You must visit a physical branch with your original National ID or use one of our Smart ATMs equipped with biometric fingerprint authentication.

Q: Are there fees for international ATM withdrawals?
A: Yes. For Standard accounts, international withdrawals incur a flat fee of 2.5 BHD plus a 2% foreign exchange markup. Wealth Management and Private Banking tier clients enjoy fee-free international withdrawals, subject only to the Visa/Mastercard exchange rate.
""".strip()
    },
    "data/internal_docs": {
        "aion_architecture_memo.txt": """
Memo: AION AI Factory Architecture Update
Date: June 28, 2026
Subject: Vector Database Transition

This document outlines the architectural shift for the AION AI Factory conversational assistant. To improve retrieval latency for our growing repository of unstructured banking data, the core vector storage has been transitioned from the pgvector extension in PostgreSQL to a dedicated Qdrant instance. 

PostgreSQL will remain the primary relational database for managing user session states, chat history, and RBAC (Role-Based Access Control) configurations. The RAG ingestion pipeline has been updated to generate embeddings using our locally served models and upsert the resulting vectors directly into Qdrant collections mapped by document type (e.g., 'policies', 'faqs').
""".strip(),
        
        "treasury_transfer_limits.txt": """
Document ID: REG-OPS-202
Title: Funds Transfer & Daily Transaction Limits Policy
Last Reviewed: May 10, 2026

1. Retail Banking Channels (Daily Aggregate Limits)
Limits are enforced per unique customer profile across digital channels (Mobile Banking and Internet Banking):
- Standard Account Tier: Daily transfer limit of 5,000 BHD. Local Fawri+ transfers are capped at 1,000 BHD per transaction (regulatory cap), while Fawri transfers allow up to the daily aggregate.
- Premium/Platinum Tier: Daily transfer limit of 20,000 BHD.
- Private Banking Tier: Daily transfer limit of 100,000 BHD. Any outbound transfer exceeding 50,000 BHD triggers an automated SMS verification token and a 30-minute cooling-off period for new beneficiaries.

2. Corporate & SME Digital Channels
- Single-Signatory Profiles: Capped at 50,000 BHD per day.
- Multi-Signatory (Matrix Routing): Up to 500,000 BHD per day online, subject to Corporate Governance approval tokens from Maker, Checker, and Authorizer roles.
- Cross-Border SWIFT Transfers: No hard digital cap, but transactions over 250,000 BHD require a scanned supporting document (e.g., commercial invoice or supplier agreement) attached directly via the portal prior to execution.
""".strip()
    }
}

def populate_folders(base_path="./"):
    print("Starting document population with expanded banking entities...")
    for folder, files in mock_data.items():
        folder_path = os.path.join(base_path, folder)
        
       
        os.makedirs(folder_path, exist_ok=True)
        
        for file_name, content in files.items():
            file_path = os.path.join(folder_path, file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created/Updated: {file_path}")
            
    print("\nPopulation complete. Documents successfully loaded into directory structure.")

if __name__ == "__main__":
    populate_folders()
