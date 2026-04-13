from pathlib import Path

# ---------- Models ----------
EMBEDDING_MODEL = "text-embedding-3-small"
LANGUAGE_MODEL = "gpt-4o-mini"
MAX_NEW_TOKENS = 1024
TEMPERATURE = 0

EMBEDDING_BATCH_SIZE = 100

# ---------- Chunking ----------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

TOP_K = 10

# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCE_DIR = BASE_DIR / "resources"
KNOWLEDGE_BASE_DIR = RESOURCE_DIR / "knowledge-base"
VECTORSTORE_DIR = RESOURCE_DIR / "vectorstores"

VECTOR_DB_ID = "insurellm"
ACCEPTED_FILE_PATH = "**/*.md"
