import sqlglot

def parser_agent(state):
    query = state.get("query")
    if not query:
        return state

    if query.strip().lower() == "hi":
        return {
            **state,
            "is_greeting": True,
            "tables": [],
            "columns": [],
            "issues": [],
            "suggestion": "Hi! Please share a SQL query you'd like to optimize."
        }

    parsed = sqlglot.parse_one(query)

    tables = [t.name for t in parsed.find_all(sqlglot.exp.Table)]
    columns = [c.name for c in parsed.find_all(sqlglot.exp.Column)]

    return {
        **state,
        "tables": tables,
        "columns": columns
    }