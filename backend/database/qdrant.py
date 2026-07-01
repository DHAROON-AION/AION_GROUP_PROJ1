from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(
    host="localhost",
    port=6333,
)

COLLECTION_NAME = "banking_documents"


def create_collection():
    """
    Create the Qdrant collection if it doesn't already exist.
    """

    collections = client.get_collections().collections
    names = [collection.name for collection in collections]

    if COLLECTION_NAME in names:
        print("Collection already exists.")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE,
        ),
    )

    print("Collection created successfully!")


def upload_embeddings(embedded_chunks):
    """
    Upload embedded chunks to Qdrant.

    Each embedded chunk contains:
    - embedding
    - text
    - filename
    - category
    """

    points = []

    for index, item in enumerate(embedded_chunks, start=1):

        points.append(
            PointStruct(
                id=index,
                vector=item["embedding"],
                payload={
                    "text": item["text"],
                    "filename": item["filename"],
                    "category": item["category"],
                    "chunk_number": index,
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(f"Uploaded {len(points)} vectors successfully!")