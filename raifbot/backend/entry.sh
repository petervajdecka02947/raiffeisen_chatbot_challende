#!/bin/sh

# Print a message
echo "Running tests..."

# Run pytest and capture the exit code
poetry run pytest tests
TEST_EXIT_CODE=$?

# Check if tests passed (exit code 0 means success)
if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "Tests failed, exiting."
    exit $TEST_EXIT_CODE
else
    echo "Tests passed, starting the FastAPI application..."
    echo "Starting the FastAPI application with Gunicorn"
    # Exec should be outside if-else if running in a context where it matters (e.g., Docker)
    exec poetry run gunicorn backend.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 2000
fi
