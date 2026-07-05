import os
import httpx

# --- OPENROUTER EMBEDDINGS ENDPOINT ROUTING ---
OPENROUTER_EMBEDDING_URL = "https://openrouter.ai/api/v1/embeddings"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# We use BAAI's bge-m3 on OpenRouter to keep model parity, or you can use "openai/text-embedding-3-small"
EMBEDDING_MODEL_SLUG = "baai/bge-m3"


async def generate_embeddings_for_chunks(chunks: list) -> list:
    """
    Takes a list of chunk dictionaries, extracts the text content,
    generates vector embeddings via OpenRouter's Cloud API in bulk,
    and maps the vectors back to each object securely.
    """
    if not chunks:
        return []

    if not OPENROUTER_API_KEY:
        print(
            "❌ [CRITICAL ERROR] OPENROUTER_API_KEY is missing from environment variables.")
        return chunks

    # Extract raw text components for bulk batch payload transmission
    texts_to_embed = [chunk["content"] for chunk in chunks]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # OpenRouter handles standard array lists for batch input processing
    payload = {
        "model": EMBEDDING_MODEL_SLUG,
        "input": texts_to_embed
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(OPENROUTER_EMBEDDING_URL, headers=headers, json=payload)

            if response.status_code != 200:
                print(
                    f"🔥 [API EMBEDDING FAULT] OpenRouter responded with status code {response.status_code}: {response.text}")
                return chunks

            response_data = response.json()

            # Map the response float data matrices back onto chunk layout arrays
            # Response format contains a sorted data list: response_data["data"][index]["embedding"]
            for data_item in response_data.get("data", []):
                index = data_item.get("index")
                vector = data_item.get("embedding")
                if index is not None and index < len(chunks):
                    chunks[index]["vector"] = vector

            print(
                f"✅ [SUCCESS] Cloud batch embedding completed for {len(chunks)} chunks.")
            return chunks

    except Exception as e:
        print(
            f"🔥 [CRITICAL API CONNECTION EXCEPTION] Failed to generate cloud embeddings: {str(e)}")
        return chunks
