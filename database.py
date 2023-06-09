import sqlite3


DB_PATH = "database.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def select(rqst):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(rqst)
        return cursor.fetchall()
