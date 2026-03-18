from dotenv import load_dotenv
import os

load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(model="llama-3.3-70b-versatile")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful DevOps tutor. Explain things simply."),
    ("human", "{input}")
])

# Create chain
chain = prompt | llm

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = chain.invoke({"input": user_input})

    print("AI:", response.content)