from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

from utils.constants import TOP_K
from utils.llm import get_llm
from utils.prompt import contextualize_prompt, prompt
from utils.vector_store import load_vector_store


def get_qa_chain(store_id, streaming=False):
    db = load_vector_store(store_id)

    llm = get_llm(streaming=streaming)

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )

    # Create the history-aware retriever
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_prompt
    )

    qa_chain = create_stuff_documents_chain(llm, prompt)

    # Create the history aware RAG chain
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return rag_chain


store = {}


# Function to get the session history for a given session ID
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def ask_question(query, session_id, store_id):
    db = load_vector_store(store_id)

    docs_and_scores = db.similarity_search_with_score(query, k=TOP_K)
    # Sort by distance (ascending = most similar first)
    docs_and_scores.sort(key=lambda x: x[1])

    source_docs = []
    for doc, score in docs_and_scores:
        # Convert distance to similarity score (1 - distance for cosine)
        try:
            dist = float(score)
            doc.metadata["distance"] = dist
            doc.metadata["score"] = max(0, 1 - dist)
        except (ValueError, TypeError):
            doc.metadata["score"] = 0.0
        source_docs.append(doc)

    rag_chain = get_qa_chain(store_id)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    response = conversational_rag_chain.invoke(
        {"input": query},
        config={"configurable": {"session_id": session_id}},
    )

    answer = response["answer"]

    sources = [doc.metadata.get("source", "Unknown") for doc in source_docs]

    return answer, list(set(sources))


async def ask_question_stream(query, session_id, store_id):
    db = load_vector_store(store_id)

    docs_and_scores = db.similarity_search_with_score(query, k=TOP_K)
    # Sort by distance (ascending = most similar first)
    docs_and_scores.sort(key=lambda x: x[1])

    source_docs = []
    for doc, score in docs_and_scores:
        # Convert distance to similarity score (1 - distance for cosine)
        try:
            dist = float(score)
            doc.metadata["distance"] = dist
            doc.metadata["score"] = max(0, 1 - dist)
        except (ValueError, TypeError):
            doc.metadata["score"] = 0.0
        source_docs.append(doc)

    rag_chain = get_qa_chain(store_id, streaming=True)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    async for chunk in conversational_rag_chain.astream(
        {"input": query},
        config={"configurable": {"session_id": session_id}},
    ):
        if "answer" in chunk:
            yield {"type": "chunk", "data": chunk["answer"]}

    sources = [doc.metadata.get("source", "Unknown") for doc in source_docs]
    yield {"type": "sources", "data": list(set(sources))}
