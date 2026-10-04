import json

import requests

import time

from app.core.exceptions import VectorStoreException

RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}

class VectorStoreService:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Prefer": "return=representation",
        }

    def add_chunk(
        self, document_id: str, metadata: dict, content: str, embedding: list[float]
    ) -> dict:
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
            "content": content,
            "embedding": embedding,
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code == 200:
            return response.json()
        else:
            raise VectorStoreException(
                status_code=response.status_code,
                detail=f"Failed to add chunk: {response.text}",
            )

    def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        department: str | None = None,
        ):

        url = f"{self.supabase_url}/rest/v1/rpc/match_rag_chunks"

        payload = {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "filter_department": department,
        }

        try:

            response = requests.post(url, headers=self.headers, data=json.dumps(payload), timeout=10)

            if response.status_code != 200:
                raise VectorStoreException(
                    status_code=response.status_code,
                    detail=f"Failed to perform similarity search: {response.text}",
                )
        

        except requests.Timeout as e:
                raise VectorStoreException(
                    status_code=504,
                    detail=f"similarity search request failed: {str(e)}",
                ) from e
            
        except requests.RequestException as e:
                raise VectorStoreException(
                    status_code=503,
                    detail=f"similarity search request failed: {str(e)}",
                ) from e


        return response.json()

    def keyword_search(
        self, keyword: str, top_k: int = 5, department: str | None = None
    ):
        url = f"{self.supabase_url}/rest/v1/rpc/keyword_search_rag_chunks"

        try: 
            response = requests.post(
                url,
                headers=self.headers,
                json={
                    "search_query": keyword,
                    "match_count": top_k,
                    "filter_department": department,
                },
                timeout=10
            )

            if response.status_code != 200:
                raise VectorStoreException(
                    status_code=response.status_code,
                    detail=f"Failed to perform keyword search: {response.text}",
                )
        except requests.RequestException as e:
            raise VectorStoreException(
                    status_code=503,
                    detail=f"keyword search request failed: {str(e)}",
                ) from e
        except requests.Timeout as e:
                raise VectorStoreException(
                    status_code=504,
                    detail=f"keyword search request failed: {str(e)}",
                ) from e

        return response.json()

def retry_request(
    self,
    url: str,
    payload: dict,
    max_attempts: int = 3,
    timeout: int = 10,
):
    """
    Send a POST request with retry and exponential backoff.
    """

    base_delay = 1

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=timeout,
            )

            # Success
            if 200 <= response.status_code < 300:
                return response

            # Non-retryable HTTP error
            if response.status_code not in RETRYABLE_STATUS_CODES:
                raise VectorStoreException(
                    status_code=response.status_code,
                    detail=f"Request failed: {response.text}",
                )

            # Retryable HTTP error, but attempts exhausted
            if attempt == max_attempts:
                raise VectorStoreException(
                    status_code=response.status_code,
                    detail=(
                        f"Request failed after {max_attempts} attempts: "
                        f"{response.text}"
                    ),
                )

            print(
                f"Request failed with status {response.status_code}. "
                f"Attempt {attempt}/{max_attempts}."
            )

        except requests.Timeout as e:
            if attempt == max_attempts:
                raise VectorStoreException(
                    status_code=504,
                    detail=f"Request timed out after {max_attempts} attempts",
                ) from e

            print(
                f"Request timed out. "
                f"Attempt {attempt}/{max_attempts}."
            )

        except requests.RequestException as e:
            if attempt == max_attempts:
                raise VectorStoreException(
                    status_code=503,
                    detail=f"Request failed after {max_attempts} attempts: {e}",
                ) from e

            print(
                f"Network request failed. "
                f"Attempt {attempt}/{max_attempts}."
            )

        # Exponential backoff before next attempt
        delay = base_delay * (2 ** (attempt - 1))

        print(f"Retrying in {delay} seconds...")
        time.sleep(delay)


