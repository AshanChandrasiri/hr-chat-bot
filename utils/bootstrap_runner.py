from contextlib import asynccontextmanager

from fastapi import FastAPI

from utils.constants import VECTOR_DB_ID, KNOWLEDGE_BASE_DIR
from utils.file_loader import load_files
from utils.vector_store import create_vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Runs once on startup
    print("App is starting...")

    print(f"Vector store '{VECTOR_DB_ID}' initializing...")
    documents = load_files(KNOWLEDGE_BASE_DIR)
    create_vector_store(documents, VECTOR_DB_ID)
    print(f"Vector store '{VECTOR_DB_ID}' initialized successfully.")

    yield

    # 🔹 Runs on shutdown
    print("App is shutting down...")