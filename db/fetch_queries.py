from db.connection import get_db_connection

def fetch_queries(config):
    conn = get_db_connection(config)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT query
        FROM pg_stat_statements
        ORDER BY total_exec_time DESC
        LIMIT {config['app']['max_queries']};
    """)

    queries = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return queries