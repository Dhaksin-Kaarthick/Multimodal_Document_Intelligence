import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> list:
    """
    Opens a PDF file and extracts text page by page.
    Returns a list of dictionaries containing page numbers and text content.
    """
    extracted_data = []
    
    # Open the PDF document
    doc = fitz.open(file_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        extracted_data.append({
            "page": page_num + 1,  # Human-readable 1-based indexing
            "text": text.strip()
        })
        
    doc.close()
    return extracted_data