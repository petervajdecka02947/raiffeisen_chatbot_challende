from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "default_openai_api_key")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "default_pinecone_api_key")
    PINECONE_ENV: str = os.getenv("PINECONE_ENV", "gcp-starter")
    INDEX_NAME: str = os.getenv("INDEX_NAME", "brainsoft")
    EMBEDDING_NAME: str = os.getenv("EMBEDDING_NAME", "default_ambeddings")
    LLM_NAME: str = os.getenv("LLM_NAME", "default_LLM")
    MONGO_DB_KEY: str = os.getenv("MONGO_DB_KEY", "default_MONGO_DB_KEY")


# Instantiate settings to be imported by other modules
settings = Settings()
