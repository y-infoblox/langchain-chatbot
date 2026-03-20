from dotenv import load_dotenv
import os
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

llm = ChatGroq(model="llama-3.3-70b-versatile")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful DevOps tutor. Explain things simply."),
    ("human", "{input}")
])

chain = prompt | llm


store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input"
)


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = chain_with_memory.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "user1"}}
    )

    print("AI:", response.content)
