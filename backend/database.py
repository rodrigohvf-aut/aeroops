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

    try:
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

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runways (
                id INTEGER PRIMARY KEY,
                airport_ident TEXT NOT NULL,
                le_ident TEXT,
                he_ident TEXT,
                length_ft INTEGER,
                width_ft INTEGER,
                surface TEXT,
                lighted INTEGER,
                closed INTEGER,
                le_latitude_deg REAL,
                le_longitude_deg REAL,
                he_latitude_deg REAL,
                he_longitude_deg REAL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS aircraft_positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                icao24 TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                observed_at TEXT NOT NULL,
                UNIQUE (icao24, observed_at)
            )
            """
        )

        existing_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(runways)")
        }

        coordinate_columns = (
            "le_latitude_deg",
            "le_longitude_deg",
            "he_latitude_deg",
            "he_longitude_deg",
        )

        for column in coordinate_columns:
            if column not in existing_columns:
                connection.execute(
                    f"ALTER TABLE runways ADD COLUMN {column} REAL"
                )

        connection.commit()

    finally:
        connection.close()