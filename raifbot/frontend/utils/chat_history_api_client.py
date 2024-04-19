import requests
from typing import List
import os


def save_chat_history(session_id: str, history_items: List[List[str]], BASE_URL):
    """
    Saves the chat history for a given session.

    Parameters:
    session_id (str): The session ID for the chat history.
    history_items (List[dict]): A list of chat history items to save.

    Returns:
    dict: The saved chat history from the server response.
    """
    url = f"http://{BASE_URL}/save_chat_history/{session_id}"
    response = requests.post(url, json=history_items)
    response.raise_for_status()  # This will raise an exception for HTTP error codes
    return response.json()


def get_chat_history(session_id: str, BASE_URL):
    """
    Retrieves the chat history for a given session.

    Parameters:
    session_id (str): The session ID for the chat history.

    Returns:
    dict: The chat history from the server response.
    """
    url = f"http://{BASE_URL}/get_chat_history/{session_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
