from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def document_chunker(documents: list[Document]) -> list[Document]:

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_documents(documents)
    return chunks
