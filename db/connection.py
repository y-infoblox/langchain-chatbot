import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection(config):
    env = config["environment"]
    db_config = config["databases"][env]

    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["name"],
        user=config["database"]["user"],
        password=os.getenv("DB_PASSWORD")
    )

    return conn