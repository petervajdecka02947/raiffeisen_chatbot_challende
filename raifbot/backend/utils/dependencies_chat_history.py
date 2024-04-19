# from mongo_db import db
from backend.utils.error_handler import UpdateError
from typing import List
from bson import ObjectId


async def update_or_insert_chat_history(db: object, session_id: str, new_history: List):
    """
    Updates or inserts chat history for a given session ID in the database.

    Args:
        db (object): The database object.
        session_id (str): The session ID for which chat history needs to be updated or inserted.
        new_history (List): The new chat history to be added.

    Returns:
        dict: A success message indicating whether the chat history was updated or inserted.

    Raises:
        UpdateError: If there is an exception during database update or insert operations.
    """
    existing_doc = await db.find_one({"_id": ObjectId(session_id)})
    if existing_doc:
        try:
            await db.update_one(
                {"_id": ObjectId(session_id)},
                {"$push": {"chat_history": {"$each": new_history}}},
            )
            suc_message = "Chat history successfully updated."

        except Exception as e:
            raise UpdateError(f"Failed to update chat history: {e}", 500)
    else:
        try:
            new_doc = {"_id": ObjectId(session_id), "chat_history": new_history}
            await db.insert_one(new_doc)
            suc_message = "Chat history successfully inserted."

        except Exception as e:
            raise UpdateError(f"Failed to create chat history: {e}", 500)

    return {"message": suc_message}


async def get_chat_history_item(db: object, session_id: str):
    """
    Retrieves the chat history for a specific session ID from the database.

    Args:
        db (object): The database object.
        session_id (str): The session ID for which chat history needs to be retrieved.

    Returns:
        dict: The chat history associated with the given session ID.

    Raises:
        UpdateError: If there is an exception during the database query.
    """
    try:
        doc = await db.find_one({"_id": ObjectId(session_id)})
        return {"chat_history": doc["chat_history"]}

    except Exception as e:
        raise UpdateError(
            f"Failed to get chat history for id {session_id} with error: {e}", 500
        )


async def delete_chat_history_item(db: object, session_id: str):
    """
    Deletes the chat history for a specific session ID from the database.

    Args:
        db (object): The database object.
        session_id (str): The session ID for which chat history needs to be deleted.

    Returns:
        dict: A message indicating successful deletion of the chat history.

    Raises:
        UpdateError: If there is no chat history for the given session ID, or if there is an exception during the delete operation.
    """
    try:
        doc = await db.find_one({"_id": ObjectId(session_id)})
        if "chat_history" not in doc:
            raise UpdateError(
                f"There is no chat history for id {session_id} with error: {e}", 401
            )
    except Exception as e:
        raise UpdateError(
            f"There is no chat history item for id {session_id} with error: {e}", 402
        )
    try:
        await db.delete_one({"_id": ObjectId(session_id)})
        return {"message": "Chat history deleted"}

    except Exception as e:
        raise UpdateError(
            f"Failed to delete chat history for id {session_id} with error: {e}", 500
        )


async def delete_whole_chat_history(db: object):
    """
    Deletes all chat histories in the database. This is a sensitive operation and should be used with caution.

    Args:
        db (object): The database object.

    Returns:
        dict: A message indicating successful deletion of the entire chat history.

    Raises:
        UpdateError: If there is an exception during the delete operation.
    """
    try:
        await db.delete_many({})
        return {"message": "Whole chat history deleted"}

    except Exception as e:
        raise UpdateError(f"Failed to delete whole chat history with error: {e}", 500)
