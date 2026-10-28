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


def list_airports():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, ident, name, country, latitude, longitude
        FROM airports
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


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