from ingest import load_text, chunk_text

import ollama # type: ignore

def generate_embeddings(chunks):

    embeddings = []

    for chunk in chunks:

        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )

        embeddings.append(response["embedding"])

    return embeddings


if __name__ == "__main__":

    document = load_text("sample.txt")

    chunks = chunk_text(document)

    embeddings = generate_embeddings(chunks)

    print(f"\nGenerated {len(embeddings)} embeddings.\n")

    print("First embedding dimension:")

    print(len(embeddings[0]))