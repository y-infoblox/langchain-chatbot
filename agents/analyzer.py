def analyzer_agent(state):
    if state.get("is_greeting"):
        return state

    query = state.get("query")
    issues = []

    if not query:
        return state

    if "SELECT *" in query.upper():
        issues.append("Avoid SELECT *")

    if "WHERE" not in query.upper():
        issues.append("Missing WHERE clause")

    if "JOIN" in query.upper() and "ON" not in query.upper():
        issues.append("JOIN without ON condition")

    return {
        **state,
        "issues": issues
    }