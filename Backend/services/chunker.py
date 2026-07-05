# Make sure the old 'from langchain_text_splitters import ...' line is completely GONE from this file!

def chunk_document_pages(parsed_pages: list, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Takes a list of dictionaries containing page extraction data: [{"page": X, "text": "..."}]
    and recursively creates overlapping string blocks using pure Python logic (0MB RAM footprint).
    """
    final_chunks = []
    chunk_id_counter = 0

    for page_data in parsed_pages:
        page_num = page_data.get("page", 1)
        raw_text = page_data.get("text", "").strip()

        if not raw_text:
            continue

        start_index = 0
        text_length = len(raw_text)

        # Slide a text window across the page string
        while start_index < text_length:
            end_index = start_index + chunk_size
            chunk_content = raw_text[start_index:end_index]

            final_chunks.append({
                "chunk_id": chunk_id_counter,
                "page": page_num,
                "content": chunk_content
            })

            chunk_id_counter += 1

            # Slide forward by chunk_size minus the overlapping context buffer
            start_index += (chunk_size - chunk_overlap)

    return final_chunks
    