import ollama
from qdrant_client import QdrantClient

from backend.core.config import get_settings

settings = get_settings()

client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
)

ollama_client = ollama.Client(
    host=settings.ollama_base_url,
)

TOP_K = 3


def ask_question(question: str) -> tuple[str, list[str]]:
    """
    Retrieve relevant context from Qdrant and generate an answer.

    Returns:
        answer (str)
        sources (list[str])
    """

    response = ollama_client.embeddings(
        model="nomic-embed-text:latest",
        prompt=question,
    )

    query_vector = response["embedding"]

    results = client.query_points(
        collection_name="banking_documents",
        query=query_vector,
        limit=TOP_K,
    )

    context = ""
    sources = []

    for point in results.points:
        context += point.payload["text"] + "\n\n"

        source = f"{point.payload['category']}/{point.payload['filename']}"

        if source not in sources:
            sources.append(source)

    prompt = f"""
You are an AI banking assistant.

Use ONLY the information provided in the context.

Answer in 1–3 complete sentences.

Do not answer with only "Yes" or "No".
Explain the answer briefly using the context.

If the answer is not contained in the context, reply exactly:

"I could not find this information in the available banking documents."

Context:
{context}

Question:
{question}

Answer:
"""

    answer = ollama_client.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return answer["message"]["content"], sources


if __name__ == "__main__":
    print(f"Ollama URL : {settings.ollama_base_url}")
    print(f"Qdrant     : {settings.qdrant_host}:{settings.qdrant_port}")

    question = input("\nQuestion: ")

    answer, sources = ask_question(question)

    print("\nAnswer:\n")
    print(answer)

    print("\nSources:")

    for source in sources:
        print(f"- {source}")