from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_document_pages(combined_pages: list) -> list:
    """
    Splits text into chunks. Narrative text is split recursively, 
    while structured table lines are preserved as intact atomic chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,       # Slightly increased to safely hold full network tables
        chunk_overlap=100     # Higher overlap preserves numeric boundaries safely
    )

    all_chunks = []
    chunk_counter = 1

    for item in combined_pages:
        page_num = item["page"]
        content = item["text"]

        if not content.strip():
            continue

        # --- FIX: If this block is explicit tabular data, don't chop up individual lines ---
        if "[Table Data]" in content:
            # We treat the table block as a single, solid context chunk so numbers stay grouped
            all_chunks.append({
                "chunk_id": str(chunk_counter),
                "page": page_num,
                "content": content.strip()
            })
            chunk_counter += 1
        else:
            # Normal narrative text gets split gracefully
            page_chunks = text_splitter.split_text(content)
            for chunk_text in page_chunks:
                all_chunks.append({
                    "chunk_id": str(chunk_counter),
                    "page": page_num,
                    "content": chunk_text.strip()
                })
                chunk_counter += 1

    return all_chunks
