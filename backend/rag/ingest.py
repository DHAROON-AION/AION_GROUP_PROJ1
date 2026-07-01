from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_postgres.vectorstores import PGVector
from backend.core.config import settings

def ingest_documents(docs_dir: str = "documents/"):
    print(f"Loading documents from {docs_dir}...")
    loader = PyPDFDirectoryLoader(docs_dir)
    documents = loader.load()

    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    print(f"Initializing Ollama embeddings with {settings.EMBEDDING_MODEL}...")
    
    embeddings = OllamaEmbeddings(
        model=settings.EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL
    )

    print("Pushing vectors to PostgreSQL...")
    
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="bank_knowledge_base",
        connection=settings.DATABASE_URL,
        use_jsonb=True, 
    )

    vector_store.add_documents(docs)
    print(f"Successfully ingested {len(docs)} document chunks into the database.")

if __name__ == "__main__":
    ingest_documents()
