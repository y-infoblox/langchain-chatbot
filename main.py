from langgraph.graph import StateGraph

from utils.config_loader import load_config
from db.fetch_queries import fetch_queries

from agents.parser import parser_agent
from agents.analyzer import analyzer_agent
from agents.optimizer import optimizer_agent

config = load_config()

def optimizer_wrapper(state):
    return optimizer_agent(state, config)

graph = StateGraph(dict)

graph.add_node("parser", parser_agent)
graph.add_node("analyzer", analyzer_agent)
graph.add_node("optimizer", optimizer_wrapper)

graph.set_entry_point("parser")

graph.add_edge("parser", "analyzer")
graph.add_edge("analyzer", "optimizer")

app = graph.compile()

if __name__ == "__main__":
    queries = fetch_queries(config)

    for query in queries:
        print("\n============================")
        print("QUERY:", query)

        result = app.invoke({"query": query})

        print("Tables:", result.get("tables"))
        print("Columns:", result.get("columns"))
        print("Issues:", result.get("issues"))
        print("Suggestion:\n", result.get("suggestion"))