import requests, json

class VectorStoreService:
    def __init__(self, superbase_url: str, superbase_key:str):
        self.superbase_url = superbase_url
        self.superbase_key = superbase_key
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.superbase_key,
            "Authorization": f"Bearer {self.superbase_key}"
        }

    def add_chunk(self, document_id: str, metadata: dict, content: str, embedding: list[float]) -> dict:
        """
        Add a chunk to the vector store.

        Args:
            document_id (str): The ID of the document.
            metadata (dict): The metadata associated with the chunk.
            embedding (list[float]): The embedding vector for the chunk.
    
        """
        url = f"{self.superbase_url}/rest/v1/rag_chunks"
        payload = {
            "document_id": document_id,
            "metadata": metadata,
            "content" : content,
            "embedding": embedding
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to add chunk: {response.status_code} - {response.text}")