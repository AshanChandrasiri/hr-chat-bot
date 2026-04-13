from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import json

from dto.requests.query_request import QueryRequest
from utils.constants import VECTOR_DB_ID
from utils.rag_chain import ask_question_stream, ask_question


def chat_controller(app):

    @app.post("/api/query")
    async def query_repository(request: QueryRequest):
        try:
            answer, sources = ask_question(request.question, request.session_id, VECTOR_DB_ID)
            return {"answer": answer, "sources": sources}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/query-stream")
    async def query_repository(request: QueryRequest):
        try:
            return StreamingResponse(generate(request.question, request.session_id, VECTOR_DB_ID), media_type="text/event-stream")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def generate(question, session_id, store_id):
        async for chunk in ask_question_stream(question, session_id, store_id):
            yield f"data: {json.dumps(chunk)}\n\n"
