from fastapi import FastAPI
from backend.routers.generation import router as chat_router
from backend.routers.chat_history import router as chat_history_router

app = FastAPI(
    title="Raiffeisen bank interview RAG chatbot",
    description="RaiffBot API",
    version="1.0.0",
)


app.include_router(chat_router, tags=["generation"])
app.include_router(chat_history_router, tags=["mongo_db"])
