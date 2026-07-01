import ollama
from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6333,
)

TOP_K = 3

# -----------------------------
# Get User Question
# -----------------------------

question = input("Question: ")

# -----------------------------
# Generate Query Embedding
# -----------------------------

response = ollama.embeddings(
    model="nomic-embed-text",
    prompt=question
)

query_vector = response["embedding"]

# -----------------------------
# Retrieve Relevant Chunks
# -----------------------------

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

# -----------------------------
# Debug: Show Retrieved Context
# -----------------------------

print("\n" + "=" * 80)
print("CONTEXT SENT TO LLM")
print("=" * 80)
print(context)
print("=" * 80)

# -----------------------------
# Build Prompt
# -----------------------------

prompt = f"""
You are an AI banking assistant.

Answer ONLY using the provided context.

If the answer is not explicitly present in the context, reply exactly:

"I could not find this information in the available banking documents."

Context:
{context}

Question:
{question}

Answer:
"""

# -----------------------------
# Generate Answer
# -----------------------------

answer = ollama.chat(
    model="qwen2.5:1.5b",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)

# -----------------------------
# Display Result
# -----------------------------

print("\nAnswer:\n")
print(answer["message"]["content"])

print("\nSources:")

for source in sources:
    print(f"- {source}")