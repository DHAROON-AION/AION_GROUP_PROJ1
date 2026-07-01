from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(
    host="localhost",
    port=6333,
)

COLLECTION_NAME = "banking_documents"


def create_collection():

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


def upload_embeddings(chunks, embeddings):

    points = []

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):

        points.append(

            PointStruct(
                id=index,
                vector=embedding,
                payload={
                    "text": chunk,
                    "chunk_number": index,
                    "document": "sample.txt",
                },
            )

        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(f"Uploaded {len(points)} vectors successfully!")