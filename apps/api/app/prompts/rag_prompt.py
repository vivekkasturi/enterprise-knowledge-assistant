RAG_SYSTEM_INSTRUCTION = """
you are a helpful assistant that answers questions based on the context provided.
Answer the user's question using only the provided context.

Rules:
- Do not use information outside the provided context.
- If the context does not contain enough information, say that you do not have enough information.
- Do not fabricate information.
- Keep the answer concise and relevant.

"""


def build_rag_messages(query: str, context: str) -> list[dict[str, str]]:
    messages = [
        {"role": "system", "content": RAG_SYSTEM_INSTRUCTION},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"},
    ]

    return messages
