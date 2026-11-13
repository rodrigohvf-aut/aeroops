from .database import get_connection
from .config import DATABASE_URL


def create_airport(airport):
    connection = get_connection()

    values = (
        airport.ident,
        airport.name,
        airport.country,
        airport.latitude,
        airport.longitude,
    )

    if DATABASE_URL:
        cursor = connection.execute(
            """
            INSERT INTO airports (ident, name, country, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            values,
        )
        airport_id = cursor.fetchone()["id"]
    else:
        cursor = connection.execute(
            """
            INSERT INTO airports (ident, name, country, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
            """,
            values,
        )
        airport_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {**airport.model_dump(), "id": airport_id}



def list_airports(search: str = "", limit: int = 20, offset: int = 0):
    connection = get_connection()

    try:
        placeholder = "%s" if DATABASE_URL else "?"
        query = """
            SELECT id, ident, name, country, latitude, longitude
            FROM airports
        """
        values = []

        if search.strip():
            query += f"""
                WHERE LOWER(ident) LIKE LOWER({placeholder})
                   OR LOWER(name) LIKE LOWER({placeholder})
                   OR LOWER(country) LIKE LOWER({placeholder})
            """
            term = f"%{search.strip()}%"
            values.extend([term, term, term])

        query += f" ORDER BY name, id LIMIT {placeholder} OFFSET {placeholder}"
        values.extend([limit, offset])

        rows = connection.execute(query, tuple(values)).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()



def delete_airport(airport_id):
    connection = get_connection()

    if DATABASE_URL:
        cursor = connection.execute(
            "DELETE FROM airports WHERE id = %s",
            (airport_id,),
        )
    else:
        cursor = connection.execute(
            "DELETE FROM airports WHERE id = ?",
            (airport_id,),
        )

    deleted = cursor.rowcount > 0
    connection.commit()
    connection.close()

    return deleted


def list_runways(airport_ident: str):
    connection = get_connection()

    try:
        placeholder = "%s" if DATABASE_URL else "?"

        rows = connection.execute(
            f"""
            SELECT id, airport_ident, le_ident, he_ident,
                   length_ft, width_ft, surface, lighted, closed,le_latitude_deg,le_longitude_deg,he_latitude_deg,he_longitude_deg
            FROM runways
            WHERE airport_ident = {placeholder}
            ORDER BY le_ident
            """,
            (airport_ident,),
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def count_runways():
    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT COUNT(*) AS total FROM runways"
        ).fetchone()
        return row["total"]
    finally:
        connection.close()


def count_airports(search: str = ""):
    connection = get_connection()

    try:
        placeholder = "%s" if DATABASE_URL else "?"
        query = "SELECT COUNT(*) AS total FROM airports"
        values = ()

        if search.strip():
            query += f"""
                WHERE LOWER(ident) LIKE LOWER({placeholder})
                   OR LOWER(name) LIKE LOWER({placeholder})
                   OR LOWER(country) LIKE LOWER({placeholder})
            """
            term = f"%{search.strip()}%"
            values = (term, term, term)

        row = connection.execute(query, values).fetchone()
        return row["total"]
    finally:
        connection.close()


def count_countries():
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT COUNT(DISTINCT country) AS total
            FROM airports
            WHERE country IS NOT NULL AND country != ''
            """
        ).fetchone()
        return row["total"]
    finally:
        connection.close()