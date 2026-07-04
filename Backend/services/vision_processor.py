import io
import os
import fitz  # PyMuPDF
import requests
import base64


def process_standalone_image(file_bytes: bytes) -> str:
    """
    Takes raw image bytes, converts them to Base64, and sends them 
    to gemma3:4b to generate a descriptive summary.
    """
    image_b64 = base64.b64encode(file_bytes).decode('utf-8')

    try:
        ollama_url = os.getenv(
            "OLLAMA_HOST", "http://localhost:11434") + "/api/generate"
        prompt = (
            "Analyze this diagram, mindmap, or chart. Extract all key headers, words, "
            "metrics, and connected nodes so this text can be indexed for semantic vector search."
        )

        payload = {
            "model": "gemma3:4b",  # Ensure this matches your downloaded model
            "prompt": prompt,
            "images": [image_b64],
            "stream": False
        }

        # Optimized timeout to prevent the server thread from locking up indefinitely
        response = requests.post(ollama_url, json=payload, timeout=120)

        if response.status_code == 400:
            return "[Vision processing bypassed: Text-only model active or image payload rejected by Ollama]"

        if response.status_code != 200:
            return f"[Vision processing skipped due to Ollama error status {response.status_code}]"

        return response.json().get("response", "").strip()

    except requests.exceptions.Timeout:
        print("-> WARNING: Ollama vision generation timed out.")
        return "[Image file indexed without description due to processing timeout]"
    except requests.exceptions.ConnectionError:
        print("-> ERROR: Cannot reach local Ollama daemon.")
        return "[Image file indexed without description because local Ollama server was unreachable]"
    except Exception as e:
        print(f"-> Standalone vision processing error: {e}")
        return f"[Image analysis skipped due to system error: {str(e)}]"


def process_pdf_images(file_path: str) -> list:
    """
    Extracts images from a PDF page-by-page, sends them to Ollama's 
    vision model for description, and returns text records for embedding.
    """
    image_descriptions = []

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"-> Error opening PDF for image extraction: {e}")
        return []

    # Process only up to a safe threshold of images to prevent multi-minute processing locks
    max_total_images = 5
    images_processed = 0

    for page_num in range(len(doc)):
        if images_processed >= max_total_images:
            print(
                f"-> Reached maximum visual indexing limit ({max_total_images}). Skipping remaining images.")
            break

        page = doc[page_num]
        try:
            image_list = page.get_images(full=True)
        except Exception:
            continue

        if image_list:
            xref = image_list[0][0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
            except Exception:
                continue

            image_b64 = base64.b64encode(image_bytes).decode('utf-8')

            try:
                ollama_url = os.getenv(
                    "OLLAMA_HOST", "http://localhost:11434") + "/api/generate"
                prompt = "Briefly summarize the core metrics, charts, or diagrams on this page for document indexing."

                payload = {
                    "model": "gemma3:4b",
                    "prompt": prompt,
                    "images": [image_b64],
                    "stream": False
                }

                response = requests.post(ollama_url, json=payload, timeout=60)

                if response.status_code == 200:
                    description = response.json().get("response", "").strip()
                    if description:
                        image_descriptions.append({
                            "page": page_num + 1,
                            "text": f"[Visual Content Description]\n{description}"
                        })
                        print(
                            f"-> Generated visual description for image on Page {page_num + 1}")
                        images_processed += 1
            except Exception as e:
                print(
                    f"-> Vision processing skipped for page {page_num + 1}: {e}")

    doc.close()
    return image_descriptions
