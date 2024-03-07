import logging
from psycopg2 import DatabaseError

from connect import create_connect

def create_table(conn, sql_stmt: str):
    c = conn.cursor()
    try:
        c.execute(sql_stmt)
        conn.commit()
    except DatabaseError as err:
        logging.error(f"Database error: {err}")
        conn.rollback()
    finally:
        c.close()

if __name__ == "__main__":
    sql_users = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY, 
        fullname VARCHAR(100), 
        email VARCHAR(100) UNIQUE
    );
    """
    sql_status = """   
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY, 
        name VARCHAR(50) UNIQUE
    );   
    """
    sql_tasks = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY, 
        title VARCHAR(100), 
        description TEXT,
        status_id INTEGER, 
        user_id INTEGER,
            FOREIGN KEY (status_id) REFERENCES status (id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
    );      
    """
    try:
        with create_connect() as conn:
            create_table(conn,sql_users)
            create_table(conn,sql_status)
            create_table(conn,sql_tasks)

    except RuntimeError as err:
        logging.error(f"Runtime error: {err}")