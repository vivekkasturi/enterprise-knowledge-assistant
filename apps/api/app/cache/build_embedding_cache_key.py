import hashlib


def build_cache_key(query: str, model_name: str) -> str:
    """
    Build a unique cache key based on the query and department.
    """
    normalized_query = query.lower().strip()
    query_hash = hashlib.sha256(normalized_query.encode()).hexdigest()
    return f"embedding:{model_name}:{query_hash}"

