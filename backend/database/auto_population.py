import os


mock_data = {
    "data/policies": {
        "aml_kyc_policy_2026.txt": """Document ID: POL-AML-004
Title: Anti-Money Laundering (AML) & Know Your Customer (KYC) Compliance Policy
Effective Date: January 1, 2026

1. Purpose
The purpose of this policy is to establish the minimum standards for preventing the bank's products and services from being used for money laundering or terrorist financing. This policy aligns with the FATF recommendations and local Central Bank regulatory frameworks.

2. Customer Due Diligence (CDD)
All new retail and corporate accounts must undergo strict CDD procedures prior to activation. 
- Retail Customers: Must provide a valid National ID, proof of address (utility bill within the last 3 months), and a declaration of the source of funds.
- Corporate Customers: Must provide a valid Commercial Registration (CR), Memorandum of Association, and identification for all Ultimate Beneficial Owners (UBOs) holding more than 10% equity.

3. Enhanced Due Diligence (EDD)
EDD is required for Politically Exposed Persons (PEPs) and cross-border correspondent banking relationships. EDD requires approval from the Chief Risk Officer (CRO). Transactions exceeding 10,000 BHD (or equivalent in foreign currency) require automated flagging and manual review by the compliance team within 24 hours.""",
        "data_privacy_guidelines.txt": """All customer interactions via the AI assistant must comply with local data protection laws. PII (Personally Identifiable Information) must be masked before being logged in the PostgreSQL database."""
    },
    "data/complaints": {
        "dispute_ticket_88392.txt": """Ticket ID: TKT-88392
Date: July 2, 2026
Customer: Ahmed Al-Farsi
Account Ending In: 4092
Category: Transaction Dispute

Message:
I am writing to formally dispute an unauthorized charge on my Platinum Credit Card. On June 30th, a charge of 450 BHD was processed by a merchant named "TechStore Online", which I did not authorize. I was traveling and my card was in my possession the entire time. I immediately froze the card via the mobile app, but the transaction still went through from pending to posted. 

I expect a provisional credit to be applied to my account while this is investigated, as per the standard customer protection guidelines. Please contact me at my registered mobile number between 4 PM and 6 PM to resolve this."""
    },
    "data/faqs": {
        "retail_faq_q3.txt": """Category: Retail Banking & Personal Finance FAQs

Q: What are the eligibility requirements for the Sharia-compliant Murabaha Auto Finance?
A: To be eligible for the Murabaha Auto Finance, applicants must be at least 21 years old, have a minimum monthly salary of 800 BHD, and have been employed at their current company for a minimum of 6 months. The maximum financing tenure is 72 months.

Q: How do I update my registered mobile number?
A: For security reasons, updating your registered mobile number cannot be done entirely online. You must visit a physical branch with your original National ID or use one of our Smart ATMs equipped with biometric fingerprint authentication.

Q: Are there fees for international ATM withdrawals?
A: Yes. For Standard accounts, international withdrawals incur a flat fee of 2.5 BHD plus a 2% foreign exchange markup. Wealth Management and Private Banking tier clients enjoy fee-free international withdrawals, subject only to the Visa/Mastercard exchange rate."""
    },
    "data/internal_docs": {
        "aion_architecture_memo.txt": """Memo: AION AI Factory Architecture Update
Date: June 28, 2026
Subject: Vector Database Transition

This document outlines the architectural shift for the AION AI Factory conversational assistant. To improve retrieval latency for our growing repository of unstructured banking data, the core vector storage has been transitioned from the pgvector extension in PostgreSQL to a dedicated Qdrant instance. 

PostgreSQL will remain the primary relational database for managing user session states, chat history, and RBAC (Role-Based Access Control) configurations. The RAG ingestion pipeline has been updated to generate embeddings using our locally served models and upsert the resulting vectors directly into Qdrant collections mapped by document type (e.g., 'policies', 'faqs')."""
    }
}

def populate_folders(base_path="./"):
    print("Starting document population...")
    for folder, files in mock_data.items():
        folder_path = os.path.join(base_path, folder)
        
       
        os.makedirs(folder_path, exist_ok=True)
        
        for file_name, content in files.items():
            file_path = os.path.join(folder_path, file_name)
            
            # Write the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            print(f"Created: {file_path}")
            
    print("Population complete. Ready for RAG ingestion pipeline.")

if __name__ == "__main__":
    populate_folders()
