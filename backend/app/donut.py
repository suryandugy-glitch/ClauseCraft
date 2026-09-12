# backend/app/donut.py
import fitz  # PyMuPDF

def extract_text_and_layout(pdf_bytes: bytes):
    """
    Extract text from PDF using PyMuPDF (fitz).
    Returns a list of text lines and an empty list for bounding boxes
    (the layout information is not needed for the simple demo).
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")

    # Split into lines, remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    # Placeholder for bounding boxes (not used in this simple version)
    bboxes = []
    return lines, bboxes