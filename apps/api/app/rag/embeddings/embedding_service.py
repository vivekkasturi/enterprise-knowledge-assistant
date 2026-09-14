from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, embedding_model="sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(embedding_model)


    def generate_embedding(self, text: list[list[float]])->list[float]:
        """
        Generate an embedding for the given text using the specified embedding model.

        Args:
            text (str): The input text to generate an embedding for.

        Returns:
            list[float]: A list representing the generated embedding vector.
        """
        embedding = self.embedding_model.encode(text)

        return embedding.tolist()
    
    def batch_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts (list[str]): A list of input texts to generate embeddings for.

        Returns:
            list[list[float]]: A list of lists representing the generated embedding vectors.
        """
        embeddings = self.embedding_model.encode(texts)

        return [embedding.tolist() for embedding in embeddings]
        
service = EmbeddingService()
