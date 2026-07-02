"""Chat API — Track C RAG implementation."""

from fastapi import APIRouter
import ollama
from qdrant_client import QdrantClient
from backend.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

client = QdrantClient(host="localhost", port=6333)
TOP_K = 3


def retrieve_and_answer(question: str) -> tuple[str, list[str]]:
    response = ollama.embeddings(model="nomic-embed-text", prompt=question)
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

    prompt = f"""You are an AI banking assistant.
Answer ONLY using the provided context.
If the answer is not in the context, reply exactly:
"I could not find this information in the available banking documents."

Context:
{context}

Question:
{question}

Answer:"""

    answer = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[{"role": "user", "content": prompt}]
    )

    return answer["message"]["content"], sources


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    reply, sources = retrieve_and_answer(request.message)
    return ChatResponse(
        reply=reply,
        sources=sources,
        framework_used=request.agent_framework
    )