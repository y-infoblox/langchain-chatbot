from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
import sqlglot

llm = ChatGroq(model="llama-3.3-70b-versatile")

def parser_agent(state):
    print("DEBUG (parser):", state)

    query = state.get("query")
    if not query:
        return state

    parsed = sqlglot.parse_one(query)

    tables = [t.name for t in parsed.find_all(sqlglot.exp.Table)]
    columns = [c.name for c in parsed.find_all(sqlglot.exp.Column)]

    return {
        **state,
        "tables": tables,
        "columns": columns
    }
def analyzer_agent(state):
    print("DEBUG (analyzer):", state)

    query = state.get("query")
    if not query:
        return state

    issues = []

    if "SELECT *" in query.upper():
        issues.append("Using SELECT * (inefficient)")

    if "WHERE" not in query.upper():
        issues.append("No WHERE clause (full table scan risk)")

    return {
        **state,
        "issues": issues
    }
def optimizer_agent(state):
    print("DEBUG (optimizer):", state)

    query = state.get("query")
    issues = state.get("issues", [])

    if not query:
        return state

    response = llm.invoke(f"""
You are a SQL Optimization Expert.

Analyze the query and suggest improvements.

Query:
{query}

Issues:
{issues}

Give clear and practical suggestions.
""")

    return {
        **state,
        "suggestion": response.content
    }

graph = StateGraph(dict)   

graph.add_node("parser", parser_agent)
graph.add_node("analyzer", analyzer_agent)
graph.add_node("optimizer", optimizer_agent)

graph.set_entry_point("parser")

graph.add_edge("parser", "analyzer")
graph.add_edge("analyzer", "optimizer")

app = graph.compile()

if __name__ == "__main__":
    while True:
        query = input("\nEnter SQL Query (or 'exit'): ")

        if query.lower() == "exit":
            break

        result = app.invoke({"query": query})

        print("\n--- RESULT ---")
        print("Tables:", result.get("tables"))
        print("Columns:", result.get("columns"))
        print("Issues:", result.get("issues"))
        print("Suggestion:\n", result.get("suggestion"))