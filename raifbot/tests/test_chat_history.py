import pytest
import httpx
import bson
from backend.routers.chat_history import init_mongo_DB
from backend.main import app

unique_id = str(bson.ObjectId())


@pytest.fixture(scope="session", autouse=True)
def run_before_tests():
    """
    A pytest fixture that runs before all tests in the session.
    It initializes the MongoDB connection by triggering the startup event explicitly.
    This ensures that the database is ready for use in all the tests that follow.
    """
    global db
    # Manually trigger startup event
    init_mongo_DB()


@pytest.mark.asyncio
async def test_mongo_DB_async():
    """
    Tests various MongoDB operations asynchronously within the FastAPI application context.

    This test performs the following operations:
    - Creates and saves chat history for a unique session ID.
    - Updates the chat history for the same session ID.
    - Retrieves the correct chat history for the session ID.
    - Attempts to retrieve chat history for a nonexistent session, expecting a failure.
    - Deletes the chat history for the session ID.
    - Verifies that the chat history for the session ID has been deleted.

    Assertions:
    - Asserts that each operation returns the correct HTTP status code,
      verifying the success or intended failure of each operation.
    """
    global db
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        session_id = unique_id
        history_items = [["Hello", "Hi there!"]]

        # create chat history
        response = await client.post(
            f"/save_chat_history/{session_id}", json=history_items
        )
        assert response.status_code == 200

        # update chat history
        response = await client.post(
            f"/save_chat_history/{session_id}", json=history_items
        )
        assert response.status_code == 200

        # get correct chat history
        response = await client.get(f"/get_chat_history/{session_id}")
        assert response.status_code == 200

        # get wrong chat hisotry
        response = await client.get(f"/get_chat_history/ ")
        assert response.status_code == 500

        # delete chat history
        response = await client.delete(f"/delete_chat_history/{session_id}")
        assert response.status_code == 200

        # verify deleted chat_history
        response = await client.get(f"/get_chat_history/{session_id}")
        assert response.status_code == 500
