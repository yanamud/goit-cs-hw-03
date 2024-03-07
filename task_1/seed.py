import logging

from faker import Faker
import random
import psycopg2
from psycopg2 import DatabaseError

fake = Faker()

# Підключення до бази
conn = psycopg2.connect(host = "localhost", 
                        database = "HW03", 
                        user = "postgres", 
                        password = "567234")
cur =  conn.cursor()

total_subjects = 20
total_tasks = 50

# Заповнення таблиці users
for i in range(total_subjects):
    cur.execute(f"INSERT INTO users (id, fullname, email) VALUES ({i+1}, '{fake.name()}', '{fake.email()}');")

# Заповнення таблиці status
cur.execute(f"INSERT INTO status (id, name) VALUES (1,'new'), (2, 'in progress'), (3, 'done');")

# Заповнення таблиці tasks
for _ in range(total_tasks):
    cur.execute(f"INSERT INTO tasks (title, description, status_id, user_id) VALUES ('{fake.sentence()}', '{fake.text()}', {random.randint(1, 3)}, {random.randint(1, total_subjects)});")

try:
    conn.commit()
except DatabaseError as err:
    logging.error(f"Database error: {err}")
    conn.rollback()
finally:
    cur.close()
    conn.close()
