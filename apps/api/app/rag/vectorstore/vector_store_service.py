import requests, json

class VectorStoreService:
    def __init__(self, supabase_url: str, supabase_key:str):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Prefer": "return=representation",
        }

    def add_chunk(self, document_id: str, metadata: dict, content: str, embedding: list[float]) -> dict:
        """
        Add a chunk to the vector store.

        Args:
            document_id (str): The ID of the document.
            metadata (dict): The metadata associated with the chunk.
            embedding (list[float]): The embedding vector for the chunk.
    
        """
        url = f"{self.supabase_url}/rest/v1/rag_chunks"
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


    
    def similarity_search(self, query_embedding: list[float], top_k: int = 5):

        url = f"{self.supabase_url}/rest/v1/rpc/match_rag_chunks"

        payload = {
            "query_embedding": query_embedding,
            "match_count": top_k
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if(response.status_code!=200):
            raise Exception(f"Failed to perform similarity search: {response.status_code} - {response.text}")

        return response.json()
        

    