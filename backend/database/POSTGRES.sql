/* ============================================================================
   AION AI Factory - PostgreSQL Core Relational Schema (Qdrant Hybrid Setup)
   ============================================================================
   In this architecture, PostgreSQL is stripped of pgvector. It focuses entirely
   on ACID-compliant relational data, relational metadata, and message tracking.
   ============================================================================ */

-- ============================================================================
-- INITIALIZATION & SCHEMA CREATION
-- ============================================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS bank_knowledge;  
CREATE SCHEMA IF NOT EXISTS bank_operations; 
CREATE SCHEMA IF NOT EXISTS agent_memory;    

-- ============================================================================
-- ROLES & PERMISSIONS
-- ============================================================================
CREATE ROLE aion_reader WITH LOGIN PASSWORD 'reader_secure_password_2026';
CREATE ROLE aion_ingest WITH LOGIN PASSWORD 'ingest_secure_password_2026';

GRANT USAGE ON SCHEMA bank_knowledge TO aion_reader;
GRANT USAGE ON SCHEMA bank_knowledge TO aion_ingest;
GRANT USAGE ON SCHEMA bank_operations TO aion_ingest;

ALTER DEFAULT PRIVILEGES IN SCHEMA bank_knowledge GRANT SELECT ON TABLES TO aion_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA bank_knowledge GRANT ALL PRIVILEGES ON TABLES TO aion_ingest;
ALTER DEFAULT PRIVILEGES IN SCHEMA bank_operations GRANT ALL PRIVILEGES ON TABLES TO aion_ingest;

-- ============================================================================
-- 1. BANK KNOWLEDGE SCHEMA (Metadata Tracking for RAG)
-- ============================================================================
CREATE TABLE IF NOT EXISTS bank_knowledge.source_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    source_url TEXT,
    category TEXT NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS bank_knowledge.document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_document_id UUID REFERENCES bank_knowledge.source_documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    metadata JSONB 
);

-- ============================================================================
-- 2. BANK OPERATIONS SCHEMA (Core Relational Banking)
-- ============================================================================
CREATE TABLE IF NOT EXISTS bank_operations.customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    tier TEXT DEFAULT 'standard',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bank_operations.accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL REFERENCES bank_operations.customers(id) ON DELETE RESTRICT,
    account_type TEXT NOT NULL,
    balance NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'USD',
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bank_operations.transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID NOT NULL REFERENCES bank_operations.accounts(id) ON DELETE RESTRICT,
    amount NUMERIC(15, 2) NOT NULL,
    transaction_type TEXT NOT NULL,
    counterparty_info JSONB,
    status TEXT DEFAULT 'completed',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_accounts_customer ON bank_operations.accounts(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_account ON bank_operations.transactions(account_id);

-- ============================================================================
-- 3. AGENT MEMORY SCHEMA (Conversation State Tracking)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agent_memory.conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES bank_operations.customers(id) ON DELETE SET NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE,
    summary TEXT 
);

CREATE TABLE IF NOT EXISTS agent_memory.messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES agent_memory.conversations(id) ON DELETE CASCADE,
    sender TEXT NOT NULL, 
    content TEXT NOT NULL,
    tokens_used INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_messages_conversation ON agent_memory.messages(conversation_id, created_at ASC);
