import ollama
from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6333,
)

question = input("Question: ")

response = ollama.embeddings(
    model="nomic-embed-text",
    prompt=question
)

query_vector = response["embedding"]

results = client.query_points(
    collection_name="banking_documents",
    query=query_vector,
    limit=3,
)

context = ""

for point in results.points:
    context += point.payload["text"] + "\n\n"

prompt = f"""
You are a banking assistant.

Answer ONLY using the information below.

Context:
{context}

Question:
{question}
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

print("\nAnswer:\n")

print(answer["message"]["content"])