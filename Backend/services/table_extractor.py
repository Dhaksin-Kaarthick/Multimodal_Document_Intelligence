import pdfplumber


def extract_tables_from_pdf(file_path: str) -> list:
    """
    Extracts tables page-by-page from a PDF and converts rows 
    into a structured string format that can be cleanly embedded.
    """
    extracted_tables_data = []

    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            for table in tables:
                table_text_lines = []
                # Filter out completely empty rows
                valid_rows = [row for row in table if any(
                    cell is not None and str(cell).strip() for cell in row)]

                if not valid_rows:
                    continue

                # Use the first valid row as header options if possible
                headers = [str(cell).strip()
                           if cell else "" for cell in valid_rows[0]]

                # Format each subsequent data row into clear vertical markdown properties
                for row in valid_rows[1:]:
                    row_elements = []
                    for col_idx, cell in enumerate(row):
                        val = str(cell).strip() if cell else "N/A"
                        header_label = headers[col_idx] if col_idx < len(
                            headers) and headers[col_idx] else f"Col_{col_idx+1}"
                        # --- FIX: Format as clear vertical line items ---
                        row_elements.append(f"  - {header_label}: {val}")

                    # Group columns structurally under an explicit entity header
                    entity_name = str(row[0]).strip(
                    ) if row and row[0] else "Unknown Entity"
                    table_text_lines.append(
                        f"\nProperties for {entity_name}:\n" + "\n".join(row_elements))

                if table_text_lines:
                    combined_table_content = f"[Table Data Table Block]\n" + \
                        "\n".join(table_text_lines)
                    extracted_tables_data.append({
                        "page": page_num + 1,
                        "text": combined_table_content
                    })

    return extracted_tables_data
