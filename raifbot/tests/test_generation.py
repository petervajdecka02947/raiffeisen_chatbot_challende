import pytest
from fastapi.testclient import TestClient
from backend.config import settings
from backend.main import app  # replace with your actual app import
from backend.routers.generation import startup_event


client = TestClient(app)


@pytest.fixture(autouse=True)
def run_before_tests():
    """
    A pytest fixture that runs before each test. It manually triggers the startup event
    to initialize necessary components for the test environment.
    """
    startup_event()


def test_health():
    """
    Tests the health check endpoint of the FastAPI application.

    Asserts:
    - The response status code is 200 (OK).
    - The response body matches the expected health check status.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "🤙"}


def test_get_current_model():
    """
    Tests the endpoint for retrieving the current model used by the application.

    Asserts:
    - The response status code is 200 (OK).
    - The response body contains the correct current model information.
    """
    response = client.get("/get_current_model/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Current model is {}".format(settings.LLM_NAME)
    }


def test_chat_no_stream():
    """
    Tests the endpoint for handling conversational queries without streaming.

    Asserts:
    - The response status code is 200 (OK), indicating successful handling of the query.
    """
    response = client.get(
        "/chat_no_stream", params={"query": "Hello, answer with few words!"}
    )
    assert response.status_code == 200


def test_get_document_source():
    """
    Tests the endpoint for retrieving document sources based on a given query.

    Asserts:
    - The response status code is 200 (OK), indicating successful retrieval of the document source.
    """
    response = client.get(
        "/get_document_source/", params={"query": "Where is maintainer SDK ?"}
    )
    assert response.status_code == 200
