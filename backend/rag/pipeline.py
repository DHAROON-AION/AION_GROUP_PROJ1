from ingest import load_documents
from embed import generate_embeddings

import sys
from pathlib import Path

# Add backend folder to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from database.qdrant import create_collection, upload_embeddings


def main():
    print("=" * 60)
    print("AION RAG Pipeline")
    print("=" * 60)

    # Step 1: Load all documents
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.")

    # Step 2: Generate embeddings
    embedded_chunks = generate_embeddings(documents)
    print(f"Generated {len(embedded_chunks)} embeddings.")

    # Step 3: Create collection (if needed)
    create_collection()

    # Step 4: Upload to Qdrant
    upload_embeddings(embedded_chunks)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()