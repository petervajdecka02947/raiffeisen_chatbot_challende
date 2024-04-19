from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Take environment variables from .env.


class Settings(BaseSettings):
    PAGE_ICON: str = os.getenv("PAGE_ICON", "default_openai_api_key")
    PAGE_TITLE: str = os.getenv("PAGE_TITLE", "default_pinecone_api_key")
    RAIF_IMAGE_PATH: str = os.getenv("RAIF_IMAGE_PATH", "gcp-starter")
    PROFILE_IMAGE_PATH: str = os.getenv("PROFILE_IMAGE_PATH", "brainsoft")
    AUTHOR_NAME: str = os.getenv("AUTHOR_NAME", "default_ambeddings")
    AUTHOR_EMAIL: str = os.getenv("AUTHOR_EMAIL", "default_LLM")
    ENDPOINT: str = os.getenv("ENDPOINT", "default_MONGO_DB_KEY")


# Instantiate settings to be imported by other modules
settings = Settings()
