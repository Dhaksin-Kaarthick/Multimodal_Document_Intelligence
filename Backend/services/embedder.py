from sentence_transformers import SentenceTransformer

# Load the model specified in your roadmap blueprint (loads locally into memory)
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def generate_embeddings_for_chunks(chunks: list) -> list:
    """
    Takes a list of chunk dictionaries, extracts the text content,
    generates vector embeddings for each, and attaches the vector to the object.
    """
    if not chunks:
        return []
        
    # Extract just the raw strings to pass to the model efficiently in bulk
    texts_to_embed = [chunk["content"] for chunk in chunks]
    
    # Generate the vectors
    embeddings = model.encode(texts_to_embed, show_progress_bar=False)
    
    # Map the generated vectors back to their respective chunk objects
    for i, chunk in enumerate(chunks):
        # Convert numpy array vector to a standard Python list of floats
        chunk["vector"] = embeddings[i].tolist()
        
    return chunks