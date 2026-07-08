from langchain_groq import ChatGroq

def get_llm(config):
    return ChatGroq(
        model=config["llm"]["model"],
        temperature=config["llm"]["temperature"]
    )

def optimizer_agent(state, config):
    if state.get("is_greeting"):
        return state

    query = state.get("query")
    issues = state.get("issues", [])

    if not query:
        return state

    llm = get_llm(config)

    response = llm.invoke(f"""
You are a SQL Optimization Expert.

Query:
{query}

Issues:
{issues}

Give optimized query and suggestions.
""")

    return {
        **state,
        "suggestion": response.content
    }