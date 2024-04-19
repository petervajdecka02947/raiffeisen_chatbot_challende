FROM python:3.9

RUN apt-get update && apt-get install -y \
    python3-pip && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock* ./.env ./

# Install Poetry at a specific version
RUN pip3 install poetry==1.7.1

# Install dependencies using Poetry
RUN poetry install --no-root

# Now copy your entire backend application
COPY ./backend /backend
COPY ./tests /tests

# Set the ENTRYPOINT
ENTRYPOINT ["sh", "backend/entry.sh"]