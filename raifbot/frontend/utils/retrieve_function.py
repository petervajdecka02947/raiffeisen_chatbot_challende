import requests


def get_source(query: str, end_point: str):
    """
    Retrieves the source from retrieval

    Parameters:
    query: query to find the most similar source

    Returns:
    str: the source found
    """
    url = f"http://{end_point}/get_document_source/"
    params = {"query": query}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
