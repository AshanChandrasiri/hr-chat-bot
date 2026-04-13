from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

contextualize_system_prompt = (
    "using chat history and the latest user question, just reformulate question if needed and otherwise return it as is"
)

contextualize_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

system_prompt = (
    "You are an intelligent chatbot. Use the following context to answer the question. If you don't know the answer, just say that you don't know. Answer should be in text format, no code blocks, no markdown, just plain text."
    "\n\n"
    "{context}"
)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
