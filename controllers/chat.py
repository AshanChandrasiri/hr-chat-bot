from fastapi import HTTPException

from dto.requests.query_request import QueryRequest
from utils.constants import VECTOR_DB_ID
from utils.rag_chain import ask_question


def chat_controller(app):

    @app.post("/api/query")
    async def query_repository(request: QueryRequest):
        try:
            answer, sources = ask_question(request.question, request.session_id, VECTOR_DB_ID)
            return {"answer": answer, "sources": sources}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))