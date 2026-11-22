import fitz


def extract_text_and_layout(pdf_bytes: bytes):
    """Read text from a bounded PDF; scanned pages require OCR elsewhere."""
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            if document.needs_pass or len(document) > 50:
                raise ValueError("PDF is encrypted or exceeds 50 pages")
            text = "\n\n".join(page.get_text() for page in document)
    except Exception as error:
        raise RuntimeError("Failed to extract text from PDF") from error
    return text.splitlines(), []
