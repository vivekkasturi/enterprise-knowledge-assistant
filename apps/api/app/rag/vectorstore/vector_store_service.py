import json

import requests

import time

from app.core.exceptions import VectorStoreException
from app.rag.vectorstore.circuit_breaker import CircuitBreaker


RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}

CIRCUIT_BREAKER_FAILURE_CODES = {
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

        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_time=60,
        )

    def execute_with_circuit_breaker(
        self,
        url: str,
        payload: dict,
    ):
        """
        Execute a request with circuit breaker protection.

        The circuit breaker wraps the complete retry operation,
        so one exhausted retry sequence counts as one circuit failure.
        """

        # Check circuit BEFORE calling Supabase
        if not self.circuit_breaker.can_execute():
            raise VectorStoreException(
                status_code=503,
                detail="Circuit breaker is OPEN. Supabase request blocked.",
            )

        try:
            # retry_request performs the actual requests.post(...)
            response = self.retry_request(
                url=url,
                payload=payload,
            )

            # retry_request returns only for successful 2xx
            self.circuit_breaker.record_success()

            return response

        except VectorStoreException as e:
            # Only dependency-health failures affect circuit state
            if e.status_code in CIRCUIT_BREAKER_FAILURE_CODES:
                self.circuit_breaker.record_failure()

            raise

    def retry_request(
        self,
        url: str,
        payload: dict,
        max_attempts: int = 3,
        timeout: int = 10,
    ):
        """
        Send a POST request with bounded retries
        and exponential backoff.
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

                # Successful HTTP response
                if 200 <= response.status_code < 300:
                    return response

                # Non-retryable HTTP failure
                if response.status_code not in RETRYABLE_STATUS_CODES:
                    raise VectorStoreException(
                        status_code=response.status_code,
                        detail=f"Request failed: {response.text}",
                    )

                # Retryable error, but no attempts remaining
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
                        detail=(
                            f"Request timed out after "
                            f"{max_attempts} attempts"
                        ),
                    ) from e

                print(
                    f"Request timed out. "
                    f"Attempt {attempt}/{max_attempts}."
                )

            except requests.RequestException as e:
                if attempt == max_attempts:
                    raise VectorStoreException(
                        status_code=503,
                        detail=(
                            f"Request failed after "
                            f"{max_attempts} attempts: {e}"
                        ),
                    ) from e

                print(
                    f"Network request failed. "
                    f"Attempt {attempt}/{max_attempts}."
                )

            # Exponential backoff:
            # attempt 1 -> 1 second
            # attempt 2 -> 2 seconds
            delay = base_delay * (2 ** (attempt - 1))

            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    def add_chunk(
        self,
        document_id: str,
        metadata: dict,
        content: str,
        embedding: list[float],
    ) -> dict:
        """
        Add a chunk to the vector store.

        Note:
        We are intentionally not applying automatic retries
        to writes yet because retrying non-idempotent writes
        can create duplicate data.
        """

        url = f"{self.supabase_url}/rest/v1/rag_chunks"

        payload = {
            "document_id": document_id,
            "metadata": metadata,
            "content": content,
            "embedding": embedding,
        }

        try:
            response = requests.post(
                url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=10,
            )

        except requests.Timeout as e:
            raise VectorStoreException(
                status_code=504,
                detail=f"Add chunk request timed out: {e}",
            ) from e

        except requests.RequestException as e:
            raise VectorStoreException(
                status_code=503,
                detail=f"Add chunk request failed: {e}",
            ) from e

        if 200 <= response.status_code < 300:
            return response.json()

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
        """
        Perform semantic similarity search.
        """

        url = f"{self.supabase_url}/rest/v1/rpc/match_rag_chunks"

        payload = {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "filter_department": department,
        }

        response = self.execute_with_circuit_breaker(
            url=url,
            payload=payload,
        )

        return response.json()

    def keyword_search(
        self,
        keyword: str,
        top_k: int = 5,
        department: str | None = None,
    ):
        """
        Perform PostgreSQL full-text keyword search.
        """

        url = (
            f"{self.supabase_url}"
            "/rest/v1/rpc/keyword_search_rag_chunks"
        )

        payload = {
            "search_query": keyword,
            "match_count": top_k,
            "filter_department": department,
        }

        response = self.execute_with_circuit_breaker(
            url=url,
            payload=payload,
        )

        return response.json()