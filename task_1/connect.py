import psycopg2
from contextlib import contextmanager

@contextmanager
def create_connect():
    try:
        conn = psycopg2.connect(
            user = "postgres",
            password = "567234",
            host = "localhost",
            database = "HW03"
        )
        yield conn
        conn.close()
    
    except psycopg2.OperationalError:
        print("Connection failed")
    