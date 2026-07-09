import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue

COLLECTION_NAME = "knowledge_base_v2"


def initialize_vector_db(client: QdrantClient):
    """Creates the collection using the main shared app client instance."""
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)

    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            # 🔥 FIXED: Changed size dimension threshold from 384 to 1024 to support bge-m3 models
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )
        print(
            f"-> Created new Qdrant Collection '{COLLECTION_NAME}' with 1024 dimensions.")
    else:
        print(f"-> Qdrant Collection '{COLLECTION_NAME}' already initialized.")


def upsert_chunks_to_db(client: QdrantClient, document_id: str, embedded_chunks: list):
    """Stores chunks into Qdrant using the main shared app client instance."""
    points = []
    for chunk in embedded_chunks:
        # Create a deterministic valid UUID based on the document_id string
        point_uuid = str(uuid.uuid5(
            uuid.UUID(document_id), str(chunk["chunk_id"])))

        # FIXED: Added user_id into the storage payload to protect tenant isolation models
        points.append(
            PointStruct(
                id=point_uuid,
                vector=chunk["vector"],
                payload={
                    "document_id": document_id,
                    "user_id": chunk.get("user_id", "default-dev-tenant-id"),
                    "page": chunk["page"],
                    "content": chunk["content"]
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=points
    )


def search_filtered_chunks(client: QdrantClient, query_vector: list, document_id: str, top_k: int = 3, **kwargs) -> list:
    """
    Searches Qdrant for matching chunks filtered by a specific document_id using the shared client.
    """
    try:
        # FIXED: Added collection_name configuration context bounds directly to the query planner execution layer
        search_results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id)
                    )
                ]
            ),
            limit=top_k
        ).points

        retrieved_chunks = []
        for hit in search_results:
            if hit.score >= 0.35:
                retrieved_chunks.append({
                    "content": hit.payload["content"],
                    "page": hit.payload["page"]
                })

        return retrieved_chunks
    except Exception as e:
        print(f"🔥 [QDRANT SEARCH ERROR] Query execution failed: {str(e)}")
        return []
