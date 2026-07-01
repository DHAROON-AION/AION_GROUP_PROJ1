-- ============================================================================
-- AION AI Factory - Core Database Initialization
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE SCHEMA IF NOT EXISTS bank_knowledge;  
CREATE SCHEMA IF NOT EXISTS bank_operations; 
CREATE SCHEMA IF NOT EXISTS agent_memory;    =


CREATE ROLE aion_reader WITH LOGIN PASSWORD 'reader_secure_password_2026';
GRANT USAGE ON SCHEMA bank_knowledge TO aion_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA bank_knowledge TO aion_reader;


CREATE ROLE aion_ingest WITH LOGIN PASSWORD 'ingest_secure_password_2026';
GRANT USAGE ON SCHEMA bank_knowledge TO aion_ingest;
GRANT USAGE ON SCHEMA bank_operations TO aion_ingest;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA bank_knowledge TO aion_ingest;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA bank_operations TO aion_ingest;

CREATE TABLE IF NOT EXISTS bank_knowledge.document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(384)
);


CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx 
ON bank_knowledge.document_chunks 
USING hnsw (embedding vector_cosine_ops);
