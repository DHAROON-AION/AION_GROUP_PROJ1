import ollama
from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6333,
)

TOP_K = 3


def ask_question(question: str) -> tuple[str, list[str]]:
    """
    Retrieve relevant context from Qdrant and generate an answer.

    Returns:
        answer (str)
        sources (list[str])
    """

    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=question
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

Answer ONLY using the provided context.

If the answer is not contained in the context, reply exactly:

"I could not find this information in the available banking documents."

Context:
{context}

Question:
{question}

Answer:
"""

    answer = ollama.chat(
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

    question = input("Question: ")

    answer, sources = ask_question(question)

    print("\nAnswer:\n")
    print(answer)

    print("\nSources:")

    for source in sources:
        print(f"- {source}")