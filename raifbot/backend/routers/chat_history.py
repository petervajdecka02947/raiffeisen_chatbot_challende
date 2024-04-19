from fastapi import APIRouter
from fastapi import HTTPException
from typing import List
from backend.models import ChatHistoryResponse
from backend.models import MessageResponse
from backend.utils.dependencies_chat_history import update_or_insert_chat_history
from backend.utils.dependencies_chat_history import get_chat_history_item
from backend.utils.dependencies_chat_history import delete_chat_history_item
from backend.utils.dependencies_chat_history import delete_whole_chat_history
from backend.utils.error_handler import UpdateError
import logging
from backend.mongo_db import database

router = APIRouter()


def init_mongo_DB():
    """
    Initializes the MongoDB connection for chat history storage.

    This function sets up a global variable `db` which holds the chat history collection from the database.

    Raises:
        HTTPException: If there is an unexpected error during database initialization.
    """
    global db

    try:
        db = database.chat_history_collection
    except Exception as e:
        msg = f"Unexpected error during database initialization: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=e.status_code, detail=msg)


router.add_event_handler("startup", init_mongo_DB)


@router.post("/save_chat_history/{session_id}", response_model=MessageResponse)
async def save_chat_history(session_id: str, history_items: List[List[str]]):
    """
    Saves or updates the chat history for a given session.

    Args:
        session_id (str): The unique identifier for the chat session.
        history_items (List[List[str]]): A list of chat history items to be saved or updated.

    Returns:
        MessageResponse: A response indicating the success of the operation.

    Raises:
        HTTPException: If there's an error during the update/insert of chat history.
    """
    global db
    try:
        return await update_or_insert_chat_history(db, session_id, history_items)

    except UpdateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        msg = f"Unexpected error during update/insert of chat history: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.get("/get_chat_history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(session_id: str):
    """
    Retrieves the chat history for a specific session.

    Args:
        session_id (str): The unique identifier for the chat session.

    Returns:
        ChatHistoryResponse: The chat history associated with the given session.

    Raises:
        HTTPException: If there's an error during the retrieval of chat history.
    """
    global db
    try:
        return await get_chat_history_item(db, session_id)

    except UpdateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        msg = f"Unexpected error during getting of chat history: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.delete("/delete_chat_history/{session_id}", response_model=MessageResponse)
async def delete_chat_history(session_id: str):
    """
    Deletes the chat history for a specific session.

    Args:
        session_id (str): The unique identifier for the chat session to be deleted.

    Returns:
        MessageResponse: A response indicating the success of the deletion operation.

    Raises:
        HTTPException: If there's an error during the deletion of chat history.
    """
    global db
    # Delete the chat history by session ID
    try:
        return await delete_chat_history_item(db, session_id)

    except UpdateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        msg = f"Unexpected error during deleting of chat history: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=e.status_code, detail=msg)


@router.delete("/delete_all_chat_histories", response_model=MessageResponse)
async def delete_all_chat_histories():
    """
    Deletes all chat histories in the database. This is a sensitive operation.

    Returns:
        MessageResponse: A response indicating the success of the deletion operation.

    Raises:
        HTTPException: If there's an error during the deletion of all chat histories.
    """
    global db
    # Very sensitive !
    try:
        return await delete_whole_chat_history(db)

    except UpdateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        msg = f"Unexpected error during deleting of whole chat history: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=e.status_code, detail=msg)
