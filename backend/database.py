import sqlite3
from .config import DATABASE_PATH, DATABASE_URL
import psycopg
from psycopg.rows import dict_row

def get_connection():
    if DATABASE_URL:
        return psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row,
        )
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    if DATABASE_URL:
        return
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS airports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ident TEXT NOT NULL,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()