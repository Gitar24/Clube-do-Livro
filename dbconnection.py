import psycopg2
def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        user="konton",
        database="postgres",
        password="314"
    )
    return conn