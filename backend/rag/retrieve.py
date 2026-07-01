from langchain_postgres.vectorstores import PGVector
from langchain_community.embeddings import OllamaEmbeddings
from backend.core.config import settings

def get_retriever():
    """Returns a retriever object to be used in LangChain or Agno agents."""
    
    embeddings = OllamaEmbeddings(
        model=settings.EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL
    )

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="bank_knowledge_base",
        connection=settings.DATABASE_URL,
    )
    

    return vector_store.as_retriever(search_kwargs={"k": 4})

def search_knowledge_base(query: str):
    """Utility function to test retrieval manually."""
    retriever = get_retriever()
    results = retriever.invoke(query)
    return results
