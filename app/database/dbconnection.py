import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.environ["host"],
        user=os.environ["user"],
        database=os.environ["database"],
        password=os.environ["password"]
    )
    return conn
    