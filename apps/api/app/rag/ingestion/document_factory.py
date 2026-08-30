from langchain_core.documents import Document


def create_document(raw_text: str, metadata: dict[str, str]) -> Document:
    """
    Create a Document object from raw text.

    Args:
        raw_text (str): The raw text to be converted into a Document.

    Returns:
        list[dict[str, str]]: A list containing a single Document object with the raw text.
    """

    if not raw_text.strip():
        raise ValueError("Raw text is empty. Cannot create Document.")
  

    document = Document(page_content=raw_text, metadata=metadata)

    return document
