from ingest import load_documents, chunk_text

import ollama  # type: ignore


def generate_embeddings(documents):
    """
    Generate embeddings for every chunk of every document.

    Returns:
        [
            {
                "embedding": [...],
                "text": "...",
                "filename": "...",
                "category": "..."
            }
        ]
    """

    embedded_chunks = []

    for document in documents:

        chunks = chunk_text(document["text"])

        for chunk in chunks:

            response = ollama.embeddings(
                model="nomic-embed-text:latest",
                prompt=chunk
            )

            embedded_chunks.append(
                {
                    "embedding": response["embedding"],
                    "text": chunk,
                    "filename": document["filename"],
                    "category": document["category"],
                }
            )

    return embedded_chunks


if __name__ == "__main__":

    documents = load_documents()

    embedded_chunks = generate_embeddings(documents)

    print(f"\nGenerated {len(embedded_chunks)} embeddings.\n")

    if embedded_chunks:

        print("First embedding dimension:")
        print(len(embedded_chunks[0]["embedding"]))

        print("\nExample Metadata:")
        print(f"Filename : {embedded_chunks[0]['filename']}")
        print(f"Category : {embedded_chunks[0]['category']}")

        print("\nChunk Preview:")
        print(embedded_chunks[0]["text"][:100], "...")